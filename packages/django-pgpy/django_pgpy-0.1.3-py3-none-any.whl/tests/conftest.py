import pytest
from django.contrib.auth.models import User

from django_pgpy.models import Identity
from test_app.models import EncryptedMessage


class UserTestData:

    def __init__(self):
        self.pwd_user_1 = 'pwd_user_1'
        self.pwd_user_2 = 'pwd_user_2'
        self.pwd_user_4 = 'pwd_user_4'
        self.user_1 = User.objects.create(username='user1')
        self.user_2 = User.objects.create(username='user2')
        self.user_4 = User.objects.create(username='user4')

        self.user_1.set_password(self.pwd_user_1)
        self.user_1.save()
        self.user_2.set_password(self.pwd_user_2)
        self.user_2.save()
        self.user_4.set_password(self.pwd_user_4)
        self.user_4.save()

class UserIdentityTestData(UserTestData):

    def __init__(self):
        super().__init__()

        self.uid_1 = Identity.objects.create(self.user_1, self.pwd_user_1)
        self.uid_2 = Identity.objects.create(self.user_2, self.pwd_user_2, [self.uid_1])
        self.uid_4 = Identity.objects.create(self.user_4, self.pwd_user_4)


class EncryptedMessageTestData(UserIdentityTestData):

    def __init__(self):
        super().__init__()

        self.text_1 = 'aaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbcccccccccccccccccc'
        self.text_1_encrypters = [self.uid_1]
        self.enc_text_1 = EncryptedMessage.objects.create(text=self.text_1,
                                                          encrypters=self.text_1_encrypters)

        self.text_2 = 'dddddddddddddddddddeeeeeeeeeeeeeeeeeeeeeeeeeffffffffffff'
        self.text_2_encrypters = [self.uid_2]
        self.enc_text_2 = EncryptedMessage.objects.create(text=self.text_2,
                                                          encrypters=self.text_2_encrypters)

        self.text_3 = 'dddddddddddddddddddeeeeeeeeeeeeeeeeeeeeeeeeeffffffffffff'
        self.text_3_encrypters = [self.uid_1, self.uid_2]
        self.enc_text_3 = EncryptedMessage.objects.create(text=self.text_3,
                                                          encrypters=self.text_3_encrypters)


@pytest.fixture
def user_test_data(db):
    return UserTestData()


@pytest.fixture
def identity_test_data(db):
    return IdentityTestData()


@pytest.fixture
def user_identity_test_data(db):
    return UserIdentityTestData()


@pytest.fixture
def encrypted_message_test_data(db):
    return EncryptedMessageTestData()


@pytest.fixture
def add_remove_encrypter_test_data(encrypted_message_test_data):
    data = encrypted_message_test_data

    data.pwd_user_3 = 'pwd_user_3'
    data.user_3 = User.objects.create(username='user3')

    data.user_3.set_password(data.pwd_user_3)
    data.user_3.save()

    data.uid_3 = Identity.objects.create(data.user_3, data.pwd_user_3)

    return data
