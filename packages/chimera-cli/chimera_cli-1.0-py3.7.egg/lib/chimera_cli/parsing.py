import argparse
main_parser = argparse.ArgumentParser(
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
    '--namespace',
    required=False,
    type=str,
    help='''Namespace specification for chimera cluster'''

)

parent_parser.add_argument(
    '--name',
    required=False,
    type=str,
    help='''Name for the deployment that will be sent'''
)



subcommands = parent_parser.add_subparsers(
    title='subcommand',
    description='Subcommand to use',
    dest='subcommand',
    required=False)


subcommands.add_parser('pipeline')
subcommands.add_parser('channel')

DeployParser = subparsers.add_parser('deploy',
                                     parents=[parent_parser],
                                     )


DeleteParser = subparsers.add_parser('delete',
                                     parents=[parent_parser]
                                     )


if __name__ == "__main__":
    print(main_parser.parse_args())
