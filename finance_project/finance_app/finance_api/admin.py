from django.contrib import admin
from finance_api.models import Transaction, UserCategory, User, Account


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     pass


# Register your models here.
admin.site.register(Account)
admin.site.register(User)
admin.site.register(Transaction)
admin.site.register(UserCategory)

