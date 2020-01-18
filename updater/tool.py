import json
import codecs


def change():

    with open('data_old.json', 'r') as f:
        original_data = json.loads(f.read())

    with open('data_new.json', 'r') as f:
        new_data = json.loads(f.read())

    new_data.sort(key=lambda x:  x['number'])
    for node in new_data:
        try:
            original_node = list(filter(lambda x: x['name'] == node['name'], original_data))[0]
        except IndexError:
            original_node = {'downloaded': False, 'links': ''}

        node['downloaded'] = original_node['downloaded']
        node['links'] = set(node['links'].split(' || ') + original_node['links'].split(' || '))
        node['links'] = ' || '.join([str(x) for x in node['links'] if x])

    with codecs.open('data_synced.json', 'w+', encoding='utf-8') as f:
        f.write(json.dumps(new_data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    change()
