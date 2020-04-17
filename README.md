# README

这个项目用于构建一个简单的策略批量测试与排序系统。

## HDH ALPHA v0.1 

### 目标

借助 rqalpha 3.x 的回测平台完成下列目标：
- 进行多策略的批量回测
- 完成策略比较，并形成报告
- 将报告通过邮件形式自动发送到指定邮箱

### 设计

主要模块：
- 策略模块
- 调参模块
- 结果分析模块
- 调度模块
- 自备数据获取与存储模块

#### 策略模块 *_strategy.py

每一个策略模块对应于一个独立、完整的投资策略。编写方法参考rqalpha的策略编写要求。

策略模块位于 ```hdhalpha/strategies``` 目录下。系统逐一读取该文件夹下所有文件，进行策略回测，结果保存于```hdhalpha/results``` 目录下。

策略文件名任意，但最好言简意赅。

#### 调参模块 *_tuning.py

调参模块与1或多个策略模块对应，用于对策略模块中不能确定的参数进行穷举调优。

调优模块中包含策略运行的配置信息，其格式参照rqalpha config格式。

> TODO: 该模块可能会与rqalpha mod的功能有部分重叠，目前不明。

调参的基本思路：
- 对未定超参进行合理穷举
- 超参个数原则上不要超过3个
- 注意使用交叉验证，防止过拟合

#### 结果分析模块 analyze.py

结果分析模块用于对策略回测结果进行排序，并将排序结果详情发送到指定邮箱。

#### 调度模块 run.py

协调各模块的运行。

#### 自备数据获取与存储模块 data.py

由于rqalpha目前版本不提供宏观数据、股票基础数据等查询，所以考虑构建一个可用于综合选股的数据获取和存储模块。

数据获取目前的数据来源为 tushare：
- 基本面数据获取 ，主要来自 tushare.stock.fundamental.py

初步考虑数据存储方案有以下几个：
- 以 csv 文件形式存放 ，函数 to_csv()
- 以 postgresql 数据库形式存放，函数 to_postgresql()
- 以 bcolz 数据库形式存放，函数 to_bcolz()

## 模块与函数详情

### 基本面数据获取模块

#### 获取某股票的历史所有时期资产负债表

枚举所有股票代码，循环调用 get_balance_sheet(code) 函数，将返回数据按选定存储方案存到本地。

#### 获取某股票的历史所有时期现金流表
    get_cash_flow(code)
     
#### 获取现金流量数据
    
    get_cashflow_data(year, quarter)
            

#### 获取偿债能力数据
    
    get_debtpaying_data(year, quarter)
            
#### 获取成长能力数据
    get_growth_data(year, quarter)
            
#### 获取营运能力数据   
    
    get_operation_data(year, quarter)
            
#### 获取盈利能力数据
    
    get_profit_data(year, quarter)
            
#### 获取某股票的历史所有时期利润表
    get_profit_statement(code)
            
#### 获取业绩报表数据     
    get_report_data(year, quarter)
            
#### 获取沪深上市公司基本情况
    get_stock_basics(date=None)
            
       







