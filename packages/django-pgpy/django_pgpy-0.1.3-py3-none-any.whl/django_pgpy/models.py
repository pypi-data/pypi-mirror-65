from __future__ import unicode_literals, annotations

import json
from contextlib import nullcontext
from typing import List, Union

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import CASCADE, QuerySet
from django.utils import timezone
from django.utils.functional import cached_property

from django_pgpy.helpers import hash_password, encrypt, \
    add_encrypters, RSAKey, decrypt
from django_pgpy.managers import EncryptedMessageManager, UserIdentityManager


def get_secret(decrypter_uid: Identity, secret_blob: str) -> str:
    assert decrypter_uid.private_key.is_unlocked

    encrypted_message = secret_blob
    msg = decrypt(encrypted_message, decrypter_uid.private_key)
    return msg


class Identity(models.Model):
    objects = UserIdentityManager()

    user = models.OneToOneField(get_user_model(),
                                on_delete=CASCADE,
                                null=True,
                                blank=True,
                                related_name='pgp_identity')

    encrypters = models.ManyToManyField(
        'self',
        related_name='restorable_identities',
        symmetrical=False,
    )

    public_key_blob = models.TextField()
    private_key_blob = models.TextField()
    secret_blob = JSONField(blank=True, null=True)
    hash_info = models.CharField(max_length=256, null=True, blank=True)

    @cached_property
    def public_key(self) -> RSAKey:
        return RSAKey(self.public_key_blob)

    @cached_property
    def private_key(self) -> RSAKey:
        return RSAKey(self.private_key_blob)

    def get_secret(self, decrypter_uid: Identity) -> str:
        return get_secret(decrypter_uid, self.secret_blob)

    def set_secret(self, secret):
        encrypters = list(self.encrypters.all())
        encrypters.append(self)
        public_keys = [x.public_key for x in encrypters]
        result = encrypt(secret, public_keys)
        self.secret_blob = result

    @property
    def can_decrypt(self):
        return self.reset_requests.filter(secret_blob__isnull=False).exists() is False

    def protect(self, password):
        self.hash_info, password_hash = hash_password(password)
        protected_key = self.private_key.protect(password_hash)
        self.private_key_blob = protected_key.private_key_blob
        self.save()
        return password_hash

    def unlock(self, password):
        _, password_hash = hash_password(password, self.hash_info)
        priv = self.private_key
        priv.unlock(password_hash)

        return self.private_key.unlock(password_hash)

    def decrypt(self, encrypted_msg: EncryptedMessageBase, password=None):
        unlock_gen = self.unlock(password) if password else nullcontext()

        with unlock_gen:
            return encrypted_msg.decrypt(self)

    def change_password(self, old_password: str, new_password: str):
        with self.unlock(old_password):
            new_password_hash = self.protect(new_password)
            self.set_secret(new_password_hash)

            self.save()

    def reset_password(self, new_pwd):
        hash_info, new_secret = hash_password(new_pwd)
        public_keys = [e.public_key for e in self.encrypters.all()]

        new_secret_blob = encrypt(new_secret, public_keys)
        return RequestKeyRecovery.objects.create(uid=self, secret_blob=new_secret_blob, hash_info=hash_info)

    def add_restorers(self, password, encrypters: Union[QuerySet, List[Identity]]):
        encrypter_public_keys = [e.public_key for e in encrypters]
        with self.unlock(password):
            message = add_encrypters(self.secret_blob, self.private_key, encrypter_public_keys)
            self.secret_blob = message

            for e in encrypters:
                self.encrypters.add(e)
            self.save()


class EncryptedMessageBase(models.Model):
    class Meta:
        abstract = True

    objects = EncryptedMessageManager()

    text = JSONField(blank=True, null=True)

    encrypters = models.ManyToManyField(
        Identity,
        help_text='The user doing the impersonating.',
        related_name='encrypted_keys',
    )

    @property
    def encrypted_text(self):
        return self.text

    def can_decrypt(self, uid: Identity):
        return uid.id in [e.id for e in self.encrypters.all()]

    def encrypt(self, text, encrypters: Union[QuerySet, List[Identity]]):
        public_keys = [e.public_key for e in encrypters]
        encrypted = encrypt(text, public_keys)

        self.text = encrypted
        self.save()

        for e in encrypters:
            self.encrypters.add(e)

        return encrypted

    def decrypt(self, uid: Identity) -> str:
        if not uid.private_key.is_unlocked:
            raise ValueError('Cannot decrypt with a protected key')

        if not self.can_decrypt(uid):
            raise ValueError('This UID is not in the list of encrypters')

        return decrypt(self.encrypted_text, uid.private_key)

    def add_encrypters(self, uid, password, encrypters: Union[QuerySet, List[Identity]]):
        encrypter_public_keys = [e.public_key for e in encrypters]
        with uid.unlock(password):
            message = add_encrypters(self.encrypted_text, uid.private_key, encrypter_public_keys)
            self.text = message

            for e in encrypters:
                self.encrypters.add(e)
            self.save()
            return message

        return None

    def remove_encrypters(self, encrypters: Union[QuerySet, List[Identity]]):
        encrypted = self.encrypted_text
        encrypter_public_keys = encrypted['keys']
        pub_blobs_to_remove = [e.public_key_blob for e in encrypters]
        new_encrypter_public_keys = [pk for pk in encrypter_public_keys if pk not in pub_blobs_to_remove]
        encrypted['keys'] = new_encrypter_public_keys
        self.text = encrypted
        self.save()

        for e in encrypters:
            self.encrypters.remove(e)


class RequestKeyRecovery(models.Model):
    # pgp = PasswordResetManager()

    uid = models.ForeignKey(Identity,
                            on_delete=CASCADE,
                            related_name='reset_requests')

    reset_by = models.ForeignKey(Identity,
                                 on_delete=CASCADE,
                                 null=True,
                                 blank=True,
                                 related_name='password_reset_requests')

    secret_blob = JSONField(null=True, blank=True)
    hash_info = models.CharField(max_length=64, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def get_secret(self, uid: Identity):
        return get_secret(uid, self.secret_blob)

    def reset_password(self, reset_by: Identity, uid_password: str):
        with reset_by.unlock(uid_password):
            if self.uid.encrypters.filter(id=reset_by.id).exists():
                old_secret = self.uid.get_secret(reset_by)
                new_secret = self.get_secret(reset_by)

                with self.uid.private_key.unlock(old_secret):
                    self.uid.private_key.protect(new_secret)

                self.uid.private_key_blob = self.uid.private_key.private_key_blob
                self.uid.hash_info = self.hash_info
                self.uid.secret_blob = self.secret_blob

                self.uid.save()
                self.finished(reset_by)

    def finished(self, uid):
        self.reset_by = uid
        self.finished_at = timezone.now()
        self.secret_blob = None
        self.hash_info = None

        self.save()
