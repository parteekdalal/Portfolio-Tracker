import threading
import pandas as pd
from asset import Asset

class Portfolio:
    # Initializing the assets data frames
    def __init__(self):
        columns = ["Name", "Quantity", "Average Buy Price", "Current Price", "Invested Value", "Current Value", "PnL"]

        try:    # check for existing data. if found then refresh it
            self.stocks = pd.read_csv(r"data\stocks.csv", index_col=0)
        except Exception as e:      # else create new portfolio
            print('No portfolio backup found for stocks:', e)
            self.stocks = pd.DataFrame(columns=columns)
        
        try:
            self.crypto = pd.read_csv(r"data\crypto.csv", index_col=0)
        except Exception as e:
            print('No portfolio backup found for crypto:', e)
            self.crypto = pd.DataFrame(columns=columns)


    # --- PROPERTIES ---
    @property
    def empty(self) -> bool:
        return self.stocks.empty and self.crypto.empty

    @property
    def invested_value(self) -> float:
        if self.stocks.empty and self.crypto.empty:
            return 0.0
        else:
            stocks= self.stocks['Invested Value'].sum()
            crypto= self.crypto['Invested Value'].sum()
            return stocks+crypto

    @property
    def current_value(self) -> float:
        if self.stocks.empty and self.crypto.empty:
            return 0.0
        else:
            stocks= self.stocks['Current Value'].sum()
            crypto= self.crypto['Current Value'].sum()
            return stocks+crypto

    @property
    def pnl(self) -> float:
        return round(self.current_value - self.invested_value, 2)

    # --- METHODS ---
    def backup_stocks(self) -> None:
        self.stocks.to_csv(r"data\stocks.csv")

    def backup_crypto(self) -> None:
        self.crypto.to_csv(r"data\crypto.csv")

    def update_asset(self, symbol:str, quantity:float, buy_price:float, category:str = 'Stocks', backup:bool = True) -> None:
        buy_price = round(buy_price, 2)
        if category == 'Stocks':
            asset = Asset(symbol, quantity, buy_price)
            updated_asset =  asset.get_info()
            self.stocks.loc[symbol] = updated_asset.iloc[0]
            if backup:
                self.backup_stocks()
        elif category == 'Cryptocurrencies':
            asset = Asset(symbol, quantity, buy_price)
            updated_asset =  asset.get_info()
            self.crypto.loc[symbol] = updated_asset.iloc[0]
            if backup:
                self.backup_crypto()
        print(f'Updated asset: {symbol} (in {category})')

    def add_stock(self, symbol:str, quantity:float, buy_price:float) -> None:
        symbol = symbol.upper()
        if not self.stocks.empty and symbol in self.stocks.index:
            new_quantity = quantity + self.stocks.loc[symbol]['Quantity']
            average_price = (self.stocks.loc[symbol]['Invested Value'] + (quantity * buy_price)) / new_quantity
            self.update_asset(symbol, new_quantity, average_price, 'Stocks', False)
        else:
            asset = Asset(symbol, quantity, buy_price)
            new_asset =  asset.get_info()
            if self.stocks.empty: 
                self.stocks= new_asset
            else:
                self.stocks= pd.concat([self.stocks, new_asset])
        threading.Thread(target=self.backup_stocks).start()
        print(f'Added asset: {symbol} (to Stocks)')

    def add_crypto(self, symbol:str, quantity: float, buy_price:float) -> None:
        symbol = f'{symbol.upper()}-USD'
        if not self.crypto.empty and symbol in self.crypto.index:
            new_quantity = quantity + self.crypto.loc[symbol]['Quantity']
            average_price = (self.crypto.loc[symbol]['Invested Value'] + (quantity * buy_price)) / new_quantity
            self.update_asset(symbol, new_quantity, average_price, 'Cryptocurrencies', False)
        else:    
            asset = Asset(symbol, quantity, buy_price)
            new_asset =  asset.get_info()
            
            # add assset to df
            if self.crypto.empty: 
                self.crypto= new_asset
            else:
                self.crypto= pd.concat([self.crypto, new_asset])
                print(f'Added asset: {symbol} (to Cryptocurrency)')
        threading.Thread(target=self.backup_crypto).start()

    def refresh_portfolio(self) -> None:
        if not self.stocks.empty:
            for symbol, data in self.stocks.iterrows():
                self.update_asset(symbol, data[0], data[1], data[2])
        if not self.crypto.empty:
            for symbol, data in self.crypto.iterrows():
                self.update_asset(symbol, data[0], data[1], data[2])

    def remove_asset(self, symbol:str, category:str) -> None:
        if category == 'Stocks':
            if symbol in self.stocks.index:
                self.stocks = self.stocks.drop(index=symbol)
                threading.Thread(target=self.backup_stocks).start()
                print(f'Removed asset: {symbol} (from {category})')
            else:
                print(f"Error: Couldn't find {symbol}")

        elif category == 'Cryptocurrencies':
            if symbol in self.crypto.index:
                self.crypto = self.crypto.drop(index=symbol)
                threading.Thread(target=self.backup_crypto).start()
                print(f'Removed asset: {symbol} (from {category})')
            else:
                print(f"Error removing asset: Couldn't find {symbol}")