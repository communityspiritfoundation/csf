from rest_framework import serializers

from .models import User

class SignUpmodelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password']
        fields = ['first_name', 'last_name', 'email']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        print(self.validated_data, "data")
        user = User(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
        )
        # password = self.validated_data['password']
        # confirm_password = self.validated_data['confirm_password']

        # if password != confirm_password:
            # raise serializers.ValidationError({'password': 'The Password do not match.'})
        # user.set_password(password)
        user.save()
        return user