import pytest

from django_pgpy.auth import ModelUserWithIdentityBackend, ModelUserWithIdentityAndSuperuserRestorersBackend
from django_pgpy.models import Identity

@pytest.mark.django_db
class TestModelUserWithIdentityBackend:
    def test_authenticate_encrypters(self, rf, user_test_data):
        test_data = user_test_data
        request = rf.get('/login')

        test_data.user_1.is_superuser = True
        test_data.user_1.save()
        martin = test_data.user_1

        user1 = test_data.user_2

        backend = ModelUserWithIdentityAndSuperuserRestorersBackend()

        assert Identity.objects.exists_for_user(martin) is False
        backend.authenticate(request, username=martin.username, password=test_data.pwd_user_1)
        assert Identity.objects.exists_for_user(martin)
        martin.refresh_from_db()
        uid_martin = Identity.objects.get(user=martin)
        assert uid_martin.encrypters.all().count() == 0

        assert Identity.objects.exists_for_user(user1) is False
        backend.authenticate(request, username=user1.username, password=test_data.pwd_user_2)
        assert Identity.objects.exists_for_user(user1)
        martin.refresh_from_db()
        uid_martin = Identity.objects.get(user=martin)
        uid_user1 = Identity.objects.get(user=user1)
        assert uid_martin.encrypters.all().count() == 0
        assert uid_user1.encrypters.all().count() == 1
        assert uid_martin in uid_user1.encrypters.all()

    def test_authenticate(self, rf, user_test_data):
        test_data = user_test_data
        request = rf.get('/login')

        backend = ModelUserWithIdentityBackend()

        assert Identity.objects.exists_for_user(test_data.user_1) is False
        backend.authenticate(request, username=test_data.user_1.username, password=test_data.pwd_user_1)

        assert Identity.objects.exists_for_user(test_data.user_1)

        uid: Identity = test_data.user_1.pgp_identity
        assert uid.private_key.is_protected

        with uid.unlock(test_data.pwd_user_1):
            assert uid.private_key.is_unlocked

    def test_authenticate__have_already_an_identity(self, rf, user_identity_test_data):
        test_data = user_identity_test_data
        request = rf.get('/login')

        backend = ModelUserWithIdentityBackend()

        assert Identity.objects.exists_for_user(test_data.user_1)
        assert Identity.objects.filter(user=test_data.user_1).count() == 1
        backend.authenticate(request, username=test_data.user_1.username, password=test_data.pwd_user_1)

        assert Identity.objects.exists_for_user(test_data.user_1)
        assert Identity.objects.filter(user=test_data.user_1).count() == 1

        uid: Identity = test_data.user_1.pgp_identity
        assert uid.private_key.is_protected

        with uid.unlock(test_data.pwd_user_1):
            assert uid.private_key.is_unlocked


    def test_authenticate_superuser_restorers(self, rf, user_test_data):
        test_data = user_test_data
        request = rf.get('/login')
        test_data.user_1.is_superuser = True
        test_data.user_1.save()

        backend = ModelUserWithIdentityAndSuperuserRestorersBackend()

        assert Identity.objects.exists_for_user(test_data.user_1) is False
        backend.authenticate(request, username=test_data.user_1.username, password=test_data.pwd_user_1)
        assert Identity.objects.exists_for_user(test_data.user_1)
        assert Identity.objects.get(user=test_data.user_1).encrypters.count() == 0


        assert Identity.objects.exists_for_user(test_data.user_2) is False
        backend.authenticate(request, username=test_data.user_2.username, password=test_data.pwd_user_2)

        assert Identity.objects.exists_for_user(test_data.user_2)
        assert Identity.objects.get(user=test_data.user_2).encrypters.count() == 1
        assert Identity.objects.get(user=test_data.user_1) in Identity.objects.get(user=test_data.user_2).encrypters.all()
        private_key = Identity.objects.get(user=test_data.user_2).private_key.private_key_blob

        test_data.user_4.is_superuser = True
        test_data.user_4.save()
        backend.authenticate(request, username=test_data.user_4.username, password=test_data.pwd_user_4)

        backend.authenticate(request, username=test_data.user_2.username, password=test_data.pwd_user_2)
        assert Identity.objects.get(user=test_data.user_2).encrypters.count() == 2
        assert Identity.objects.get(user=test_data.user_1) in Identity.objects.get(
            user=test_data.user_2).encrypters.all()
        assert Identity.objects.get(user=test_data.user_4) in Identity.objects.get(
            user=test_data.user_2).encrypters.all()
        assert private_key == Identity.objects.get(user=test_data.user_2).private_key.private_key_blob

        uid: Identity = test_data.user_1.pgp_identity
        assert uid.private_key.is_protected

        with uid.unlock(test_data.pwd_user_1):
            assert uid.private_key.is_unlocked

    def test_authenticate_superuser_restorers__have_already_an_identity(self, rf, user_identity_test_data):
        test_data = user_identity_test_data
        request = rf.get('/login')

        backend = ModelUserWithIdentityAndSuperuserRestorersBackend()

        assert Identity.objects.exists_for_user(test_data.user_1)
        assert Identity.objects.filter(user=test_data.user_1).count() == 1
        keyid = Identity.objects.get(user=test_data.user_1).private_key.private_key_blob
        backend.authenticate(request, username=test_data.user_1.username, password=test_data.pwd_user_1)

        assert Identity.objects.exists_for_user(test_data.user_1)
        assert Identity.objects.filter(user=test_data.user_1).count() == 1
        assert keyid == Identity.objects.get(user=test_data.user_1).private_key.private_key_blob

        uid: Identity = test_data.user_1.pgp_identity
        assert uid.private_key.is_protected

        with uid.unlock(test_data.pwd_user_1):
            assert uid.private_key.is_unlocked