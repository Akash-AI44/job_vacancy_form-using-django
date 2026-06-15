from django.contrib import admin
from .models import Applicant
from django.utils.html import format_html


class Applicantadmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'submitted_at')
    search_fields = ('name', 'email')
    list_filter = ('submitted_at',)

    def download_cv(self, obj):
        if obj.cv:
            return format_html('<a href="{}" target="_blank">📄 View CV</a>', obj.cv.url)
        return "No CV"

    download_cv.short_description = 'CV'


admin.site.register(Applicant, Applicantadmin)
# Register your models here.
