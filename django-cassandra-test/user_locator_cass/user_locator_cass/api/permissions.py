import jwt
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.serializers import jwt_decode_handler, jwt_get_username_from_payload

from user_locator_cass.api.models import AdminUser
from user_locator_cass.api.serializers import AdminUserSerializer


class IsAuthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        if hasattr(request, '_auth') :
            payload =  self._check_payload(request._auth)
            return self._check_user(payload=payload)
        return False
        #return request.user and request.user.is_authenticated

    def _check_payload(self, token):
        # Check payload valid (based off of JSONWebTokenAuthentication,
        # may want to refactor)
        try:
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            msg = 'Signature has expired.'
            raise ValidationError(msg)
        except jwt.DecodeError:
            msg = 'Error decoding signature.'
            raise ValidationError(msg)

        return payload

    def _check_user(self, payload):
        username = jwt_get_username_from_payload(payload)

        if not username:
            msg = 'Invalid payload.'
            raise ValidationError(msg)

        # Make sure user exists
        try:
            #should go to db and query .  session.execute(user)
            user = AdminUser.objects.filter(username=username)
        except AdminUser.DoesNotExist:
            msg = "User doesn't exist."
            raise ValidationError(msg)

        return user
