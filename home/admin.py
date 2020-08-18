import sett as sett
from django.contrib import admin

# Register your models here.
from home.models import Setting,ContactF
from product.models import comment


class SettAdmin(admin.ModelAdmin):
    list_display = ['title','company','update_at', 'status']

class ContactFAdmin(admin.ModelAdmin):
    list_display = ['name','subject','update_at', 'status']
    readonly_fields =  ('name','subject','email', 'message','ip')
    list_filter = ['status']





admin.site.register(Setting, SettAdmin)

admin.site.register(ContactF, ContactFAdmin)