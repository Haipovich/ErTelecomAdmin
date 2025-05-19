from django.contrib import admin
from .models import Activity, Application, CompanyContact, Faq, HrContact, Job, User, ActivityReminder

# Register your models here.

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'is_active', 'created_at')
    list_filter = ('is_active', 'start_time', 'created_at')
    search_fields = ('title', 'description')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_job_title', 'get_activity_title', 'status', 'application_time')
    list_filter = ('status', 'application_time', 'job__type')
    search_fields = ('user__full_name', 'user__email', 'job__title', 'activity__title', 'hr_comment')
    raw_id_fields = ('user', 'job', 'activity') # For better performance with many related objects

    def get_job_title(self, obj):
        return obj.job.title if obj.job else None
    get_job_title.short_description = 'Job Title'

    def get_activity_title(self, obj):
        return obj.activity.title if obj.activity else None
    get_activity_title.short_description = 'Activity Title'

@admin.register(CompanyContact)
class CompanyContactAdmin(admin.ModelAdmin):
    list_display = ('department', 'email', 'phone')
    search_fields = ('department', 'email', 'phone')

@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'display_order')
    list_filter = ('display_order',)
    search_fields = ('question', 'answer')
    ordering = ('display_order',)

@admin.register(HrContact)
class HrContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone')
    search_fields = ('full_name', 'email', 'phone')

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'is_active', 'created_at')
    list_filter = ('type', 'is_active', 'created_at')
    search_fields = ('title', 'description')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'phone', 'city', 'created_at')
    search_fields = ('full_name', 'email', 'phone', 'city')
    readonly_fields = ('id', 'created_at', 'updated_at') # Telegram ID and timestamps are usually not manually edited

@admin.register(ActivityReminder)
class ActivityReminderAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity', 'reminder_type', 'sent_at', 'created_at')
    list_filter = ('reminder_type', 'sent_at', 'created_at')
    search_fields = ('user__full_name', 'activity__title', 'reminder_type')
    raw_id_fields = ('user', 'activity')
    readonly_fields = ('created_at', 'updated_at')
