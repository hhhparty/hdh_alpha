r"""Stock data retrieving and storing model. 
 
Copyright 2020 hhhparty@163.com. 
 
Licensed under the Apache License, Version 2.0 (the "License"); 
you may not use this file except in compliance with the License. 
You may obtain a copy of the License at 
 
    http://www.apache.org/licenses/LICENSE-2.0 
 
Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
See the License for the specific language governing permissions and 
limitations under the License. 
""" 
import os
import tushare as ts 
import pandas as pd 
from hdh_alpha.utils import dateutil
import datetime 
import time
import random

def getStockBasicInfo(settings,date=None):
    r"""获取沪深上市公司基本情况。
    若本地已经存有最新的基本面数据，则直接返回该数据；
    若本地没有则通过tushare爬取，并以CSV文件存储股票基本信息。
    
    """
    
    if not date:
        date = dateutil.last_tddate()
    else:
        date = datetime.datetime.strptime(date,"%Y-%m-%d")

    print("获取最新沪深上市公司基本情况...")
    csvfile = os.path.join(settings.CSVDIR, 'stockbasicinfo'+date.strftime("%Y%m%d")+'.csv')    
    if os.path.exists(csvfile):
        print("完成")
        return pd.read_csv(csvfile,dtype={'code':str})
        
    df = ts.get_stock_basics(date.strftime("%Y-%m-%d"))
    if os.path.exists(settings.CSVDIR):
        # 以CSV文件存储股票基本信息
        if not os.path.exists(csvfile):
            df.to_csv(csvfile)        
    if settings.DATABASES:
        pass
    print("完成")   
    return df

def getBalanceSheets(settings,codelist=None):
    """枚举codelist中的股票代码，循环调用 ts.get_balance_sheet(code) 函数，获取股票的历史所有时期资产负债表,将返回数据按选定存储方案存到本地。
    """
    df = pd.DataFrame()
    if not codelist:
        codelist = getStockBasicInfo(settings).code
       
    bsdir = os.path.join(settings.CSVDIR,'balancesheets/')
    if not os.path.exists(bsdir):
        os.mkdir(bsdir)
    print("获取{}只股票的历史所有时期资产负债表...".format(len(codelist)))
    for i,code in enumerate(codelist):
        print("\r{}%".format(round(i/len(codelist)*100)),end="")
        csvfile = os.path.join(bsdir, 's_'+str(code)+'banlancesheet.csv')
        
        if os.path.exists(csvfile):
            continue
        else:
            df = ts.get_balance_sheet(str(code))
            df.to_csv(csvfile)            
            time.sleep(random.randint(2,5))     
      
            if settings.DATABASES:
                pass
    print("完成")    
    return df
        
def getCashFlowSheets(settings,codelist=None):
    """枚举codelist中的股票代码，循环调用 ts.get_cash_flow(code) 函数，获取某股票的历史所有时期现金流表,将返回数据按选定存储方案存到本地。
    """
    df = pd.DataFrame()
    if not codelist:
        codelist = getStockBasicInfo(settings).code
       
    outdir = os.path.join(settings.CSVDIR,'cashflowsheets/')
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    print("获取{}只股票的历史所有时期现金流表...".format(len(codelist)))
    for i,code in enumerate(codelist):
        print("\r{}%".format(round(i/len(codelist)*100)),end="")
        csvfile = os.path.join(outdir, 's_'+str(code)+'cashflowsheet.csv')
        
        if os.path.exists(csvfile):
            continue
        else:
            df = ts.get_cash_flow(str(code))
            df.to_csv(csvfile)            
            time.sleep(random.randint(2,5))     
      
            if settings.DATABASES:
                pass
    print("完成")    
    return df        
    

