import customtkinter as ctk
from pathlib import Path
from portfolio import Portfolio

class PortfolioTracker(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Portfolio Tracker")
        self.geometry("920x700+50+50")
        self.load_theme()

        self.portfolio = Portfolio()
        self.init_ui()
        self.restock_portfolio_frame()
        
    def init_ui(self) -> None:
        ctk.CTkLabel(self, text="Portfolio Tracker", font=("Arial", 24, "bold")).pack(pady=10, padx=10)

        #NOTE portfolio head
        self.portfolio_head = ctk.CTkFrame(self.master)
        self.portfolio_head.pack(padx=10, pady=5, fill='x')

        ctk.CTkLabel(self.portfolio_head, text="Your Portfolio:", font=("Roboto", 18, "bold")).grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        # current value
        self.current_value_label = ctk.CTkLabel(self.portfolio_head, text=f"${self.portfolio.current_value}", font=("Roboto", 32, "bold"))
        self.current_value_label.grid(row=1, column=0, padx=10, pady=10, columnspan=2)
        self.pnl_label = ctk.CTkLabel(self.portfolio_head, text=f"${self.portfolio.pnl}", font=("Roboto", 20, "bold"), text_color="green")
        self.pnl_label.grid(row=1, column=2, padx=2, pady=10)

        # invested value
        ctk.CTkLabel(self.portfolio_head, text="Invested:", font=("Roboto", 16, "bold")).place(relx=1.0, x=-5, y=50, anchor="ne")
        self.invested_value_label = ctk.CTkLabel(self.portfolio_head, text=f"${self.portfolio.invested_value}")
        self.invested_value_label.place(relx=1.0, x=-5, y=70, anchor="ne")

        # portfolio settings frame (grid)
        self.portfolio_settings = ctk.CTkFrame(self)
        self.portfolio_settings.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.portfolio_settings, text="Add Asset", font=("Roboto", 18), width=50, command=lambda: self.add_asset_dialog(self.portfolio_frame)).grid(row=0, column=0, pady=10, padx=10)
        ctk.CTkButton(self.portfolio_settings, text="Refresh", font=("Roboto", 18), width=50, command=self.refresh).grid(row=0, column=1, pady=10, padx=10)

        self.portfolio_frame = ctk.CTkScrollableFrame(self)
        self.portfolio_frame.pack(pady=5, padx=10, fill="both", expand=True)

    def add_asset_dialog(self, master) -> None:
        # add asset dialog box (grid)
        self.asset_info_dialog = ctk.CTkToplevel(master)
        self.asset_info_dialog.title("Add Asset")
        self.asset_info_dialog.geometry("600x230+200+200")

        categories = ["Stocks", "Cryptocurrencies"]

        asset_info_frame = ctk.CTkFrame(self.asset_info_dialog)
        asset_info_frame.pack(padx=10, pady=10, expand=True, fill='x')
        
        # asset_type
        ctk.CTkLabel(asset_info_frame, text="Asset Type:").grid(row=0, column=0, padx=10, pady=10)
        category= ctk.CTkComboBox(asset_info_frame, values=categories)
        category.grid(row=0, column=1, padx=10, pady=10)

        #symbol
        ctk.CTkLabel(asset_info_frame, text="Symbol:").grid(row=2, column=0, padx=10, pady=10)
        symbol = ctk.CTkEntry(asset_info_frame)
        symbol.grid(row=2, column=1, padx=10, pady=10)

        # quantity
        ctk.CTkLabel(asset_info_frame, text="Quantity:").grid(row=3, column=0, padx=10, pady=10)
        quantity= ctk.CTkEntry(asset_info_frame)
        quantity.grid(row=3, column=1, padx=10, pady=10)

        # buy price
        ctk.CTkLabel(asset_info_frame, text="Buy Price:").grid(row=3, column=2, padx=10, pady=10)
        buy_price= ctk.CTkEntry(asset_info_frame)
        buy_price.grid(row=3, column=3, padx=10, pady=10)
        
        self.asset_info_dialog.grab_set()

        ctk.CTkButton(self.asset_info_dialog, text="Cancel", command=self.asset_info_dialog.destroy).pack(pady=10, padx=10, side="right")
        ctk.CTkButton(self.asset_info_dialog, text="Continue", command=lambda: self.add_asset(symbol.get().upper(), float(quantity.get()), float(buy_price.get()), category.get())).pack(pady=10, padx=10, side="right")

    def add_asset(self, symbol:str, quantity:float, buy_price:float, category: str):
        self.asset_info_dialog.destroy()
        if category == "Stocks":
            self.portfolio.add_stock(symbol, quantity, buy_price)
        elif category == 'Cryptocurrencies':
            self.portfolio.add_crypto(symbol, quantity, buy_price)
        self.refresh()
        self.restock_portfolio_frame()

    def refresh(self) -> None:
        self.current_value_label.configure(text=f"${self.portfolio.current_value}")
        self.invested_value_label.configure(text=f"${self.portfolio.invested_value}")

        if self.portfolio.pnl >= 0:
            self.pnl_label.configure(text=f"${self.portfolio.pnl}", text_color="green")
        else:
            self.pnl_label.configure(text=f"${self.portfolio.pnl}", text_color="red")

    def restock_portfolio_frame(self):
        for widget in self.portfolio_frame.winfo_children():
            widget.destroy()

        if self.portfolio.empty:
            ctk.CTkLabel(self.portfolio_frame, text="Your assets will appear here...").pack(fill='x', expand=1)
        else:
            # load stocks first
            if not self.portfolio.stocks.empty:
                self.load_stocks()
            if not self.portfolio.crypto.empty:
                self.load_crypto()

    def load_stocks(self):
        stocks_frame = ctk.CTkFrame(self.portfolio_frame)
        stocks_frame.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkLabel(stocks_frame, text="Stocks", font=("Roboto", 24, "bold")).pack(padx=5, pady=5, fill="x")

        for symbol in self.portfolio.stocks.itertuples():
            asset_card = ctk.CTkFrame(stocks_frame, width=940, height=130, border_width=2)
            asset_card.pack(pady=5, padx=10, fill="x")

            ctk.CTkLabel(asset_card, text=f"{symbol.Name}", font=("Roboto", 24, "bold")).place(x=5, y=5)
            ctk.CTkLabel(asset_card, text=f"{symbol[4]} USD").place(x=6, y=32)
            ctk.CTkLabel(asset_card, text=f"{symbol[2]} QTY").place(relx=1.0, x=-8, y=5, anchor="ne")
            ctk.CTkLabel(asset_card, text=f"${symbol[3]} AVG").place(relx=1.0, x=-8, y=30, anchor="ne")

            asset_card_info = ctk.CTkFrame(asset_card, width=890, height=60, corner_radius=10)
            asset_card_info.place(x=15, y=60)
            asset_card_info.pack_propagate(False)

            frame1 = ctk.CTkFrame(asset_card_info)
            frame1.pack(side="left", expand=True, fill="both", padx=7, pady=5)
            ctk.CTkLabel(frame1, text="Invested", font=("Roboto", 16)).pack(pady=1, padx=1)
            ctk.CTkLabel(frame1, text=f"${symbol[5]}", font=("Roboto", 20)).pack(pady=1, padx=1)

            frame2 = ctk.CTkFrame(asset_card_info)
            frame2.pack(side="left", expand=True, fill="both", padx=7, pady=5)
            ctk.CTkLabel(frame2, text="Current", font=("Roboto", 16)).pack(pady=1, padx=1)
            ctk.CTkLabel(frame2, text=f"${symbol[6]}", font=("Roboto", 20)).pack(pady=1, padx=1)

            frame3 = ctk.CTkFrame(asset_card_info)
            frame3.pack(side="left", expand=True, fill="both", padx=7, pady=5)
            
            ctk.CTkLabel(frame3, text="P&L", font=("Roboto", 16)).pack(pady=1, padx=1)
            if symbol.PnL >= 0:
                ctk.CTkLabel(frame3, text=f"${symbol.PnL}", font=("Roboto", 20), text_color="green").pack(pady=1, padx=1)
            else:
                ctk.CTkLabel(frame3, text=f"${symbol.PnL}", font=("Roboto", 20), text_color="red").pack(pady=1, padx=1)

    def load_crypto(self):
        crypto_frame = ctk.CTkFrame(self.portfolio_frame)
        crypto_frame.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkLabel(crypto_frame, text="Stocks", font=("Roboto", 24, "bold")).pack(padx=5, pady=5, fill="x")

        for symbol in self.portfolio.crypto.itertuples():
            print(symbol)
            asset_card = ctk.CTkFrame(crypto_frame, width=940, height=130, border_width=2)
            asset_card.pack(pady=5, padx=10, fill="x")

            ctk.CTkLabel(asset_card, text=f"{symbol.Name}", font=("Roboto", 24, "bold")).place(x=5, y=5)
            ctk.CTkLabel(asset_card, text=f"{symbol[4]} USD").place(x=6, y=32)
            ctk.CTkLabel(asset_card, text=f"{symbol[2]} QTY").place(relx=1.0, x=-8, y=5, anchor="ne")
            ctk.CTkLabel(asset_card, text=f"${symbol[3]} AVG").place(relx=1.0, x=-8, y=30, anchor="ne")

            asset_card_info = ctk.CTkFrame(asset_card, width=890, height=60, corner_radius=10)
            asset_card_info.place(x=15, y=60)
            asset_card_info.pack_propagate(False)

            frame1 = ctk.CTkFrame(asset_card_info)
            frame1.pack(side="left", expand=True, fill="both", padx=7, pady=5)
            ctk.CTkLabel(frame1, text="Invested", font=("Roboto", 16)).pack(pady=1, padx=1)
            ctk.CTkLabel(frame1, text=f"${symbol[5]}", font=("Roboto", 20)).pack(pady=1, padx=1)

            frame2 = ctk.CTkFrame(asset_card_info)
            frame2.pack(side="left", expand=True, fill="both", padx=7, pady=5)
            ctk.CTkLabel(frame2, text="Current", font=("Roboto", 16)).pack(pady=1, padx=1)
            ctk.CTkLabel(frame2, text=f"${symbol[6]}", font=("Roboto", 20)).pack(pady=1, padx=1)

            frame3 = ctk.CTkFrame(asset_card_info)
            frame3.pack(side="left", expand=True, fill="both", padx=7, pady=5)
            
            ctk.CTkLabel(frame3, text="P&L", font=("Roboto", 16)).pack(pady=1, padx=1)
            if symbol.PnL >= 0:
                ctk.CTkLabel(frame3, text=f"${symbol.PnL}", font=("Roboto", 20), text_color="green").pack(pady=1, padx=1)
            else:
                ctk.CTkLabel(frame3, text=f"${symbol.PnL}", font=("Roboto", 20), text_color="red").pack(pady=1, padx=1)
            
    def load_theme(self, theme:str = 'orange', mode:str = 'System'):
        ctk.set_appearance_mode(mode)
        try:
            theme_path = Path(f'themes/{theme}.json')
            ctk.set_default_color_theme(theme_path)
        except Exception as e:
            print(f'could not load {theme} theme')
            print(e)