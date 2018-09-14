import json
import codecs


def change():

    with open('data.json', 'r') as f:
        d = f.read()
        d = json.loads(d)

    d.sort(key=lambda x:  x['number'])

    with codecs.open('data_new.json', 'w+', encoding='utf-8') as f:
        f.write(json.dumps(d, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    change()
