import json

import pytest
from Crypto.PublicKey import RSA

from django_pgpy.helpers import hash_password, RSAKey
from django_pgpy.models import Identity
from test_app.models import EncryptedMessage


@pytest.mark.django_db
class TestRSAKey:
    def test_key(self, user_test_data):
        key = RSA.generate(1024)

        rsa = RSAKey(key)
        assert rsa.has_private
        assert rsa.has_public
        assert rsa.is_protected is False

        rsa_pub = RSAKey(key.publickey())
        assert rsa_pub.has_private is False
        assert rsa_pub.has_public
        assert rsa_pub.is_protected is False
        assert rsa_pub.public_key == key.publickey()
        assert rsa_pub.private_key is None
        assert rsa_pub.private_key_blob is None
        assert rsa_pub.public_key_blob is not None

        rsa_pem = RSAKey(key.export_key())
        assert rsa_pem.has_private
        assert rsa_pem.has_public
        assert rsa_pem.is_protected is False
        assert rsa_pem.public_key == key.publickey()
        assert rsa_pem.private_key == key

        rsa_pem_str = RSAKey(key.export_key().decode('utf8'))
        assert rsa_pem_str.has_private
        assert rsa_pem_str.has_public
        assert rsa_pem_str.is_protected is False
        assert rsa_pem_str.public_key == key.publickey()
        assert rsa_pem_str.private_key == key
        assert rsa_pem_str.private_key_blob is not None
        assert rsa_pem_str.public_key_blob is not None

        rsa_pem_pub = RSAKey(key.publickey().export_key())
        assert rsa_pem_pub.has_private is False
        assert rsa_pem_pub.has_public
        assert rsa_pem_pub.is_protected is False
        assert rsa_pem_pub.public_key == key.publickey()
        assert rsa_pem_pub.private_key is None

        rsa_pem_enc = RSAKey(RSAKey.encrypt_key(key, "pwd"))
        assert rsa_pem_enc.has_private
        assert rsa_pem_enc.has_public is False
        assert rsa_pem_enc.public_key_blob is None
        assert rsa_pem_enc.is_protected
        with pytest.raises(ValueError):
            rsa_pem_enc.public_key
        with pytest.raises(ValueError):
            rsa_pem_enc.private_key
        assert not rsa_pem_enc.is_unlocked
        failed = True
        with rsa_pem_enc.unlock("pwd"):
            assert rsa_pem_enc.is_unlocked
            failed = False
        assert not failed
        assert not rsa_pem_enc.is_unlocked
        assert rsa_pem_enc.private_key_blob is not None
        assert rsa_pem_enc.public_key_blob is not None

        rsa_protect = RSAKey(key)
        assert rsa_protect.has_private
        assert rsa_protect.has_public
        assert rsa_protect.is_protected is False
        rsa_protect.protect("pwd")
        assert rsa_protect.has_private
        assert rsa_protect.has_public
        assert rsa_protect.is_protected
        with pytest.raises(ValueError):
            rsa_protect.private_key
        assert rsa_protect.public_key == key.publickey()
        assert rsa_protect.private_key_blob is not None
        assert rsa_protect.public_key_blob is not None


