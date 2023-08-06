import requests
import json
import numpy as np

baseUrl = 'https://financialmodelingprep.com/api/v3/'


def stockDaily(ticker, fromDate, toDate):
    url = baseUrl + 'historical-price-full/{}?from={}&to={}'.format(ticker, fromDate, toDate)
    resp = requests.get(url)
    if resp.ok:
        jData = json.loads(resp.content)
        return np.array(jData["historical"])


def historicalChart(symbol, period, fromDate, toDate):
    url = baseUrl + 'historical-chart/{}/{}?from={}&to={}'.format(period, symbol, fromDate, toDate)
    resp = requests.get(url)
    if resp.ok:
        jData = json.loads(resp.content)
        return np.array(jData)


def stockSplit(ticker):
    url = baseUrl + 'historical-price-full/stock_split/{}'.format(ticker)
    resp = requests.get(url)
    if resp.ok:
        jData = json.loads(resp.content)
        return np.array(jData["historical"])


def stockDividend(ticker):
    url = baseUrl + 'historical-price-full/stock_dividend/{}'.format(ticker)
    resp = requests.get(url)
    if resp.ok:
        jData = json.loads(resp.content)
        return np.array(jData["historical"])


def companyRating(ticker):
    url = baseUrl + 'company/rating/{}'.format(ticker)
    resp = requests.get(url)
    if resp.ok:
        jData = json.loads(resp.content)
        return np.array(jData["rating"])


def companyKeyMetrics(ticker, period):
    url = baseUrl + 'company-key-metrics/{}?period={}'.format(ticker, period)
    resp = requests.get(url)
    if resp.ok:
        jData = json.loads(resp.content)
        return np.array(jData["metrics"])


def companyEnterpriseValue(ticker, period):
    url = baseUrl + 'enterprise-value/{}?period={}'.format(ticker, period)
    resp = requests.get(url)
    if resp.ok:
        jData = json.loads(resp.content)
        return np.array(jData["enterpriseValues"])


def companyFinantialIncomeStatement(ticker, period):
    url = baseUrl + 'financials/income-statement/{}?period={}'.format(ticker, period)
    resp = requests.get(url)
    if resp.ok:
        jData = json.loads(resp.content)
        return np.array(jData["financials"])


def companyCashflowStatement(ticker, period):
    url = baseUrl + 'financials/cash-flow-statement/{}?period={}'.format(ticker, period)
    resp = requests.get(url)
    if resp.ok:
        jData = json.loads(resp.content)
        return np.array(jData["financials"])


def companySearch(tickerLike):
    url = baseUrl + 'search?query={}'.format(tickerLike)
    resp = requests.get(url)
    if resp.ok:
        jData = json.loads(resp.content)
        return np.array(jData)


def companyProfile(ticker):
    url = baseUrl + 'company/profile/{}'.format(ticker)
    resp = requests.get(url)
    if resp.ok:
        jData = json.loads(resp.content)
        return np.array(jData["profile"])


def companyFinantialRatios(ticker):
    url = baseUrl + 'financial-ratios/{}'.format(ticker)
    resp = requests.get(url)
    if resp.ok:
        jData = json.loads(resp.content)
        return np.array(jData["ratios"])


def stockRealTime():
    url = baseUrl + 'stock/real-time-price'
    resp = requests.get(url)
    if resp.ok:
        jData = json.loads(resp.content)
        return np.array(jData["stockList"])


def majorIndexList():
    url = baseUrl + 'stock/majors-indexes'
    resp = requests.get(url)
    if resp.ok:
        jData = json.loads(resp.content)
        return np.array(jData["majorIndexesList"])


def majorIndexQuote():
    url = baseUrl + 'quotes/index'
    resp = requests.get(url)
    if resp.ok:
        jData = json.loads(resp.content)
        return np.array(jData)


def availableIndex():
    url = baseUrl + 'symbol/available-indexes'
    resp = requests.get(url)
    if resp.ok:
        jData = json.loads(resp.content)
        return np.array(jData)


def availableCommodities():
    url = baseUrl + 'symbol/available-commodities'
    resp = requests.get(url)
    if resp.ok:
        jData = json.loads(resp.content)
        return np.array(jData)


def commodityQuote():
    url = baseUrl + 'quotes/commodity'
    resp = requests.get(url)
    if resp.ok:
        jData = json.loads(resp.content)
        return np.array(jData)


def availableETF():
    url = baseUrl + 'symbol/available-etfs'
    resp = requests.get(url)
    if resp.ok:
        jData = json.loads(resp.content)
        return np.array(jData)


def availableETFQuote():
    url = baseUrl + 'quotes/etf'
    resp = requests.get(url)
    if resp.ok:
        jData = json.loads(resp.content)
        return np.array(jData)


def availableMutualFunds():
    url = baseUrl + 'symbol/available-mutual-funds'
    resp = requests.get(url)
    if resp.ok:
        jData = json.loads(resp.content)
        return np.array(jData)


def availableTSX():
    url = baseUrl + 'symbol/available-tsx'
    resp = requests.get(url)
    if resp.ok:
        jData = json.loads(resp.content)
        return np.array(jData)


def availableCryptocurrencies():
    url = baseUrl + 'cryptocurrencies'
    resp = requests.get(url)
    if resp.ok:
        jData = json.loads(resp.content)
        return np.array(jData)


def quoteCrypto():
    url = baseUrl + 'quotes/crypto'
    resp = requests.get(url)
    if resp.ok:
        jData = json.loads(resp.content)
        return np.array(jData)


def quote(symbol):
    url = baseUrl + 'quote/{}'.format(symbol)
    resp = requests.get(url)
    if resp.ok:
        jData = json.loads(resp.content)
        return np.array(jData)


def availableEuroNext():
    url = baseUrl + 'symbol/available-euronext'
    resp = requests.get(url)
    if resp.ok:
        jData = json.loads(resp.content)
        return np.array(jData)


def availableForexPair():
    url = baseUrl + 'symbol/available-forex-currency-pairs'
    resp = requests.get(url)
    if resp.ok:
        jData = json.loads(resp.content)
        return np.array(jData)


def forex():
    url = baseUrl + 'forex'
    resp = requests.get(url)
    if resp.ok:
        jData = json.loads(resp.content)
        return np.array(jData["forexList"])


def forexQuote():
    url = baseUrl + 'quotes/forex'
    resp = requests.get(url)
    if resp.ok:
        jData = json.loads(resp.content)
        return np.array(jData)


def stockList():
    url = baseUrl + 'company/stock/list'
    resp = requests.get(url)
    if resp.ok:
        jData = json.loads(resp.content)
        return np.array(jData["symbolsList"])


def mostActive():
    url = baseUrl + 'stock/actives'
    resp = requests.get(url)
    if resp.ok:
        jData = json.loads(resp.content)
        return np.array(jData["mostActiveStock"])


def gainers():
    url = baseUrl + 'stock/gainers'
    resp = requests.get(url)
    if resp.ok:
        jData = json.loads(resp.content)
        return np.array(jData["mostGainerStock"])


def losers():
    url = baseUrl + 'stock/losers'
    resp = requests.get(url)
    if resp.ok:
        jData = json.loads(resp.content)
        return np.array(jData["mostLoserStock"])


def sectorPerformance():
    url = baseUrl + 'stock/sectors-performance'
    resp = requests.get(url)
    if resp.ok:
        jData = json.loads(resp.content)
        return np.array(jData["sectorPerformance"])


def marketHoliday():
    url = baseUrl + 'is-the-market-open'
    resp = requests.get(url)
    if resp.ok:
        jData = json.loads(resp.content)
        return jData

