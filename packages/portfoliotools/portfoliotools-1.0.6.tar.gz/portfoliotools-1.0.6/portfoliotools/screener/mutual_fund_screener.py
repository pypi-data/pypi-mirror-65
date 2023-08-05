from mftool import Mftool
from portfoliotools.screener.utility.util import flatten_dicts_of_dicts, memoize
import pandas as pd
import requests

from mftool import Mftool
class MutualFundScreener( object ):
    
    def __init__( self,):
        self.mf = Mftool()
        self._get_quote_url = 'https://www.amfiindia.com/spages/NAVAll.txt'
        self._session = requests.session()
    
    @memoize
    def get_all_schemes( self,):
        schemes = []
        url = self._get_quote_url
        response = self._session.get(url)
        data = response.text.split("\n")
        for scheme_data in data:
            if ";INF" in scheme_data:
                scheme_info = {'scheme_code':"",
                            'scheme_isin1':"-",
                            'scheme_isin2': "-",
                            'scheme_name':"",
                    
                }
                scheme = scheme_data.split(";")
                scheme_info['scheme_code']  = scheme[0]
                scheme_info['scheme_isin1'] = scheme[1]
                scheme_info['scheme_isin2'] = scheme[2]
                scheme_info['scheme_name']  = scheme[3]
                schemes.append(scheme_info)

        result = pd.DataFrame(schemes)
        result.index = result.scheme_code
        result.drop( columns = ['scheme_code'], inplace = True)
        return result

    def searchSchemes(self, includes = (), excludes = (), isin_list = ()):
        '''
            Usage: MutualFundScreener.searchSchemes(includes = ('ICICI', 'GROWTH', 'DIRECT'), excludes=('Dividend',))
        '''
        schemes = self.get_all_schemes()
        
        if isin_list:
            isin_list = [isin.lower() for isin in isin_list]
            schemes = schemes[(schemes['scheme_isin1'].str.lower().str.contains('|'.join(isin_list)) == True) |
                        (schemes['scheme_isin2'].str.lower().str.contains('|'.join(isin_list)) == True)]
        
        for wrd in includes:
            schemes = schemes[(schemes['scheme_name'].str.lower().str.contains(wrd.lower()) == True)]
        for wrd in excludes:
            schemes = schemes[(schemes['scheme_name'].str.lower().str.contains(wrd.lower()) == False)]
            
        return schemes
    
    def get_scheme_details( self, codes = ()):
        '''
            Usage: MutualFundScreener.get_scheme_details(codes = (120256,120692))
        '''
        data = []
        for code in codes:
            data.append(flatten_dicts_of_dicts(self.mf.get_scheme_details(code)))
        data = pd.DataFrame(data)
        data.index = data.scheme_code
        data.index = data.index.astype(str)
        data.drop(columns = ['scheme_code'], inplace = True)
        data = data.join(self.get_all_schemes()[['scheme_isin1', 'scheme_isin2']], how = 'left' )
        return data
    
    def get_historical_nav(self, codes = ()):
        '''
            Usage: MutualFundScreener.get_historical_nav(codes = (120256,120692))
        '''
        result = pd.DataFrame()
        for code in codes:
            hist_nav = self.mf.get_scheme_historical_nav(code)['data']
            hist_nav = pd.DataFrame(hist_nav)
            hist_nav['date'] = pd.to_datetime(hist_nav['date'], format = "%d-%m-%Y")
            hist_nav = hist_nav.sort_values(by = 'date')
            hist_nav.index = hist_nav.date
            hist_nav.drop(columns = ['date'], inplace = True)
            hist_nav.columns = [code]
            hist_nav[code] = pd.to_numeric(hist_nav[code],errors='coerce')

            if result.empty:
                start_dt = hist_nav.index.min()
                end_dt = hist_nav.index.max()
                date_range = pd.date_range(start_dt, end_dt, freq='D')
                hist_nav = hist_nav.reindex(index = date_range, method='ffill')
                result = hist_nav
            else:
                start_dt = min(result.index.min(),hist_nav.index.min())
                end_dt = max(result.index.max(), hist_nav.index.max())
                date_range = pd.date_range(start_dt, end_dt, freq='D')
                result = result.reindex(index = date_range, method='ffill')
                hist_nav = hist_nav.reindex(index = date_range, method='ffill')
                result = result.join(hist_nav)
        return result