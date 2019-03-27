import jwt
from django.contrib.auth import get_user_model
from rest_framework_jwt.authentication import jwt_decode_handler, jwt_get_username_from_payload, \
    JSONWebTokenAuthentication
from rest_framework import  exceptions

class UseAdminJSONWebTokenAuthentication(JSONWebTokenAuthentication):

    def authenticate(self, request):
        from user_locator_cass.api.models import AdminUser

        """
        Returns a two-tuple of `User` and token if a valid signature has been
        supplied using JWT-based authentication.  Otherwise returns `None`.
        """
        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            return None

        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            msg = 'Signature has expired.'
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = 'Error decoding signature.'
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()

        user = self.authenticate_credentials(payload)

        return (user, jwt_value)


    def authenticate_credentials(self, payload):
        from user_locator_cass.api.models import AdminUser

        """
        Returns an active user that matches the payload's user id and email.
        """

        """ should try with """
        #admin_user = self.get_model('AdminUser')
        #user = admin_user.objects.all() or user = admin_user.objects.filter(username=username) on line 51
        admin_user = AdminUser
        username = jwt_get_username_from_payload(payload)

        if not username:
            msg = 'Invalid payload.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            #users = AdminUser.objects.all()
            admin_user = AdminUser.objects.filter(username=username)
        except AdminUser.DoesNotExist:
            msg = 'Invalid signature.'
            raise exceptions.AuthenticationFailed(msg)

        # print('*** user : ' + admin_user.is_active + " acitve")
        # if not admin_user.is_active:
        #     msg = 'User account is disabled.'
        #     raise jwt.exceptions.AuthenticationFailed(msg)

        return admin_user
