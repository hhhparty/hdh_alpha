import glob
import pandas as pd
import os
from manage.manage import pass_environment
import click

def export(results,exportdir = None):
    """对各个产品按夏普比率和年收益率降序排序，输出前10"""
    if not results:
        print("没有可分析的策略回测输出结果，请检查results文件夹。")
        return False
    results_df = pd.DataFrame(results)
    for bookid in results_df['order_book_id'].value_counts().index:
        """对各个产品按夏普比率和年收益率降序排序，输出前10"""
        #Sort by sharpe
        top10_results_bysharpe = results_df[results_df['order_book_id'] == bookid].sort_values(by=["sharpe"], ascending=False)[:10]
        
        #Sort by annualized_returns
        top10_results_byannualret = results_df[results_df['order_book_id'] == bookid].sort_values(by=["annualized_returns"], ascending=False)[:10]

        print("-" * 50)
        print("Sort by sharpe")
        print(top10_results_bysharpe.iloc[:,[0,2,3,4,5,6,7]])
        
        print("-" * 50)
        print("Sort by annualized_returns")
        print(top10_results_byannualret.iloc[:,[0,2,3,4,5,6,7]])
        
        if exportdir:
            filename = 'report-' + results_df['strategy_file'][0] +'-'+ bookid +'.csv'
            exportfile = os.path.join(exportdir,filename)
            
            top10_results_bysharpe.to_csv(exportfile, mode='a')
            top10_results_byannualret.to_csv(exportfile, mode='a')
            print("Export analysis report to {}".format(exportfile))
    return True

@click.command("analyse",short_help="对各个产品按夏普比率和年收益率降序排序，输出前10")
@pass_environment
def cli(ctx):
    results = []
    resultfiles = os.path.join(ctx.settings.BASE_DIR,'results/*.pkl')
    for name in glob.glob(resultfiles):
        result = pd.read_pickle(name)
        summary = result["summary"]
        if not result["trades"].empty:
            results.append({
                "name": name[8:-4],
                "order_book_id": result["trades"]["order_book_id"][0],
                "start_date": summary["start_date"],
                "end_date": summary["end_date"],
                "strategy_file":os.path.basename(summary['strategy_file']).split('.')[0],
                "annualized_returns": summary["annualized_returns"],
                "sharpe": summary["sharpe"],
                "max_drawdown": summary["max_drawdown"],
                "trade_times": result["trades"].shape[0],
            })
            
    export(results,exportdir=os.path.join(ctx.settings.BASE_DIR,'reports/'))
    
