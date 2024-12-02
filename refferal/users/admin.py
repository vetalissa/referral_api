from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number',)
    fields = ('phone_number', 'user_invite_code', 'activate_invite_code', 'who_activate_my_code')
    readonly_fields = ('phone_number', 'user_invite_code', 'who_activate_my_code')

    def who_activate_my_code(self, obj):
        # Используем метод из модели для получения количества приглашенных пользователей
        return list(obj.get_who_activate_my_code())

    who_activate_my_code.short_description = 'кто активировал'  # Название для отображения в админке
