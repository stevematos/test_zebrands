
def clean_dict(data: dict) -> dict:
    update_data = {}
    for key, value in data.items():
        if value:
            update_data[key] = value
    return update_data
