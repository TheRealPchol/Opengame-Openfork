import argparse

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

    parser.add_argument("-v", "--verbose", action="store_true", help="Включить более подробный вывод")
    subparsers = parser.add_subparsers(dest="command")

    update_subpars = subparsers.add_parser("update", help="скачать справочники жанров и платформ", parents=[common_parser])
    update_subpars.add_argument("-c", '--count', help="Количество игр которые надо распарсить", type=int)
    update_subpars.add_argument("-p", "--page", help="Страница которую надо распарсить", type=int, default=0)

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

