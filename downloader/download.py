import codecs
import json
import logging
import os
import time
from urllib.request import urlretrieve

logging.basicConfig(format='%(message)s', level=logging.INFO)


def reporthook(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return

    duration = time.time() - start_time

    print(' '*50, end='\r')

    if total_size > 0:
        progress_size = int(count * block_size)/1000000
        speed = int(progress_size / (1024 * duration))
        percent = int(count * block_size * 100 / total_size)
        print(f"... {percent}%, {progress_size:.0f} MB, {speed} KB/s, {duration:.0f} секунд", end='\r')
        if percent >= 100:
            print('\n')

    else:
        print(f"... {int(count*block_size)/1000000:.2f} MB, {duration:.0f} секунд", end='\r')


def download():
    with open('input/data.json', 'r') as f:
        data = f.read()
        data = json.loads(data)

    data.sort(key=lambda x: x['number'], reverse=True)

    counter = 0
    line = 0
    while counter < 30:
        if data[line]['downloaded'] in [False, 'err']:
            filename = f"{data[line]['number']}.{data[line]['author']} - {data[line]['name']}.mp3".replace('/', '_')
            logging.info(filename)
            for index, link in enumerate(data[line]['links'].split(' || ')):
                try:
                    logging.info(f"Ссылка {index + 1} из {len(data[line]['links'].split(' || '))}")
                    urlretrieve(link, f'output/{filename}', reporthook)
                    data[line]['downloaded'] = True
                    break
                except (Exception, KeyboardInterrupt) as e:
                    logging.info(f'Отмена ({e})')
                    continue
            else:
                data[line]['downloaded'] = 'err'

            with codecs.open('input/data.json', 'w+', encoding='utf-8') as f:
                f.write(json.dumps(data, ensure_ascii=False, indent=2))
            counter += 1
        line += 1
    else:
        print(' ')
        logging.info('Готово!')

    for f in os.listdir('output'):
        if os.path.getsize('output/' + f) < 1000000:
            os.remove('output/' + f)


if __name__ == '__main__':
    download()
