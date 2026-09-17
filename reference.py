import os
import logging
import csv

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

if __name__ == "__main__":
    from client import StopGameClient
    from logging_config import BASIC_CONFIG
    logging.basicConfig(**BASIC_CONFIG)
    client = StopGameClient()
    data = client.fetch_tags()
    save_tags(data)