@pytest.mark.django_db
class TestUserIdentity:
    def test_protect(self, user_test_data):
        test_data = user_test_data
        uid_1 = Identity.objects.create(test_data.user_1, None)

        uid_1.private_key.is_protected is False
        uid_1.protect('1234567890')
        assert uid_1.private_key.is_protected

        failed = True
        with uid_1.unlock('1234567890'):
            assert uid_1.private_key.is_unlocked
            failed = False
        assert not failed

    def test_unlock(self, user_identity_test_data):
        test_data = user_identity_test_data

        failed = True
        with test_data.uid_1.unlock(test_data.pwd_user_1):
            assert test_data.uid_1.private_key.is_unlocked
            failed = False
        assert not failed

    def test_private_key(self, user_identity_test_data):
        test_data = user_identity_test_data

        priv_key_1 = test_data.uid_1.private_key
        assert isinstance(priv_key_1, RSAKey)

        priv_key_2 = test_data.uid_1.private_key
        assert priv_key_1 == priv_key_2

    def test_public_key(self, user_identity_test_data):
        test_data = user_identity_test_data

        pub_key_1 = test_data.uid_1.public_key
        assert isinstance(pub_key_1, RSAKey)

        pub_key_2 = test_data.uid_1.public_key
        assert pub_key_1 == pub_key_2

    def test_set_secret(self, user_test_data):
        test_data = user_test_data

        uid_1 = Identity.objects.create(test_data.user_1, None)

        uid_1.set_secret('test')
        assert 'nonce' in uid_1.secret_blob
        assert 'keys' in uid_1.secret_blob
        assert len(uid_1.secret_blob['keys']) == 1

    def test_get_secret(self, user_identity_test_data):
        test_data = user_identity_test_data

        fail = True # hack
        with test_data.uid_1.unlock(test_data.pwd_user_1):
            secret = test_data.uid_2.get_secret(test_data.uid_1)
            assert secret is not None
            assert test_data.uid_2.private_key.is_protected
            assert not test_data.uid_2.private_key.is_unlocked
            with test_data.uid_2.private_key.unlock(secret):
                assert test_data.uid_2.private_key.is_unlocked
                fail = False
        assert not fail
        assert test_data.uid_2.private_key.is_protected
        assert not test_data.uid_2.private_key.is_unlocked


    def test_decrypt(self, encrypted_message_test_data):
        test_data = encrypted_message_test_data

        assert test_data.uid_1.decrypt(test_data.enc_text_1, test_data.pwd_user_1) == test_data.text_1
        assert test_data.uid_1.decrypt(test_data.enc_text_3, test_data.pwd_user_1) == test_data.text_3

        # decrypt with protected key
        with pytest.raises(ValueError):
            test_data.uid_1.decrypt(test_data.enc_text_1)

        # decrypt a message with wrong UID
        with pytest.raises(ValueError):
            test_data.uid_1.decrypt(test_data.enc_text_2)

    def test_unlock_private_key(self, user_identity_test_data):
        test_data = user_identity_test_data

        assert test_data.uid_2.private_key.is_protected

        alg, password = hash_password(test_data.pwd_user_2, test_data.uid_2.hash_info)
        with test_data.uid_2.private_key.unlock(password):
            assert test_data.uid_2.private_key.is_unlocked

    def test_change_password(self, user_identity_test_data):
        test_data = user_identity_test_data

        old_password = test_data.pwd_user_2
        new_password = '1234567890'
        uid = test_data.uid_2

        failed = True
        with uid.unlock(old_password):
            assert uid.private_key.is_unlocked
            failed = False
        assert not failed

        uid = Identity.objects.get(id=uid.id)
        uid.change_password(old_password, new_password)

        uid = Identity.objects.get(id=uid.id)
        failed = True
        with uid.unlock(new_password):
            assert uid.private_key.is_unlocked
            failed = False
        assert not failed

        # fallback still works
        # uid_1 = test_data.uid_1
        # _, uid_1_password_hash = hash_password(test_data.pwd_user_1, uid_1.hash_info)
        # with test_data.uid_1.private_key.unlock(uid_1_password_hash):

    def test_password_reset(self, user_identity_test_data):
        test_data = user_identity_test_data

        new_password = '1234567890'
        uid_admin = test_data.uid_1
        uid_user = test_data.uid_2

        with uid_user.unlock(test_data.pwd_user_2):
            assert uid_user.private_key.is_unlocked

        reset_request = uid_user.reset_password(new_password)

        uid_user = Identity.objects.get(id=uid_user.id)
        assert uid_user.can_decrypt is False

        reset_request.reset_password(uid_admin, test_data.pwd_user_1)

        uid_user = Identity.objects.get(id=uid_user.id)
        uid_admin = Identity.objects.get(id=uid_admin.id)

        assert uid_user.can_decrypt

        with uid_user.unlock(new_password):
            assert uid_user.private_key.is_unlocked

        with uid_admin.unlock(test_data.pwd_user_1):
            secret = uid_user.get_secret(uid_admin)

            with uid_user.private_key.unlock(secret):
                assert uid_user.private_key.is_unlocked

    def test_add_restorers(self, user_identity_test_data):
        test_data = user_identity_test_data

        uid_admin = test_data.uid_1
        uid_user = test_data.uid_2
        new_user =  test_data.uid_4


        uid_user = Identity.objects.get(id=uid_user.id)
        assert new_user not in uid_user.encrypters.all()

        uid_user.add_restorers(test_data.pwd_user_2, [new_user])
        assert new_user in uid_user.encrypters.all()
        assert uid_admin in uid_user.encrypters.all()

        with new_user.unlock(test_data.pwd_user_4):
            secret = uid_user.get_secret(new_user)

            with uid_user.private_key.unlock(secret):
                assert uid_user.private_key.is_unlocked

        with uid_admin.unlock(test_data.pwd_user_1):
            secret = uid_user.get_secret(uid_admin)

            with uid_user.private_key.unlock(secret):
                assert uid_user.private_key.is_unlocked

