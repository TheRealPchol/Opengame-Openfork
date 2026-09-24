import argparse
import logging
import reference
from build_parser import build_parser

from logging_config import BASIC_CONFIG

logger = logging.getLogger(__name__)



def cmd_update(args):
    reference.get_games(page=args.page, count=args.count, verbose=args.verbose)


def cmd_genres(args):
    logger.info(f"command genres {args}")


def cmd_platforms(args):
    logger.info(f"command platforms {args}")


def cmd_games(args):

    platforms = reference.load_platforms()
    platform_codes = []
    for user_input in args.platforms:
        for platform in platforms:
            if platform.matches(user_input):
                platform_codes.append(platform.code)

    tags = reference.load_tags()
    tag_slugs = []
    for user_input in args.genres:
        for tag in tags:
            if tag.matches(user_input):
                tag_slugs.append(tag.slug)

    print(f"{platform_codes=}, {tag_slugs=}")



def main():
    commands = {
        "update": cmd_update,
        "genres": cmd_genres,
        "platforms": cmd_platforms,
        "games": cmd_games,
    }
    parser = build_parser()
    args = parser.parse_args()

    BASIC_CONFIG["level"] = args.log_level
    logging.basicConfig(
        **BASIC_CONFIG,
    )

    func = commands[args.command]  # выбираем функцию по имени команды
    func(args)


if __name__ == "__main__":
    main()
