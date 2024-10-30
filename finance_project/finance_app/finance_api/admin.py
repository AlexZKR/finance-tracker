from django.contrib import admin
from finance_api.models import Transaction, Category

# Register your models here.
admin.site.register(Transaction)
admin.site.register(Category)
