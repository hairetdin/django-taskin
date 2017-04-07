from django.contrib import admin

from .models import (Person, Task, TaskStatus, Project, ProjectMember,
    TaskExecutor, TaskFile)


class TaskExecutorInline(admin.StackedInline):
    model = TaskExecutor
    extra = 0


class TaskAdmin(admin.ModelAdmin):
    inlines = [TaskExecutorInline]


class ProjectMemberInline(admin.TabularInline):
    model = ProjectMember
    extra = 0

class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectMemberInline]


admin.site.register(Task, TaskAdmin)
admin.site.register(TaskStatus)
admin.site.register(Person)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectMember)
admin.site.register(TaskExecutor)
admin.site.register(TaskFile)
