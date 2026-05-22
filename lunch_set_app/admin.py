from django.contrib import admin
from django import forms


from .models import (
    DishesType,
    Dish,
    LunchSet,
    ObjectForSetLunch
)

class DishInline(admin.TabularInline):
    model = Dish
    extra = 0
    exclude = ('slug',)

class ObjectForSetLunchInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ObjectForSetLunchInlineForm, self).__init__(*args, **kwargs)
        try:
            self.fields['dish'].queryset = Dish.objects.filter(dish_type__title=self.instance.dish_type.title)
        except:
            self.fields['dish'].queryset = Dish.objects.all()

class DishesForSetLunchInline(admin.TabularInline):
    form = ObjectForSetLunchInlineForm
    model = ObjectForSetLunch
    extra = 0

@admin.register(DishesType)
class DishesTypeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    inlines = [DishInline]

@admin.register(LunchSet)
class LunchSetAdmin(admin.ModelAdmin):
    list_display = ('date', 'comment')
    search_fields = ('date',)
    inlines = [DishesForSetLunchInline]
