from django.contrib import admin

from .models import Project, Person, Report

admin.site.register(Project)
admin.site.register(Person)
admin.site.register(Report)