'''
Created on 05-Sep-2019

@author: rahul jain
Description: Utility module for screener calculations
'''

import datetime
import pandas as pd
import logging as log
import pandas_datareader as pdr
import numpy as np
import matplotlib.pyplot as plt
import bs4 as bs
import requests

from collections.abc import Iterable
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from nsepy import get_history

#from .constant import STOCK_LIST

def memoize( func ):
    memory = {}
    
    def wrapper( *args, **kwargs):
        key = hash(func.__name__ + str(args) + str(kwargs))
        if key not in memory:
            memory[key] = func( *args, **kwargs)
        return memory[key]
    
    return wrapper
    

def getHistoricStockPrices(stock_name, end_date = None, days = 700):
    ''' 
        [Description]: Factory method to get historic stock prices 
        [Input] 
            stock_name: Name of the stock
            start_date: Start Date. Defaulted to today.
            days: No of past days. Defaulted to 700 days
        [Output]
            Pandas data frame with high, close, AdjClose, volume for each historical date.
    '''
    
    log.info("Fetching details for: {0}".format(stock_name))
    try:
        if end_date is None: end_date = datetime.datetime.today()
        start_date = end_date + datetime.timedelta( days = -1* days )
        
        hist_prices = getHistoricStockPricesFromYahoo(stock_name + '.NS',start_date, end_date)
        if not hist_prices.empty: return hist_prices

        hist_prices = getHistoricStockPricesFromYahoo(stock_name,start_date, end_date)
        if not hist_prices.empty: return hist_prices

        hist_prices = getHistoricalIndexData(stock_name,start_date, end_date)
        if not hist_prices.empty: return hist_prices
        
        hist_prices = getHistoricalMFData(stock_name,start_date, end_date)
        if not hist_prices.empty: return hist_prices
    
    except:
        log.error("Unable to fetch details for: {0}".format(stock_name))
    return pd.DataFrame(columns = ['High', 'Low', 'Open', 'Close', 'Volume', 'Adj Close'])

def getHistoricStockPricesFromYahoo( stock_name, start_date = None, end_date = None):
    '''
        [Description]: Utility method to get historic stock prices from Yahoo 
        [Input] 
            stock_name: Name of the stock
            start_date: Start Date. Defaulted to today.
            days: No of past days. Defaulted to 365 days
        [Output]
            Pandas data frame with high, close, AdjClose, volume for each historical date.
    '''

    try:
        if end_date is None: end_date = datetime.datetime.today()
        if start_date is None: start_date = end_date + datetime.timedelta( days = -1* 365 )

        hist_prices = pdr.DataReader(name = stock_name, data_source = 'yahoo',start = start_date, end = end_date)
        return hist_prices
        
    except:
        return pd.DataFrame()
    
def getHistoricalIndexData( index_name, start_date = None, end_date = None):
    '''
        [Description]: Utility method to get historic index returns
        [Input] 
            index_name: Name of the stock
            start_date: Start Date. Defaulted to 1 year back.
            end_date: End Date. Defaulted to today.
        [Output]
            Pandas data frame with high, close, AdjClose, volume for each historical date.
    '''
    try:
        if end_date is None: end_date = datetime.datetime.today()
        if start_date is None: start_date = end_date + datetime.timedelta( days = -1* 365 )
            
        hist_prices = get_history(index_name, start=start_date, end=end_date, index=True)
        hist_prices['Adj Close'] = hist_prices['Close']
        return hist_prices
        
    except:
        return pd.DataFrame()
    
def getHistoricalMFData( isin, start_date = None, end_date = None):
    '''
        [Description]: Utility method to get historic index returns
        [Input] 
            index_name: Name of the stock
            start_date: Start Date. Defaulted to 1 year back.
            end_date: End Date. Defaulted to today.
        [Output]
            Pandas data frame with high, close, AdjClose, volume for each historical date.
    '''
    try:
        from portfoliotools.screener.mutual_fund_screener import MutualFundScreener
        if end_date is None: end_date = datetime.datetime.today()
        if start_date is None: start_date = end_date + datetime.timedelta( days = -1* 365 )
            
        obj = MutualFundScreener()
        scheme_code = obj.searchSchemes(isin_list=[isin]).index.tolist()[0]
        
        nav = obj.get_historical_nav(codes = [scheme_code])
        mask = (nav.index <= end_date) & (nav.index >= start_date)
        nav = nav[mask]
        
        nav.columns      = ['Close']
        nav['Volume']    = 0
        nav['Open']      = nav['Close']
        nav['High']      = nav['Close']
        nav['Low']       = nav['Close']
        nav['Adj Close'] = nav['Close']

        return nav
        
    except:
        return pd.DataFrame()
        
    
