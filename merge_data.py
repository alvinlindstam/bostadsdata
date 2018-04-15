import json


from utils import write_prettier_json


if __name__ == "__main__":
    with open("data/full_list.json", "r") as full_list:
        all_items = json.loads(full_list.read())

    with open("data/extra_ad_data.json", "r") as old_extra_data:
        extra_data = json.loads(old_extra_data.read())

    for item in all_items:
        aid = item[0]
        extra_data_item = extra_data.get(str(aid), {})
        for key in ["pub_d", "ad_d", "move_d", "ll", "x", "y"]:
            item.append(extra_data_item.get(key))

    with open("data/full_data.json", "w+") as full_data_file:
        write_prettier_json(all_items, file=full_data_file)

