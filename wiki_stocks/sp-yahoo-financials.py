from base import Base
from wikistock import WikiStocks, TickerData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///wiki_stocks/wiki.db')
Session = sessionmaker(bind=engine)

import time
import requests
from bs4 import BeautifulSoup
import json
import datetime

Base.metadata.create_all(engine)
session = Session()
#{"GET":{"scheme":"https","host":"query1.finance.yahoo.com","filename":"/v8/finance/chart/AAPL","query":{"region":"US","lang":"en-US","includePrePost":"false","interval":"2m","range":"1d","corsDomain":"finance.yahoo.com",".tsrc":"finance"},"remote":{"Address":"68.180.135.252:443"}}}
#{"GET":{"scheme":"https","host":"query1.finance.yahoo.com","filename":"/v7/finance/quote","query":{"formatted":"true","crumb":"sD0gBL8xdVS","lang":"en-US","region":"US","symbols":"AAPL","fields":"messageBoardId,longName,shortName,marketCap,underlyingSymbol,underlyingExchangeSymbol,headSymbolAsString,regularMarketPrice,regularMarketChange,regularMarketChangePercent,regularMarketVolume,uuid,regularMarketOpen,fiftyTwoWeekLow,fiftyTwoWeekHigh,toCurrency,fromCurrency,toExchange,fromExchange","corsDomain":"finance.yahoo.com"},"remote":{"Address":"68.180.135.252:443"}}}
# Dividend data on main page
# https://finance.yahoo.com/quote/AAPL
# https://query1.finance.yahoo.com/v8/finance/chart/AAPL?region=US&lang=en-US&includePrePost=false&interval=2m&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance
# https://query1.finance.yahoo.com/v7/finance/quote?formatted=true&crumb=sD0gBL8xdVS&lang=en-US&region=US&symbols=AAPL&fields=messageBoardId%2ClongName%2CshortName%2CmarketCap%2CunderlyingSymbol%2CunderlyingExchangeSymbol%2CheadSymbolAsString%2CregularMarketPrice%2CregularMarketChange%2CregularMarketChangePercent%2CregularMarketVolume%2Cuuid%2CregularMarketOpen%2CfiftyTwoWeekLow%2CfiftyTwoWeekHigh%2CtoCurrency%2CfromCurrency%2CtoExchange%2CfromExchange&corsDomain=finance.yahoo.com
session.flush()

