import click 
import os,glob
import Handle as Hl 





cmdHandler = Hl.Handle()

@click.group()
def main():
    
    pass

@main.command() #mostra tutte le ontologie
def show():
    cmdHandler.show_ontologies()

@main.command()
@click.option("--eg")
def demo(eg):
    cmdHandler.demos(eg)

def parseList(arg):
    arg = arg.replace("[","").replace("]","")
    args = arg.split(',')
    return args


@main.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.argument("path")
@click.option('--about')
@click.option('--to')
def load(path,about,to): #parsa un'ontologia in un grafo di tipo networkx 
    about = parseList(about)
    to = parseList(to)
    cmdHandler.load_ontologia(path,about,to)


@main.command()
@click.argument("ws")
def use(ws): #utilizzo di un workspace esistente 
    cmdHandler.loadWorkspace(ws)

@main.command()
def workspace(): #mostra tutti i workspace creati 
    cmdHandler.show_workspace()
 
@main.command()
@click.argument("ws")
@click.option('--effects')
@click.option('--cause')
def bayes(ws,effects,cause):
    effects = effects.split(',')
    cmdHandler.bayesanOp(ws,effects,cause)
     
if __name__ == "__main__":
    main()
