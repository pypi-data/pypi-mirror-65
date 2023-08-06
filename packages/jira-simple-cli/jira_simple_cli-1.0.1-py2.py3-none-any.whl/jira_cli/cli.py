import argparse 
from . import __version__ as VERSION
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
    parser_create.add_argument('-t','--type', type=str, default=None, help="Issue Type",metavar=None) 
    parser_create.add_argument('-a','--assignee', type=str, default=None, help="Assignee",metavar=None) 
    parser_create.add_argument('-f','--fake', action="store_true", help="Do not send request to Jira") 
    parser_create.set_defaults(func=Command.create)
    
    # Global Arguments
    parser.add_argument('-v','--version',action='version', help="jira-cli Version", version=VERSION) 
    parser.set_defaults(help=lambda x: parser.print_help())
    # parse the arguments from standard input 
    args = parser.parse_args() 
    # Execute func for the parsed command, if func attribute exists
    ## func attribute only exists when a command is sent.
    if hasattr(args,'func'):
        # Parameter is self = instance of Command
        args.func(Command(args))
    else:
        args.help(args)

if __name__ == "__main__":
    main()