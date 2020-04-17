"""Double Exponential Moving Average Strategy

The double exponential moving average (DEMA), shown in Figure 1, was developed by Patrick Mulloy in an attempt to reduce the amount of lag time found in traditional moving averages. It was first introduced in the February 1994 issue of the magazine Technical Analysis of Stocks & Commodities in Mulloy's article "Smoothing Data with Faster Moving Averages."

The moving average appears as a smooth, curving line that provides a visual representation of the longer-term trend of an instrument. Faster moving averages, with shorter look-back periods, are choppier; slower moving averages, with longer look-back periods, are smoother. Because a moving average is a backward-looking indicator, it is described as lagging.
"""
import talib

def init(context):
    context.STRATEGY_NAME = 'dema_strategy'
    context.BUYINRATIO = 0.25

def handle_bar(context,bar_dict):   
    
    stocks = []
    if isinstance(context.STOCK,str):
        stocks.append(context.STOCK)
    elif isinstance(context.STOCK,list):
        stocks = context.STOCK
    SHORTPERIOD = context.TURNING_ARG01
    LONGPERIOD = context.TURNING_ARG02
    
    for s in stocks:
        prices = history_bars(s,LONGPERIOD+1,'1d','close')        
        shortEMA = talib.EMA(prices,SHORTPERIOD)
        longEMA = talib.EMA(prices,LONGPERIOD)
        curpos = context.portfolio.positions[s].quantity
    
        if shortEMA[-1] - longEMA[-1] < 0 and shortEMA[-2] - longEMA[-2] > 0 and curpos > 0 :
            #清仓
            order_target_value(s,0)
        if shortEMA[-1] - longEMA[-1] > 0 and shortEMA[-2] - longEMA[-2] < 0:
            #按比例建仓
            order_value(s,context.portfolio.cash * context.BUYINRATIO)



