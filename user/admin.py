from django.contrib import admin
from user.models import User, UserSubscription


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    pass
