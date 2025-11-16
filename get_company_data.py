import yfinance as yf
from datetime import datetime, timedelta
from clean_csv import clean_csv_file


class CompanData:
    def __init__(self, ticker):
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)

    def get_data(self):
        try:
            stock = yf.Ticker(self.ticker)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            hist = stock.history(
                start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d")
            )

            if hist.empty:
                return {"error": "No data found for the given ticker."}

            hist.reset_index(inplace=True)
            hist = clean_csv_file(hist)
            hist["Date"] = hist["Date"].dt.strftime("%Y-%m-%d")

            data = {
                "ticker": self.ticker,
                "company_name": stock.info.get("longName", "N/A"),
                "data": hist[
                    ["Date", "Open", "High", "Low", "Close", "Volume"]
                ].to_dict(orient="records"),
            }
            return data
        except Exception as e:
            return {"error": str(e)}

    def get_52_week(self):
        try:
            hist = self.stock.history(period="1y")
            if hist.empty:
                return {"error": "No data found for the given ticker."}
            hist = clean_csv_file(hist)
            high_52week = hist["High"].max()
            low_52week = hist["Low"].min()
            average_close = hist["Close"].mean()
            return {
                "52_week_high": high_52week,
                "52_week_low": low_52week,
                "52_week_average_close": average_close,
            }
        except Exception as e:
            return {"error": str(e)}


def compare_two_comp(ticker1, ticker2):
    try:
        first_stock = yf.Ticker(ticker1)
        second_stock = yf.Ticker(ticker2)

        first_hist = first_stock.history(period="1y")
        second_hist = second_stock.history(period="1y")

        if first_hist.empty or second_hist.empty:
            return {"error": "No data found for one or both of the given tickers."}

        first_hist = clean_csv_file(first_hist)
        second_hist = clean_csv_file(second_hist)

        first_per = (
            (first_hist["Close"].iloc[0] - first_hist["Close"].iloc[-1])
            / first_hist["Close"].iloc[0]
            * 100
        )
        second_per = (
            (second_hist["Close"].iloc[0] - second_hist["Close"].iloc[-1])
            / second_hist["Close"].iloc[0]
            * 100
        )

        comparison = {
            "ticker1": {
                "ticker": ticker1,
                "52_week_high": first_hist["High"].max(),
                "52_week_low": first_hist["Low"].min(),
                "average_close": first_hist["Close"].mean(),
                "percentage_change": first_per,
            },
            "ticker2": {
                "ticker": ticker2,
                "52_week_high": second_hist["High"].max(),
                "52_week_low": second_hist["Low"].min(),
                "average_close": second_hist["Close"].mean(),
                "percentage_change": second_per,
            },
        }
        return comparison
    except Exception as e:
        return {"error": str(e)}


def get_top_gainers():
    try:
        tickers_list = [
            "AAPL",
            "MSFT",
            "GOOGL",
            "AMZN",
            "META",
            "NVDA",
            "AMD",
            "TSM",
            "INTC",
            "JPM",
            "BAC",
            "HDFC.NS",
            "ICICIBANK.NS",
            "TSLA",
            "TATAMOTORS.NS",
            "MARUTI.NS",
            "JNJ",
            "PFE",
            "XOM",
            "RELIANCE.NS",
        ]

        market_data = yf.Tickers(" ".join(tickers_list))

        gainers = []
        for t in market_data.tickers.values():
            try:
                info = t.info
                gainers.append(
                    {
                        "ticker": info.get("symbol"),
                        "name": info.get("longName", "N/A"),
                        "change_percent": info.get("regularMarketChangePercent", 0),
                    }
                )
            except:
                pass

        gainers = [g for g in gainers if g["change_percent"] is not None]
        gainers.sort(key=lambda x: x["change_percent"], reverse=True)

        return gainers[:5]

    except Exception as e:
        return {"error": str(e)}
