import argparse
from joetags.add import add
from joetags.search import search_interface
from joetags.browse import browse


def main():
    # top level parser
    parser = argparse.ArgumentParser(prog='Joetags')
    parser.add_argument('-v', '--version', help='displays current version', action="store_true")
    subparsers = parser.add_subparsers(help='sub-command help')

    parser_add = subparsers.add_parser('add', aliases=['a'], description='add tags to dirs')
    parser_add.add_argument('directory', nargs='?', default="", help="subdir must be in currend dir")
    parser_add.set_defaults(func=add)

    parser_search = subparsers.add_parser('search', aliases=['s'], description="search for tags and groups by applying filters")
    parser_search.add_argument('filter', nargs='?', help="use tags or groups and combine with union(|), intersection(&) and negation(!), and brackets. put filter inside ''")
    parser_search.set_defaults(func=search_interface)

    parser_browse = subparsers.add_parser('ls', aliases=['browse', 'b'], description="browse for tags and groups to find what you are looking for or explore stuff")
    parser_browse.add_argument("-g", "--groups", action="store_true", help="get all groups in selection ignored when -c flag used")
    parser_browse.add_argument("-t", "--tags", action="store_true", help="get all tags in selection, ignored when -c flag used")
    parser_browse.add_argument("-c", "--use_groupname", action="store_true", help="selection will be groupname, -t and -g tags are ignored when used")
    parser_browse.add_argument("browse_selection", type=str, nargs='?', help="folder or groupname")
    parser_browse.set_defaults(func=browse)

    args = parser.parse_args()
    if args.version:
        print_version()
        exit()

    args.func(args)

def print_version():
    # for faster startup lazy import
    import pkg_resources
    version =  pkg_resources.require("joetags")[0].version
    print(f"joetags version {version}")

if __name__ == '__main__':
    main()
