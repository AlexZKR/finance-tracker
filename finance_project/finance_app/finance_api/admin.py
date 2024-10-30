from django.contrib import admin
from finance_api.models import Transaction, Category, User, Account, Budget


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     pass


# Register your models here.
admin.site.register(Transaction)
admin.site.register(Category)
admin.site.register(Account)
admin.site.register(Budget)
