"""
This is a template algorithm on Quantopian for you to adapt and fill in.
"""
import quantopian.algorithm as algo
from quantopian.pipeline import Pipeline
from quantopian.pipeline.filters import Q500US, Q1500US, QTradableStocksUS, StaticAssets
from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.factors import RSI, ExponentialWeightedMovingAverage
import talib
def initialize(context):
    context.aapl = sid(24)
    set_benchmark(sid(24))
    # algo.attach_pipeline(
    #     make_pipeline(),
    #     'data_pipe'
    # )   

    # schedule_function(ma_crossover_handling,date_rules.every_day(),time_rules.market_open(minutes=1))
    schedule_function(market_close_handling,date_rules.every_day(),time_rules.market_close(hours=0.5))   
    
# def make_pipeline():
#     """
#     Pipeline definition
#     """
   
#     # Return Pipeline containing sentiment_score that has our trading universe as a screen
#     base_universe  = StaticAssets([sid(24)])
#     #hist = data.history(context.aapl,'price',390,'1d')
#     # period = 14
#     # rsi = talib.RSI(hist, timeperiod=period)
#     # rsi = RSI(inputs=[USEquityPricing.close],
#     #     window_length=14,
#     #     mask=base_universe)
#     # ema_rsi_10 = ExponentialWeightedMovingAverage(  
#     #                         inputs=[],  
#     #                         window_length=30,  
#     #                         decay_rate=(1 - (2.0 / (1 + 15.0))),    
#     #                           )
#     ema_rsi_10 = talib.EMA(rsi, timeperiod=10)
#     return Pipeline(
#         columns={
#             'rsi': rsi[sid(24)],
#             'ema_rsi_10': ema_rsi_10
#         },
#         screen=base_universe & sentiment_score.notnull(),
#         domain=US_EQUITIES,
#     )    
# def ma_crossover_handling(context,data):
#     context.hist = data.history(context.aapl,'price',390,'1d')
#     context.sma_50 = hist.mean()
#     context.sma_20 = hist[-20:].mean()
#     context.period = 14
#     context.rsi = talib.RSI(hist, timeperiod=context.period)
#     #record(RSI=rsi[-1])
#     #log.info(rsi)
#     #log.info(hist)
#     #log.info(len(rsi))
#     context.ema_50 = talib.EMA(context.hist, timeperiod=50)
#     context.ema_20 = talib.EMA(context.hist, timeperiod=20)
#     context.ema_rsi_20 = talib.EMA(context.rsi, timeperiod=20)
#     context.ema_rsi_10 = talib.EMA(context.rsi, timeperiod=10)
#     context.RSI=context.rsi[-1]
#     context.count=0
#     log.info(context.ema_rsi_10)
#     pass


  
# def is_long_position_opened(context,data):
    
#     for Position in context.portfolio.positions[context.aapl]:
#         if Position.amount==0:
#             position_opened_1='no_pos'
#         if Position.amount > 0:  
#             postion_opened_1='long'   
#         if Position.amount < 0:  
#             position_opened_1='short'
    
#     return position_opened_1
 

   
def market_close_handling(context,data):
    order_target_percent(context.aapl, 0)
    # hist = data.history(context.aapl,'price',390,'1d')
    # rsi = talib.RSI(hist, timeperiod=14)
    # log.info(rsi)

def handle_data(context, data):
    """
    Called every minute.
    """
    # hist = data.history(context.aapl,'price',390,'1d')
    
    # sma_50 = hist.mean()
    # sma_20 = hist[-20:].mean()
    # period = 14
    # rsi = talib.RSI(hist, timeperiod=period)
    # #record(RSI=rsi[-1])
    # #log.info(rsi)
    # #log.info(hist)
    # #log.info(len(rsi))
    # ema_50 = talib.EMA(hist, timeperiod=50)
    # ema_20 = talib.EMA(hist, timeperiod=20)
    # ema_rsi_20 = talib.EMA(rsi, timeperiod=20)
    # ema_rsi_10 = talib.EMA(rsi, timeperiod=10)
   
    # EMA_RSI_20 = ema_rsi_20[-1]
    # EMA_50 = ema_50[-1]
    # EMA_20 = ema_20[-1]
    pipeline_data = algo.pipeline_output('data_pipe')
    EMA_RSI_10 = pipeline_data.ema_rsi_10[-1]
    RSI=pipeline_data.rsi[-1]
    context.count+=1
    #log.info(RSI)    
    open_orders = get_open_orders() 
    
    # long_position_opened = is_long_position_opened(context,data)
    if RSI>EMA_RSI_10 and EMA_RSI_10>40 and EMA_RSI_10<60:
         if context.portfolio.portfolio_value == context.portfolio.cash:
             if context.aapl not in open_orders:
                 order_target_percent(context.aapl, 1.0)
         elif context.portfolio.portfolio_value<context.portfolio.cash:
             if context.aapl not in open_orders:
                 order_target_percent(context.aapl, 0)
    
    
    if RSI<EMA_RSI_10 and EMA_RSI_10>40 and EMA_RSI_10<60:
         if context.portfolio.portfolio_value==context.portfolio.cash:
            if context.aapl not in open_orders:
                order_target_percent(context.aapl, -1.0)
         elif context.portfolio.portfolio_value>context.portfolio.cash:
             if context.aapl not in open_orders:
                 order_target_percent(context.aapl, 0)    
    #record(portfolio_value=context.portfolio.portfolio_value)
    #record(portfolio_cash = context.portfolio.cash)
    
    #log.info(context.portfolio.positions[context.aapl])
    #log.info(len(context.portfolio.positions))
    #log.info(len(context.portfolio.positions))
    
    pass