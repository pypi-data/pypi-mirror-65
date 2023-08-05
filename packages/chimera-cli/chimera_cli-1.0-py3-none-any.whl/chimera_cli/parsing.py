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
    dest='subcommand')

parent_subparser = argparse.ArgumentParser(
    add_help=False
)

parent_subparser.add_argument('--name', required=False, default=None)

subcommands.add_parser('pipeline', parents=[parent_subparser], help='Specifies for the cli to use the subcommand on pipelines.')
subcommands.add_parser('channel', parents=[parent_subparser], help='Specifies for the cli to use the subcommand on channels')

DeployParser = subparsers.add_parser('deploy',
                                     prog='deploy',
                                     parents=[parent_parser],
                                     description='''Deploys elements to chimera.
                                     ''',
                                     help='''Deploys elements to chimera.
                                     Usage: chimera deploy - deploys everything
                                            chimera deploy {argument}: deploys the argument''' )


DeleteParser = subparsers.add_parser('delete',
                                     parents=[parent_parser],
                                     prog='delete',
                                     help='''Delete elements to chimera.
                                     Usage: chimera delete - deletes everything
                                            chimera delete {argument}: deletes the argument''')

GetParser = subparsers.add_parser('get', parents=[parent_parser], prog='get')
GetParser = subparsers.add_parser('watch', prog='watch')

InitParser = subparsers.add_parser('init')
if __name__ == "__main__":
    print(main_parser.parse_args())
