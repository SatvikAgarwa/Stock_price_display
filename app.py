from flask import Flask, jsonify, request, render_template
from flask_caching import Cache
from get_company_data import CompanData, compare_two_comp, get_top_gainers
from storage import companies_dict
import os

app = Flask(__name__)

cache = Cache(app, config={"CACHE_TYPE": "simple"})

@app.route("/")
@cache.cached(timeout=300)
def home():
    top_gainers = get_top_gainers()
    return render_template("index.html", top_gainers=top_gainers)


@app.route("/companies")
def companies():
    return jsonify(companies_dict)


@app.route("/data/<ticker>")
@cache.cached(timeout=300)
def company_data(ticker):
    company = CompanData(ticker)
    data = company.get_data()
    return jsonify(data)


@app.route("/summary/<ticker>")
def company_52_week(ticker):
    company = CompanData(ticker)
    return jsonify(company.get_52_week())


@app.route("/compare", methods=["GET"])
def compare_companies():
    symbol1 = request.args.get("symbol1", "INFY")
    symbol2 = request.args.get("symbol2", "TCS")
    comparison = compare_two_comp(symbol1, symbol2)
    return jsonify(comparison)


@app.route("/stock/<symbol>")
@cache.cached(timeout=300)
def stock_detail(symbol):
    return render_template("stocks.html", symbol=symbol)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
