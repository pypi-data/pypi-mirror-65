import argparse 
#from . import __version__ as VERSION
# Commands
from .commands import Command

def main():
    """Main CLI entrypoint."""
    # create a parser object 
    parser = argparse.ArgumentParser(description = "A Command Line Interface for Jira") 
    subparsers = parser.add_subparsers()

    # Create Issue Command
    parser_create = subparsers.add_parser('create')
    parser_create.add_argument('summary', type=str, metavar="Issue Summary") 
    parser_create.add_argument('-p','--project', type=str, default=None, help="Jira Project Key", metavar=None) 
    parser_create.add_argument('-d','--description', type=str, default="Do this", help="Issue Description",metavar=None) 
    parser_create.add_argument('-t','--type', type=str, default="Task", help="Issue Type",metavar=None) 
    parser_create.set_defaults(func=Command.create)
    
    # parse the arguments from standard input 
    args = parser.parse_args() 
    # Execute func for the parsed command
    # Parameter is self = instance of Command
    args.func(Command(args)) 

if __name__ == "__main__":
    main()