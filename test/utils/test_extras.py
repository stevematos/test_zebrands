from utils.extras import clean_dict


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
