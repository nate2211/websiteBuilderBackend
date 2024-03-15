from django.contrib import admin

# Register your models here.
from accounts.models import Account, AccountImage, AccountLink, DigitalProduct, PhysicalProduct, AccountLayout


class AccountLayoutInline(admin.TabularInline):
    model = AccountLayout
    extra = 1
class DigitalProductInline(admin.TabularInline):
    model = DigitalProduct
    extra = 1

class PhysicalProductInline(admin.TabularInline):
    model = PhysicalProduct
    extra = 1

class AccountImageInline(admin.TabularInline):
    model = AccountImage
class AccountLinkInline(admin.TabularInline):
    model = AccountLink

class AccountAdmin(admin.ModelAdmin):
    inlines = [AccountImageInline, AccountLinkInline, DigitalProductInline, PhysicalProductInline, AccountLayoutInline]

admin.site.register(Account, AccountAdmin)