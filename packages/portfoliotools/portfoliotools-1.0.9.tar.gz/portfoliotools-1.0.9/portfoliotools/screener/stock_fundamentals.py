'''
Created on 01-Dec-2019

@author: rahuljain
'''
import requests
import pandas as pd
import logging as log
import numpy as np

from bs4 import BeautifulSoup
from portfoliotools.screener.utility.util import flatten_dicts_of_dicts


col_map = {"EBITDA": "EBITDA",
         "Depreciation & amortisation" : "D&A",
         "Market cap (intra-day)" : "MarketCap",
         "Net income available to common shareholders" : "NetIncome",
         "Net cash provided by operating activities" : "CashFlowOps",
         "Capital expenditure" : "Capex",
         "Total current assets" : "CurrAsset",
         "Total current liabilities" : "CurrLiability",
         "Net property, plant and equipment" : "PPE",
         "Total stockholders' equity" : "BookValue",
         "Long-term debt" : "LTDebt",
         "Forward annual dividend yield" : "DivYield",
         "EPS (TTM)" : "EPS",
         "1y target est" : "Yahoo 1 yr target"}

class StockFundamentals( object ):
    
    def __init__(self, stock):
        self.stock  = stock
        self.suffix = self._get_suffix()
        
    def get_details_info(self, cols = None):
        try:
            df_cols = cols
            if df_cols:
                df_cols = list(set(list(cols) + list(col_map.values())))
            result = {}
            result = self.get_balance_sheet_info(df_cols)
            result.update(self.get_financial_info(df_cols))
            result.update(self.get_cash_flow_info(df_cols))
            result.update(self.get_key_statistics(df_cols))
            result.update(self.get_summary_statistics(df_cols))
            #result = self._format_results(result, cols = df_cols)
            result.update(self.get_derived_info(result))
        except:
            log.error("Error calculating details {0}".format(self.stock))
        
        return {k:v for k,v in result.items() if k in cols} if cols else result
    
    def get_details_info_df(self, cols = None):
        df = pd.DataFrame([self.get_details_info(cols)])
        cols = df.columns.to_list()
        df['Stock'] = self.stock
        df = df[['Stock'] + cols]
        return df.transpose()
    
    def get_derived_info(self, info):
        result = {}
        try:
            try:
                result["EBIT"]         = info["EBITDA"] - info["D&A"]
            except:
                result["EBIT"]         = info.get('EBITDA', np.nan)
            try:
                result["TEV"]          = info["MarketCap"] + info["LTDebt"] - (info["CurrAsset"]-info["CurrLiability"])
            except:
                result["TEV"]          = info.get("MarketCap", np.nan)
            try:
                result["EarningYield"] = result["EBIT"]/result["TEV"]
            except:
                result["EarningYield"] = np.nan
            try:
                result["FCFYield"]     = (info["CashFlowOps"]-info["Capex"])/info["MarketCap"]
            except:
                result["FCFYield"]     = np.nan
            try:
                result["ROC"]          = (info["EBITDA"] - info["D&A"])/(info["PPE"]+info["CurrAsset"]-info["CurrLiability"])
            except:
                result["ROC"]          = np.nan
            try:
                result["BookToMkt"]    = info["BookValue"]/info["MarketCap"]
            except:
                result["BookToMkt"]    = np.nan
            try:
                pe = 1/result['EarningYield'] if result['EarningYield'] !=np.nan else info['Forward P/E'] if info['Forward P/E'] != 'N/A' else info['Trailing P/E']
                result['Intrinsic Value'] = np.round(pe*info['EPS']*(1+info['EPS Growth Rate'])**5/(1.15)**5,2)
            except:
                result['Intrinsic Value'] = np.nan
                
        except Exception as e:
            log.error(e)
            log.error("Error calculating derived info {0}".format(self.stock))
        
        return result
    
    def get_balance_sheet_info(self, cols = None):
        
        info = {}
        try:
            
            ticker = self.stock + self.suffix
            url = 'https://in.finance.yahoo.com/quote/'+ticker+'/balance-sheet?p='+ticker
            page = requests.get(url)
            page_content = page.content
            soup = BeautifulSoup(page_content,'html.parser')
            tabl = soup.find_all('div', class_='D(tbrg)')
            for t in tabl:
                rows = t.find_all("div", {"class" : "rw-expnded"})
                for row in rows:
                    key = col_map.get(row.get_text(separator='|').split("|")[0],row.get_text(separator='|').split("|")[0])
                    info[key]=row.get_text(separator='|').split("|")[1]
        except:
            log.error("Error fetching balance sheet info - {0}".format(self.stock))
        finally:
            return self._format_results(info, cols)
    
    def get_financial_info(self, cols = None):
        
        info = {}
        try:

            ticker = self.stock + self.suffix
            url = 'https://in.finance.yahoo.com/quote/'+ticker+'/financials?p='+ticker
            page = requests.get(url)
            page_content = page.content
            soup = BeautifulSoup(page_content,'html.parser')
            tabl = soup.find_all('div', class_='D(tbrg)')
            for t in tabl:
                rows = t.find_all("div", {"class" : "rw-expnded"})
                for row in rows:
                    key = col_map.get(row.get_text(separator='|').split("|")[0],row.get_text(separator='|').split("|")[0])
                    info[key]=row.get_text(separator='|').split("|")[1]
        except:
            log.error("Error fetching financial info - {0}".format(self.stock))
        finally:
            return self._format_results(info, cols)
    
    def get_cash_flow_info(self, cols = None):
        
        info = {}
        try:

            ticker = self.stock + self.suffix
            url = 'https://in.finance.yahoo.com/quote/'+ticker+'/cash-flow?p='+ticker
            page = requests.get(url)
            page_content = page.content
            soup = BeautifulSoup(page_content,'html.parser')
            tabl = soup.find_all('div', class_='D(tbrg)')
            for t in tabl:
                rows = t.find_all("div", {"class" : "rw-expnded"})
                for row in rows:
                    key = col_map.get(row.get_text(separator='|').split("|")[0],row.get_text(separator='|').split("|")[0])
                    info[key]=row.get_text(separator='|').split("|")[2]
        except:
            log.error("Error fetching cash flow info - {0}".format(self.stock))
        finally:
            return self._format_results(info, cols)
    
    def get_key_statistics(self, cols = None):
        
        info = {}
        try:

            ticker = self.stock + self.suffix
            url = 'https://in.finance.yahoo.com/quote/'+ticker+'/key-statistics?p='+ticker
            page = requests.get(url)
            page_content = page.content
            soup = BeautifulSoup(page_content,'html.parser')
            tabl = soup.findAll("table") # try soup.findAll("table") if this line gives error 
            for t in tabl:
                rows = t.find_all("tr")
                for row in rows:
                    if len(row.get_text(separator='|').split("|")[0:2])>0:
                        key = col_map.get(row.get_text(separator='|').split("|")[0],row.get_text(separator='|').split("|")[0])
                        info[key]=row.get_text(separator='|').split("|")[-1]
        except:
            log.error("Error fetching key statistics info - {0}".format(self.stock))
        finally:
            return self._format_results(info, cols)
        
    def get_summary_statistics( self, cols = None):
        
        info = {}
        try:

            ticker = self.stock + self.suffix
            url = 'https://in.finance.yahoo.com/quote/'+ticker+'?p='+ticker
            page = requests.get(url)
            page_content = page.content
            soup = BeautifulSoup(page_content,'html.parser')
            tabl = soup.findAll("table") # try soup.findAll("table") if this line gives error 
            for t in tabl:
                rows = t.find_all("tr")
                for row in rows:
                    if len(row.get_text(separator='|').split("|")[0:2])>0:
                        key = col_map.get(row.get_text(separator='|').split("|")[0],row.get_text(separator='|').split("|")[0])
                        info[key]=row.get_text(separator='|').split("|")[-1]
                        
            temp_info = {}
            url = 'https://in.finance.yahoo.com/quote/'+ticker+'/analysis?p='+ticker
            page = requests.get(url)
            page_content = page.content
            soup = BeautifulSoup(page_content,'html.parser')
            tabl = soup.findAll("table")
            t = tabl[-1]
            rows = t.find_all("tr")
            for row in rows:
                if len(row.get_text(separator='|').split("|")[0:2])>0:
                    key = col_map.get(row.get_text(separator='|').split("|")[0],row.get_text(separator='|').split("|")[0])
                    val = row.get_text(separator='|').split("|")[1]
                    if val != 'N/A': temp_info[key]=val
            info['EPS Growth Rate'] = temp_info.get('Next 5 years (per annum)', temp_info.get('Next year', temp_info.get('Current year', '')))
            
        except:
            log.error("Error fetching Summary statistics info - {0}".format(self.stock))
        finally:
            return self._format_results(info, cols)
    
    def _get_suffix(self):
        
        try:
            for ext in [".NS", ".BSE", ""]:
                stock = self.stock + ext
                url = 'https://in.finance.yahoo.com/quote/'+stock+'/balance-sheet?p='+stock
                page = requests.get(url)
                page_content = page.content
                soup = BeautifulSoup(page_content,'html.parser')
                tabl = soup.find_all('div', class_='D(tbrg)')
                if len(tabl):
                    break
            return ext
        except:
            log.error("Error calculating suffix {0}".format(self.stock))
            return ""
    
    def _format_results( self, dictObj, drop_nan = True, cols = None ):
        df = pd.DataFrame()
        try:
            df = pd.DataFrame([dictObj])
            if cols:
                cols = [c for c in df.columns.to_list() if c in cols]
                df = df[cols]
            df = df.replace({','  : ''}, regex=True)
            df = df.replace({'-'  : '0'}, regex=True)
            df = df.replace({'N/A': '0'}, regex=True)
            df = df.replace({'M'  : 'E+03'}, regex=True)
            df = df.replace({'B'  : 'E+06'}, regex=True)
            df = df.replace({'T'  : 'E+09'}, regex=True)
            df = df.replace({'%'  : 'E-02'}, regex=True)
            
            df.iloc[0,:] = pd.to_numeric(df.iloc[0,:].values,errors='coerce')
            if drop_nan: df.dropna(axis = 1, inplace = True)
            #df = df.rename(columns = col_map)
            #cols = df.columns.to_list()
            #df['Stock'] = self.stock
            #df = df[['Stock'] + cols]
        except:
            log.error("Error formatting results {0}".format(self.stock))
        return flatten_dicts_of_dicts(df.transpose().to_dict())