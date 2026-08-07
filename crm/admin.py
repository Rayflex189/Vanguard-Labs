from django.contrib import admin
from .models import Lead, Opportunity, Interaction, Task, Note

class InteractionInline(admin.TabularInline):
    model = Interaction
    extra = 1
    fields = ('interaction_type', 'subject', 'details', 'date', 'user')
    readonly_fields = ('date',)

class TaskInline(admin.TabularInline):
    model = Task
    extra = 1
    fields = ('title', 'assigned_to', 'due_date', 'completed')
    show_change_link = True

class NoteInline(admin.TabularInline):
    model = Note
    extra = 1
    fields = ('content', 'is_internal', 'user')
    readonly_fields = ('user',)

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'company', 'email', 'status', 'assigned_to', 'score', 'created_at')
    list_filter = ('status', 'source', 'assigned_to', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'company', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'company', 'job_title', 'website')
        }),
        ('Status & Scoring', {
            'fields': ('status', 'source', 'score', 'probability', 'expected_value')
        }),
        ('Assignment', {
            'fields': ('assigned_to', 'created_by')
        }),
        ('Client Conversion', {
            'fields': ('client',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'last_contacted')
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    inlines = [InteractionInline, TaskInline, NoteInline]

    def full_name(self, obj):
        return obj.get_full_name()
    full_name.short_description = 'Name'

@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'lead', 'client', 'stage', 'value', 'probability', 'expected_close_date')
    list_filter = ('stage', 'assigned_to')
    search_fields = ('name', 'lead__first_name', 'lead__last_name', 'client__name')

@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ('subject', 'interaction_type', 'lead', 'client', 'user', 'date')
    list_filter = ('interaction_type', 'user', 'date')
    search_fields = ('subject', 'details')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'lead', 'client', 'due_date', 'completed')
    list_filter = ('completed', 'assigned_to', 'due_date')
    search_fields = ('title', 'description')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'lead', 'client', 'is_internal', 'created_at')
    list_filter = ('is_internal', 'user', 'created_at')
    search_fields = ('content',)