def ema( data, period = 10):
    '''
        [Description] : Utility method to calculate exponential moving averages over a period.
    '''
    result = [0]*len(data)
    
    for i, j in enumerate(data):
        if i < period-1:
            result[i] = 0
        elif i == period-1:
            result[i] = sum(data[:period])/period
        else:
            result[i] = (j * 2)/(period + 1) + result[i-1]*(1 - 2/(period + 1))
    return result
    
def cum_pattern( data ):
    '''
        [Description] : Utility method to calculate cumulative sum of sequential no.s if sign is same.
    '''
    prev = 0
    out = []
    for l in data:
        new = l + prev if l*prev > 0 else l
        out.append(new)
        prev = new
    return out

def smooth_avg(values, lookback_period = 14):
    '''
        [Description] : Utility method to calculate smooth average for a list of values using a lookback period
    '''
    result = [np.nan]*len(values)
    total = 0
    for i,val in enumerate(values):
        if i < lookback_period-1:
            total += val
        elif i == lookback_period-1:
            total += val
            result[i] = total/lookback_period
        else:
            result[i] = (result[i-1]*(lookback_period-1) + val)/lookback_period
    return result

def slope( ser, period = 5):
    '''
        [Description] : Utility method to calculate slope of a series based on last (period) of points
    '''
    import statsmodels.api as sm
    
    slope = [0]*(period-1)
    for i in range(period, len(ser) + 1):
        y = ser[i-period:i]
        x = np.array(range(period))
        y_scaled = y-y.min()/(y.max() - y.min())
        x_scaled = x-x.min()/(x.max() - x.min())
        x_scaled = sm.add_constant(x_scaled)
        model = sm.OLS(y_scaled, x_scaled)
        result = model.fit()
        slope.append(result.params[-1])
    slope = np.rad2deg(np.arctan(slope))
    return slope

def flatten_dicts_of_dicts(dictOfdict):
    '''
        [Description] : Flattens dictionary of dictionaries to return the dictionary type
        [Input']
            dictOfdict = {'a' : {'b' : 1,
                                'c' : 2
                                }
                         'd' : {'e' : 3,
                                 'f' : 4
                                 }
                         'g' : 5
                        }
        [Output]
            {'b' : 1, 'c' : 2', 'e' : 3, 'f' : 4 'g' : 5}
    '''
    result = dict()
    for key, val in dictOfdict.items():
        if isinstance(val, dict):
            result.update(flatten_dicts_of_dicts(val))
        else:
            result.update({key : val})
            
    return result

def timeit(func):
    
    ''' Decorator to time the function '''
    
    def wrapper( *args, **kwargs ):
        start = datetime.datetime.utcnow()
        
        result = func( *args, **kwargs)
        end = datetime.datetime.utcnow()
        log.info("{0} executed in {1} seconds.".format(func.__name__, str((end-start).seconds)))
        print("{0} executed in {1} seconds.".format(func.__name__, str((end-start).seconds)))
        return result
    
    return wrapper

def NumToStr(val):
    if isinstance(val, Iterable):
        return ['{:,}'.format(l) for l in val]
    else:
        return '{:,}'.format(val)

def backTestStrategy(data, signal_col_name = 'Signal'):
    df = data.copy()
    dates = df.index.tolist()
    startCash = np.ceil(df.loc[dates[0],'Close']/100000)*100000
    
    df['Passive Holding'] = 0
    df['Active Holding']  = 0
    df['Signal'] = df[signal_col_name]
    df['Passive Cash'] = startCash
    df['Active Cash'] = startCash
    df['Passive Investment'] = startCash
    df['Active Investment']  = startCash
    for i in range(0,df.shape[0]):
        dt = dates[i]
        
        # Passive Strategy
        if i>0:
            df.loc[dt, 'Passive Holding'] = df.loc[dates[i-1], 'Passive Holding']
            df.loc[dt, 'Passive Cash']    = df.loc[dates[i-1], 'Passive Cash']
        if df.loc[dt,'Signal'] == "BUY" and df.loc[dt,'Passive Holding'] == 0:
            df.loc[dt, 'Passive Holding'] = np.floor(df.loc[dt,'Passive Cash']/df.loc[dt,'Close'])
            df.loc[dt, 'Passive Cash']    -= (df.loc[dt,'Close'] * df.loc[dt, 'Passive Holding'])
        elif df.loc[dt,'Signal'] == "SELL" and df.loc[dt,'Passive Holding'] > 0:
            df.loc[dt, 'Passive Cash'] += df.loc[dt, 'Passive Holding']*df.loc[dt, 'Close']
            df.loc[dt, 'Passive Holding'] = 0
        
        # Active Strategy
        if i>0:
            df.loc[dt, 'Active Holding']    = df.loc[dates[i-1], 'Active Holding']
            df.loc[dt, 'Active Cash']       = df.loc[dates[i-1], 'Active Cash']
            df.loc[dt, 'Active Investment'] = df.loc[dates[i-1], 'Active Investment']
        if df.loc[dt, 'Signal'] == 'BUY':
            if df.loc[dt, 'Active Cash'] < df.loc[dt, 'Close']:
                df.loc[dt,'Active Cash']        += startCash
                df.loc[dt, 'Active Investment'] += startCash
            newShares = np.floor(df.loc[dt,'Active Cash']/df.loc[dt,'Close'])
            df.loc[dt, 'Active Holding'] += newShares
            df.loc[dt, 'Active Cash']    -= (df.loc[dt,'Close'] * newShares)
        elif df.loc[dt, 'Signal'] == 'SELL' and df.loc[dt, 'Active Holding'] >0:
            df.loc[dt, 'Active Cash'] += df.loc[dt, 'Active Holding']*df.loc[dt, 'Close']
            df.loc[dt, 'Active Holding'] = 0
                
            
            
    df['Passive Portfolio'] = (df['Close']*df['Passive Holding'] + df['Passive Cash'])*100.0/df['Passive Investment']
    df['Active Portfolio'] = (df['Close']*df['Active Holding'] + df['Active Cash'])*100.0/df['Active Investment']

    #Drop Signal Col
    if not signal_col_name == "Signal": 
        df.drop('Signal', axis = 1, inplace = True)
    return df

