from manage.manage import pass_environment
import click
from hdh_alpha import data

@click.command("updatetsdata",short_help="更新可由tushare获取的股票数据。")
@pass_environment
def cli(ctx):

    for i in range(0,5):
        try:           
            data.getStockBasicInfo(ctx.settings)  
            data.getCashFlowData(ctx.settings)
            data.getDebtPayingData(ctx.settings)
            data.getGrowthData(ctx.settings)
            data.getOperationData(ctx.settings)
            data.getProfitData(ctx.settings)
            data.getReportData(ctx.settings)
            data.getBalanceSheets(ctx.settings)
            data.getProfitStatementSheets(ctx.settings)
            data.getCashFlowSheets(ctx.settings)
            break
        except Exception as e:
            print("Some exception raised. To retry...")
            print(e)

