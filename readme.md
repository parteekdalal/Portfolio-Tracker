# Portfolio Tracker

A desktop application built with Python that helps users track their investment portfolio across different asset classes. The application provides a clean, modern interface to monitor investments, track profit/loss, and manage various assets.

## Features:

1. Real-time portfolio value tracking
2. Support for multiple asset classes:
   - Stocks
   - Cryptocurrencies
3. Individual asset performance monitoring
4. Profit/Loss tracking
5. Modern GUI interface
6. Data persistence through CSV storage

## Python tools and libraries used:

* `customtkinter` - For creating a modern GUI interface
* `pandas` - For data manipulation and storage
* Python's built-in libraries for core functionality

## Technical Details:

- **Architecture**: Object-oriented design with separate classes for Portfolio, Assets, and UI
- **Data Storage**: CSV files in the `data/` directory
- **User Interface**: Modern, responsive GUI built with CustomTkinter

## Installation and Usage:

1. Ensure Python is installed on your system
2. Install required dependencies:
   ```
   pip install customtkinter pandas
   ```
3. Run the application:
   ```
   python app.py
   ```

## Project Structure:

- `app.py` - Main application entry point
- `PortfolioTracker.py` - Main GUI and application logic
- `portfolio.py` - Portfolio management class
- `asset.py` - Asset class definition
- `data/` - Directory containing portfolio data
- `themes/` - CustomTkinter theme file

## Future Enhancements:

* Support for Forex/Currency assets
* Support for Commodities assets
* Enhanced data visualization
* Portfolio analytics and reports