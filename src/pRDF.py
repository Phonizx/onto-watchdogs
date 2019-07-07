import click 
import os,glob
import Handle as Hl 

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter

#/usr/bin/python3 pRDF.py load toystory.xml --about ["titolo","direttore","attore","autore"] --to ["genere"]

cmdHandler = Hl.Handle()



@click.group()
def main():
    pass

@main.command() #mostra tutte le ontologie
def show():
    cmdHandler.show_ontologies()

@main.command()
@click.option("--ws")
def draw(ws):
    cmdHandler.draw_graph(ws)

@main.command()
@click.option("--ws")
def query(ws):
        suggest = ['SELECT', 'WHERE', 'FILTER', '?'] 
        SPARQLCompleter = WordCompleter(suggest,
                             ignore_case=True)
        #print(SPARQLCompleter.words)
        net = cmdHandler.loadGraph(".ws/" + ws)
        entity = net.get_entity().values() 
        fr = net.get_FromNode()
        for v in entity:
                SPARQLCompleter.words.append(v)
        for v in fr:
                SPARQLCompleter.words.append("/" + v.lower())
        query = prompt('SPARQL>', 
                history=FileHistory('history.txt'),
                auto_suggest=AutoSuggestFromHistory(),
                completer=SPARQLCompleter,
                )
        cmdHandler.quering(ws,query)

@main.command()
@click.option("--ws")
@click.option("--path")
def parse(ws,path):
    cmdHandler.parseToRdf(ws,path)


@main.command()
@click.option("--eg")
def demo(eg):
    if(eg is not None):
        cmdHandler.demos(eg)

def parseList(arg):
    arg = arg.replace("[","").replace("]","")
    args = arg.split(',')
    return args


@main.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.argument("path")
@click.option('--about')
@click.option('--to')
@click.option('--prob', '-p', is_flag=True, help="Print more output.")
def load(path,about,to,prob): #parsa un'ontologia in un grafo di tipo networkx 
    about = parseList(about)
    to = parseList(to)
    cmdHandler.load_ontologia(path,about,to,prob)

@main.command()
def workspace(): #mostra tutti i workspace creati 
    cmdHandler.show_workspace()

def parserBayes(testo): 
    if("ask" in testo):
        testo = testo.replace('ask','').strip()
        testo = testo.split('|')
        cause = testo[0].upper()
        effects = [] 
        eff = testo[1].split(',')
        for seff in eff:
                effects.append(seff.strip().upper())
        return effects,cause
    else:
        return None,None

   
@main.command()
@click.option("--ws")
def bayes(ws):
        EntityCompleters = WordCompleter([""],
                             ignore_case=True)
        net = cmdHandler.loadGraph(".ws/" + ws)
        fr = net.get_FromNode()
        to = net.get_ToNode() 
        
        for v in fr:
                EntityCompleters.words.append(v.lower())
        for v in to:
                EntityCompleters.words.append(v.lower())

        bayes = prompt('Bayes>', 
                history=FileHistory('history.txt'),
                auto_suggest=AutoSuggestFromHistory(),
                completer=EntityCompleters
                )
        effects,cause = parserBayes(bayes)
        if(effects is not None and cause is not None):
                cmdHandler.bayesanOp(ws,effects,cause)
        else:
                print("Exception query")
        
if __name__ == "__main__":
    main()
