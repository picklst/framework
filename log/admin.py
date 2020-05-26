from django.contrib import admin
from .models import *


@admin.register(ListReport)
class ListReportAdmin(admin.ModelAdmin):
    pass


@admin.register(UserReport)
class ListReportAdmin(admin.ModelAdmin):
    pass


@admin.register(ListChangeLog)
class ListChangeLogAdmin(admin.ModelAdmin):
    pass


@admin.register(ItemChangeLog)
class ItemChangeLogAdmin(admin.ModelAdmin):
    pass
