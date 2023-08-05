import argparse
main_parser = argparse.ArgumentParser(prog='chimera',
                                      description='Command line interface for chimera',
                                      usage='Use one of the subcommands'
                                      )

subparsers = main_parser.add_subparsers(
    title='command',
    description='Command to send to chimera',
    dest='command',
    required=False
)

parent_parser = argparse.ArgumentParser(
    add_help=False
)
parent_parser.add_argument(
    '--namespace', '-n',
    required=False,
    type=str,
    help='''Namespace specification for chimera cluster'''
)

subcommands = parent_parser.add_subparsers(
    title='subcommand',
    description='Subcommand to use',
    dest='subcommand',
    required=False)

parent_subparser = argparse.ArgumentParser(
    add_help=False
)

parent_subparser.add_argument('--name', required=False, default=None)

subcommands.add_parser('pipeline', parents=[parent_subparser])
subcommands.add_parser('channel', parents=[parent_subparser])

DeployParser = subparsers.add_parser('deploy',
                                     prog='deploy',
                                     parents=[parent_parser],
                                     )


DeleteParser = subparsers.add_parser('delete',
                                     parents=[parent_parser],
                                     prog='delete'
                                     )

GetParser = subparsers.add_parser('get', parents=[parent_parser], prog='get')

if __name__ == "__main__":
    print(main_parser.parse_args())
