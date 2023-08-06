import click
import subprocess as sub
from datetime import datetime as date
import socket
from cli.utils import TableDisplay

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """
    git pull add commit push 4 step in one.
    """
    if ctx._depth == 2:
        click.echo('\nGit pull')
        sub.run('git pull',shell=True,)
        click.echo('\nCommit to Git')
        msg = click.prompt("Enter a comment",show_default=True,
            default=f"ON: {date.now().strftime('%c')}, FROM: {socket.gethostname()}")
        sub.run(f'git add . \n git commit -m "{msg}" \n git push',shell=True)
        result = sub.run('git config --get remote.origin.url',stdout=sub.PIPE,encoding='utf-8',shell=True).stdout
        td = TableDisplay()
        click.echo(td(title='>>> <g>! Success</g> <<<',text=f"Commited to [{result.strip()}]"))

README="# This Repo is created by [OK git][huik]\n[![python version](https://img.shields.\
io\/badge/python-3.5%20%7C%203.6%20%7C%203.7%20-blue)][pythonwebsite]\n[![Alt text]\
(https://img.shields.io/pypi/v/huik-module 'Hover to see this text.')][huik]\n### \
Emphasis\n*Italic* ; **Bold** ; ***Bold and Italic*** ; ~~Scratch~~\n### List items\n1. \
First ordered list item\n* Unordered list can use asterisks\n\n[huik]:https://pypi.org\
/project/huik-module\n[pythonwebsite]: https://www.python.org/downloads/release/python-375\n"

IGNORE={
"py": '*.py[cod]\n__pycache__\n*.so\n.env\n*.json\ntest*.*\ntest*\n*.bak\n*.dat\n*.dir\
\n*.egg\n*.egg-info\ndump.rdb\ndist\nbuild\neggs\nparts\nbin\nvar\nsdist\ndevelop-eggs\n\
.installed.cfg\nlib\nlib64\n.DS_Store\npip-log.txt\n.coverage\n.tox\nnosetests.xml\n*.vscode\
\n*.code-workspace\n*.mo\n.mr.developer.cfg\n.project\n.pydevproject\n.env\nvenv\nlogs\n',
"js":'/node_modules\n/.pnp\n.pnp.js\n/coverage\n/build\n.DS_Store\n.env.local\n\
.env.development.local\n.env.test.local\n.env.production.local\nnpm-debug.log*\
\nyarn-debug.log*\nyarn-error.log*\n'
}

@cli.command()
@click.option('--javascript','-js','project',flag_value='js',help='Setup javascript .gitignore')
@click.option('--python','-py','project',flag_value='py',help='Setup python .gitignore')
def init(project):
    "Init a new git package with .gitignore and README.md"
    if not project:
        project =  click.prompt("Type of project to init",
        show_default=True,type=click.Choice(["py","js"],case_sensitive=False),
        default="py")
    with open('README.md','wt') as f:
        f.write(README)
    with open('.gitignore','wt') as f:
        f.write(IGNORE[project])
    url = click.prompt("Enter github repo url")
    sub.run(f'git init\ngit add .\ngit commit -m "First Commit"\ngit remote add origin {url}\ngit push --set-upstream origin master',shell=True)
   
    
    