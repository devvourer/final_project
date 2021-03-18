from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from rest_framework import decorators, response, status, generics, permissions
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import *
from .token import account_activation_token
from main import settings

class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if request.method == 'POST':
            if not serializer.is_valid():
                return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save()
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            to_email = user.email
            message = render_to_string('confirmation.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })
            msg = EmailMultiAlternatives(mail_subject, 'Follow this link', settings.EMAIL_HOST_USER, [to_email])
            msg.attach_alternative(message, 'text/html')
            msg.send()
        return response.Response('Email was send for confirmation', status.HTTP_201_CREATED)


@decorators.api_view(['POST', 'GET'])
@decorators.renderer_classes([JSONRenderer])
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # refresh = RefreshToken.for_user(user)
        # res = {
        #     'refresh': str(refresh),
        #     'access': str(refresh.access_token)
        # }

        return response.Response('Account has been activated!')
    else:
        return response.Response('invalid')


class UserEditView(generics.RetrieveUpdateAPIView):
    serializer_class = UserEditSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
