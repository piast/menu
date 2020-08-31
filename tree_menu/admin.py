from django.contrib import admin

from .models import Menu, MenuItem


admin.site.register(Menu)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'level', 'position')
    list_editable = ( 'parent', 'position',)
    list_filter = ('parent',)
    ordering = ['level', 'position']
    readonly_fields = ('level',)
