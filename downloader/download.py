# -*- coding: utf-8 -*-

import codecs
import json
import os
import sys
import time
import urllib


def reporthook(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration))
    percent = int(count * block_size * 100 / total_size)
    if percent < 0:
        percent = '? '
    sys.stdout.write("\r... %d%%, %d MB, %d KB/s, %d секунд" % (percent, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()
    if percent >= 100:
        print('')


def download():

    with open('input/data.json', 'r') as f:
        data = f.read()
        data = json.loads(data)

    data.sort(key=lambda x: x['number'], reverse=True)

    counter = 0
    line = 0
    while counter < 30:
        if not data[line]['downloaded'] or data[line]['downloaded'] == 'err':
            filename = u'{}.{} - {}.mp3'.format(data[line]['number'], data[line]['author'], data[line]['name'])
            print(filename)
            for index, link in enumerate(data[line]['links'].split(' || ')):
                try:
                    print('Ссылка {} из {}'.format(index+1, len(data[line]['links'].split(' || '))))
                    urllib.urlretrieve(link, 'output/'+filename, reporthook)
                    data[line]['downloaded'] = True
                    break
                except Exception as e:
                    data[line]['downloaded'] = 'err'
                    print('    Отмена.')
                    continue
                except KeyboardInterrupt:
                    data[line]['downloaded'] = 'err'
                    print('    Отмена.')
                    continue

            with codecs.open('input/data.json', 'w+', encoding='utf-8') as f:
                f.write(json.dumps(data, ensure_ascii=False, indent=2))
            counter += 1
        line += 1
    else:
        print('')
        print('Готово!')

    for f in os.listdir('output'):
        if os.path.getsize('output/' + f) < 1000000:
            os.remove('output/' + f)


if __name__ == '__main__':
    download()
