from utils.extras import clean_dict, diff_dict


def test_password_hashing():
    input_data = {
        'test': None,
        'QWER': False,
        'name': 'John Doe',
        'age': 13
    }

    actual = clean_dict(input_data)

    expected = {
        'name': 'John Doe',
        'age': 13
    }

    assert expected == actual


def test_diff_dict():
    dict1 = {
        'test': 13,
        'test2': 14,
        'test3': 15,
        'test8': 18
    }
    dict2 = {
        'test2': 'test',
        'test3': 16,
        'test8': 21,
    }

    actual = diff_dict(dict1, dict2)
    expected = {'test8': 21, 'test2': 'test', 'test3': 16}

    assert expected == actual