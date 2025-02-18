from django.contrib import admin
from baseapp.models import ( 
    Breakfast 
)

class BreakfastAdmin(admin.ModelAdmin):
    list_display = (
        'slug',
        'image'
    )
    readonly_fields = ('slug',)

admin.site.register(Breakfast, BreakfastAdmin)