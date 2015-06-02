import json
import codecs

def change():

    with open('data.json', 'r') as f:
        d = f.read()
        d = json.loads(d)

    for item in d:
        try:
            item['link']['size'] = float(item['link']['size'].split(' ')[0])
            item['link']['size'] = int(item['link']['size'])
        except:
            pass

    with codecs.open('data_new.json', 'w+', encoding='utf-8') as f:
        f.write(json.dumps(d, ensure_ascii=False))

    print'Done'

if __name__ == "__main__":
    change()
