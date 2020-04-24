"""My Customized bollinger Buyin Strategy"""
import talib

def init(context):
    context.strategyName = 'mybollinger_strategy'   
    context.PERIOD = 20
    context.FACTOR = 2
   
    #context.BUYRATIO = 0.2
    #context.SELLRATIO = 0.25

def handle_bar(context,bar_dict):
    stocks = []
    if isinstance(context.STOCK,str):
        stocks.append(context.STOCK)
    elif isinstance(context.STOCK,list):
        stocks = context.STOCK
    
    BUYRATIO = context.TURNING_ARG01 / 100
    SELLRATIO = context.TURNING_ARG02 / 100
    
    for s in stocks:
        prices = history_bars(s,context.PERIOD + 1,'1d','close')
        # EMA(20)均线
        mediumline = talib.EMA(prices, context.PERIOD)   
        # EMA(20)均值标准差
        stddev = talib.STDDEV(prices,context.PERIOD)
        # Bollingar upper line
        upperLine = mediumline + context.FACTOR * stddev 
        # Bollingar low line
        lowerLine = mediumline - context.FACTOR * stddev 
        # Current Position
        curpos = context.portfolio.positions[s].quantity
        
        # 当收益率高于0.1时，卖出该股票适当份额。
        if curpos > 0:
            cumReturnRatio = ( prices[-1]  - context.portfolio.positions[s].avg_price)/context.portfolio.positions[s].avg_price
            if cumReturnRatio >= 0.1:                         
                shares = curpos * SELLRATIO              
                order_shares(s,-shares)
            
        # 当收盘价小于下轨值时，买入股票适当份额
        if prices[-1] < lowerLine[-1]:           
            order_value(s,  context.portfolio.cash * BUYRATIO)  
