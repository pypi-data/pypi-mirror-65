from django.contrib import admin
from .models import ClientTrace, LoginTimes


class ClientTraceAdmin(admin.ModelAdmin):
    pass


class LoginTimesAdmin(admin.ModelAdmin):
    pass


admin.site.register(ClientTrace, ClientTraceAdmin)
admin.site.register(LoginTimes, LoginTimesAdmin)
