'''
Created on 07-Sep-2019

@author: rahuljain
'''

import logging as log
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import datetime

from itertools import combinations
from scipy.optimize import minimize
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
from plotly.subplots import make_subplots
from portfoliotools.screener.stock_detail import StockDetail
from portfoliotools.screener.utility.util import flatten_dicts_of_dicts, getHistoricStockPrices,memoize,get_port_ret_vol_sr
#from StockScreenerAPI.utility.util import isValidStock, getSector
sns.set()

class StockScreener( object ):
    
    def __init__(self, stock_list, cob = None):
        self.cob        = cob if cob else datetime.datetime.today()
        self.stock_list = stock_list
        self._summary   = pd.DataFrame()
        
    @property
    def cob(self):
        return self._cob
    
    @cob.setter
    def cob(self, cob):
        self._cob = cob
        
    @property
    def stock_list(self):
        return self._stock_list
    
    @stock_list.setter
    def stock_list(self, stock_list):
        self._stock_list = stock_list#[stock for stock in stock_list if isValidStock(stock)]
        invalid = set(stock_list) - set(self._stock_list)
        if invalid:
            log.info('Dropped following stocks since these were not valid indicators : {0}'.format(invalid))
            
    def get_summary(self,result_format = 'dataframe'):
        if self._summary.empty:
            self._summary = self._generate_summary(result_format)
        return self._summary
    
    def _generate_summary(self, result_format = 'dataframe'):
        if result_format not in ['dataframe', 'list']: 
            log.error("Result format not valid")
            raise TypeError("Result format not valid")
        
        try:
            i = 1
            summary = []
            total_stocks = len(self.stock_list)
                        
            for stock in self.stock_list:
                log.info("Fetching details for - {0} ({1}/{2})".format(stock, i, total_stocks))
                detail              = flatten_dicts_of_dicts(StockDetail(stock, self.cob).details())
                detail['Sector']    = ""#getSector(stock)
                summary.append(detail)
                #print(str((i)*100/total_stocks) + " % completed")
                i+=1
        except:
            log.error("Error generating summary report for screener")
        finally:
            return pd.DataFrame(summary) if result_format == 'dataframe' else summary
            
    def get_recommendations(self):
        try:
            return pd.concat([self.buy_recommondations(), self.sell_recommondations()])
        except:
            log.error("Error generating recommendations")
            return pd.DataFrame()
    
    def buy_recommondations(self):
        pass
    
    def sell_recommondations(self):
        pass
    

