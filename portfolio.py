import pandas as pd
from asset import Asset

class Portfolio:
    # Initializing the assets data frames
    def __init__(self):
        columns = ["Name", "Quantity", "Average Buy Price", "Current Price", "Invested Value", "Current Value", "PnL"]

        # checking for existing data and refreshing it
        try:
            self.stocks = pd.read_csv(r"data\stocks.csv")

        # else we'll create an empty df and add assets later
        except Exception as e:
            print('No portfolio backup found for stocks')
            self.stocks = pd.DataFrame(columns=columns)
        
        try:
            self.crypto = pd.read_csv(r"data\crypto.csv")
        except Exception as e:
            print('No portfolio backup found for crypto')
            self.crypto = pd.DataFrame(columns=columns)
    

    # --- PROPERTIES ---
    @property
    def invested_value(self):
        if self.stocks.empty and self.crypto.empty:
            return 0.0
        else:
            stocks= self.stocks['Invested Value'].sum()
            crypto= self.crypto['Invested Value'].sum()
            return stocks+crypto

    @property
    def current_value(self):
        if self.stocks.empty and self.crypto.empty:
            return 0.0
        else:
            stocks= self.stocks['Current Value'].sum()
            crypto= self.crypto['Current Value'].sum()
            return stocks+crypto

    @property
    def pnl(self):
        return round(self.current_value - self.invested_value, 2)


    # --- METHODS ---

    def write_stocks(self):
        self.stocks.to_csv(r"data\stocks.csv")

    def write_crypto(self):
        self.crypto.to_csv(r"data\crypto.csv")

    def add_asset(self, symbol:str, quantity:float, buy_price:float, category: str = "Stocks"):
        if category == "Stocks":
            asset = Asset(symbol, quantity, buy_price)
            new_asset =  asset.get_asset_df()
            
            # add assset to the df
            if self.stocks.empty: 
                self.stocks= new_asset
            else:
                self.stocks= pd.concat([self.stocks, new_asset])
            self.write_stocks()

        else:
            asset = Asset(f"{symbol}-USD", quantity, buy_price)
            new_asset =  asset.get_asset_df()
            
            # add assset to df
            if self.crypto.empty: 
                self.crypto= new_asset
            else:
                self.crypto= pd.concat([self.crypto, new_asset])
            self.write_crypto()
        print("Asset added successfully")

    def update_asset(self, symbol:str, quantity:float, buy_price:float, category:str = "Stocks"):
        if category == "Stocks":
            asset = Asset(symbol, quantity, buy_price)
            updated_asset =  asset.get_asset_df()
            self.stocks.loc[symbol.upper] = updated_asset
            self.write_stocks()
        else:
            asset = Asset(f"{symbol}-USD", quantity, buy_price)
            updated_asset =  asset.get_asset_df()
            self.crypto.loc[f"{symbol}-USD"] = updated_asset
            self.write_crypto()

    def refresh_portfolio(self):
        if not self.stocks.empty:
            for symbol, data in self.stocks.iterrows():
                self.update_asset(symbol, data[0], data[1], data[2])
        if not self.crypto.empty:
            for symbol, data in self.crypto.iterrows():
                self.update_asset(symbol, data[0], data[1], data[2])

p = Portfolio()

print("Stocks:", p.stocks)