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

import tushare as ts
import pandas as pd
import datetime


def saveStockBasicInfo(settings):
    r"""查询当前所有正常上市交易的股票列表，默认为参数date=now"""
    stockBasicInfo = ts.get_stock_basics()    
    
    if settings.CSVDIR:
        # 以CSV文件存储股票基本信息
        today = datetime.datetime.today().date().strftime("%Y%m%d")
        csvfile = os.path.join(settings.CSVDIR, 'stockbasicinfo'+today+'.csv')       
        if not os.path.exists(csvfile):
            stockBasicInfo.to_csv(csvfile)
        return csvfile
    if settings.DATABASES:
        pass
        

if __name__ == "__main__":
    saveStockBasicInfo()