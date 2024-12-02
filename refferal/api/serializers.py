from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'user_invite_code', 'activate_invite_code']



class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11, min_length=11)

    def validate_phone_number(self, phone_number):
        if not phone_number:
            raise serializers.ValidationError("Номер телефона не может быть пустым.")
        if len(phone_number) != 11:
            raise serializers.ValidationError("Номер телефона должен содержать 11 цифр.")
        if phone_number[0] not in ('7', '8'):
            raise serializers.ValidationError("Номер телефона должен начинаться с 7 или 8.")

        return phone_number