class TestEncryptedMessage:

    def test_create(self, user_identity_test_data):
        test_data = user_identity_test_data

        encrypters = [test_data.uid_1]
        enc_msg = EncryptedMessage.objects.create('1234567890', encrypters)
        encoded = enc_msg.text
        assert 'nonce' in encoded
        assert 'keys' in encoded
        assert 'ciphertext' in encoded
        assert [e.id for e in enc_msg.encrypters.all()] == [e.id for e in encrypters]

        with test_data.uid_1.unlock(test_data.pwd_user_1):
            assert test_data.uid_1.private_key.is_unlocked

            m = test_data.uid_1.decrypt(enc_msg)
            assert m == '1234567890'

        with test_data.uid_2.unlock(test_data.pwd_user_2):
            assert test_data.uid_2.private_key.is_unlocked

            with pytest.raises(ValueError):
                test_data.uid_2.decrypt(enc_msg)

    def test_encrypt(self, user_identity_test_data):
        test_data = user_identity_test_data

        encrypters = [test_data.uid_1]
        enc_msg = EncryptedMessage()
        enc_msg.encrypt('1234567890', encrypters)

        encoded = enc_msg.text
        assert 'nonce' in encoded
        assert 'keys' in encoded
        assert 'ciphertext' in encoded
        assert [e.id for e in enc_msg.encrypters.all()] == [e.id for e in encrypters]

        with test_data.uid_1.unlock(test_data.pwd_user_1):
            assert test_data.uid_1.private_key.is_unlocked

            m = test_data.uid_1.decrypt(enc_msg)
            assert m == '1234567890'

        with test_data.uid_2.unlock(test_data.pwd_user_2):
            assert test_data.uid_2.private_key.is_unlocked

            with pytest.raises(ValueError):
                test_data.uid_2.decrypt(enc_msg)

    def test_decrypt(self, encrypted_message_test_data):
        test_data = encrypted_message_test_data

        with test_data.uid_1.unlock(test_data.pwd_user_1):
            assert test_data.enc_text_1.decrypt(test_data.uid_1) == test_data.text_1
            assert test_data.enc_text_3.decrypt(test_data.uid_1) == test_data.text_3

            with pytest.raises(ValueError):
                test_data.enc_text_2.decrypt(test_data.uid_1)

        with test_data.uid_2.unlock(test_data.pwd_user_2):
            assert test_data.enc_text_2.decrypt(test_data.uid_2) == test_data.text_2
            assert test_data.enc_text_3.decrypt(test_data.uid_2) == test_data.text_3

            with pytest.raises(ValueError):
                test_data.enc_text_1.decrypt(test_data.uid_2)

    def test_add_encrypter(self, add_remove_encrypter_test_data):
        test_data = add_remove_encrypter_test_data

        with test_data.uid_2.unlock(test_data.pwd_user_2):
            with pytest.raises(ValueError):
                test_data.enc_text_1.decrypt(test_data.uid_2)

        test_data.enc_text_1.add_encrypters(test_data.uid_1,
                                            test_data.pwd_user_1,
                                            [test_data.uid_2])

        with test_data.uid_2.unlock(test_data.pwd_user_2):
            enc_msg = EncryptedMessage.objects.get(id=test_data.enc_text_1.id)
            assert enc_msg.decrypt(test_data.uid_2) == test_data.text_1

        assert test_data.enc_text_3.encrypters.filter(id=test_data.uid_3.id).exists() is False
        with test_data.uid_3.unlock(test_data.pwd_user_3):
            with pytest.raises(ValueError):
                test_data.enc_text_3.decrypt(test_data.uid_3)

        test_data.enc_text_3.add_encrypters(test_data.uid_2,
                                            test_data.pwd_user_2,
                                            [test_data.uid_3])

        with test_data.uid_3.unlock(test_data.pwd_user_3):
            enc_msg = EncryptedMessage.objects.get(id=test_data.enc_text_3.id)
            assert enc_msg.decrypt(test_data.uid_3) == test_data.text_3

            assert enc_msg.encrypters.filter(id=test_data.uid_3.id).exists()

    def test_remove_encrypter(self, add_remove_encrypter_test_data):
        test_data = add_remove_encrypter_test_data

        assert test_data.enc_text_3.encrypters.filter(id=test_data.uid_2.id).exists()

        test_data.enc_text_3.remove_encrypters([test_data.uid_2])

        with test_data.uid_2.unlock(test_data.pwd_user_2):
            enc_msg = EncryptedMessage.objects.get(id=test_data.enc_text_3.id)
            assert enc_msg.encrypters.filter(id=test_data.uid_2.id).exists() is False
            with pytest.raises(ValueError):
                assert enc_msg.decrypt(test_data.uid_2) == test_data.text_3
