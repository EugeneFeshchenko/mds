import argparse
import codecs
import json
import logging
import os
import time
from urllib.request import urlretrieve

logging.basicConfig(format='%(message)s', level=logging.INFO)


class Downloader:
    def __init__(self):
        with open('input/data.json', 'r') as f:
            data = f.read()
            data = json.loads(data)
            data.sort(key=lambda x: x['number'], reverse=True)
        self.data = data

        parser = argparse.ArgumentParser(description='Скачивает файлы с сайта MDS.')
        parser.add_argument(
            '-n', metavar='Number', default=30, type=int, required=False, help='количество файлов(30 по умолчанию)'
        )
        self.args = parser.parse_args()
        self.batch_size = self.args.n

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

    def save_data(self) -> None:
        with codecs.open('input/data.json', 'w+', encoding='utf-8') as f:
            f.write(json.dumps(self.data, ensure_ascii=False, indent=2))

    def download_batch(self) -> None:
        downloaded_counter = 0

        for item in filter(lambda x: x['downloaded'] != True, self.data):
            filename = f"{item['number']}.{item['author']} - {item['name']}.mp3".replace('/', '_')
            logging.info(filename)
            links = item['links'].split(' || ')
            for index, link in enumerate(links):
                logging.info(f"Ссылка {index + 1} из {len(links)}")
                try:
                    urlretrieve(link, f'output/{filename}', self.reporthook)
                    item['downloaded'] = True
                    downloaded_counter += 1
                    break
                except (Exception, KeyboardInterrupt) as e:
                    logging.info(f'Отмена ({e})')
                    continue
            else:
                item['downloaded'] = 'err'

            self.save_data()
            logging.info('_' * 50)

            if downloaded_counter >= self.batch_size:
                logging.info(f'Готово! {downloaded_counter}')
                self.cleanup()
                break

    @staticmethod
    def cleanup() -> None:
        for f in os.listdir('output'):
            if os.path.getsize('output/' + f) < 1000000:
                os.remove('output/' + f)


if __name__ == '__main__':
    Downloader().download_batch()
