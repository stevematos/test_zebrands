from utils.tokens import decode, encode


def test_encode_and_decode():
    key = "fake"
    payload = {"test": "test", "email": "test@example.com"}
    token = encode(payload, key)
    payload_decode = decode(token, key)

    assert payload_decode == payload
