from django.contrib import admin
from baseapp.models import ( 
    Breakfast,
    Menu,
    BarMenu
)

class BreakfastAdmin(admin.ModelAdmin):
    list_display = (
        'slug',
        'image'
    )
    readonly_fields = ('slug',)

admin.site.register(Breakfast, BreakfastAdmin)

class MenuAdmin(admin.ModelAdmin):
    list_display = (
        'slug',
        'page1',
        'page2'
    )
    readonly_fields = ('slug',)

admin.site.register(Menu, MenuAdmin)

class BarMenuAdmin(admin.ModelAdmin):
    list_display = (
        'slug',
        'page1',
        'page2'
    )
    readonly_fields = ('slug',)

admin.site.register(BarMenu, BarMenuAdmin)