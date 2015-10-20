from django.contrib.auth.models import User
from ldap3 import Server, Connection, ALL

class LDAP3AuthBackend:

    def authenticate(self, username=None, password=None):
        if '@' in username:
            servername = username.split('@')[1]
            s = Server(servername, get_info=ALL)
            c = Connection(s, user=username, password=password)
            if c.bind():
                try:
                    user = User.objects.get(username=username)
                    return user
                except User.DoesNotExist:
                    return None
        else:
            return None

    # Required for your backend to work properly - unchanged in most scenarios
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
