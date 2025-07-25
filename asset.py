import yfinance as yf
import pandas as pd

class Asset:
    def __init__(self, symbol:str, quantity:float, buy_price:float):
        self.symbol= symbol.upper()
        self.quantity= quantity
        self.buy_price= buy_price
        self.invested_value= round(self.quantity * self.buy_price, 2)

        # fetching data using yfinance
        self.ticker = self.fetch_data()
        if self.ticker is not None:
            self.name = self.ticker.info.get("shortName", "Unknown")
        else:
            self.name = "Unknown"
        print(f"Asset added: {self.symbol}")

    """PROPERTIES"""
    @property
    def current_price(self) -> float:
        if self.ticker:
            return round(self.ticker.history(period="1d")["Close"].iloc[-1], 2)
        else:
            return 0.0
        
    @property
    def current_value(self) -> float:
        return round(self.quantity * self.current_price, 2)
    
    @property
    def pnl(self) -> float:
        return round(self.current_value - self.invested_value, 2)
    
    """METHODS"""
    def fetch_data(self) -> yf.Ticker | None:
        try:
            print(f"Fetching data for {self.symbol}")
            ticker =  yf.Ticker(self.symbol)
            return ticker
        except Exception as e:
            print(f"Error fetching data")
            return None

    # this returns a data frame containing the required details 
    def get_info(self) -> pd.DataFrame:
        print("Gathering data")
        data =  [[
            self.name,
            self.quantity,
            self.buy_price,
            self.current_price,
            self.invested_value,
            self.current_value,
            self.pnl
        ]]
        columns = ["Name", "Quantity", "Average Buy Price", "Current Price", "Invested Value", "Current Value", "PnL"]
        return pd.DataFrame(data=data, index=[self.symbol], columns=columns)