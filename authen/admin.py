from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import FoundationalModel, Student, StudentExtended, Teacher



class FoundationalUserAdmin(UserAdmin):
    model = FoundationalModel
    list_display = ('email', 'is_staff', 'is_active', 'type')
    
    fieldsets = (
        (None, {'fields': ('email', 'name','type', 'password')}),
        # ('Permissions', {'fields': 
            # ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions',)}),   #'is_customer' , 'is_seller'
    )
    ordering = ('email',)


class StudentExtendedInline(admin.StackedInline):
    model = StudentExtended
    can_delete = False
    verbose_name_plural = 'Student Extended'
    
    
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    inlines = (StudentExtendedInline,)

# admin.site.unregister(User)
admin.site.register(FoundationalModel, FoundationalUserAdmin)
# admin.site.register(Student)
admin.site.register(Teacher)
# Register your models here.
