from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q



User = get_user_model()

class MultiFieldModelBackend(ModelBackend):
    '''
    authentication with username, email
    '''
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = None
        if username is None:
            # گاهی به جای username پارامتر دیگه‌ای توی kwargs هست (مثلاً وقتی از فرم خاصی اومده)
            username = kwargs.get(User.USERNAME_FIELD)

        try:
            user = User.objects.get(
                Q(username__iexact=username) |
                Q(email__iexact=username) 
            )
        except User.DoesNotExist:
            return None
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