def getCashFlowData(settings,year=None,quarter=1):
    """获取指定年度,季度日近5年的季报现金流量数据
    从tushare获取此类数据是按照年度+季度下载，若某股票当季发布公告则有，否则无。
    
    """
    if not year:
        year = dateutil.get_year()
    if quarter not in [1,2,3,4]:
        raise Exception("The value of parameter 'quarter' was error, it should be in [1,2,3,4].")
    
    df = pd.DataFrame()  
    outdir = os.path.join(settings.CSVDIR,'cashflowdata/')
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    print("获取近10年公开发布的季度现金流数据...")
    for t in dateutil.genYearQuarterSeries(end=datetime.date(year,quarter*3,30)):
        csvfile = os.path.join(outdir, str(t[0])+'q'+str(t[1])+'cashflow.csv')        
        if os.path.exists(csvfile):
            continue
        else:
            df = ts.get_cashflow_data(t[0], t[1])
            df.to_csv(csvfile)            
            time.sleep(random.randint(2,5))     
      
            if settings.DATABASES:
                pass
    print("完成")                
    return df 
              
def getDebtPayingData(settings,year=None,quarter=1):
    """获取指定年度,季度日近10年的偿债能力数据
    从tushare获取此类数据是按照年度+季度下载，若某股票当季发布公告则有，否则无。
    
    """
    if not year:
        year = dateutil.get_year()
    if quarter not in [1,2,3,4]:
        raise Exception("The value of parameter 'quarter' was error, it should be in [1,2,3,4].")
    
    df = pd.DataFrame()  
    outdir = os.path.join(settings.CSVDIR,'debtpayingdata/')
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    print("获取近10年公开发布的季度偿债能力数据...")
    for t in dateutil.genYearQuarterSeries(end=datetime.date(year,quarter*3,30)):
        csvfile = os.path.join(outdir, str(t[0])+'q'+str(t[1])+'debtpaying.csv')        
        if os.path.exists(csvfile):
            continue
        else:
            df = ts.get_debtpaying_data(t[0], t[1])
            df.to_csv(csvfile)            
            time.sleep(random.randint(2,5))     
      
            if settings.DATABASES:
                pass
    print("完成")    
    return df 

def getGrowthData(settings,year=None,quarter=1):
    """获取指定年度,季度日近10年的成长能力数据。    从tushare获取此类数据是按照年度+季度下载，若某股票当季发布公告则有，否则无。
    
    """
    if not year:
        year = dateutil.get_year()
    if quarter not in [1,2,3,4]:
        raise Exception("The value of parameter 'quarter' was error, it should be in [1,2,3,4].")
    
    df = pd.DataFrame()  
    outdir = os.path.join(settings.CSVDIR,'growthdata/')
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    print("获取近10年公开发布的季度成长能力数据...")
    for t in dateutil.genYearQuarterSeries(end=datetime.date(year,quarter*3,30)):
        csvfile = os.path.join(outdir, str(t[0])+'q'+str(t[1])+'growth.csv')        
        if os.path.exists(csvfile):
            continue
        else:
            df = ts.get_growth_data(t[0], t[1])
            df.to_csv(csvfile)            
            time.sleep(random.randint(2,5))     
      
            if settings.DATABASES:
                pass        
    print("完成")
    return df           

def getOperationData(settings,year=None,quarter=1):
    """获取指定年度,季度日近10年的营运能力数据。    从tushare获取此类数据是按照年度+季度下载，若某股票当季发布公告则有，否则无。
    
    """
    if not year:
        year = dateutil.get_year()
    if quarter not in [1,2,3,4]:
        raise Exception("The value of parameter 'quarter' was error, it should be in [1,2,3,4].")
    
    df = pd.DataFrame()  
    outdir = os.path.join(settings.CSVDIR,'operationdata/')
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    print("获取近10年公开发布的季度营运能力数据...")
    for t in dateutil.genYearQuarterSeries(end=datetime.date(year,quarter*3,30)):
        csvfile = os.path.join(outdir, str(t[0])+'q'+str(t[1])+'operation.csv')        
        if os.path.exists(csvfile):
            continue
        else:
            df = ts.get_operation_data(t[0], t[1])
            df.to_csv(csvfile)            
            time.sleep(random.randint(2,5))     
      
            if settings.DATABASES:
                pass        
    print("完成")
    return df    
    
