from django.contrib.admin.forms import AdminPasswordChangeForm
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm


class PasswordChangeFormMixin:
    def save(self, commit=True):
        old_password = self.cleaned_data["old_password"]
        new_password = self.cleaned_data["new_password1"]
        if self.user.pgp_identity:
            self.user.pgp_identity.change_password(old_password, new_password)
        super().save(commit)


class PasswordResetFormMixin:
    def save(self, commit=True):
        new_password = self.cleaned_data["new_password1"]
        if self.user.pgp_identity:
            self.user.pgp_identity.reset_password(new_password)
        super().save(commit)


class PasswordChangeForUsersWithIdentityForm(PasswordChangeFormMixin, PasswordChangeForm):
    pass


class AdminPasswordChangeForUsersWithIdentityForm(PasswordChangeFormMixin, AdminPasswordChangeForm):
    pass


class PasswordResetForUsersWithIdentityForm(PasswordResetFormMixin, SetPasswordForm):
    pass
