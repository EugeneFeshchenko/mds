import argparse
import logging
import os
import sqlite3
import time
from enum import Enum
from urllib.request import urlretrieve


logging.basicConfig(format="%(message)s", level=logging.INFO)


class Status(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class Downloader:
    def __init__(self):
        parser = argparse.ArgumentParser(description="Скачивает файлы с сайта MDS.")
        parser.add_argument(
            "-n",
            metavar="Number",
            default=3,
            type=int,
            required=False,
            help="количество файлов(10 по умолчанию)",
        )
        self.args = parser.parse_args()
        self.batch_size = self.args.n

        self.conn = sqlite3.connect("input/mds.db")
        self.cursor = self.conn.cursor()

    @staticmethod
    def reporthook(count: int, block_size: int, total_size: int) -> None:
        global start_time
        if count == 0:
            start_time = time.time()
            return

        duration = time.time() - start_time

        print(' '*50, end='\r')

        progress_size = int(count * block_size) / 1000000
        if total_size > 0:
            percent = int(count * block_size * 100 / total_size)
            print(f"... {percent}%, {progress_size:.0f} MB, {duration:.0f} секунд", end='\r')
        else:
            print(f"... {progress_size:.2f} MB, {duration:.0f} секунд", end='\r')

    def set_book_status(self, book_id, status):
        self.cursor.execute(
            """
            UPDATE books
            SET status = ?
            WHERE id = ?
            """,
            (status, book_id),
        )
        self.conn.commit()

    def download_batch(self) -> None:
        self.cursor.execute(
            """
            SELECT * FROM books
            WHERE status = ?
            ORDER BY number ASC
            LIMIT ?
        """,
            ("pending", self.batch_size),
        )

        for item in self.cursor.fetchall():
            filename = f"{item[1]}.{item[4]} - {item[2]}.mp3".replace('/', '_')
            logging.info(filename)
            links = item[3].split(' || ')
            for index, link in enumerate(links):
                logging.info(f"Ссылка {index + 1} из {len(links)}")
                try:
                    urlretrieve(url=link, filename=f"output/{filename}", reporthook=self.reporthook)
                    self.set_book_status(item[0], Status.COMPLETED)
                    break
                except (Exception, KeyboardInterrupt) as e:
                    logging.info(f"Отмена ({e})")
                    continue
            else:
                self.set_book_status(item[0], Status.FAILED)

            logging.info('_' * 50)

        self.cleanup()
        self.conn.close()

    @staticmethod
    def cleanup() -> None:
        for f in os.listdir("output"):
            if os.path.getsize("output/" + f) < 1000000:
                os.remove("output/" + f)


if __name__ == "__main__":
    Downloader().download_batch()
