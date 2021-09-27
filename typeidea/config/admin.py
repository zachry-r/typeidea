from django.contrib import admin
from .models import Link, SideBar
from typeidea.base_admin import BaseOwnerAdmin
from typeidea.custom_site import custom_site


# Register your models here.

@admin.register(SideBar, site=custom_site)
@admin.register(SideBar)
class SideBarAdmin(BaseOwnerAdmin):
    list_display = ('title', 'display_type', 'content', 'create_time')
    fields = ('title', 'display_type', 'content')

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(SideBarAdmin).save_model(request, obj, form, change)


@admin.register(Link, site=custom_site)
@admin.register(Link)
class LinkAdmin(BaseOwnerAdmin):
    list_display = ('title', 'href', 'status', 'weight', 'create_time')
    fields = ('title', 'href', 'status', 'weight')

    # def save_form(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(LinkAdmin).save_model(request, obj, form, change)
