import pytest

from django_pgpy.models import Identity, RequestKeyRecovery
from django_pgpy.forms import PasswordChangeForUsersWithIdentityForm, PasswordResetForUsersWithIdentityForm


@pytest.mark.django_db
class TestPasswordChangeForUsersWithIdentityForm:
    def test_save(self, rf, user_identity_test_data):
        test_data = user_identity_test_data

        form = PasswordChangeForUsersWithIdentityForm(user=test_data.user_1, data={
            'old_password': test_data.pwd_user_1,
            'new_password1': '1234567890',
            'new_password2': '1234567890'
        })
        form.full_clean()
        form.save()

        uid: Identity = test_data.user_1.pgp_identity
        assert uid.private_key.is_protected

        with uid.unlock('1234567890'):
            assert uid.private_key.is_unlocked


@pytest.mark.django_db
class TestPasswordResetForUsersWithIdentityForm:
    def test_save(self, rf, user_identity_test_data):
        test_data = user_identity_test_data

        form = PasswordResetForUsersWithIdentityForm(user=test_data.user_1, data={
            'new_password1': '1234567890',
            'new_password2': '1234567890'
        })
        form.full_clean()
        form.save()

        uid: Identity = test_data.user_1.pgp_identity
        assert uid.private_key.is_protected

        with uid.unlock(test_data.pwd_user_1):
            assert uid.private_key.is_unlocked

        recovery_request = RequestKeyRecovery.objects.get(uid=test_data.user_1.pgp_identity)
        assert recovery_request.secret_blob is not None
        assert recovery_request.hash_info is not None
        assert recovery_request.reset_by is None
