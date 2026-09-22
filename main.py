import argparse
import logging
import reference


from logging_config import BASIC_CONFIG

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Уровень сообщений в логе",
    )
    parser = argparse.ArgumentParser(
        prog="stopgame",
        description="Каталог игр StopGame из командной строки",
        parents=[common_parser]
    )

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("update", help="скачать справочники жанров и платформ", parents=[common_parser])

    p_genres = subparsers.add_parser("genres", help="показать доступные жанры", parents=[common_parser])
    p_genres.add_argument("--save", metavar="ФАЙЛ", help="записать список в файл")

    p_platforms = subparsers.add_parser("platforms", help="показать доступные платформы", parents=[common_parser])
    p_platforms.add_argument("--save", metavar="ФАЙЛ", help="записать список в файл")

    p_games = subparsers.add_parser("games", help="загрузить игры по фильтрам", parents=[common_parser])
    p_games.add_argument("--genres", nargs="+", metavar="ЖАНР",
                         help="жанры, темы, режимы (как на сайте)", default=[])
    p_games.add_argument("--platforms", nargs="+", metavar="ПЛАТФОРМА",
                         help="платформы (как на сайте)", default=[])
    p_games.add_argument("--pages", type=int, default=1, help="сколько страниц скачать")
    p_games.add_argument("--out", default="games.csv", help="куда сохранить результат")

    return parser


def cmd_update(args):
    logger.info(f"command update {args}")


def cmd_genres(args):
    logger.info(f"command genres {args}")


def cmd_platforms(args):
    logger.info(f"command platforms {args}")


def cmd_games(args):
    logger.info(f"command games {args}")

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
