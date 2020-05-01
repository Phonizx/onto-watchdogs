import click
import os, glob
import Handle as Hl

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter


cmdHandler = Hl.Handle()

@click.group()
# @click.option("--ws", help="specifica il workspace caricato")
# @click.option("--path", ="Percorso file di un ontologia da caricare o da serializzare")
# @click.option("--eg", help="Nome dell'esempio da mostrare {toystory | metastaticcancer}")
# @click.option('--about', help="Lista nodi from")
# @click.option('--to', help="Lista nodi to")
# @click.option('--prob', '-p', is_flag=True, help="calcola le probabilita' di tutte le entita' presenti nel grafo")
# @click.command("bayes", help="Apre Shell interattiva in cui e' possibile fare inferenza nella rete bayesiana")
def main():
    pass

@main.command(help="Mostra le ontologie presenti nella cartella di lavoro") #mostra tutte le ontologie
def show():
    cmdHandler.show_ontologies()

@main.command(help="Visualizza la rete bayesiana")
@click.option("--ws")
def draw(ws):
    cmdHandler.draw_graph(ws)

@main.command(help="Apre una shell interattiva per query SPARQL")
@click.option("--ws")
def query(ws):
        suggest = ['SELECT', 'WHERE', 'FILTER', '?']
        SPARQLCompleter = WordCompleter(suggest, ignore_case=True)
        #print(SPARQLCompleter.words)
        net = cmdHandler.loadGraph(".ws/" + ws)
        entity = net.get_entity().values()
        fr = net.get_FromNode()
        for v in entity:
                SPARQLCompleter.words.append(v)
        for v in fr:
                SPARQLCompleter.words.append("/" + v.lower())
        shell = True
        while(shell):
                query = prompt('SPARQL>',
                        history=FileHistory('history/SQLhistory.txt'),
                        auto_suggest=AutoSuggestFromHistory(),
                        completer=SPARQLCompleter,
                        )
                if("exit" not in query):
                        cmdHandler.quering(ws, query)
                else:
                        shell = False

@main.command(help="Serializza un grafo in un'ontologia in formato xml")
@click.option("--ws")
@click.option("--path")
def parse(ws, path):
    cmdHandler.parseToRdf(ws, path)

@main.command(help="Visualizza una demo specificata con l'opzione --eg")
@click.option("--eg")
def demo(eg):
    if(eg is not None):
        cmdHandler.demos(eg)

def parseList(arg):
    arg = arg.replace("[", "").replace("]", "")
    args = arg.split(',')
    return args

@main.command(context_settings=dict(help_option_names=['-h', '--help']), help="Crea da un ontologia una rete bayesiana")
@click.argument("path")
@click.option('--about')
@click.option('--to')
@click.option('--prob', '-p', is_flag=True, help="Print more output.")
def load(path, about, to, prob): #parsa un'ontologia in un grafo di tipo networkx
    about = parseList(about)
    to = parseList(to)
    cmdHandler.load_ontologia(path, about, to, prob)

@main.command(help="Mostra tutti i workspace caricati")
def workspace(): #mostra tutti i workspace creati 
    cmdHandler.show_workspace()

def parserBayes(testo):
    if("ask" in testo):
        testo = testo.replace('ask', '').strip()
        testo = testo.split('|')
        cause = testo[0].upper()
        effects = [] 
        eff = testo[1].split(',')
        for seff in eff:
                effects.append(seff.strip().upper())
        return effects, cause
    else:
        return None, None

@main.command(help="Apre Shell interattiva per l'inferenza nella rete bayesiana")
@click.option("--ws")
def bayes(ws):
        EntityCompleters = WordCompleter([""], ignore_case=True)
        net = cmdHandler.loadGraph(".ws/" + ws)
        fr = net.get_FromNode()
        to = net.get_ToNode()
        for v in fr:
                EntityCompleters.words.append(v.lower())
        for v in to:
                EntityCompleters.words.append(v.lower())
        shell = True
        while(shell):
                bayes = prompt('Bayes>',
                        history=FileHistory('history/Bhistory.txt'),
                        auto_suggest=AutoSuggestFromHistory(),
                        completer=EntityCompleters
                        )
                effects, cause = parserBayes(bayes)
                if(effects is not None and cause is not None or  "exit" not in bayes):
                        cmdHandler.bayesianOp(ws, effects, cause)
                else:
                        shell = False
                        #print("Exception query")

if __name__ == "__main__":
    main()
