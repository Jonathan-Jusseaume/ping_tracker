from django.contrib import admin

# Register your models here.
from ping.models import MatchStatus


class MatchStatusAdmin(admin.ModelAdmin):
    exclude = ["id"]


admin.site.register(MatchStatus, MatchStatusAdmin)
