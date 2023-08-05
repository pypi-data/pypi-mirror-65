import talib

from copy import deepcopy
from portfoliotools.screener.utility.util import slope

class CandleStickPatters( object ):
    
    def __init__( self, df, mark = True):
        ''' 
        [Inputs] - df: Dataframe containing Stock Close, Open, High and Low values
                    mark: Set True to replace integer patters to Bull and Bear
        '''
        self.df         = deepcopy(df)
        self.df.columns = [col.lower() for col in self.df.columns]
        self.cols       = list(self.df.columns) + ['Slope']
        self.mark       = mark
        
    def get_patterns( self, df = None, details = True):
        ''' Method to get all patterns '''
        
        if df is None: df = deepcopy(self.df)
        df = deepcopy(df)
        df = self._three_black_crow(df)    # Three Black Crow
        df = self._doji_gravestone(df)     # Gravestone Doji
        df = self._doji_dragonfly(df)      # Dragon Fly Doji
        df = self._rickshaw_doji(df)       # Rickshaw Doji
        df = self._doji(df)                # Doji
        return df if details else self._get_latest_patterns(df)
    
    def get_bullish_patters( self, df = None, details = True):
        ''' Method to get all candle stick bullish patters '''
        
        if df is None: df = deepcopy(self.df)
        df = deepcopy(df)
        df = self._doji_dragonfly(df)      # Dragon Fly Doji
        
        return df if details else self._get_latest_patterns(df)
    
    def get_bearish_patters( self, df = None, details = True):
        ''' Method to get all candlestick bearish patters '''
        
        if df is None: df = deepcopy(self.df)
        df = deepcopy(df)
        df = self._three_black_crow(df)    # Three Black Crow
        df = self._doji_gravestone(df)     # Gravestone Doji
        return df if details else self._get_latest_patterns(df)
    
    def _get_latest_patterns( self, df = None):
        
        result = dict()
        last = df.tail(1)
        for col in set(last.columns) - set(self.cols):
            try:
                result[col] = last[col].values[0]
            except:
                result[col] = ''
        
        return result
    
    def _three_black_crow( self, df):
        ''' 
            Three Black Crow - Bearish Pattern 
            Output : 0 - No Pattern
                     1 - Pattern
        '''
        try:
            df['Three Black Crow'] = talib.CDL3BLACKCROWS(df['open'], df['high'], df['low'], df['close'])
            if self.mark:
                df['Three Black Crow'] = df[['Three Black Crow']].apply(lambda x: 'BEAR' if x['Three Black Crow'] == 1 else '', axis = 1)
        except:
            df['Three Black Crow'] = '' if self.mark else 0
        return df.dropna()
    
    def _doji( self, df):
        ''' 
            Doji - Doji Pattern 
            Output : 0   - No Pattern
                     100 - Pattern
        '''
        try:
            df['Doji'] = talib.CDLDOJI(df['open'], df['high'], df['low'], df['close'])
            df                    = self._slope(df)
            if self.mark:
                df['Doji'] = df[['Doji', 'Slope']].apply(lambda x: 'BULL' if x['Doji'] == 100 and x['Slope'] < 0 else 'BEAR' if x['Doji'] == 100 else '', axis = 1)
        except:
            df['Doji'] = '' if self.mark else 0
        return df.dropna()
    
    def _rickshaw_doji( self, df):
        ''' 
            Rickshaw Doji - Rickshaw Doji Pattern 
            Output : 0   - No Pattern
                     100 - Pattern
        '''
        try:
            df['Rickshaw Doji'] = talib.CDLDOJI(df['open'], df['high'], df['low'], df['close'])
            df                    = self._slope(df)
            if self.mark:
                df['Rickshaw Doji'] = df[['Rickshaw Doji', 'Slope']].apply(lambda x: 'BULL' if x['Rickshaw Doji'] == 100 and x['Slope'] < 0 else 'BEAR' if x['Rickshaw Doji'] == 100 else '', axis = 1)
        except:
            df['Rickshaw Doji'] = '' if self.mark else 0
        return df.dropna()
    
    def _doji_dragonfly( self, df):
        ''' 
            Dragon Fly Doji - Bullish Pattern 
            Output : 0   - No Pattern
                     100 - Pattern
        '''
        try:
            df['Dragon Fly Doji'] = talib.CDLDRAGONFLYDOJI(df['open'], df['high'], df['low'], df['close'])
            df                    = self._slope(df)
            if self.mark:
                df['Dragon Fly Doji'] = df[['Dragon Fly Doji', 'Slope']].apply(lambda x: 'BULL' if x['Dragon Fly Doji'] == 100 and x['Slope'] < 0 else 'UNCERTAIN' if x['Dragon Fly Doji'] == 100 else '', axis = 1)
        except:
            df['Dragon Fly Doji'] = '' if self.mark else 0
        return df.dropna()
    
    def _doji_gravestone( self, df):
        ''' 
            Gravestone Doji - Bearish Pattern 
            Output : 0   - No Pattern
                     100 - Pattern
        '''
        try:
            df['Gravestone Doji'] = talib.CDLGRAVESTONEDOJI(df['open'], df['high'], df['low'], df['close'])
            df                    = self._slope(df)
            if self.mark:
                df['Gravestone Doji'] = df[['Gravestone Doji', 'Slope']].apply(lambda x: 'BEAR' if x['Gravestone Doji'] == 100 and x['Slope'] > 0 else 'UNCERTAIN' if x['Gravestone Doji'] == 100 else '', axis = 1)
        except:
            df['Gravestone Doji'] = '' if self.mark else 0
        return df.dropna()
    
    def _slope(self, df):
        '''
            Method to calculate slope of close prices using last 5 sessions
            
        '''
        
        try:
            if 'Slope' in df.columns: return df
            df['Slope'] = slope(df['close'])
        except:
            df['Slope'] = 0
        return df.dropna()
    
    