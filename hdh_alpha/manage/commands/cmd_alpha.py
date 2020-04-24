r"""协调各模块，启动回测过程，目前为应用执行起点。

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

import re
import sys
import click
from manage.manage import pass_environment
from hdh_alpha.tunings import dema_tuning,macd_tuning,mybollinger_tuning
#from hdh_alpha import analyse

@click.command("alpha",short_help="启动回测过程并输出回测结果。")
@pass_environment
def cli(ctx):
    
    if input("是否清空之前的输出文件[Y/N]").upper() == "Y":
        import os 
        import shutil 
        outdir = os.path.join(ctx.settings.BASE_DIR,'results/')
        if os.path.exists(outdir):
            print("正在清空results文件夹中的文件...")             
            shutil.rmtree(outdir)  
            os.mkdir(outdir) 
    print("开始进行策略回测并参数调优...")        
    #dema_tuning.run()
    #macd_tuning.run()
    mybollinger_tuning.run(ctx.settings)
    print("策略回测运行结束，请运行analyse命令，启动按年化收益率和夏普比率对结果排序...")
    #analyse.analyse()

if __name__ == "__main__":
    run()
    
