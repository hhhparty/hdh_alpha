from rqalpha import run_file
import os

STOCKLIST = ["510500.XSHG","159902.XSHE","510710.XSHG"] 
STRATEGY_NAME = 'macd_strategy'
BASE_DIR = ""
tasks = []

for stock in STOCKLIST:
    
    for TURNING_ARG01 in range(1, 101, 2):
        for TURNING_ARG02 in range(1, 101, 2):
            if TURNING_ARG01 > TURNING_ARG02:
                continue
                
            outfname = "results/out-{}-{}-{}-{}.pkl".format(STRATEGY_NAME,stock,TURNING_ARG01,TURNING_ARG02)
            outfpath = os.path.join(BASE_DIR,outfname)
            
            config = {
                "extra": {
                    "context_vars": {
                        "TURNING_ARG01": TURNING_ARG01,
                        "TURNING_ARG02": TURNING_ARG02,
                        "STRATEGY_NAME": STRATEGY_NAME,
                        "STOCK": stock,
                    },
                    "log_level": "info",
                },
                "base": {
                    "matching_type": "current_bar",
                    "start_date": "2017-01-01",
                    "end_date": "2020-03-13",
                    "frequency": "1d",                
                    "accounts": {
                        "stock": 200000
                    },
                    "benchmark": "000300.XSHG",
                    "data_bundle_path": os.path.join(BASE_DIR,'bundle/'),
                },
                "mod": {
                    "sys_progress": {
                        "enabled": True,
                        "show": True,
                    },
                    "sys_analyser": {
                        "enabled": True,
                        "output_file": outfpath
                    },
                    "sys_transaction_cost": {
                        "enabled": True,
                        "cn_stock_min_commission": 5,
                        "commission_multiplier": 1.5,
                    },
                    "sys_simulation": {
                            "enabled": True,
                            "slippage": 0.01
                    },
                },
            }

            tasks.append(config)


def run_bt(config):
    f = os.path.join(BASE_DIR,"hdh_alpha","strategies",STRATEGY_NAME+'.py')
    run_file(f,config)


def run():
    #with concurrent.futures.ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
    BASE_DIR = settings.BASE_DIR
    for task in tasks:
        #executor.submit(run_bt, task)
        run_bt(task)
        