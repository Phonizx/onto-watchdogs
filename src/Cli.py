import click 
import os,glob
import Handle as Hl 
import json




oshandle = Hl.Handle()

@click.group()
def main():
    
    pass

@main.command() #mostra tutte le ontologie
def demo():
    oshandle.show_ontologies()

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
    oshandle.load_demo(path,about,to)


@main.command()
@click.argument("ws")
def use(ws): #utilizzo di un workspace esistente 
    oshandle.loadWorkspace(ws)

@main.command()
def workspace(): #mostra tutti i workspace creati 
    oshandle.show_workspace()
 
@main.command()
@click.option('--effects')
@click.option('--cause')
def bayes(effects,cause):
    effects = effects.split(',')
    oshandle.
if __name__ == "__main__":
    main()