class PortfolioStrategy( object ):
    
    def __init__(self, stock_list, cob = None, period = 700):
        self.stock_list     = stock_list
        self.cob            = cob or datetime.datetime.today()
        self.stock_prices   = self.get_historical_prices(self.stock_list, period = period)
    
    def get_screener_details( self ):

        obj = StockScreener(self.stock_list, cob = self.cob)
        return obj.get_summary()
    
    @memoize
    def get_details( self):
        result = []
        for ind, stock in enumerate(self.stock_list):
            temp = {}
            wt = [0]*len(self.stock_list)
            wt[ind] = 1
            temp['Name'] = stock
            temp['Return'], temp['Risk'], temp['Sharpe'] = get_port_ret_vol_sr(self.stock_prices, wt)
            result.append(temp)
        return pd.DataFrame(result)
    
    @memoize
    def get_historical_prices(self, stock_list = None, end_date = None, period = 700):
        
        end_date = end_date or self.cob
        if stock_list is None:
            stock_list = self.stock_list
        prices = pd.DataFrame()
        
        for stock in stock_list:
            prices[stock] = getHistoricStockPrices(stock, end_date = end_date, days = period)['Adj Close']
            
        return prices
    
    @memoize
    def calcStat( self, stock_prices = None, format_result = False):
        
        if stock_prices is None:
            stock_prices = self.stock_prices

        stock_prices.index = pd.to_datetime(stock_prices.index)
            
        stat = pd.DataFrame( columns = stock_prices.columns, 
                            index = ["Period Start Date", "Period End Date", "Period Start Value", "Period End Value",
                                    "Return (ann.)", "Risk (ann.)", "Sharpe Ratio", 'Best Day', 'Worst Day',
                                    'Max Drawdown', 'Best Month', 'Best Month Return (abs)', 'Worst Month', 
                                     'Worst Month Return (abs)',] )

        stat.loc['Period Start Date']   = stock_prices.index.min()
        stat.loc['Period End Date']     = stock_prices.index.max()
        stat.loc['Period Start Value']  = stock_prices.iloc[0,:]
        stat.loc['Period End Value']    = stock_prices.iloc[-1,:]

        stat.loc['Return (ann.)']       = np.round(np.log(stock_prices/stock_prices.shift(1)).mean()*252*100,2)
        stat.loc['Risk (ann.)']         = np.round(np.log(stock_prices/stock_prices.shift(1)).std()*np.sqrt(252)*100,2)
        stat.loc['Sharpe Ratio']        = stat.loc['Return (ann.)']/stat.loc['Risk (ann.)']

        stat.loc['Best Day']            = np.round((stock_prices/stock_prices.shift(1) -1).max()*100,2)
        stat.loc['Worst Day']           = np.round((stock_prices/stock_prices.shift(1) -1).min()*100,2)
        stat.loc['Max Drawdown']        = np.round(((stock_prices / stock_prices.expanding(min_periods=1).max()).min() - 1)*100,2)

        monthly_prices                  = stock_prices.resample('M').last()
        monthly_prices                  = monthly_prices/monthly_prices.shift(1) - 1
        monthly_prices['Month']         = monthly_prices.index.month_name().tolist()

        stat.loc['Best Month']                = monthly_prices.groupby('Month').mean().idxmax()
        stat.loc['Best Month Return (abs)']   = np.round(monthly_prices.groupby('Month').mean().max()*100,2)
        stat.loc['Worst Month']               = monthly_prices.groupby('Month').mean().idxmin()
        stat.loc['Worst Month Return (abs)']  = np.round(monthly_prices.groupby('Month').mean().min()*100,2)

        if format_result:
            stat.loc['Best Day']            = stat.loc['Best Day'] .astype(str) + "%"
            stat.loc['Worst Day']           = stat.loc['Worst Day'] .astype(str) + "%"
            stat.loc['Return (ann.)']       = stat.loc['Return (ann.)'] .astype(str) + "%"
            stat.loc['Risk (ann.)']         = stat.loc['Risk (ann.)'] .astype(str) + "%"
            stat.loc['Max Drawdown']        = stat.loc['Max Drawdown'] .astype(str) + "%"
            stat.loc['Best Month Return (abs)']   = stat.loc['Best Month Return (abs)'] .astype(str) + "%"
            stat.loc['Worst Month Return (abs)']  = stat.loc['Worst Month Return (abs)'] .astype(str) + "%"

        return stat


    @memoize
    def get_daily_returns( self, stock_prices = None):
        if stock_prices is None:
            stock_prices = self.stock_prices
        return stock_prices.pct_change().dropna()
    
    @memoize
    def get_cumulative_returns( self, stock_prices = None):
        if stock_prices is None:
            stock_prices = self.stock_prices
        return self.get_daily_returns().add(1).cumprod().dropna()
    
    @memoize
    def get_correlation_matrix( self, stock_prices = None):
        if stock_prices is None:
            stock_prices = self.stock_prices
        cum_returns = self.get_cumulative_returns(stock_prices)
        return cum_returns.corr()
    
    @memoize
    def get_correlation_pair( self, stock_prices = None):
        
        correlation_pair = []
        if stock_prices is None:
            stock_prices = self.stock_prices
            
        corr = self.get_correlation_matrix(stock_prices)
        stock_list = corr.columns.tolist()
        
        for s1,s2 in combinations(stock_list, 2):
            correlation_pair.append((s1,s2,corr.loc[s1][s2]))
            
        correlation_pair = pd.DataFrame(correlation_pair, columns = ['Stock 1', 'Stock 2', 'Correlation'])
        correlation_pair = correlation_pair.sort_values(by ='Correlation', ascending=False)
        correlation_pair.reset_index(drop = True, inplace = True)
        return correlation_pair
    
    def plot_correlation_matrix( self, corr = None, annot = False):
        if corr is None:
            corr = self.get_correlation_matrix()
            
        _, ax = plt.subplots(figsize=(11, 9))
        cmap = sns.diverging_palette(220, 10, as_cmap = True)
        sns.heatmap(corr, cmap = cmap, ax = ax, vmax = 1.0, vmin = -1.0, linewidths = 0.5, annot = annot)
        plt.title('Correlation Matrix')
        return plt
    
    def get_efficient_market_portfolio(self, stock_prices = None, plot = False, show_frontier = False, num_ports = 10000):
    
        def _get_ret_vol_sr(weights):
            weights = np.array(weights)
            ret = np.sum(log_ret.mean() * weights) * 252
            vol = np.sqrt(np.dot(weights.T, np.dot(log_ret.cov()*252, weights)))
            sr = ret/vol
            return np.array([ret, vol, sr])

        def _neg_sharpe(weights):
        # the number 2 is the sharpe ratio index from the get_ret_vol_sr
            return _get_ret_vol_sr(weights)[2] * -1

        def _check_sum(weights):
            #return 0 if sum of the weights is 1
            return np.sum(weights)-1

        def _minimize_volatility(weights):
            return _get_ret_vol_sr(weights)[1]

        if stock_prices is None:
            stock_prices = self.stock_prices

        stocks     = stock_prices.columns.tolist()
        log_ret    = np.log(stock_prices/stock_prices.shift(1))
        
        cons       = {'type' : 'eq', 'fun' : _check_sum}
        bounds     = tuple([(0,1)]*len(stocks))
        init_guess = [1/len(stocks)]*len(stocks)

        opt_results = minimize(_neg_sharpe, init_guess, method='SLSQP', bounds = bounds, constraints=cons)

        market_port = {k + ' (%)':v*100 for k,v in zip(stocks, np.round(opt_results.x, 4))}
        market_port['Return'], market_port['Risk'], market_port['Sharpe'] = np.round(_get_ret_vol_sr(opt_results.x),4)
        
        if plot:
            np.random.seed(42)
            num_ports   = num_ports
            all_weights = np.zeros((num_ports, len(stocks)))
            ret_arr     = np.zeros(num_ports)
            vol_arr     = np.zeros(num_ports)
            sharpe_arr  = np.zeros(num_ports)

            for x in range(num_ports):
                # Weights
                weights = np.array(np.random.random(len(stocks)))
                weights = weights/np.sum(weights)

                # Save weights
                all_weights[x,:] = weights

                # Calc Details
                ret_arr[x], vol_arr[x], sharpe_arr[x] = _get_ret_vol_sr(weights)

            # Calculate Frontier
            if show_frontier:
                _det = self.get_details()
                frontier_upper_bound = np.max(_det['Return'].max(),0)
                frontier_lower_bound = np.max(_det['Return'].min(),0)
                frontier_y = np.linspace(frontier_lower_bound,frontier_upper_bound,10)
                frontier_x = []
                frontier_wt = []
                i = 0
                for possible_return in frontier_y:
                    cons = ({'type':'eq', 'fun':_check_sum},
                            {'type':'eq', 'fun': lambda w: _get_ret_vol_sr(w)[0] - possible_return})

                    result = minimize(_minimize_volatility,init_guess,method='SLSQP', bounds=bounds, constraints=cons)
                    if result.success:
                        frontier_wt.append({k:v for k,v in zip(stocks, np.round(result.x, 4))})
                        frontier_x.append(result['fun'])
                    else:
                        frontier_wt.append({})
                        frontier_x.append(np.nan)
                        frontier_y[i] = np.nan
                    i+=1
            
            fig = make_subplots(rows = 1, cols = 1)
            
            fig.add_trace(go.Scatter(x=vol_arr,y=ret_arr, mode='markers', name = '',
                    marker=dict( size=2, color=sharpe_arr, colorbar=dict( title="Sharpe"),
                    colorscale="Viridis")), row = 1, col = 1)
            fig.add_trace(
                        go.Scatter(x=[market_port['Risk']], y=[market_port['Return']], name = '', mode='markers',
                                   marker=dict( size=8, color='blue')), row = 1, col =1,
                        )
            if show_frontier:
                hovertext = []
                i = 0
                for wt in frontier_wt:
                    text = ""
                    for k,v in wt.items():
                        if v !=0:
                            text = text + k + ": " + str(np.round(v*100,2)) + "%<br>"

                    text = text + "Return: " + str(np.round(frontier_y[i]*100,2)) + "%<br>"
                    text = text + "Risk: "   + str(np.round(frontier_x[i]*100,2)) + "%<br>"
                    text = text + "Sharpe: " + str(np.round(frontier_y[i]/frontier_x[i],4)) + "<br>"
                    hovertext.append(text)
                    i+=1
                fig.add_trace(
                        go.Scatter(x=frontier_x, y=frontier_y, name = '', text = hovertext, mode='markers',
                                   marker=dict( size=8, color='red')), row = 1, col =1,
                        )
            fig['layout']['yaxis1'].update(title='Return')
            fig['layout']['xaxis1'].update(title='Risk')
            fig.update_layout(
                        title={
                            'text': "Efficient Frontier",
                            'y':0.9,
                            'x':0.4,
                            'xanchor': 'center',
                            'yanchor': 'top'})

            fig.show()

        return pd.DataFrame([market_port], index = ['MP'])


