import click 
import os,glob
import Handle as Hl 
import ast

class PythonLiteralOption(click.Option):
    def type_cast_value(self, ctx, value):
        try:
            return ast.literal_eval(value)
        except:
            raise click.BadParameter(value)

oshandle = Hl.Handle()


@click.group()
def main():
    pass

@main.command()
def show():
    oshandle.show_ontologies()

    
#@main.command()
#@click.argument('onto')
#@click.option("--f",multiple=True)
#@click.option('--f', cls=PythonLiteralOption, default=[])
#@click.option('--to', cls=PythonLiteralOption, default=[])

@main.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--option', help='Whatever')
def load(option):
    print(option)
   # print(f)
    #oshandle.load_demo(onto)

if __name__ == "__main__":
    main()