with open('./wiki_stocks/sp500tickers.json') as f:
    sp_data = json.load(f)
    for stock in sp_data['stocks']:
        cash_flow_annual = requests.get(f'https://query2.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/{stock["ticker"]}?lang=en-US&region=US&symbol={stock["ticker"]}&padTimeSeries=true&type=annualFreeCashFlow%2CtrailingFreeCashFlow%2CannualCapitalExpenditure%2CtrailingCapitalExpenditure%2CannualOperatingCashFlow%2CtrailingOperatingCashFlow%2CannualEndCashPosition%2CtrailingEndCashPosition%2CannualBeginningCashPosition%2CtrailingBeginningCashPosition%2CannualChangeInCashSupplementalAsReported%2CtrailingChangeInCashSupplementalAsReported%2CannualCashFlowFromContinuingFinancingActivities%2CtrailingCashFlowFromContinuingFinancingActivities%2CannualNetOtherFinancingCharges%2CtrailingNetOtherFinancingCharges%2CannualCashDividendsPaid%2CtrailingCashDividendsPaid%2CannualRepurchaseOfCapitalStock%2CtrailingRepurchaseOfCapitalStock%2CannualCommonStockIssuance%2CtrailingCommonStockIssuance%2CannualRepaymentOfDebt%2CtrailingRepaymentOfDebt%2CannualInvestingCashFlow%2CtrailingInvestingCashFlow%2CannualNetOtherInvestingChanges%2CtrailingNetOtherInvestingChanges%2CannualSaleOfInvestment%2CtrailingSaleOfInvestment%2CannualPurchaseOfInvestment%2CtrailingPurchaseOfInvestment%2CannualPurchaseOfBusiness%2CtrailingPurchaseOfBusiness%2CannualOtherNonCashItems%2CtrailingOtherNonCashItems%2CannualChangeInAccountPayable%2CtrailingChangeInAccountPayable%2CannualChangeInInventory%2CtrailingChangeInInventory%2CannualChangesInAccountReceivables%2CtrailingChangesInAccountReceivables%2CannualChangeInWorkingCapital%2CtrailingChangeInWorkingCapital%2CannualStockBasedCompensation%2CtrailingStockBasedCompensation%2CannualDeferredIncomeTax%2CtrailingDeferredIncomeTax%2CannualDepreciationAndAmortization%2CtrailingDepreciationAndAmortization%2CannualNetIncome%2CtrailingNetIncome&merge=false&period1=493590046&period2={int(time.time())}&corsDomain=finance.yahoo.com')
        json_result = cash_flow_annual.json()
        try:
            for item in json_result['timeseries']['result']:
                try:
                    finance_type = item['meta']['type'][0]
                    for record in item[finance_type]:
                        try:
                            session.merge(TickerData(stock['ticker'], finance_type, datetime.datetime.strptime(record['asOfDate'], '%Y-%m-%d'), record['reportedValue']['raw']))
                        except Exception as e:
                            print(f'cash_flow_annual record exception occurred: {stock["ticker"]}, {finance_type}') 
                            print(e)
                            print(record)
                except Exception as e:
                    print(f'cash_flow_annual item exception occurred: {stock["ticker"]}, {finance_type}') 
                    print(e)
                    print(item)
        except Exception as e:
            print(f'cash_flow_annual exception occurred: {stock["ticker"]}, {finance_type}') 
            print(e)

        
        cash_flow_quarter = requests.get(f'https://query2.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/{stock["ticker"]}?lang=en-US&region=US&symbol={stock["ticker"]}&padTimeSeries=true&type=quarterlyFreeCashFlow,quarterlyCapitalExpenditure,quarterlyOperatingCashFlow,quarterlyEndCashPosition,quarterlyBeginningCashPosition,quarterlyChangeInCashSupplementalAsReported,quarterlyCashFlowFromContinuingFinancingActivities,quarterlyNetOtherFinancingCharges,quarterlyCashDividendsPaid,quarterlyRepurchaseOfCapitalStock,quarterlyCommonStockIssuance,quarterlyRepaymentOfDebt,quarterlyInvestingCashFlow,quarterlyNetOtherInvestingChanges,quarterlySaleOfInvestment,quarterlyPurchaseOfInvestment,quarterlyPurchaseOfBusiness,quarterlyOtherNonCashItems,quarterlyChangeInAccountPayable,quarterlyChangeInInventory,quarterlyChangesInAccountReceivables,quarterlyChangeInWorkingCapital,quarterlyStockBasedCompensation,quarterlyDeferredIncomeTax,quarterlyDepreciationAndAmortization&merge=false&period1=493590046&period2={int(time.time())}&corsDomain=finance.yahoo.com')
        json_result = cash_flow_quarter.json()
        try:
            for item in json_result['timeseries']['result']:
                try:
                    finance_type = item['meta']['type'][0]
                    for record in item[finance_type]:
                        try:
                            session.merge(TickerData(stock["ticker"], finance_type, datetime.datetime.strptime(record['asOfDate'], '%Y-%m-%d'), record['reportedValue']['raw']))
                        except Exception as e:
                            print(f'A cash_flow_quarter record exception occurred: {stock["ticker"]}, {finance_type}')
                            print(record)
                except Exception as e:
                    print(f'A cash_flow_quarter item exception occurred: {stock["ticker"]}, {finance_type}')
                    print(item)
        except Exception as e:
            print(f'A cash_flow_quarter exception occurred: {stock["ticker"]}, {finance_type}') 
        

        income_annual = requests.get(f'https://query2.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/{stock["ticker"]}?lang=en-US&region=US&symbol={stock["ticker"]}&padTimeSeries=true&type=annualEbitda%2CtrailingEbitda%2CannualWeighteAverageShare%2CtrailingWeighteAverageShare%2CannualDilutedAverageShares%2CtrailingDilutedAverageShares%2CannualBasicAverageShares%2CtrailingBasicAverageShares%2CannualearningsPerShare%2CtrailingearningsPerShare%2CannualDilutedEPS%2CtrailingDilutedEPS%2CannualBasicEPS%2CtrailingBasicEPS%2CannualNetIncomeCommonStockholders%2CtrailingNetIncomeCommonStockholders%2CannualNetIncomeContinuousOperations%2CtrailingNetIncomeContinuousOperations%2CannualTaxProvision%2CtrailingTaxProvision%2CannualPretaxIncome%2CtrailingPretaxIncome%2CannualOtherIncomeExpense%2CtrailingOtherIncomeExpense%2CannualInterestExpense%2CtrailingInterestExpense%2CannualOperatingIncome%2CtrailingOperatingIncome%2CannualOperatingExpense%2CtrailingOperatingExpense%2CannualSellingGeneralAndAdministration%2CtrailingSellingGeneralAndAdministration%2CannualResearchAndDevelopment%2CtrailingResearchAndDevelopment%2CannualGrossProfit%2CtrailingGrossProfit%2CannualCostOfRevenue%2CtrailingCostOfRevenue%2CannualTotalRevenue%2CtrailingTotalRevenue&merge=false&period1=493590046&period2={int(time.time())}&corsDomain=finance.yahoo.com')
        json_result = income_annual.json()
        try:
            for item in json_result['timeseries']['result']:
                try:
                    finance_type = item['meta']['type'][0]
                    for record in item[finance_type]:
                        try:
                            session.merge(TickerData(stock["ticker"], finance_type, datetime.datetime.strptime(record['asOfDate'], '%Y-%m-%d'), record['reportedValue']['raw']))
                        except Exception as e:
                            print(f'A income_annual record exception occurred: {stock["ticker"]}, {finance_type}')
                            print(e)
                            print(record)
                except Exception as e:
                    print(f'A income_annual item exception occurred: {stock["ticker"]}, {finance_type}')
                    print(e)
                    print(item)
        except Exception as e:
            print(f'An exception occurred: {stock["ticker"]}, {finance_type}') 
            print(e)


        income_quarter = requests.get(f'https://query2.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/{stock["ticker"]}?lang=en-US&region=US&symbol={stock["ticker"]}&padTimeSeries=true&type=quarterlyEbitda%2CquarterlyWeighteAverageShare%2CquarterlyDilutedAverageShares%2CquarterlyBasicAverageShares%2CquarterlyearningsPerShare%2CquarterlyDilutedEPS%2CquarterlyBasicEPS%2CquarterlyNetIncomeCommonStockholders%2CquarterlyNetIncome%2CquarterlyNetIncomeContinuousOperations%2CquarterlyTaxProvision%2CquarterlyPretaxIncome%2CquarterlyOtherIncomeExpense%2CquarterlyInterestExpense%2CquarterlyOperatingExpense%2CquarterlySellingGeneralAndAdministration%2CquarterlyResearchAndDevelopment%2CquarterlyCostOfRevenue%2CquarterlyTotalRevenue&merge=false&period1=493590046&period2={int(time.time())}&corsDomain=finance.yahoo.com')
        json_result = income_quarter.json()
        try:
            for item in json_result['timeseries']['result']:
                try:
                    finance_type = item['meta']['type'][0]
                    for record in item[finance_type]:
                        try:
                            session.merge(TickerData(stock["ticker"], finance_type, datetime.datetime.strptime(record['asOfDate'], '%Y-%m-%d'), record['reportedValue']['raw']))
                        except Exception as e:
                            print(f'A income_quarter record exception occurred: {stock["ticker"]}, {finance_type}')
                            print(e)
                            print(record)
                except Exception as e:
                    print(f'A income_quarter item exception occurred: {stock["ticker"]}, {finance_type}')
                    print(e)
                    print(item)
        except Exception as e:
            print(f'An exception occurred: {stock["ticker"]}, {finance_type}') 
            print(e)


        balance_annual = requests.get(f'https://query2.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/{stock["ticker"]}?lang=en-US&region=US&symbol={stock["ticker"]}&padTimeSeries=true&type=annualTotalAssets%2CtrailingTotalAssets%2CannualStockholdersEquity%2CtrailingStockholdersEquity%2CannualGainsLossesNotAffectingRetainedEarnings%2CtrailingGainsLossesNotAffectingRetainedEarnings%2CannualRetainedEarnings%2CtrailingRetainedEarnings%2CannualCapitalStock%2CtrailingCapitalStock%2CannualTotalLiabilitiesNetMinorityInterest%2CtrailingTotalLiabilitiesNetMinorityInterest%2CannualTotalNonCurrentLiabilitiesNetMinorityInterest%2CtrailingTotalNonCurrentLiabilitiesNetMinorityInterest%2CannualOtherNonCurrentLiabilities%2CtrailingOtherNonCurrentLiabilities%2CannualNonCurrentDeferredRevenue%2CtrailingNonCurrentDeferredRevenue%2CannualNonCurrentDeferredTaxesLiabilities%2CtrailingNonCurrentDeferredTaxesLiabilities%2CannualLongTermDebt%2CtrailingLongTermDebt%2CannualCurrentLiabilities%2CtrailingCurrentLiabilities%2CannualOtherCurrentLiabilities%2CtrailingOtherCurrentLiabilities%2CannualCurrentDeferredRevenue%2CtrailingCurrentDeferredRevenue%2CannualCurrentAccruedExpenses%2CtrailingCurrentAccruedExpenses%2CannualIncomeTaxPayable%2CtrailingIncomeTaxPayable%2CannualAccountsPayable%2CtrailingAccountsPayable%2CannualCurrentDebt%2CtrailingCurrentDebt%2CannualTotalNonCurrentAssets%2CtrailingTotalNonCurrentAssets%2CannualOtherNonCurrentAssets%2CtrailingOtherNonCurrentAssets%2CannualOtherIntangibleAssets%2CtrailingOtherIntangibleAssets%2CannualGoodwill%2CtrailingGoodwill%2CannualInvestmentsAndAdvances%2CtrailingInvestmentsAndAdvances%2CannualNetPPE%2CtrailingNetPPE%2CannualAccumulatedDepreciation%2CtrailingAccumulatedDepreciation%2CannualGrossPPE%2CtrailingGrossPPE%2CannualCurrentAssets%2CtrailingCurrentAssets%2CannualOtherCurrentAssets%2CtrailingOtherCurrentAssets%2CannualInventory%2CtrailingInventory%2CannualAccountsReceivable%2CtrailingAccountsReceivable%2CannualCashCashEquivalentsAndMarketableSecurities%2CtrailingCashCashEquivalentsAndMarketableSecurities%2CannualOtherShortTermInvestments%2CtrailingOtherShortTermInvestments%2CannualCashAndCashEquivalents%2CtrailingCashAndCashEquivalents&merge=false&period1=493590046&period2={int(time.time())}&corsDomain=finance.yahoo.com')
        json_result = balance_annual.json()
        try:
            for item in json_result['timeseries']['result']:
                try:
                    finance_type = item['meta']['type'][0]
                    for record in item[finance_type]:
                        try:
                            session.merge(TickerData(stock["ticker"], finance_type, datetime.datetime.strptime(record['asOfDate'], '%Y-%m-%d'), record['reportedValue']['raw']))
                        except Exception as e:
                            print(f'A balance_annual record exception occurred: {stock["ticker"]}, {finance_type}')
                            print(e)
                            print(record)
                except Exception as e:
                    print(f'A balance_annual item exception occurred: {stock["ticker"]}, {finance_type}')
                    print(e)
                    print(item)
        except Exception as e:
            print(f'An exception occurred: {stock["ticker"]}, {finance_type}') 
            print(e)

        balance_quarter = requests.get(f'https://query2.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/{stock["ticker"]}?lang=en-US&region=US&symbol={stock["ticker"]}&padTimeSeries=true&type=quarterlyTotalAssets%2CtrailingTotalAssets%2CquarterlyStockholdersEquity%2CtrailingStockholdersEquity%2CquarterlyGainsLossesNotAffectingRetainedEarnings%2CtrailingGainsLossesNotAffectingRetainedEarnings%2CquarterlyRetainedEarnings%2CtrailingRetainedEarnings%2CquarterlyCapitalStock%2CtrailingCapitalStock%2CquarterlyTotalLiabilitiesNetMinorityInterest%2CtrailingTotalLiabilitiesNetMinorityInterest%2CquarterlyTotalNonCurrentLiabilitiesNetMinorityInterest%2CtrailingTotalNonCurrentLiabilitiesNetMinorityInterest%2CquarterlyOtherNonCurrentLiabilities%2CtrailingOtherNonCurrentLiabilities%2CquarterlyNonCurrentDeferredRevenue%2CtrailingNonCurrentDeferredRevenue%2CquarterlyNonCurrentDeferredTaxesLiabilities%2CtrailingNonCurrentDeferredTaxesLiabilities%2CquarterlyLongTermDebt%2CtrailingLongTermDebt%2CquarterlyCurrentLiabilities%2CtrailingCurrentLiabilities%2CquarterlyOtherCurrentLiabilities%2CtrailingOtherCurrentLiabilities%2CquarterlyCurrentDeferredRevenue%2CtrailingCurrentDeferredRevenue%2CquarterlyCurrentAccruedExpenses%2CtrailingCurrentAccruedExpenses%2CquarterlyIncomeTaxPayable%2CtrailingIncomeTaxPayable%2CquarterlyAccountsPayable%2CtrailingAccountsPayable%2CquarterlyCurrentDebt%2CtrailingCurrentDebt%2CquarterlyTotalNonCurrentAssets%2CtrailingTotalNonCurrentAssets%2CquarterlyOtherNonCurrentAssets%2CtrailingOtherNonCurrentAssets%2CquarterlyOtherIntangibleAssets%2CtrailingOtherIntangibleAssets%2CquarterlyGoodwill%2CtrailingGoodwill%2CquarterlyInvestmentsAndAdvances%2CtrailingInvestmentsAndAdvances%2CquarterlyNetPPE%2CtrailingNetPPE%2CquarterlyAccumulatedDepreciation%2CtrailingAccumulatedDepreciation%2CquarterlyGrossPPE%2CtrailingGrossPPE%2CquarterlyCurrentAssets%2CtrailingCurrentAssets%2CquarterlyOtherCurrentAssets%2CtrailingOtherCurrentAssets%2CquarterlyInventory%2CtrailingInventory%2CquarterlyAccountsReceivable%2CtrailingAccountsReceivable%2CquarterlyCashCashEquivalentsAndMarketableSecurities%2CtrailingCashCashEquivalentsAndMarketableSecurities%2CquarterlyOtherShortTermInvestments%2CtrailingOtherShortTermInvestments%2CquarterlyCashAndCashEquivalents%2CtrailingCashAndCashEquivalents&merge=false&period1=493590046&period2={int(time.time())}&corsDomain=finance.yahoo.com')
        json_result = balance_quarter.json()
        try:
            for item in json_result['timeseries']['result']:
                try:
                    finance_type = item['meta']['type'][0]
                    for record in item[finance_type]:
                        try:
                            session.merge(TickerData(stock["ticker"], finance_type, datetime.datetime.strptime(record['asOfDate'], '%Y-%m-%d'), record['reportedValue']['raw']))
                        except Exception as e:
                            print(f'A balance_quarter record exception occurred: {stock["ticker"]}, {finance_type}')
                            print(e)
                            print(record)
                except Exception as e:
                    print(f'A balance_quarter item exception occurred: {stock["ticker"]}, {finance_type}')
                    print(e)
                    print(item)
        except Exception as e:
            print(f'An exception occurred: {stock["ticker"]}, {finance_type}') 
            print(e)
session.flush()
session.commit()