class ModelBase( object ):
    
    def __init__( self, x, y, train_test_split = .8):
        ''' x, y are pd.Series dtype
        '''
        self.x_points = x
        self.y_points = y
        self.xTrain, self.xTest, self.yTrain, self.yTest = self.get_train_test_data(x,y, train_test_split)
        
    def get_train_test_data( self, x, y, train_test_split = .8):
        xTrain, xTest = x[:int(len(x)*train_test_split)], x[int(len(x)*train_test_split):]
        yTrain, yTest = y[:int(len(y)*train_test_split)], y[int(len(y)*train_test_split):]
        
        return xTrain, xTest, yTrain, yTest
    
class ADF_Reg_Model( ModelBase ):
    
    def __init__( self, x,y,train_test_split = .8, *args, **kwargs):
        super().__init__(x,y,train_test_split, *args, **kwargs)
        
    def plot_scatter(self, x = None, y = None, x_label = 'x', y_label = 'y'):
        
        if x is None:
            x = self.x_points
        if y is None:
            y = self.y_points
            
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.scatter(x, y)
        plt.title('Scatter Regression')
        plt.show()
        
    @memoize
    def getModel(self):
        x = self.xTrain
        y = self.yTrain
        model = linear_model.LinearRegression()
        model.fit(x.reshape((len(x), 1)), y)
        
        return model
    
    def getModelStats(self):
        
        stats = {'Correlation'     : '', 
                 'Coef'            : '',
                 'Intercept'       : '',
                 'RMSE Test'       : '',
                 'RMSE Train'      : '',
                }
        
        model = self.getModel()
        stats['Intercept']   = model.intercept_
        stats['Coef']        = model.coef_
        stats['Correlation'] = np.corrcoef(self.x_points,self.y_points)[0,1]
        if len(self.xTest)>0:
            mse_test             = np.round(mean_squared_error(self.yTest, self.predict(self.xTest)),3)
            stats['RMSE Test']   = np.round(np.sqrt(mse_test),3)
        mse_train            = np.round(mean_squared_error(self.yTrain, self.predict(self.xTrain)),3)
        stats['RMSE Train']  = np.round(np.sqrt(mse_train),3)
        
        
        return stats
                                      
    def predict(self, x):
        ''' x: series
        '''
        model = self.getModel()
        return model.predict(x.reshape((len(x),1)))
    
    def getResidual(self, x, y):
        model = self.getModel()

        residual = model.predict(x.reshape((len(x), 1))) - y
        return residual
    
    def getSignals( self, x = None, y = None):
        
        if x is None:
            x = self.x_points
        if y is None:
            y = self.y_points
        
        df             = pd.DataFrame(columns = ['x', 'y'])
        df['x']        = x
        df['y']        = y
        df['y_pred']   = self.predict(x)
        df['res']      = self.getResidual(x,y)
        df['res_mean'] = df['res'].rolling(window = 22).mean()
        df['res_std']  = df['res'].rolling(window = 22).std()
        df['x_signal'] = df[['res', 'res_mean', 'res_std']].apply(lambda x: 'SELL' if x['res'] > x['res_mean'] + 2*x['res_std']
                                                                  else 'BUY' if x['res'] < x['res_mean'] - 2*x['res_std'] else ''
                                                                  , axis = 1)
        df['y_signal'] = df[['res', 'res_mean', 'res_std']].apply(lambda x: 'BUY' if x['res'] > x['res_mean'] + 2*x['res_std']
                                                                  else 'SELL' if x['res'] < x['res_mean'] - 2*x['res_std'] else ''
                                                                  , axis = 1)
        return df
    
    def plot_results(self):
        fig = make_subplots(rows = 3, cols = 1, shared_xaxes= False, vertical_spacing = 0.08, 
            column_widths = [15], row_heights = [2,2,2],
            specs=[[{"secondary_y": False}], [{"secondary_y": False}], [{"secondary_y": False}]])

        #2X1
        data   = self.getSignals(self.x_points, self.y_points)
        x_buy  = data[data['x_signal'] == 'BUY']
        y_buy  = data[data['y_signal'] == 'BUY']
        x_sell = data[data['x_signal'] == 'SELL']
        y_sell = data[data['y_signal'] == 'SELL']

        fig.add_trace(
                go.Scatter(y=self.y_points, name="Y (Actual)", 
                           line = {'color':'RGB(150,0,0)'}), row = 2, col =1,)
        fig.add_trace(
                go.Scatter(y=self.x_points, name="X (Actual)", 
                           line = {'color':'RGB(100,100,100)'}), row = 2, col =1,)

        # Signal
        fig.add_trace(go.Scatter(x=x_buy.index,y=x_buy['x'], mode='markers', name = 'X Buy Signal (Train)',
                marker=dict( size=4, color='green')), row = 2, col = 1)
        fig.add_trace(go.Scatter(x=y_buy.index,y=y_buy['y'], mode='markers', name = 'Y Buy Signal (Train)',
                marker=dict( size=4, color='green')), row = 2, col = 1)
        fig.add_trace(go.Scatter(x=x_sell.index,y=x_sell['x'], mode='markers', name = 'X Sell Signal (Train)',
                marker=dict( size=4, color='red')), row = 2, col = 1)
        fig.add_trace(go.Scatter(x=y_sell.index,y=y_sell['y'], mode='markers', name = 'Y Sell Signal (Train)',
                marker=dict( size=4, color='red')), row = 2, col = 1)

        #1X1
        fig.add_trace(
                        go.Scatter(x = self.xTrain, y=self.yTrain, name="Data (Train)", 
                                marker=dict(color="gray", size=4), mode="markers"),row = 1, col = 1)

        fig.add_trace(
                        go.Scatter(x = self.xTest, y=self.yTest, name="Data (Test)", 
                                marker=dict(color="orange", size=4), mode="markers"),row = 1, col = 1)

        fig.add_trace(
                go.Scatter(x=self.x_points, y=self.predict(self.x_points), name="Y (Predicted)", 
                           line = {'color':'RGB(200,0,0)'}), row = 1, col =1,)

        #3X1
        res_train = self.getResidual(self.xTrain, self.yTrain)
        x_train   = list(range(len(res_train)))
        res_test  = self.getResidual(self.xTest, self.yTest)
        x_test    = list(range(len(res_train), len(res_train) + len(res_test)))

        data = self.getSignals(self.x_points, self.y_points)
        fig.add_trace(
                go.Scatter(x=x_train, y = res_train, name="Residual(Train)", 
                           line = {'color':'RGB(50,50,50)'}), row = 3, col =1,)
        fig.add_trace(
                go.Scatter(x=x_test, y = res_test, name="Residual(Test)", 
                           line = {'color':'RGB(100,100,100)'}), row = 3, col =1,)
        fig.add_trace(
                go.Scatter(y = data['res_mean'] + 2*data['res_std'], name="Residual(Upper) - BUY Y/SELL X", 
                           line = {'color':'RGB(0,200,0)'}), row = 3, col =1,)
        fig.add_trace(
                go.Scatter(y = data['res_mean'] - 2*data['res_std'], name="Residual(Lower) - SELL Y/BUY X", 
                           line = {'color':'RGB(250,0,0)'}), row = 3, col =1,)

        # Fig Props
        fig['layout']['yaxis1'].update(title='Actual')
        fig['layout']['yaxis2'].update(title='Scatter Plot')
        fig['layout']['yaxis3'].update(title='Residual')

        fig.update_layout(
            title={
                'text': "ADF Analysis",
                'y':0.9,
                'x':0.4,
                'xanchor': 'center',
                'yanchor': 'top'})
        fig.show()