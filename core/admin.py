from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUser
from django.contrib.contenttypes.admin import GenericTabularInline
from store.models import Product
from tags.models import TaggedItem
from store.admin import ProductAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUser):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2",'email','first_name','last_name'),
            },
        ),
    )

class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem
    extra = 0

class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]

admin.site.unregister(Product)
admin.site.register(Product,CustomProductAdmin)
