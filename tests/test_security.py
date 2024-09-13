from blindage.security import decrypt, encrypt, gen_key

MAIN_PASSWORD = 'Test@12345#$'


def test_generate_key():
    key = gen_key(MAIN_PASSWORD)
    assert key != MAIN_PASSWORD


def test_encrypt_and_decrypt():
    encrypt_password = encrypt(MAIN_PASSWORD, 'password')
    assert encrypt_password != 'password'

    decrypt_password = decrypt(MAIN_PASSWORD, encrypt_password)
    assert decrypt_password == 'password'
