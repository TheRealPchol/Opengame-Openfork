import os
import logging
import csv
from models import Tag, Platform, Game
from client import StopGameClient
from bs4 import BeautifulSoup as bs

logger = logging.getLogger(__name__)

CONFIG_DIR = "config"
TAGS_FILE = os.path.join(CONFIG_DIR, "tags.csv")
PLATFORMS_FILE = os.path.join(CONFIG_DIR, "platforms.csv")


def save_tags(data: list[dict]) -> None:
    """Выгружает информацию о доступных тегах в каталоге"""
    if not os.path.exists(TAGS_FILE):
        logger.info(f"Директория {CONFIG_DIR} не найдена и будет создана")
        os.makedirs(CONFIG_DIR)
    with open(TAGS_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["slug", "name_singular"], extrasaction='ignore')
        writer.writeheader()
        for item in data:
            writer.writerow(item)
    logger.info(f"Записано в файл {TAGS_FILE}, {len(data)} тегов")


def save_platforms(data: list[dict]) -> None:
    """Выгружает информацию о доступных платформах в каталоге"""
    if not os.path.exists(CONFIG_DIR):
        logger.info(f"Директория {CONFIG_DIR} не найдена и будет создана")
        os.makedirs(CONFIG_DIR)
    with open(PLATFORMS_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["code", "title"], extrasaction='ignore')
        writer.writeheader()
        for item in data:
            writer.writerow(item)
    logger.info(f"Записано в файл {PLATFORMS_FILE}, {len(data)} тегов")


def load_tags() -> list[Tag]:
    with open(TAGS_FILE, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        tags = []
        for row in reader:
            tags.append(
                Tag(slug=row["slug"], name=row["name_singular"])
            )

    logger.debug(f"Прочитано {len(tags)} тегов")
    return tags


def load_platforms() -> list[Platform]:
    with open(PLATFORMS_FILE, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        platforms = []
        for row in reader:
            platforms.append(
                Platform(code=row["code"], title=row["title"])
            )
    logger.debug(f"Прочитано {len(platforms)} платформ")
    return platforms

# def find_tag(user_input: str, tags: list[Tag]) -> Tag:

def get_games(page: str = 1, tags: list = None, platforms: list = None) -> list[Game]:
    client = StopGameClient()
    params = {}
    if tags: params['tags'] = tags
    if platforms: params['platforms'] = platforms
    response = client._get("/games/catalog", params=params)
    if response["status"] == 0:
        html = response["content"].text
    else:
        logger.warning(f"Ошибка {response["error"]["type"]}: {response['error']['message']}")
        html = None
    print(params)
    print(response["content"].url)
    if html:
        soup = bs(html, "html.parser")
        games_class = soup.find("div", class_="list-view _section-with-pagination_82nn8_509").find("div", class_="_games-grid_fl71g_283")
        games_all = soup.find_all("div")

        for i in range(len(games_all)):
            game = games_all[i]
            if game.get("data-key"):
                #print(type(games_all[i]))
                a = games_all[i].find_all("a")
                #print(f"\nGame №{i + 1}:")
                #print(f"    {a[0]['href']}")
                url = a[0]['href']
                res = client._get(url, None)
                if res["status"] == 0:
                    soup = bs(res["content"].text, "html.parser")
                    #print(url)
                    info_by_soup(soup)
                    break
def info_by_soup(soup, show: bool = False, _step: str = "", _start: str = "\n"):
    result = {}
    date_of_out = soup.find("div", class_="_game-info_1bso0_696").find("dl", class_="_game-info__grid_1bso0_993").find_all("dd")[0].text
    result["date"] = date_of_out
    name = soup.find('h1', class_="_game-title_1bso0_702").text
    result["Название"] = name
    #print(date_of_out.prettify())
    dts = soup.find("dl", class_="_game-info__grid_1bso0_993").find_all("dt")
    dds = soup.find("dl", class_="_game-info__grid_1bso0_993").find_all("dd")
    for i in range(len(dds)):
        print()



    if show:
        print(f"{_start}{_step}Информация о {name}:")
        print(f"{_step}    Дата выхода: {date_of_out}")
        #print(f"{_step}    Разработчик: {author}")
        #print(type(games_all))
if __name__ == "__main__":
    # from client import StopGameClient
    # from logging_config import BASIC_CONFIG
    #
    # logging.basicConfig(**BASIC_CONFIG)
    # client = StopGameClient()
    # # save_tags(client.fetch_tags())
    # # save_platforms(client.fetch_platforms())
    # print(load_platforms())
    get_games()