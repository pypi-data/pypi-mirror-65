import contextlib
import warnings

from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Random import get_random_bytes
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from typing import List, Union
from django_pgpy import settings

import base64
from Crypto.Cipher import AES, PKCS1_OAEP


class RSAKey:
    def __init__(self, key: Union[str, bytes, RsaKey]):
        self._key = None
        self._public_key = None
        self._encrypted_key = None

        if isinstance(key, bytes) or isinstance(key, str):
            try:
                key = RSA.importKey(key)
                if key.has_private():
                    self._key = key
                    self._public_key = key.publickey()
                else:
                    self._public_key = key
            except:
                if isinstance(key, bytes):
                    self._encrypted_key = key.decode('utf8')
                else:
                    self._encrypted_key = key
        else:
            if isinstance(key, RsaKey):
                if key.has_private():
                    self._key = key
                    self._public_key = key.publickey()
                else:
                    self._public_key = key
            else:
                raise ValueError('invalid key format')

    @property
    def has_public(self):
        return self._public_key is not None

    @property
    def has_private(self):
        return self._key is not None or self._encrypted_key is not None

    @property
    def private_key(self):
        if self._key:
            return self._key
        else:
            if self._encrypted_key:
                raise ValueError('The key is protected. Please unlock')
            else:
                return None

    @property
    def private_key_blob(self):
        if self._key:
            return self._key.export_key().decode('utf8')
        elif self._encrypted_key:
            return self._encrypted_key
        else:
            return None

    @property
    def public_key(self):
        if self._public_key:
            return self._public_key
        elif self._encrypted_key:
            raise ValueError('The key is protected. Please unlock')
        else:
            return None

    @property
    def public_key_blob(self):
        if self.has_public:
            return self.public_key.export_key().decode('utf8')
        else:
            return None

    @property
    def is_unlocked(self):
        # check if public key
        if self.has_public and not self.has_private:
            return True

        if not self.is_protected:
            return True

        return False

    @property
    def is_protected(self):
        return self._key is None and self._encrypted_key is not None

    def protect(self, password: str):
        if self._key:
            self._encrypted_key = self.encrypt_key(self._key, password)
            self._key = None
            return self

    @contextlib.contextmanager
    def unlock(self, password: str):
        if self._key:
            warnings.warn("This key is not protected with a passphrase", stacklevel=3)
            yield self
            return

        try:
            self._key = RSA.import_key(self._encrypted_key, passphrase=password)
            self._public_key = self._key.publickey()
            del password
            yield self
            self._key = None
        except:
            self._key = None
            raise

    @staticmethod
    def encrypt_key(key: RsaKey, password: str):
        return key.export_key(passphrase=password, pkcs=8, protection="scryptAndAES128-CBC").decode('utf8')


def create_identity(name, email, password=None, restorer_public_keys: List[RSAKey] = []):
    key = create_key_pair(name, email)
    restorer_public_keys.append(RSAKey(key.public_key))
    secret_blob = None
    hash_info = None

    if password:
        hash_info, password_hash = hash_password(password)
        # public_keys = [r.public_key for r in restorers]

        if restorer_public_keys:
            secret_blob = encrypt(password_hash, restorer_public_keys)

        key.protect(password_hash)

    return key, hash_info, secret_blob


def create_key_pair(name: str, email: str) -> RSAKey:
    key = RSA.generate(settings.DJANGO_PGPY_RSA_KEY_LENGTH)
    return RSAKey(key)


def hash_password(password, hash_info=None):
    hasher = PBKDF2PasswordHasher()
    if hash_info:
        algo, iterations, salt = hash_info.split('$')
        return hasher.encode(password,
                             salt=salt,
                             iterations=int(iterations)).rsplit('$', 1)
    return hasher.encode(password, hasher.salt()).rsplit('$', 1)


def encrypt(text: str, public_keys: List[RSAKey]):
    # create a session key
    session_key = get_random_bytes(settings.DJANGO_PGPY_AES_KEY_LENGTH)

    # encrypt the text with the session key
    data = text.encode('ascii')
    cipher = AES.new(session_key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    json_k = ['nonce', 'ciphertext', 'tag']
    json_v = [base64.b64encode(x).decode('utf-8') for x in [cipher.nonce, ciphertext, tag]]
    aes_result = dict(zip(json_k, json_v))

    # encrypt the session key with all the public keys
    encrypted_session_keys = {}
    for key in public_keys:
        assert key.public_key

        # Encrypt the session key with the public RSA key
        encrypted_session_keys[key.public_key_blob] = encrypt_session_key(session_key, key.public_key)

    aes_result['keys'] = encrypted_session_keys
    return aes_result


def get_session_key(encoded: dict, key: RSAKey):
    if not 'keys' in encoded:
        raise ValueError('Cannot decrypt: No encrypters available')

    encrypter_public_keys = encoded['keys']
    pub_blob = key.public_key_blob

    if not pub_blob in encrypter_public_keys:
        raise ValueError('Cannot decrypt: The identity is not in the list of encrypters')

    encrypted_session_key = base64.b64decode(encrypter_public_keys[pub_blob])

    # decrypt the session key
    cipher_rsa = PKCS1_OAEP.new(key.private_key)
    session_key = cipher_rsa.decrypt(encrypted_session_key)

    return session_key


def encrypt_session_key(session_key: bytes, public_key: RsaKey):
    # Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(public_key)
    enc_session_key = cipher_rsa.encrypt(session_key)
    return base64.b64encode(enc_session_key).decode('utf8')


def decrypt(encoded: dict, key: RSAKey):
    assert key.has_private
    # base64 decode encoded
    json_k = ['nonce', 'ciphertext', 'tag']
    jv = {k: base64.b64decode(encoded[k]) for k in json_k}

    session_key = get_session_key(encoded, key)

    # decrypt the message
    cipher = AES.new(session_key, AES.MODE_GCM, nonce=jv['nonce'])
    plaintext = cipher.decrypt_and_verify(jv['ciphertext'], jv['tag'])
    return plaintext.decode("utf-8")


def add_encrypters(encoded: dict, key: RSAKey, encrypter_public_keys: List[RSAKey]):
    assert key.is_unlocked
    encoded_session_keys = encoded['keys']
    session_key = get_session_key(encoded, key)
    for public_key in encrypter_public_keys:
        # Encrypt the session key with the public RSA key
        encoded_session_keys[public_key.public_key_blob] = encrypt_session_key(session_key, public_key.public_key)
    encoded['keys'] = encoded_session_keys
    return encoded
