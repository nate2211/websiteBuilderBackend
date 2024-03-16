from django.contrib import admin
from .models import Layout, LayoutHeader, LayoutBody, LayoutFooter, LayoutComponent, LayoutText, LayoutSetting

# Direct inlines for LayoutHeader, LayoutBody, and LayoutFooter
class LayoutHeaderInline(admin.TabularInline):
    model = LayoutHeader
    extra = 1
    show_change_link = True

class LayoutBodyInline(admin.TabularInline):
    model = LayoutBody
    extra = 1
    show_change_link = True

class LayoutFooterInline(admin.TabularInline):
    model = LayoutFooter
    extra = 1
    show_change_link = True

class LayoutAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [LayoutHeaderInline, LayoutBodyInline, LayoutFooterInline]

admin.site.register(Layout, LayoutAdmin)

class LayoutTextInline(admin.TabularInline):
    model = LayoutText
    extra = 1  # Specifies the number of extra forms the formset should display.

class LayoutSettingInline(admin.TabularInline):
    model = LayoutSetting
    extra = 1
class AccountImageInline(admin.TabularInline):
    model = LayoutComponent.images.through
    verbose_name = "Image"
    verbose_name_plural = "Images"
    extra = 1  # Adjust as needed

class LayoutComponentAdmin(admin.ModelAdmin):
    list_display = ['component']
    inlines = [LayoutTextInline, LayoutSettingInline, AccountImageInline]
# Assuming you want to manage components separately
admin.site.register(LayoutComponent, LayoutComponentAdmin)
