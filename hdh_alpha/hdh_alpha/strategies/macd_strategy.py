"""A Simple Moving Average Convergence / Divergence Strategy"""
import talib

def init(context):
    context.strategyName = 'dema_strategy'
    #context.stocks = ["510500.XSHG", "159902.XSHE","510710.XSHG"]
    context.SHORTPERIOD = 12
    context.LONGPERIOD = 26
    context.SMOOTHPERIOD = 9
    context.OBSERVATION = 100
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
        prices = history_bars(s,context.OBSERVATION,'1d','close')
        macd,signal,hist = talib.MACD(prices,context.SHORTPERIOD,context.LONGPERIOD,context.SMOOTHPERIOD)
        curpos = context.portfolio.positions[s].quantity
        
        if macd[-1] - signal[-1] < 0 and macd[-2] - signal[-2] > 0 and curpos > 0:
            #下穿时，卖出
            #order_target_value(s,0)
            shares = curpos * SELLRATIO
            order_shares(s,-shares)
        if macd[-1] - signal[-1] > 0 and macd[-2] - signal[-2] < 0:
            #上穿时，买进
            order_value(s,context.portfolio.cash * BUYRATIO)
