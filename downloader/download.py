import codecs
import json
import logging
import os
import time
from urllib.request import urlretrieve, FancyURLopener

logging.basicConfig(format='%(message)s', level=logging.INFO)


class Downloader:
    def __init__(self, batch_size=30):
        self.batch_size = batch_size
        with open('input/data.json', 'r') as f:
            data = f.read()
            data = json.loads(data)
            data.sort(key=lambda x: x['number'], reverse=True)
        self.data = data

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
            if percent >= 100:
                print('\n')
        else:
            print(f"... {progress_size:.2f} MB, {duration:.0f} секунд", end='\r')

    def download_batch(self) -> None:
        downloaded_counter = 0
        item_idx = 0
        data = self.data
        while downloaded_counter < self.batch_size and item_idx <= len(self.data):
            item = data[item_idx]
            if item['downloaded'] in [False, 'err']:
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
                    data[item_idx]['downloaded'] = 'err'

                with codecs.open('input/data.json', 'w+', encoding='utf-8') as f:
                    f.write(json.dumps(data, ensure_ascii=False, indent=2))

            item_idx += 1
        else:
            logging.info('')
            logging.info('Готово!')

        self.cleanup()

    @staticmethod
    def cleanup() -> None:
        for f in os.listdir('output'):
            if os.path.getsize('output/' + f) < 1000000:
                os.remove('output/' + f)


if __name__ == '__main__':
    Downloader().download_batch()
