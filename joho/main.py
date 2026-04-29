import argparse
from joho.core.cli.fetch_cli import FetchCLI
from joho.core.cli.export_cli import ExportCLI
from joho.core.fetchers.fetcher_factory import create_fetcher
from joho.core.normalizers.normalizer_factory import create_normalizer
from joho.core.utils import valid_filepath, create_defaulf_filepath
from joho.core.file_handler import DataIO
from joho.core.constants import VALID_DATA_SOURCES


def main_parser() -> None:
    VALID_SOURCES = {"anilist", "jikan", "all"}
    parser = argparse.ArgumentParser(prog="joho")
    subparsers = parser.add_subparsers(dest="command")

    # subcommand fetch
    fetch_parser = subparsers.add_parser("fetch", description="fetch anime data")
    fetch_parser.add_argument("--source", choices=VALID_SOURCES, required=True)
    fetch_parser.add_argument("--max-entry", type=int, default=None)
    fetch_entry_group = fetch_parser.add_mutually_exclusive_group(required=False)
    fetch_entry_group.add_argument("--entry", type=int, default=None)
    fetch_entry_group.add_argument("--show-title", action="store_true", default=False)
    search_by_group = fetch_parser.add_mutually_exclusive_group(required=True)
    search_by_group.add_argument("--title", type=str)
    search_by_group.add_argument("--id", type=int)

    # subcommand export
    export_parser = subparsers.add_parser(
        "export", description="fetch then save anime data"
    )
    export_parser.add_argument("--source", choices=VALID_SOURCES, required=True)
    search_by_group = export_parser.add_mutually_exclusive_group(required=True)
    search_by_group.add_argument("--title", type=str)
    search_by_group.add_argument("--id", type=int)
    export_entry_group = export_parser.add_mutually_exclusive_group(required=False)
    export_entry_group.add_argument("--entry", type=int, default=None)
    export_entry_group.add_argument("--save-all", action="store_true", default=False)
    export_parser.add_argument(
        "--path", type=valid_filepath, default=None, required=False
    )
    export_parser.add_argument("--overwrite", action="store_true", default=False)
    export_parser.add_argument("--max-entry", type=int, default=None)

    args = parser.parse_args()

    if args.command == "fetch":
        if args.title is None and (args.entry is not None or args.show_title):
            fetch_parser.error("--entry and --show-title can only be used with --title")
        elif args.max_entry is not None and not args.show_title:
            fetch_parser.error("--max-entry can only be used with --show-title")

        fetch_cli = FetchCLI()
        if args.source == "all":
            fetch_cli.handle_fetch_cli(
                args,
                True,
                [
                    create_normalizer(source, create_fetcher(source))
                    for source in VALID_DATA_SOURCES
                ],
            )
            return
        fetch_cli.handle_fetch_cli(
            args, False, [create_normalizer(args.source, create_fetcher(args.source))]
        )

    elif args.command == "export":
        if args.title is None and (args.entry is not None or args.save_all):
            export_parser.error("--entry and --save-all can only be used with --title")
        elif args.max_entry is not None and not args.save_all:
            export_parser.error("--max-entry can only be used with --save-all")
        if args.path is None:
            args.path = create_defaulf_filepath(
                args.title if args.title is not None else args.id
            )

        export_cli = ExportCLI(DataIO(args.path))
        if args.source == "all":
            export_cli.handle_export_cli(
                args,
                True,
                [
                    create_normalizer(source, create_fetcher(source))
                    for source in VALID_DATA_SOURCES
                ],
            )
            return
        export_cli.handle_export_cli(
            args, False, [create_normalizer(args.source, create_fetcher(args.source))]
        )

    else:
        parser.print_help()


if __name__ == "__main__":
    main_parser()
