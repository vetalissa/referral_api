
from django import forms


class PhoneNumberForm(forms.Form):
    phone_number = forms.CharField(max_length=11, min_length=11)

    def clean_phone_number(self):

        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number:
            raise forms.ValidationError("Номер телефона не может быть пустым.")
        if len(phone_number) != 11:
            raise forms.ValidationError("Номер телефона должен содержать 11 цифр.")
        if phone_number[0] not in ('7', '8'):
            raise forms.ValidationError("Номер телефона должен начинаться с 7 или 8.")

        return phone_number

class CodeForm(forms.Form):
    code = forms.CharField(max_length=4, min_length=4)

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if not code:
            raise forms.ValidationError("Для входа нужно ввести код.")
        if len(code) != 4:
            raise forms.ValidationError("Длина кода 4 цифры.")

        return code
