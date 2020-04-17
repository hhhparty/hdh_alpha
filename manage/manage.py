r"""HDH_ALPHA's command-line utility for administrative tasks.。

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

import os
import sys
import click
from hdh_alpha.conf import settings
CONTEXT_SETTINGS = dict(auto_envvar_prefix='HDH_ALPHA')
        
class Environment():
    def __init__(self):
        self.verbose = False
        self.home = os.getcwd()
        # 设置全局与用户配置
        #sys.path.append(os.path.abspath(os.path.join('..', '..', '..')))
         
        self.settings = settings
        #self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # 设置环境变量
        os.environ.setdefault('HDH_ALPHA_SETTINGS_MODULE', 'hdh_alpha.settings')
       
        
        
    def log(self,msg,*args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg,file=sys.stderr)
        
    def vlog(self,msg,*args):
        """Logs a message to stderr if verbose is enabled."""
        if self.verbose:
            self.log(msg,*args)
pass_environment = click.make_pass_decorator(Environment,ensure=True)
cmd_folder = os.path.join(os.path.dirname(__file__), 'commands')
         
class AlphaCLI(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith(".py") and filename.startswith("cmd_"):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode("ascii", "replace")
            mod = __import__(
                "manage.commands.cmd_{}".format(name), None, None, ["cli"]
            )
        except ImportError:
            return None
        return mod.cli



@click.command(cls=AlphaCLI, context_settings=CONTEXT_SETTINGS)
@click.option("-v", "--verbose", is_flag=True, help="Enables verbose mode.")
@pass_environment
def cli(ctx, verbose):
    """HDH_ALPHA mangement command line interface."""
    ctx.verbose = verbose
    
    # 下面的无法执行
    
    
    
 