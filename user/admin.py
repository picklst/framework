from django.contrib import admin
from user.models import User, UserSubscription, UserSession, UserInvite


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    pass


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    pass


@admin.register(UserInvite)
class UserInviteAdmin(admin.ModelAdmin):
    pass