def getProfitData(settings,year=None,quarter=1):
    """获取指定年度,季度日近10年的盈利能力数据。    从tushare获取此类数据是按照年度+季度下载，若某股票当季发布公告则有，否则无。
    
    """
    if not year:
        year = dateutil.get_year()
    if quarter not in [1,2,3,4]:
        raise Exception("The value of parameter 'quarter' was error, it should be in [1,2,3,4].")    
    df = pd.DataFrame()  
    outdir = os.path.join(settings.CSVDIR,'profitdata/')
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    print("获取近10年公开发布的季度盈利能力数据...")
    for t in dateutil.genYearQuarterSeries(end=datetime.date(year,quarter*3,30)):
        csvfile = os.path.join(outdir, str(t[0])+'q'+str(t[1])+'profit.csv')        
        if os.path.exists(csvfile):
            continue
        else:
            df = ts.get_profit_data(t[0], t[1])
            df.to_csv(csvfile)            
            time.sleep(random.randint(2,5))     
      
            if settings.DATABASES:
                pass        
    print("完成")
    return df    

def getProfitStatementSheets(settings,codelist=None):
    """枚举codelist中的股票代码，循环调用 ts.get_profit_statement(code) 函数，获取某股票的历史所有时期利润表,将返回数据按选定存储方案存到本地。
    """
    df = pd.DataFrame()
    if not codelist:
        codelist = getStockBasicInfo(settings).code
       
    outdir = os.path.join(settings.CSVDIR,'profitstatesheet/')
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    print("获取{}只股票的历史所有时期利润表...".format(len(codelist)))
    for i,code in enumerate(codelist):
        print("\r{}%".format(round(i/len(codelist)*100)),end="")
        csvfile = os.path.join(outdir, 's_'+str(code)+'profitsheet.csv')
        
        if os.path.exists(csvfile):
            continue
        else:
            df = ts.get_profit_statement(str(code))
            df.to_csv(csvfile)            
            time.sleep(random.randint(2,5))     
      
            if settings.DATABASES:
                pass
    print("完成")                
    return df   
    
            

def getProfitData(settings,year=None,quarter=1):
    """获取指定年度,季度日近10年的盈利能力数据。    从tushare获取此类数据是按照年度+季度下载，若某股票当季发布公告则有，否则无。
    
    """
    if not year:
        year = dateutil.get_year()
    if quarter not in [1,2,3,4]:
        raise Exception("The value of parameter 'quarter' was error, it should be in [1,2,3,4].")    
    df = pd.DataFrame()  
    outdir = os.path.join(settings.CSVDIR,'profits/')
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    print("获取近10年公开发布的盈利能力数据...")
    for t in dateutil.genYearQuarterSeries(end=datetime.date(year,quarter*3,30)):
        csvfile = os.path.join(outdir, str(t[0])+'q'+str(t[1])+'profit.csv')        
        if os.path.exists(csvfile):
            continue
        else:
            df = ts.get_profit_data(t[0], t[1])
            df.to_csv(csvfile)            
            time.sleep(random.randint(2,5))     
      
            if settings.DATABASES:
                pass        
    print("完成")
    return df 
    
def getReportData(settings,year=None,quarter=1):
    """获取指定年度,季度日近10年的业绩报表数据。    从tushare获取此类数据是按照年度+季度下载，若某股票当季发布公告则有，否则无。
    
    """
    print("获取近10年公开发布的业绩报表数据...")
    if not year:
        year = dateutil.get_year()
    if quarter not in [1,2,3,4]:
        raise Exception("The value of parameter 'quarter' was error, it should be in [1,2,3,4].")    
    df = pd.DataFrame()  
    outdir = os.path.join(settings.CSVDIR,'reports/')
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    
    for t in dateutil.genYearQuarterSeries(end=datetime.date(year,quarter*3,30)):
        csvfile = os.path.join(outdir, str(t[0])+'q'+str(t[1])+'report.csv')        
        if os.path.exists(csvfile):
            continue
        else:
            df = ts.get_report_data(t[0], t[1])
            df.to_csv(csvfile)            
            time.sleep(random.randint(2,5))     
      
            if settings.DATABASES:
                pass        
    print("完成")
    return df      