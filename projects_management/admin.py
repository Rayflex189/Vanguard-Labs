from django.contrib import admin
from django.utils.html import format_html
from .models import Project, Milestone, Task, TimeLog, Comment, ActivityLog

class MilestoneInline(admin.TabularInline):
    model = Milestone
    extra = 1
    fields = ('name', 'due_date', 'is_completed')

class TaskInline(admin.TabularInline):
    model = Task
    extra = 1
    fields = ('title', 'assigned_to', 'status', 'priority', 'due_date')
    show_change_link = True

class TimeLogInline(admin.TabularInline):
    model = TimeLog
    extra = 1
    fields = ('user', 'date', 'hours', 'description')

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    fields = ('user', 'content', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'status', 'priority', 'start_date', 'end_date')
    list_filter = ('status', 'priority', 'start_date', 'client')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic', {
            'fields': ('name', 'slug', 'description', 'client')
        }),
        ('Dates & Budget', {
            'fields': ('start_date', 'end_date', 'estimated_hours', 'budget', 'actual_cost')
        }),
        ('Status', {
            'fields': ('status', 'priority')
        }),
        ('Team', {
            'fields': ('project_manager', 'team_members')
        }),
        ('Portfolio Link', {
            'fields': ('portfolio_project',),
            'classes': ('collapse',)
        }),
    )
    inlines = [MilestoneInline, TaskInline, CommentInline]

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'assigned_to', 'status', 'priority', 'due_date')
    list_filter = ('status', 'priority', 'project')
    search_fields = ('title', 'description')
    inlines = [TimeLogInline, CommentInline]

@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'due_date', 'is_completed')

@admin.register(TimeLog)
class TimeLogAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'date', 'hours')
    list_filter = ('user', 'date')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'project', 'created_at')
    list_filter = ('user', 'created_at')

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'action', 'created_at')
    list_filter = ('user', 'created_at')
