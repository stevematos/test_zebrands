from services.email import send_plain_email


def test_send_templated_email():
    send_plain_email("test", "test", "test")