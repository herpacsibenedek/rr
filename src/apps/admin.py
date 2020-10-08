from django.contrib import admin

from .models import (
    Auto,
    Partner,
    AutoPartnerConnection
)

admin.site.register(Auto)
admin.site.register(Partner)
admin.site.register(AutoPartnerConnection)
