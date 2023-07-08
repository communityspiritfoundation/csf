from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User
from django.contrib.auth.password_validation import validate_password
from .serializers import RequestResetPasswordSerializer
from django.core.exceptions import ValidationError

@api_view(['PUT'])
def change_password(request):
    data = request.data
    # for some reason request.user doesn't work, it always returns an anonymous user
    # so instead pass the username in the request too
    try:
        user = User.objects.get(username=data["username"]) 
        try:
            validate_password(request.data["password"])
            user.set_password(request.data["password"])
            user.save()
            return Response("Success")
        except ValidationError as e:
            return Response(list(e)[0])
    except:
        return Response("Not logged in", 403)

@api_view(['POST'])
def request_reset_password(request):
    # try: user = User.objects.get(email=request.data["email"])
    # except: Response(status=404)
    # user.update(reset_token=uuid.uuid())

    print(request.user)

    serializer = RequestResetPasswordSerializer(request.data)
    serializer.is_valid(raise_exception=True)


    return Response("OK")


# resetToken
# newPassword