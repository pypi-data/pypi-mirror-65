
import datetime
import math
import logging as log
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from copy import deepcopy
from stocktrends import Renko
from portfoliotools.screener.utility.util import getHistoricStockPrices, ema, cum_pattern, smooth_avg, slope, backTestStrategy
from portfoliotools.screener.utility.constant import WILLIAM_K_UL, WILLIAM_K_LL, fundamental_info_cols
from portfoliotools.screener.stock_fundamentals import StockFundamentals

class StockDetail( object ):
    
    def __init__(self, name, cob = None, period = 700):
        
        __slots__               = 'name', 'cob', 'historical_prices', '_details'
        self._details           = dict()
        self.name               = name
        self.cob                = cob
        self.historical_prices  = self._get_historical_prices(period)
        self.technical_details  = None
        self.add_to_details_flg = False
        
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name
        self.refresh_details()
        
    @property
    def cob(self):
        return self._cob
    
    @cob.setter
    def cob(self,cob = None):
        self._cob = cob if cob else datetime.datetime.today()
        self.refresh_details()
        
    def _add_to_technical_details(self, data, data_type, cols = None, col_map = None):
        
        if self.add_to_details_flg:
            if self.technical_details is None:
                self.technical_details         = deepcopy(self.historical_prices)
                self.technical_details.columns = pd.MultiIndex.from_product([["Prices"],self.technical_details.columns.tolist()])
                
            data = deepcopy(data)

            old_cols = [col[1] for col in self.technical_details.columns.tolist()]
            if not cols:
                cols = [col for col in data.columns.tolist() if col not in old_cols]

            data = data[cols]

            if col_map is not None:
                data.rename(columns = col_map, inplace = True)

            data.columns = pd.MultiIndex.from_product([[data_type],data.columns.tolist()])
            self.technical_details = self.technical_details.join(data, how = "outer")
        
    def details(self):
        if not self._details:
            self._generate_details()
        return self._details
    
    def refresh_details(self, force_refresh = True):
        if not force_refresh and self._details:
            self._generate_details()
    
    def _get_historical_prices(self, period = 700):
        try:
            result              = getHistoricStockPrices(self.name, end_date = self.cob, days=period)
            result              = result[result['Close'] != 0]

            result['Act Close'] = result['Close']
            result['Close']     = result['Adj Close']
            result['Act High']  = result['High']
            result['High']      = result['Act High']*result['Close']/result['Act Close']
            result['Act Low']   = result['Low']
            result['Low']       = result['Act Low']*result['Close']/result['Act Close']
            result['Act Open']  = result['Open']
            result['Open']      = result['Act Open']*result['Close']/result['Act Close']

            result['High']      = result[['High', 'Close']].apply(lambda row: row['High'] if row['High'] else row['Close'], axis = 1)
            result['Low']       = result[['Low', 'Close']].apply(lambda row: row['Low'] if row['Low'] else row['Close'], axis = 1)
            mean_vol            = result['Volume'].mean()
            result['Volume']    = result[['Volume']].apply( lambda row, mean_vol: row['Volume'] if row['Volume'] > 0 else mean_vol, args = (mean_vol,), axis = 1)
        except:
            log.error("Error fetching historical prices - {0}".format(self.name))
        finally:
            return result
    
    def _generate_details(self):
        
        self.add_to_details_flg = True
        self._details['Overview']              = self.get_overview()
        self._details['Technical Analytics']   = self.get_technical_analytics()
        self._details['Fundamental Analytics'] = self.get_fundamentals_info()
        self.add_to_details_flg = False
        
    def get_overview(self):
        
        info =  dict()
        try:
            info['Info']            = self.get_info()
            info['52W Statistics']  = self.get_52W_stats()
            info['Returns']         = self.get_stock_returns()
            
        except: 
            log.error("Error generating overview details - {0}".format(self.name))
        finally:
            return info
        
    def get_info(self):
        
        info = dict()
        try:
            info['Stock Name']          = self.name
            info['Date']                = self.cob.strftime("%d%b%y")
            info['Last Close']          = self._last_close()
            info['Last COB']            = self._last_cob()
            info['Average Volume']      = self._avg_volume()
            info['Standard Deviation']  = round(self._avg_daily_std_dev(),2)
            info['CAGR']                = round(self.get_cagr(),2)
            info['Annual Volatility']   = round(self.get_volatility(),2)
            info['Sharpe']              = round(self.get_sharpe_ratio(),3)
            info['Sortino']             = round(self.get_sortino_ratio(),3)
            
        except:
            log.error("Error generating stock info - {0}".format(self.name))
        finally:
            return info
        
    def get_52W_stats(self):
        
        info = dict()
        try:
            info['52W High']            = self._52w_high()
            info['52W Low']             = self._52w_low()
            info['Price% 52 Week']      = self._52w_price_per()
            info['Price per Range']     = self._52w_price_per_range()
        except:
            log.error("Error generating 52 Week statistics - {0}".format(self.name))
        finally:
            return info
        
    def get_stock_returns(self):
        
        info = dict()
        try:
            info['Return 1D']           = round(self.calculate_return(1)['Return'][-1],2)
            info['Return 1W']           = round(self.calculate_return(5)['Return'][-1],2)
            info['Return 1M']           = round(self.calculate_return(22)['Return'][-1],2)
            info['Return 1Y']           = round(self.calculate_return(260)['Return'][-1],2)
        except:
            log.error("Error generating stock returns - {0}".format(self.name))
            if 'Return 1D' not in info: info['Return 1D'] = -999
            if 'Return 1W' not in info: info['Return 1W'] = -999
            if 'Return 1M' not in info: info['Return 1M'] = -999
            if 'Return 1Y' not in info: info['Return 1Y'] = -999
        finally:
            return info
        
    def get_technical_analytics(self):
        
        info = dict()
        try:
            info['WilliamsR']           = self.get_williams_r_results()
            info['Moving Average']      = self.get_moving_averages(linear = (30,60,200), exponential = (12,26))
            info['MacD']                = self.get_macd_results()
            info['Bollinger Band']      = self.get_bollinger_results()
            info['RSI']                 = self.get_rsi_results()
            info['ATR']                 = self.get_atr_results()
            info['ADX']                 = self.get_adx_results()
            info['OBV']                 = self.get_obv_results()
            info['Slope']               = self.get_slope_results()
            info['Renko']               = self.get_renko_results()
        except:
            log.error("Error generating technical analytics - {0}".format(self.name))
        finally:
            return info
        
    def get_fundamentals_info(self):
        
        info = {attr:-999 for attr in fundamental_info_cols}
        try:
            result = self.get_fundamentals_details()
            for col in fundamental_info_cols:
                info[col] = result.get(col, -999)
        except:
            log.error("Error fetching fundamental analytics overview - {0}".format(self.name))
        finally:
            return info
        
    def get_fundamentals_details(self):
        
        info = dict()
        try:
            result = StockFundamentals(self.name)
            info = result.get_details_info()
        except:
            log.error("Error fetching fundamental analytics overview - {0}".format(self.name))
        finally:
            return info
        
    def calculate_return(self, period_in_days = 7):
        ''' Method to calculate absolute stock returns for period in days '''
        try:
            df = deepcopy(self.historical_prices)
            df['Return'] = (df['Close'] - df['Close'].shift(period_in_days))*100/df['Close'].shift(period_in_days)
            return df.dropna()
        except:
            log.error("Error calculating return for {1} for period - {0} days".format(period_in_days, self.name))
            df['Return'] = -999
            return df.dropna()
        
    def get_atr_results( self ):
        
        info = dict()
        try:
            details = self.get_atr_details().tail(1)
            info['ATR Value'] = round(details['ATR'][0],2)
        except:
            log.error("Error calculating ATR Results - {0}".format(self.name))
            info['ATR Value'] = -999
        finally:
            return info
        
    def get_atr_details(self, lookback_period = None):
        
        df = deepcopy( self.historical_prices )
        try:
            lookback_period  = lookback_period if lookback_period else self._lookback_period()
            df['High - Low'] = df['High'] - df['Low']
            df['High - PC']  = abs(df['High'] - df['Close'].shift(1))
            df['Low - PC']   = abs(df['Low']  - df['Close'].shift(1))
            df['TR']         = df.apply( lambda x: max(x['High - Low'], x['High - PC'], x['Low - PC']), axis = 1)
            df['ATR']        = df['TR'].rolling( window = lookback_period).mean()
        except:
            log.error("Error calculating ATR Details - {0}".format(self.name))
            df['High - Low'] = -999
            df['High - PC']  = -999
            df['Low - PC']   = -999
            df['TR']         = -999
            df['ATR']        = -999
        finally:
            self._add_to_technical_details(df, 'ATR', cols = ['ATR'], col_map = {'ATR':'Value'})
            return df.dropna()
        
    def get_slope_results( self ):
        
        info = dict()
        try:
            details = self.get_slope_details().tail(1)
            info['Slope Value'] = details['Slope'].values[0]
        except:
            log.error("Error calculating Slope Results - {0}".format(self.name))
            info['Slope Value'] = -999
        finally:
            return info
        
    def get_slope_details( self, period = 5):
        
        df = deepcopy( self.historical_prices)
        try:
            df['Slope'] = np.round(slope(df['Close']),2)
        except:
            df['Slope'] = -999
        finally:
            self._add_to_technical_details(df, 'Slope', cols = ['Slope'], col_map = {'Slope': 'Value'})
            return df.dropna()
        
    def get_renko_results( self ):
        
        info = dict()
        try:
            details = self.get_renko_details().tail(1)
            info['Renko Trend']    = details['Trend'].values[0]
            info['Renko Strength'] = details['Strength'].values[0]
            info['Renko Signal']   = details['Signal'].values[0]
            info['Renko Date']     = np.datetime_as_string(details['date'].values[0])[:10]
        except:
            log.error("Error calculating Renko Results - {0}".format(self.name))
            info['Renko Trend']    = ""
            info['Renko Strength'] = -999
            info['Renko Signal']   = ""
            info['Renko Date']     = ""
        finally:
            return info
        
    def get_renko_details( self, period = 2 ):
        
        df = deepcopy( self.historical_prices)
        try:
            df.reset_index( inplace = True )
            df.columns = [col.lower() for col in df.columns]
            renko_df   = Renko(df)
            renko_df.brick_size = self.get_atr_results()['ATR Value']
            df = renko_df.period_close_bricks()
            df['uptrend'] = df[['uptrend']].apply(lambda x: 1 if x['uptrend'] else -1, axis = 1)
            df['Trend'] = df[['uptrend']].apply( lambda x: 'UP' if x['uptrend'] > 0 else 'DOWN', axis = 1)
            df['Strength'] = df[['uptrend']].apply(cum_pattern)
            df['Signal'] = df[['Strength', 'Trend']].apply( lambda x: 'BUY' if abs(x['Strength']) >period-1 and x['Trend'] == 'UP' else 'SELL' if abs(x['Strength']) >period-1 and x['Trend'] == 'DOWN' else "", axis = 1)
        except:
            log.error("Error calculating Renko details - {0}".format(self.name))
            df['Trend'] = ""
            df['Strength'] = -999
            df['Signal'] = ""
        finally:
            #self._add_to_technical_details(df, 'Renko', cols = ['Trend', 'Strength', 'Signal'])
            return df.dropna()
        
    def get_obv_results( self ):
        
        info = dict()
        try:
            details = self.get_obv_details().tail(1)
            info['OBV Value']               = round(details['OBV'].values[0],2)
            info['OBV Index']               = round(details['OBV Index'].values[0],2)
            info['OBV Slope']               = round(details['OBV Index Slope'].values[0],2)
            info['OBV Signal']              = details['Signal'][0]
            info['OBV Passive Portfolio']   = round(details['Passive Portfolio'].values[0],2)
            info['OBV Active Portfolio']    = round(details['Passive Portfolio'].values[0],2)
        except:
            log.error("Error calculating OBV Results - {0}".format(self.name))
            info['OBV Value']               = -999
            info['OBV Index']               = -999
            info['OBV Slope']               = -999
            info['OBV Signal']              = ''
            info['OBV Passive Portfolio']   = -999
            info['OBV Active Portfolio']    = -999
        finally:
            return info
        
    def get_obv_details( self ):
        def _get_obv_signal(row, signal_val):
            ratio = abs(row['OBV Slope']/row['Close Slope'])
            if row['MA Slope']>0:
                if row['OBV Slope'] > 0:
                    if row['Close Slope']<0 or ratio > signal_val: return 'BUY'
                #elif row['OBV Slope'] < 0:
                #    if row['Close Slope'] > 0 or ratio < 1/signal_val: return 'SELL1'
            else:
                if row['OBV Slope']<0:
                    if row['Close Slope'] > 0 or ratio > signal_val: return 'SELL'
                #elif row['OBV Slope']>0:
                #    if row['Close Slope'] < 0 or ratio < 1/signal_val: return 'BUY2'
            return ''
            
        df = deepcopy(self.historical_prices)
        try:
            df['OBV']                   = df['Close'] - df['Close'].shift(1)
            df['OBV']                   = df[['Volume', 'OBV']].apply( lambda x: x['Volume'] if x['OBV'] > 0 else -1*x['Volume'] if x['OBV'] < 0 else 0, axis = 1)
            df['OBV']                   = df['OBV'].cumsum()
            df['OBV Index']             = df['OBV']/self._avg_volume()
            df['OBV Index Slope']       = np.round(slope(df['OBV Index']),2)
            df['OBV Slope']             = np.round(slope(df['OBV']/df['OBV'].mean()),2)
            df['Close Slope']           = np.round(slope(df['Close']),2)
            df['MA']                    = self.get_linear_moving_average(self._lookback_period())['{0}D Moving Average'.format(self._lookback_period())]
            df['MA Slope']              = slope(df['MA'], 3*self._lookback_period())
            df['OBV Slope/Close Slope'] = df['OBV Slope']/df['Close Slope']
            signal_val                  = 2*df.nlargest(np.round(df.shape[0]*.05,0).astype(int), ['OBV Slope/Close Slope'])['OBV Slope/Close Slope'].mean()
            df['Signal']                = df[['MA Slope', 'OBV Slope','Close Slope']].apply(_get_obv_signal, args = [signal_val,], axis = 1 )
            backtest                    = backTestStrategy(df,'Signal')[['Passive Portfolio', 'Active Portfolio']]
            df['Passive Portfolio']     = backtest['Passive Portfolio']
            df['Active Portfolio']      = backtest['Active Portfolio']
        except:
            log.error("Error calculating OBV details - {0}".format(self.name))
            df['OBV']                   = -999
            df['OBV Index']             = -999
            df['OBV Index Slope']       = -999
            df['OBV Slope']             = -999
            df['Close Slope']           = -999
            df['MA']                    = -999
            df['MA Slope']              = -999
            df['OBV Slope/Close Slope'] = -999
            df['Signal']                = ""
            df['Passive Portfolio']     = -999
            df['Active Portfolio']      = -999
        finally:
            self._add_to_technical_details(df, 'OBV', cols = ['MA Slope', 'OBV Slope', 'Signal', 'Passive Portfolio', 'Active Portfolio'])
            return df.dropna()

    def plot_obv_details( self, data = None, period = None ):
        '''
        data: Pandas DataFrame containing historical stock prices and OBV details. 
                Columns expected are - High, Low, Close, Volume, Highest High, OBV Index, Signal
        period: trailing period for which data needs to be plotted. Defaulted to show all.
        '''
        if data is None:
            data = self.get_obv_details()
        if period: data = data.tail(period)
        
        data = backTestStrategy(data,'Signal')

        buy_sig = data[data['Signal'] == 'BUY']
        sell_sig = data[data['Signal'] == 'SELL']
        
        fig = make_subplots(rows = 4, cols = 1, shared_xaxes= True, vertical_spacing = 0.08, 
            column_widths = [15], row_heights = [2,2,2,2],
            specs=[[{"secondary_y": False}], [{"secondary_y": False}], [{"secondary_y": False}],[{"secondary_y": False}]])

        hovertext      = ["<br>Close : " + "{:,}".format(np.round(txt['Close'],2)) + 
                    "<br>High: " + "{:,}".format(np.round(txt['High'],2)) + 
                    "<br>Low: " + "{:,}".format(np.round(txt['Low'],2)) + 
                    "<br>Volume: " + "{:,}".format(txt['Volume']) + 
                    "<br>OBV Index: " + "{:,}".format(np.round(txt['OBV Index'],2)) +
                    "<br>Signal: " + txt['Signal']
                    for txt in data.to_dict(orient = "records")]

        # Add OBV Indicator
        fig.add_trace(
                go.Scatter(x=data.index, y=data['OBV Slope/Close Slope'], name="OBV Slope/Close Slope", 
                        line = {'color':'darkblue'
                            }),row = 1, col = 1
                )
        fig.add_trace(
        go.Scatter(x=data.index, y=data['OBV'], name="OBV", text = hovertext, line = {'color':'red'}), row = 2, col =1,
        )

        # Add Close Price
        fig.add_trace(
        go.Scatter(x=data.index, y=data['Close'], name="Close", text = hovertext, line = {'color':'purple'}), row = 3, col =1,
        )

        # Add Signals
        hovertext_buy = ["<br>Close : " + "{:,}".format(np.round(txt['Close'],2)) + 
                    "<br>High: " + "{:,}".format(np.round(txt['High'],2)) + 
                    "<br>Low: " + "{:,}".format(np.round(txt['Low'],2)) + 
                    "<br>Volume: " + "{:,}".format(txt['Volume']) + 
                    "<br>OBV Index: " + "{:,}".format(np.round(txt['OBV Index'],2)) +
                    "<br>Signal: " + txt['Signal']
                    for txt in buy_sig.to_dict(orient = "records")]

        hovertext_sell = ["<br>Close : " + "{:,}".format(np.round(txt['Close'],2)) + 
                    "<br>High: " + "{:,}".format(np.round(txt['High'],2)) + 
                    "<br>Low: " + "{:,}".format(np.round(txt['Low'],2)) + 
                    "<br>Volume: " + "{:,}".format(txt['Volume']) + 
                    "<br>OBV Index: " + "{:,}".format(np.round(txt['OBV Index'],2)) +
                    "<br>Signal: " + txt['Signal']
                    for txt in sell_sig.to_dict(orient = "records")]

        fig.add_trace(go.Scatter(x=buy_sig.index,y=buy_sig['Close'], mode='markers', name = 'Buy Signal',text = hovertext_buy,
        marker=dict( size=8, color='green')), row = 3, col = 1)
        fig.add_trace(go.Scatter(x=sell_sig.index, y=sell_sig['Close'], mode='markers', name = 'Sell Signal', text = hovertext_sell,
        marker=dict( size=8, color='red')), row = 3, col = 1)

        fig['layout']['yaxis1'].update(title='Delta OBV/Close')
        fig['layout']['yaxis2'].update(title='OBV')
        fig['layout']['yaxis3'].update(title='Close vs Signal')

        #Add Backtest
        if 'Passive Portfolio' in data:
            fig.add_trace(
            go.Scatter(x=data.index, y=data['Passive Portfolio'], name="Backtest-Passive", text = hovertext, line = {'color':'rgb(100,100,0)'}), row = 4, col =1,
            )
        if 'Active Portfolio' in data:
            fig.add_trace(
            go.Scatter(x=data.index, y=data['Active Portfolio'], name="Backtest-Active", text = hovertext, line = {'color':'rgb(0,0,0)'}), row = 4, col =1,
            )
        if 'Passive Portfolio' in data or 'Active Portfolio' in data:
            fig['layout']['yaxis4'].update(title='%Port')

        fig.update_layout(
            title={
                'text': "OBV Analysis",
                'y':0.9,
                'x':0.4,
                'xanchor': 'center',
                'yanchor': 'top'})
        return fig
        
    def get_adx_results( self ):
        
        info = dict()
        try:
            details = self.get_adx_details().tail(1)
            info['ADX Value'] = round(details['ADX'][0],2)
        except:
            log.error("Error calculating ADX Results - {0}".format(self.name))
            info['ADX Value'] = -999
        finally:
            return info
        
    def get_adx_details( self, lookback_period = None):
        
        df = deepcopy(self.historical_prices)
        try:
            lookback_period  = lookback_period if lookback_period else self._lookback_period()
            df['High - Low'] = df['High'] - df['Low']
            df['High - PC']  = abs(df['High'] - df['Close'].shift(1))
            df['Low - PC']   = abs(df['Low']  - df['Close'].shift(1))
            df['TR']         = df.apply( lambda x: max(x['High - Low'], x['High - PC'], x['Low - PC']), axis = 1)
            df['HH']         = df['High'] - df['High'].shift(1)
            df['LL']         = df['Low'].shift(1) - df['Low']
            df['DM-']        = df.apply(lambda x: max(x['LL'], 0) if x['LL'] > x['HH'] else 0, axis = 1)
            df['DM+']        = df.apply(lambda x: max(x['HH'], 0) if x['HH'] > x['LL'] else 0, axis = 1)
            df               = df.dropna()
            df['Avg DM-']    = df[['DM-']].apply(smooth_avg, axis = 0, args = (lookback_period,))
            df['Avg DM+']    = df[['DM+']].apply(smooth_avg, axis = 0, args = (lookback_period,))
            df['Avg TR']     = df[['TR']].apply(smooth_avg, axis = 0, args = (lookback_period,))
            df['DI+']        = 100*df['Avg DM+']/df['Avg TR']
            df['DI-']        = 100*df['Avg DM-']/df['Avg TR']
            df['DI Sum']     = df['DI+'] + df['DI-']
            df['DI Diff']    = abs( df['DI+'] - df['DI-'])
            df['DX']         = 100*df['DI Diff'] / df['DI Sum']
            df               = df.dropna()
            df['ADX']        = df[['DX']].apply(smooth_avg, axis = 0, args = (lookback_period,))
            df.drop(columns = ['HH', 'LL'], inplace = True)
        except:
            log.error("Error calculating ADX Details - {0}".format(self.name))
            df['High - Low'] = -999
            df['High - PC']  = -999
            df['Low - PC']   = -999
            df['TR']         = -999
            df['DM-']        = -999
            df['DM+']        = -999
            df['Avg DM-']    = -999
            df['Avg DM+']    = -999
            df['Avg TR']     = -999
            df['DI+']        = -999
            df['DI-']        = -999
            df['DI Sum']     = -999
            df['DI Diff']    = -999
            df['DX']         = -999
            df['ADX']        = -999
        finally:
            self._add_to_technical_details(df, 'ADX', cols = ['DX', 'ADX'], col_map = {'ADX':'Value'})
            return df.dropna()
        
    def get_rsi_results(self):
        
        info = dict()
        try:
            details = self.get_rsi_details().tail(1)
            info['RSI Value']               = round(details['RSI'][0],2)
            info['RSI Signal']              = details['RSI Signal'][0]
            info['RSI Passive Portfolio']   = round(details['Passive Portfolio'][0],2)
            info['RSI Active Portfolio']    = round(details['Active Portfolio'][0],2)
        except:
            log.error("Error calculating RSI Results - {0}".format(self.name))
            info['RSI Value']               = -999
            info['RSI Signal']              = ""
            info['RSI Passive Portfolio']   = -999
            info['RSI Active Portfolio']    = -999
        finally:
            return info
        
    def get_rsi_details(self, lookback_period = None):

        df = deepcopy(self.historical_prices)
        try:
            lookback_period     = lookback_period if lookback_period else self._lookback_period()
            df['Return']        = df['Close'] - df['Close'].shift(1)
            df['Gain']          = df['Return'].apply(lambda x: abs(x) if x>0 else 0)
            df['Loss']          = df['Return'].apply(lambda x: abs(x) if x<0 else 0)
            df                  = df.dropna()
            df['Avg Gain']      = df[['Gain']].apply(smooth_avg, axis = 0, args = (lookback_period,))
            df['Avg Loss']      = df[['Loss']].apply(smooth_avg, axis = 0, args = (lookback_period,))
            df['Avg Volume']    = df[['Volume']].apply(smooth_avg, axis = 0, args = (lookback_period,))
            df['RS']            = df['Avg Gain']/df['Avg Loss']
            df['RSI']           = 100 - 100/(1 + df['RS'])
            df['RSI Signal']    = df.apply(lambda x: 'BUY' if x['RSI']<=30 else 'SELL' if x['RSI']>=70 else "", axis = 1)
            backtest            = backTestStrategy(df,'RSI Signal')[['Passive Portfolio', 'Active Portfolio']]
            df['Passive Portfolio'] = backtest['Passive Portfolio']
            df['Active Portfolio']  = backtest['Active Portfolio']
        except Exception:
            log.error("Error calculating RSI Details - {0}".format(self.name))
            df['Return']            = -999
            df['Gain']              = -999
            df['Loss']              = -999
            df['Avg Gain']          = -999
            df['Avg Loss']          = -999
            df['Avg Volume']        = -999
            df['RS']                = -999
            df['RSI']               = -999
            df['RSI Signal']        = ""
            df['Passive Portfolio'] = -999
            df['Active Portfolio']  = -999
        finally:
            self._add_to_technical_details(df, 'RSI', cols = ['RSI', 'RSI Signal', 'Passive Portfolio', 'Active Portfolio'], col_map = {'RSI':'Value','RSI Signal':'Signal'})
            return df.dropna()

    def plot_rsi_details( self, data = None, period = None ):
        '''
        data: Pandas DataFrame containing historical stock prices and RSI details. 
                Columns expected are - High, Low, Close, Volume, Avg Volume, RSI, RSI Signal
        period: trailing period for which data needs to be plotted. Defaulted to show all.
        '''
        if data is None:
            data = self.get_rsi_details()
        if period: data = data.tail(period)

        data = backTestStrategy(data,'RSI Signal')

        buy_sig = data[data['RSI Signal'] == 'BUY']
        sell_sig = data[data['RSI Signal'] == 'SELL']
        
        fig = make_subplots(rows = 4, cols = 1, shared_xaxes= True, vertical_spacing = 0.08, 
            column_widths = [15], row_heights = [2,2,2,2],
            specs=[[{"secondary_y": False}], [{"secondary_y": False}], [{"secondary_y": False}], [{"secondary_y": False}]])

        hovertext      = ["<br>Close : " + "{:,}".format(np.round(txt['Close'],2)) + 
                    "<br>High: " + "{:,}".format(np.round(txt['High'],2)) + 
                    "<br>Low: " + "{:,}".format(np.round(txt['Low'],2)) + 
                    "<br>Volume: " + "{:,}".format(txt['Volume']) + 
                    "<br>RSI: " + "{:,}".format(np.round(txt['RSI'],2)) +
                    "<br>Signal: " + txt['RSI Signal']
                    for txt in data.to_dict(orient = "records")]

        # Add Close Price
        fig.add_trace(
        go.Scatter(x=data.index, y=data['Close'], name="Close", text = hovertext, line = {'color':'purple'}), row = 1, col =1,
        )

        # Add RSI Indicators
        fig.add_trace(
                go.Scatter(x=data.index, y=data['RSI'], name="RSI", line = {'color':'darkslategray'}),row = 2, col = 1
                )
        fig.add_trace(
                go.Scatter(x=data.index, y=[30]*len(data), name="Buy Line", line = {'color':'green',
                                                                                'dash':'dash'}),row = 2, col = 1
                )
        fig.add_trace(
                go.Scatter(x=data.index, y=[70]*len(data), name="Sell Line", line = {'color':'red',
                                                                                    'dash':'dash'}),row = 2, col = 1
                )

        #Add Volume Bar
        fig.add_trace(go.Bar(x=data.index, y=data['Volume'],name = 'Volume', marker = {'color':'rgb(0,0,150)'}), row = 3, col = 1)
        fig.add_trace(
                go.Scatter(x=data.index, y=data['Avg Volume'], name="Rolling Avg Volume", line = {'color':'darkred'}),row = 3, col = 1)

        # Add Signals
        hovertext_buy = ["<br>Close : " + "{:,}".format(np.round(txt['Close'],2)) + 
                    "<br>High: " + "{:,}".format(np.round(txt['High'],2)) + 
                    "<br>Low: " + "{:,}".format(np.round(txt['Low'],2)) + 
                    "<br>Volume: " + "{:,}".format(txt['Volume']) + 
                    "<br>RSI: " + "{:,}".format(np.round(txt['RSI'],2)) +
                    "<br>Signal: " + txt['RSI Signal']
                    for txt in buy_sig.to_dict(orient = "records")]

        hovertext_sell = ["<br>Close : " + "{:,}".format(np.round(txt['Close'],2)) + 
                    "<br>High: " + "{:,}".format(np.round(txt['High'],2)) + 
                    "<br>Low: " + "{:,}".format(np.round(txt['Low'],2)) + 
                    "<br>Volume: " + "{:,}".format(txt['Volume']) + 
                    "<br>RSI: " + "{:,}".format(np.round(txt['RSI'],2)) +
                    "<br>Signal: " + txt['RSI Signal']
                    for txt in sell_sig.to_dict(orient = "records")]

        fig.add_trace(go.Scatter(x=buy_sig.index,y=buy_sig['Close'], mode='markers', name = 'Buy Signal',text = hovertext_buy,
        marker=dict( size=8, color='green')), row = 1, col = 1)
        fig.add_trace(go.Scatter(x=sell_sig.index, y=sell_sig['Close'], mode='markers', name = 'Sell Signal', text = hovertext_sell,
        marker=dict( size=8, color='red')), row = 1, col = 1)

        fig['layout']['yaxis1'].update(title='Close vs Signal')
        fig['layout']['yaxis2'].update(title='RSI')
        fig['layout']['yaxis3'].update(title='Volume')

        #Add Backtest
        if 'Passive Portfolio' in data:
            fig.add_trace(
            go.Scatter(x=data.index, y=data['Passive Portfolio'], name="Backtest-Passive", text = hovertext, line = {'color':'rgb(100,100,0)'}), row = 4, col =1,
            )
        if 'Active Portfolio' in data:
            fig.add_trace(
            go.Scatter(x=data.index, y=data['Active Portfolio'], name="Backtest-Active", text = hovertext, line = {'color':'rgb(0,0,0)'}), row = 4, col =1,
            )
        if 'Passive Portfolio' in data or 'Active Portfolio' in data:
            fig['layout']['yaxis4'].update(title='%Port')

        fig.update_layout(
            title={
                'text': "RSI Analysis",
                'y':0.9,
                'x':0.4,
                'xanchor': 'center',
                'yanchor': 'top'})
        return fig
        
    def get_williams_r_results(self):
        
        info = dict()
        try:
            info['Smoothing Period']    = self._smoothing_period()
            info['Lookback Period']     = self._lookback_period()
            try:
                info['%R'], info['%D'], info['WilliamR Signal'], info['WilliamR Passive Portfolio'], info['WilliamR Active Portfolio']  = self.get_williams_r_details()[2].tail(1)[['%R', '%D', 'WilliamR Signal', 'Passive Portfolio', 'Active Portfolio']].values[0]
            except:
                info['%R'], info['%D'], info['WilliamR Signal'], info['WilliamR Passive Portfolio'], info['WilliamR Active Portfolio']  = -999, -999, "", -999,-999
        except:
            log.error("Error calculating William's R Results - {0}".format(self.name))
        finally:
            info['%R']                          = round(info['%R'],2)
            info['%D']                          = round(info['%D'],2)
            info['WilliamR Passive Portfolio']  = round(info['WilliamR Passive Portfolio'],2)
            info['WilliamR Active Portfolio']   = round(info['WilliamR Active Portfolio'],2)
            return info
        
    def get_bollinger_results(self):
        
        info = dict()
        try:
            info['Bollinger Band Upper'], info['Bollinger Band Middle'], info['Bollinger Band Lower'] = np.round(self.get_bollinger_details().tail(1)[['Bollinger Band Upper', 'Bollinger Band Middle', 'Bollinger Band Lower']].values[0],2)
        except:
            log.error("Error calculating Bollinger Band Results - {0}".format(self.name))
            info['Bollinger Band Upper'], info['Bollinger Band Middle'], info['Bollinger Band Lower'] = -999,-999,-999
        finally:
            return info
        
    def get_bollinger_details(self):
        
        result = deepcopy(self.historical_prices)
        try:
            lookback_period                 = self._lookback_period()
            result['Bollinger Band Middle'] = self.generate_moving_averages(exponential = (lookback_period,))[['{0}D Exponential Moving Average'.format(lookback_period)]].dropna()
            result['Standard Deviation']    = self.generate_moving_std(periods = (lookback_period,))[['{0}D Moving STD'.format(lookback_period)]].dropna()
            result['Bollinger Band Upper']  = result[['Bollinger Band Middle', 'Standard Deviation']].apply(lambda row: row['Bollinger Band Middle'] + 2*row['Standard Deviation'], axis = 1)
            result['Bollinger Band Lower']  = result[['Bollinger Band Middle', 'Standard Deviation']].apply(lambda row: row['Bollinger Band Middle'] - 2*row['Standard Deviation'], axis = 1)
        except:
            log.error("Error calculating Bollinger Bands - {0}".format(self.name))
            result['Bollinger Band Middle'] = -999
            result['Standard Deviation']    = -999
            result['Bollinger Band Upper']  = -999
            result['Bollinger Band Lower']  = -999
        finally:
            self._add_to_technical_details(result, 'Bollinger Band', cols = ['Bollinger Band Lower', 'Bollinger Band Middle', 'Bollinger Band Upper'], col_map = {'Bollinger Band Lower':'Lower', 'Bollinger Band Upper':'Upper', 'Bollinger Band Middle': 'Middle'})
            return result.dropna()
            
    def generate_moving_std(self, periods = ()):
        
        result = deepcopy(self.historical_prices)
        try:
            for period in periods:
                result['{0}D Moving STD'.format(period)] = self.get_linear_moving_std(period)['{0}D Moving STD'.format(period)]
        except:
            log.error("Error calculating moving standard deviations - {0}".format(self.name))
        finally:
            return result
            
    def generate_moving_averages(self, linear = (), exponential = ()):
        
        result = deepcopy(self.historical_prices)
        try:
            for period in linear:
                result['{0}D Moving Average'.format(period)]              = self.get_linear_moving_average(period)['{0}D Moving Average'.format(period)]
            for period in exponential:
                result['{0}D Exponential Moving Average'.format(period)]  = self.get_expo_moving_average(period)['{0}D Exponential Moving Average'.format(period)]
        except:
            log.error("Error calculating moving averages - {0}".format(self.name))
        finally:
            return result
        
    def get_moving_averages(self, linear = (), exponential = ()):
        
        info = dict()
        _moving_avgs = self.generate_moving_averages(linear, exponential)
        try:
            for period in linear:
                info['{0}D Moving Average'.format(period)]              = round(np.nan_to_num(_moving_avgs['{0}D Moving Average'.format(period)][-1],nan = -1),2)
            for period in exponential:
                info['{0}D Exponential Moving Average'.format(period)]  = round(np.nan_to_num(_moving_avgs['{0}D Exponential Moving Average'.format(period)][-1],nan = -1),2)
        except:
            log.error("Error calculating moving averages - {0}".format(self.name))
            for period in linear:
                info['{0}D Moving Average'.format(period)]              = -999
            for period in exponential:
                info['{0}D Exponential Moving Average'.format(period)]  = -999
        finally:
            return info
        
    def get_williams_r_details(self):
        
        try:
            df                      = deepcopy(self.historical_prices)
            smoothing_period        = self._smoothing_period()
            lookback_period         = self._lookback_period()
            df['Highest High']      = df[['High']].rolling(window = lookback_period).max()
            df['Lowest Low']        = df[['Low']].rolling(window = lookback_period).min()
            df['%R']                = df.apply(lambda row: (row['Close'] - row['Highest High']) * 100 / (row['Highest High'] - row['Lowest Low']) if row['Highest High'] != 0 else 0, axis = 1).round(2)
            df['%D']                = df['%R'].rolling(window = smoothing_period).mean().round(2)
            df['Avg Volume']        = df[['Volume']].rolling(window = lookback_period).mean()
            df['Slope %D']          = slope(df['%D'],smoothing_period)
            df['WilliamR Signal']   = df.apply(lambda row: 'BUY' if row['%D'] < WILLIAM_K_UL and row['Slope %D'] >45 else 'SELL' if row['%D'] > WILLIAM_K_LL and row['Slope %D'] < -45 else '', axis = 1)
            backtest                = backTestStrategy(df,'WilliamR Signal')[['Passive Portfolio', 'Active Portfolio']]
            df['Passive Portfolio'] = backtest['Passive Portfolio']
            df['Active Portfolio']  = backtest['Active Portfolio']
        except:
            log.error("Error calculating William's R - {0}".format(self.name))
            df                      = deepcopy(self.historical_prices)
            df['Highest High']      = -999
            df['Lowest Low']        = -999
            df['%R']                = -999
            df['%D']                = -999
            df['Avg Volume']        = -999
            df['Slope %D']          = -999
            df['WilliamR Signal']   = ""
            df['Passive Portfolio'] = -999
            df['Active Portfolio']  = -999
            return smoothing_period, lookback_period, df
        
        self._add_to_technical_details(df, 'Williams R', cols = ['%D', '%R', 'WilliamR Signal', 'Passive Portfolio', 'Active Portfolio'], col_map = {'WilliamR Signal':'Signal'})
        return smoothing_period, lookback_period, df.dropna()

    def plot_williams_r_details( self, data = None, period = None ):
        '''
        data: Pandas DataFrame containing historical stock prices and WilliamsR results. 
                Columns expected are - High, Low, Close, Volume, Highest High, Highest Low, %R, %D, WilliamR Signal
        period: trailing period for which data needs to be plotted. Defaulted to show all.
        '''
        if data is None:
            _,_,data = self.get_williams_r_details()
        if period: data = data.tail(period)

        data = backTestStrategy(data,'WilliamR Signal')

        buy_sig = data[data['WilliamR Signal'] == 'BUY']
        sell_sig = data[data['WilliamR Signal'] == 'SELL']


        fig = make_subplots(rows = 4, cols = 1, shared_xaxes= True, vertical_spacing = 0.08, column_widths = [15], row_heights = [2,2,1,1.5])
        hovertext      = ["<br>Close : " + "{:,}".format(np.round(txt['Close'],2)) + 
                    "<br>High: " + "{:,}".format(np.round(txt['High'],2)) + 
                    "<br>Low: " + "{:,}".format(np.round(txt['Low'],2)) + 
                    "<br>Volume: " + "{:,}".format(txt['Volume']) + 
                    "<br>%R: " + "{:,}".format(np.round(txt['%R'],2)) +
                    "<br>%D: " + "{:,}".format(np.round(txt['%D'],2)) +
                    "<br>Signal: " + txt['WilliamR Signal']
                    for txt in data.to_dict(orient = "records")]
        # Add traces
        fig.add_trace(
        go.Scatter(x=data.index, y=data['Close'], name="Close", text = hovertext, line = {'color':'purple'}), row = 2, col =1,
        )
        fig.add_trace(
        go.Scatter(x=data.index, y=data['%R'], name="%R", line = {'color':'skyblue'}),row = 1, col = 1
        )
        fig.add_trace(
        go.Scatter(x=data.index, y=data['%D'], name="%D", line = {'color' : 'darkslategray'}),row = 1, col = 1
        )
        fig.add_trace(
        go.Scatter(x=data.index, y=[WILLIAM_K_LL]*len(data['%D']), name="Sell Line", line = {'color' : 'red',
                                                                                'dash' : 'dash'}),row = 1, col = 1, 
        )
        fig.add_trace(
        go.Scatter(x=data.index, y=[WILLIAM_K_UL]*len(data['%D']), name="Buy Line", line = {'color' : 'green',
                                                                                'dash' : 'dash'}),row = 1, col = 1, 
        )
        # Add Signals
        hovertext_buy = ["<br>Close : " + "{:,}".format(np.round(txt['Close'],2)) + 
                    "<br>High: " + "{:,}".format(np.round(txt['High'],2)) + 
                    "<br>Low: " + "{:,}".format(np.round(txt['Low'],2)) + 
                    "<br>Volume: " + "{:,}".format(txt['Volume']) + 
                    "<br>%R: " + "{:,}".format(np.round(txt['%R'],2)) +
                    "<br>%D: " + "{:,}".format(np.round(txt['%D'],2)) +
                    "<br>Signal: " + txt['WilliamR Signal']
                    for txt in buy_sig.to_dict(orient = "records")]

        hovertext_sell = ["<br>Close : " + "{:,}".format(np.round(txt['Close'],2)) + 
                    "<br>High: " + "{:,}".format(np.round(txt['High'],2)) + 
                    "<br>Low: " + "{:,}".format(np.round(txt['Low'],2)) + 
                    "<br>Volume: " + "{:,}".format(txt['Volume']) + 
                    "<br>%R: " + "{:,}".format(np.round(txt['%R'],2)) +
                    "<br>%D: " + "{:,}".format(np.round(txt['%D'],2)) +
                    "<br>Signal: " + txt['WilliamR Signal']
                    for txt in sell_sig.to_dict(orient = "records")]

        fig.add_trace(go.Scatter(x=buy_sig.index,y=buy_sig['Close'], mode='markers', name = 'Buy Signal',text = hovertext_buy,
        marker=dict( size=8, color='green')), row = 2, col = 1)
        fig.add_trace(go.Scatter(x=sell_sig.index, y=sell_sig['Close'], mode='markers', name = 'Sell Signal', text = hovertext_sell,
        marker=dict( size=8, color='red')), row = 2, col = 1)

        #Add Volume Bar
        fig.add_trace(go.Bar(x=data.index, y=data['Volume'],name = 'Volume', marker = {'color':'blue'}), row = 3, col = 1)

        fig['layout']['yaxis1'].update(title='%R vs %D')
        fig['layout']['yaxis2'].update(title='Close vs Signal')
        fig['layout']['yaxis3'].update(title='Volume')

        #Add Backtest
        if 'Passive Portfolio' in data:
            fig.add_trace(
            go.Scatter(x=data.index, y=data['Passive Portfolio'], name="Backtest-Passive", text = hovertext, line = {'color':'rgb(100,100,0)'}), row = 4, col =1,
            )
        if 'Active Portfolio' in data:
            fig.add_trace(
            go.Scatter(x=data.index, y=data['Active Portfolio'], name="Backtest-Active", text = hovertext, line = {'color':'rgb(0,0,0)'}), row = 4, col =1,
            )
        if 'Passive Portfolio' in data or 'Active Portfolio' in data:
            fig['layout']['yaxis4'].update(title='%Port')
            
        fig.update_layout(
            title={
                'text': "Williams 'R Analysis",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'})
        return fig
    
    def get_macd_details(self):
        
        try:
            result                                                  = self.generate_moving_averages(exponential = (12,26))
            result['MACD Line']                                     = result.apply(lambda row: row['12D Exponential Moving Average'] - row['26D Exponential Moving Average'], axis = 1)
            result['MACD Indicator']                                = result['MACD Line'].rolling(window=9).mean()
            result['MACD Line to Indicator Diff (Value)']           = result[['MACD Line','MACD Indicator']].apply(lambda row: row['MACD Line'] - row['MACD Indicator'], axis = 1)
            result['MACD Line to Indicator Diff Rolling Peak']      = result[['MACD Line to Indicator Diff (Value)']].apply(abs)
            result['MACD Line to Indicator Diff Rolling Peak']      = result['MACD Line to Indicator Diff Rolling Peak'].rolling(window=9).max()
            result['MACD Line to Indicator Diff Rolling Peak per']  = result.apply(lambda row: round(row['MACD Line to Indicator Diff (Value)']*100/row['MACD Line to Indicator Diff Rolling Peak'], 2), axis = 1)
            #result['MACD Signal']                                   = result['MACD Line to Indicator Diff Rolling Peak per'].shift(1)
            #result['MACD Signal']                                   = result[['MACD Signal', 'MACD Line to Indicator Diff Rolling Peak per']].apply(lambda row: 'BUY' if row['MACD Signal'] == -100 and row['MACD Line to Indicator Diff Rolling Peak per'] not in (100,-100) else 'SELL' if row['MACD Signal'] == 100 and row['MACD Line to Indicator Diff Rolling Peak per'] not in (100,-100) else '', axis = 1)
            result['MACD Line to Indicator Diff (Days)']            = result[['MACD Line to Indicator Diff (Value)']].apply(lambda row: 1 if row['MACD Line to Indicator Diff (Value)'] > 0 else -1 if row['MACD Line to Indicator Diff (Value)'] < 0 else 0, axis = 1)
            result['MACD Line to Indicator Diff (Days)']            = result[['MACD Line to Indicator Diff (Days)']].apply(cum_pattern)
            result['Diff Slope']                                    = slope(result['MACD Line to Indicator Diff (Value)'], 9)
            result['Diff Slope Prev']                               = result['Diff Slope'].shift(1)
            result['MACD Signal']                                   = result.apply(lambda row: 'BUY' if row['MACD Line to Indicator Diff (Value)'] < 0 and row['Diff Slope'] > 0 and row['Diff Slope Prev'] < 0 else 'SELL' if row['MACD Line to Indicator Diff (Value)'] > 0 and row['Diff Slope'] < 0 and row['Diff Slope Prev'] > 0 else '', axis = 1)
            backtest                                                = backTestStrategy(result,'MACD Signal')[['Passive Portfolio', 'Active Portfolio']]
            result['Passive Portfolio']                             = backtest['Passive Portfolio']
            result['Active Portfolio']                              = backtest['Active Portfolio']
        except:
            log.error("Error generating MacD details - {0}".format(self.name))
            result                                                  = deepcopy(self.historical_prices)
            result['MACD Line']                                     = -999
            result['MACD Indicator']                                = -999
            result['MACD Line to Indicator Diff (Value)']           = -999
            result['MACD Line to Indicator Diff Rolling Peak']      = -999
            result['MACD Line to Indicator Diff Rolling Peak per']  = -999
            result['MACD Line to Indicator Diff (Days)']            = -999
            result['Diff Slope']                                    = -999
            result['Diff Slope Prev']                               = -999
            result['MACD Signal']                                   = ""
            result['Passive Portfolio']                             = -999
            result['Active Portfolio']                              = -999
        finally:
            self._add_to_technical_details(result, 'MACD', cols = ['MACD Signal', 'MACD Line to Indicator Diff (Value)', 'Passive Portfolio', 'Active Portfolio'], col_map = {'MACD Signal':'Signal', 'MACD Line to Indicator Diff (Value)':'Diff Value'})
            result = result.dropna()
            return result
    
    def plot_macd_details( self, data = None, period = None ):
        '''
        data: Pandas DataFrame containing historical stock prices and MACD details. 
                Columns expected are - High, Low, Close, Volume, MACD Line, MACD Indicator, MACD Line to Indicator Diff (Value), MACD Signal
        period: trailing period for which data needs to be plotted. Defaulted to show all.
        '''
        if data is None:
            data = self.get_macd_details()
        if period: data = data.tail(period)

        data = backTestStrategy(data,'MACD Signal')

        buy_sig = data[data['MACD Signal'] == 'BUY']
        sell_sig = data[data['MACD Signal'] == 'SELL']
        data['Slope']  = slope(data['MACD Line to Indicator Diff (Value)'])

        fig = make_subplots(rows = 4, cols = 1, shared_xaxes= True, vertical_spacing = 0.08, 
            column_widths = [15], row_heights = [2,2,1,1.5],
            specs=[[{"secondary_y": True}], [{"secondary_y": False}], [{"secondary_y": False}], [{"secondary_y": False}]])

        hovertext      = ["<br>Close : " + "{:,}".format(np.round(txt['Close'],2)) + 
                    "<br>High: " + "{:,}".format(np.round(txt['High'],2)) + 
                    "<br>Low: " + "{:,}".format(np.round(txt['Low'],2)) + 
                    "<br>Volume: " + "{:,}".format(txt['Volume']) + 
                    "<br>MACD Line: " + "{:,}".format(np.round(txt['MACD Line'],2)) +
                    "<br>MACD Indicator: " + "{:,}".format(np.round(txt['MACD Indicator'],2)) +
                    "<br>Signal: " + txt['MACD Signal']
                    for txt in data.to_dict(orient = "records")]

        # Add MACD Indicators
        fig.add_trace(
                go.Scatter(x=data.index, y=data['MACD Line'], name="MACD Line", line = {'color':'rgb(250,170,100)'}),row = 1, col = 1
                )
        fig.add_trace(
        go.Scatter(x=data.index, y=data['MACD Indicator'], name="MACD Indicator", line = {'color' : 'darkslategray'}),row = 1, col = 1
        )
        fig.add_trace(
        go.Bar(x=data.index, y=data['MACD Line to Indicator Diff (Value)'],name = 'MACD to Signal Diff', 
            marker = {'color':(
                                    (data['MACD Line to Indicator Diff (Value)'] > 0)
                                ).astype('int'),
                                'colorscale':[[0, 'rgb(20,100,60)'], [1, 'rgb(250,0,0)']]
                            }), row = 1, col = 1
        ,secondary_y=True)

        # Add Close Price
        fig.add_trace(
        go.Scatter(x=data.index, y=data['Close'], name="Close", text = hovertext), row = 2, col =1,
        )

        #Add Volume Bar
        fig.add_trace(go.Bar(x=data.index, y=data['Volume'],name = 'Volume', marker = {'color':'blue'}), row = 3, col = 1)

        # Add Signals
        hovertext_buy = ["<br>Close : " + "{:,}".format(np.round(txt['Close'],2)) + 
                    "<br>High: " + "{:,}".format(np.round(txt['High'],2)) + 
                    "<br>Low: " + "{:,}".format(np.round(txt['Low'],2)) + 
                    "<br>Volume: " + "{:,}".format(txt['Volume']) + 
                    "<br>MACD Line: " + "{:,}".format(np.round(txt['MACD Line'],2)) +
                    "<br>MACD Indicator: " + "{:,}".format(np.round(txt['MACD Indicator'],2)) +
                    "<br>Signal: " + txt['MACD Signal']
                    for txt in buy_sig.to_dict(orient = "records")]

        hovertext_sell = ["<br>Close : " + "{:,}".format(np.round(txt['Close'],2)) + 
                    "<br>High: " + "{:,}".format(np.round(txt['High'],2)) + 
                    "<br>Low: " + "{:,}".format(np.round(txt['Low'],2)) + 
                    "<br>Volume: " + "{:,}".format(txt['Volume']) + 
                    "<br>MACD Line: " + "{:,}".format(np.round(txt['MACD Line'],2)) +
                    "<br>MACD Indicator: " + "{:,}".format(np.round(txt['MACD Indicator'],2)) +
                    "<br>Signal: " + txt['MACD Signal']
                    for txt in sell_sig.to_dict(orient = "records")]

        fig.add_trace(go.Scatter(x=buy_sig.index,y=buy_sig['Close'], mode='markers', name = 'Buy Signal',text = hovertext_buy,
        marker=dict( size=8, color='green')), row = 2, col = 1)
        fig.add_trace(go.Scatter(x=sell_sig.index, y=sell_sig['Close'], mode='markers', name = 'Sell Signal', text = hovertext_sell,
        marker=dict( size=8, color='red')), row = 2, col = 1)

        fig['layout']['yaxis1'].update(title='MACD Line')
        fig['layout']['yaxis3'].update(title='Close vs Signal')
        fig['layout']['yaxis4'].update(title='Volume')

        #Add Backtest
        if 'Passive Portfolio' in data:
            fig.add_trace(
            go.Scatter(x=data.index, y=data['Passive Portfolio'], name="Backtest-Passive", text = hovertext, line = {'color':'rgb(100,100,0)'}), row = 4, col =1,
            )
        if 'Active Portfolio' in data:
            fig.add_trace(
            go.Scatter(x=data.index, y=data['Active Portfolio'], name="Backtest-Active", text = hovertext, line = {'color':'rgb(0,0,0)'}), row = 4, col =1,
            )
        if 'Passive Portfolio' in data or 'Active Portfolio' in data:
            fig['layout']['yaxis5'].update(title='%Port')

        fig.update_layout(
            title={
                'text': "MACD Analysis",
                'y':0.9,
                'x':0.4,
                'xanchor': 'center',
                'yanchor': 'top'})

        return fig
        
    def get_macd_results(self):
        info = dict()
        try:
            info['MACD Line'], info['MACD Indicator'], info['MACD Line to Indicator Diff (Value)'], info['MACD Line to Indicator Diff (Days)'], info['MACD Line to Indicator Diff Rolling Peak'], info['MACD Line to Indicator Diff Rolling Peak per'], info['MACD Signal'], info['MACD Passive Portfolio'], info['MACD Active Portfolio'] = self.get_macd_details().tail(1)[['MACD Line', 'MACD Indicator', 'MACD Line to Indicator Diff (Value)', 'MACD Line to Indicator Diff (Days)', 'MACD Line to Indicator Diff Rolling Peak', 'MACD Line to Indicator Diff Rolling Peak per', 'MACD Signal', 'Passive Portfolio', 'Active Portfolio']].values[0]
        except:
            log.error("Error generating MacD results - {0}".format(self.name))
            info['MACD Line'], info['MACD Indicator'], info['MACD Line to Indicator Diff (Value)'], info['MACD Line to Indicator Diff (Days)'], info['MACD Line to Indicator Diff Rolling Peak'], info['MACD Line to Indicator Diff Rolling Peak per'], info['MACD Signal'], info['MACD Passive Portfolio'], info['MACD Active Portfolio'] = -1,-1,-1,-1,-1,-1,"",-1,-1
        finally:
            info['MACD Line']                                    = round(info['MACD Line'],2)
            info['MACD Indicator']                               = round(info['MACD Indicator'],2)
            info['MACD Line to Indicator Diff (Value)']          = round(info['MACD Line to Indicator Diff (Value)'],2)
            info['MACD Line to Indicator Diff Rolling Peak']     = round(info['MACD Line to Indicator Diff Rolling Peak'],2)
            info['MACD Line to Indicator Diff Rolling Peak per'] = round(info['MACD Line to Indicator Diff Rolling Peak per'],2)
            info['MACD Passive Portfolio']                       = round(info['MACD Passive Portfolio'],2)
            info['MACD Active Portfolio']                        = round(info['MACD Active Portfolio'],2)
            
            return info
    def _52w_high(self):
        
        try:
            result = -999
            last_52w_prices = self.historical_prices[self.historical_prices.index > datetime.datetime.today() - datetime.timedelta(days = 365)]
            result =  result if math.isnan(round(last_52w_prices[last_52w_prices['High'] != 0]['High'].max(), 2)) else round(last_52w_prices[last_52w_prices['High'] != 0]['High'].max(), 2)
        except:
            log.error("Error fetching 52 week high - {0}".format(self.name))
        finally:
            return result
        
    def _52w_low(self):
        
        try:
            result = -999
            last_52w_prices = self.historical_prices[self.historical_prices.index > datetime.datetime.today() - datetime.timedelta(days = 365)]
            result =  result if math.isnan(round(last_52w_prices[last_52w_prices['Low'] != 0]['Low'].min(), 2)) else round(last_52w_prices[last_52w_prices['Low'] != 0]['Low'].min(), 2)
        except:
            log.error("Error fetching 52 week low - {0}".format(self.name))
        finally:
            return result
        
    def _52w_price_per(self):
        
        try:
            result = -999
            result = np.nan_to_num(round((self._last_close() - self._52w_low())*100/(self._52w_high() - self._52w_low()),2), nan = -1)
        except:
            log.error("Error calculating 52 w price percent - {0}".format(self.name))
        finally:
            return result
        
    def _52w_price_per_range(self):
        
        try:
            result = ""
            band = math.floor(self._52w_price_per()/10)
            result = str(band*10) + '% to ' + str((band + 1) * 10) + '%' if band < 10 else '100 %'
        except:
            log.error("Error calculating 52 week price percentage range - {0}".format(self.name))
        finally:
            return result
        
    def _last_close(self):
        
        try:
            result = -999
            result = round(self.historical_prices['Close'][-1],2)
        except:
            log.error("Error fetching Last COB Date - {0}".format(self.name))
        finally:
            return result
        
    def _avg_volume(self):
        
        try:
            result = -999
            result = result if math.isnan(round(self.historical_prices['Volume'].mean(),2)) else round(self.historical_prices['Volume'].mean(),2)
        except:
            log.error("Error calculating Average Volume - {0}".format(self.name))
        finally:
            return result
        
    def _last_cob(self):
        
        try:
            result = datetime.datetime.today().strftime("%d%b%y")
            result = self.historical_prices.index[-1].strftime("%d%b%y")
        except:
            log.error("Error fetching last close of business day for which price is available - {0}".format(self.name))
        finally:
            return result
        
    def _smoothing_period(self):
        
        try:
            result = 5
        except:
            log.error("Error calculating smoothing period - {0}".format(self.name))
        finally:
            return result
        
    def _avg_daily_std_dev(self):
        
        try:
            result = 0
            if not self.historical_prices.empty:
                result = np.mean(self.historical_prices[['High', 'Low']].apply(lambda row: (row['High'] - row['Low'])**2, axis = 1))**.5
            else:
                result = -999
        except:
            log.error("Error calculating Standard Deviation - {0}".format(self.name))
        finally:
            return result
        
    def _lookback_period(self):
        
        try:
            result = 14
            result = int(round(math.log(self._avg_volume(), self._avg_daily_std_dev()),0)*2)
            result = 14 if result < 0 else result
        except:
            log.error("Error calculating look back period - {0}".format(self.name))
        finally:
            return min(result,14)
        
    def get_cagr( self ):
        ''' Cumulative Average Growth Rate'''
        
        try:
            result = -999
            df = self.calculate_return(1)
            df['Return'] = (1+df['Return']/100).cumprod()
            n = len(df)/252
            result = (df['Return'][-1]**(1/n) - 1)*100
        except:
            log.error("Error calculating CAGR - {0}".format(self.name))
        finally:
            return result
        
    def get_volatility( self, neg = False ):
        ''' Yearly volatility '''
        
        try:
            result = -999
            df     = self.calculate_return(1)
            if neg: df = df[df['Return'] < 0]
            result = df['Return'].std()*np.sqrt(252)
        except:
            log.error("Error calculating annual volatility - {0}".format(self.name))
        finally:
            return result
        
    def get_sharpe_ratio( self, rf = 3.5 ):
        
        try:
            result = (self.get_cagr() - rf)/self.get_volatility()
        except:
            log.error("Error calculating sharpe ration - {0}".format(self.name))
            result = -999
        return result
    
    def get_sortino_ratio( self, rf = 3.5 ):
        
        try:
            result = (self.get_cagr() - rf)/self.get_volatility(neg = True)
        except:
            log.error("Error calculating sharpe ration - {0}".format(self.name))
            result = -999
        return result
        
    def get_linear_moving_average(self, period):
        
        try:
            result                                          = deepcopy(self.historical_prices)
            result['{0}D Moving Average'.format(period)]    = result['Close'].rolling(window=period).mean()
        except:
            log.error("Error calculating {0}D Moving Averages - {1}".format(period, self.name))
            result['{0}D Moving Average'.format(period)]    = -999
        return result
    
    def get_expo_moving_average(self, period):
        try:
            result                                                      = deepcopy(self.historical_prices)
            result['{0}D Exponential Moving Average'.format(period)]    = result[['Close']].apply(ema, args = (period,))
        except:
            log.error("Error calculating {0}D exponential moving average - {1}".format(period, self.name))
            result['{0}D Exponential Moving Average'.format(period)] = -999
        finally:
            return result
        
    def get_linear_moving_std(self, period):
        
        try:
            result                                      = deepcopy( self.historical_prices)
            result['{0}D Moving STD'.format(period)]    = result[['Close']].rolling(window = period).std()
        except:
            log.error("Error calculating {0}D Moving STD - {1}".format(period, self.name))
            result['{0}D Moving STD'.format(period)]    = -999
        finally:
            return result
