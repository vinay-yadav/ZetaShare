from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
        )


account_activation_token = AccountActivationTokenGenerator()


# subject = 'Welcome to the family'
# message = "We very much appreciated you business.\nWe will be in touch soon."
# from_email = settings.EMAIL_HOST_USER
# to_list = [obj.email, from_email]
# send_mail(subject, message, from_email, to_list, fail_silently=True)
# register_form = SignUpForm
