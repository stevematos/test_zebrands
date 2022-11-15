def clean_dict(data: dict) -> dict:
    update_data = {}
    for key, value in data.items():
        if value:
            update_data[key] = value
    return update_data


def diff_dict(dict1: dict, dict2: dict):
    set1 = set(dict1.items())
    set2 = set(dict2.items())

    return dict(set2 - set1)