def smape_kun(y_true, y_pred):
    return np.mean((np.abs(y_pred - y_true) * 200/ (np.abs(y_pred) +       np.abs(y_true))))


def get_arima_predictions(ts, p = 5, q = 1, d = 0, test_per = .8, plot = False):
    ''' data: time series.
    '''
    
    result = {
        'MSE'         : np.nan,
        'SMAPE KUN'    : np.nan,
        'Pred Value'   : np.nan,
        'Pred Low 5%'  : np.nan,
        'Pred High 5%' :np.nan,
    }
    fig = None
    
    df = pd.DataFrame(data = ts, columns = ['data'])
    train_data, test_data = df[0:int(len(df)*0.8)], df[int(len(df)*0.8):]
    
    train, test = train_data['data'].values, test_data['data'].values
    history = [x for x in train]
    predictions = list()
    for t in range(len(test)):
        model = ARIMA(history, order=(p,q,d))
        model_fit = model.fit(disp=0)
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)
    error = mean_squared_error(test, predictions)
    result['MSE'] = np.round(error, 3)
    error2 = smape_kun(test, predictions)
    result['SMAPE KUN'] = np.round(error2, 3)
    
    model = ARIMA(history, order=(p,q,d))
    model_fit = model.fit(disp=0)
    output = model_fit.forecast()
    
    result['Pred Value']  = np.round(output[0],2)
    result['Pred Low 5%'] = np.round(output[2][0][0],2)
    result['Pred High 5%']= np.round(output[2][0][1],2)
    
    # Plot
    if plot:
        df['data_lag'] = df['data'].shift(5)
        df = df.dropna()

        fig = plt.figure(figsize = (10,10))
        fig.suptitle("ARIMA Analysis")

        ax1 = fig.add_axes([0,.45,.5,.45])
        ax1.scatter(x=df['data'].values, y=df['data_lag'].values, label = "Autocorrelation")
        ax1.legend()

        ax2 = fig.add_axes([.55,.45,.5,.45])
        ax2.plot(df['data'], 'blue', label='Training Data')
        ax2.plot(test_data['data'], 'red', label='Testing Data')
        ax2.legend()

        ax3 = fig.add_axes([0,0,.5,.40])
        ax3.plot(df['data'], 'green', color='blue', label='Trained')
        ax3.plot(test_data.index, predictions, color='green', marker='o', linestyle='dashed', 
                 label='Predicted')
        ax3.plot(test_data.index, test_data['data'], color='red', label='Actual')
        ax3.legend()

        ax4 = fig.add_axes([.55,0,.5,.40])
        ax4.plot(test_data.index, predictions, color='green', marker='o', linestyle='dashed',label='Predicted')
        ax4.plot(test_data.index, test_data['data'], color='red', label='Actual')
        ax4.legend()
    
    return (result,fig)


def get_ticker_list(urlpath = 'https://en.wikipedia.org/wiki/NIFTY_50'):
    resp = requests.get(urlpath)
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = {'Name'   : row.findAll('td')[0].text,
                  'Ticker' : row.findAll('td')[1].text.replace(".NS", ""),
                  'Sector' : row.findAll('td')[2].text.replace("\n", "")
                 }
        tickers.append(ticker)
    return tickers

def get_nse_index_list():
    from nsetools import Nse
    nse = Nse()
    return nse.get_index_list()

def get_port_ret_vol_sr(stock_prices, weights):
    log_ret    = np.log(stock_prices/stock_prices.shift(1))
    weights = np.array(weights)
    ret = np.sum(log_ret.mean() * weights) * 252
    vol = np.sqrt(np.dot(weights.T, np.dot(log_ret.cov()*252, weights)))
    sr = ret/vol
    return np.array([ret, vol, sr])