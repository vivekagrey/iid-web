from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

# Imports for charts in admin panel
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay


class MembershipInline(admin.TabularInline):
    model = Account.transactions.through


class AccountAdmin(UserAdmin):

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'first_name', 'last_name', 'phone', 'date_joined', 'is_admin', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name', 'phone', 'date_joined')
    readonly_fields = ('date_joined',)
    filter_horizontal = ('transactions',)
    list_filter = ('date_joined', 'is_admin',  'is_active')
    ordering = ('-date_joined',)
    exclude = ('username', 'groups', 'user_permissions', 'transactions')

    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'phone', 'password')}),
        ('Personal info', {'fields': ('dob', 'country', 'hq', 'date_joined', 'pro_pic')}),
        ('Permissions', {
            'classes': ('collapse',),
            'fields': ('is_admin', 'is_staff', 'is_active')}),
    )
    inlines = [
        MembershipInline,
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    # These fields will be displayed in user creation form in the admin panel
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'phone', 'password1', 'password2')}
         ),
    )


    def changelist_view(self, request, extra_context=None):
        # Aggregate new subscribers per day
        chart_data = (
            Account.objects.annotate(date=TruncDay("date_joined"))
                .values("date")
                .annotate(y=Count("id"))
                .order_by("-date")
        )

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)


admin.site.site_header = 'Indian Institute of Drones'
admin.site.register(Account, AccountAdmin)
admin.site.unregister(Group)

