from django.contrib import admin
from django.utils.html import format_html
from .models import (
    ProposalStatus, ProposalTemplate, Proposal,
    ProposalLineItem, ProposalComment
)

class ProposalLineItemInline(admin.TabularInline):
    model = ProposalLineItem
    extra = 1
    fields = ('service', 'description', 'quantity', 'unit_price', 'total')
    readonly_fields = ('total',)

class ProposalCommentInline(admin.TabularInline):
    model = ProposalComment
    extra = 1
    fields = ('user', 'content', 'is_internal')
    readonly_fields = ('created_at',)

@admin.register(ProposalStatus)
class ProposalStatusAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'color', 'order')

@admin.register(ProposalTemplate)
class ProposalTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name', 'content')

@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ('proposal_number', 'title', 'client', 'status', 'total', 'created_at')
    list_filter = ('status', 'created_at', 'client')
    search_fields = ('proposal_number', 'title', 'client__name')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic', {
            'fields': ('proposal_number', 'title', 'slug', 'client', 'project', 'status')
        }),
        ('Content', {
            'fields': ('content', 'executive_summary', 'terms', 'notes')
        }),
        ('Financial', {
            'fields': ('subtotal', 'tax_rate', 'tax_amount', 'discount', 'total', 'currency')
        }),
        ('Timeline', {
            'fields': ('sent_at', 'valid_until')
        }),
        ('Team', {
            'fields': ('created_by', 'assigned_to', 'team_members')
        }),
        ('Template', {
            'fields': ('template',),
            'classes': ('collapse',)
        }),
        ('Services', {
            'fields': ('services',),
            'classes': ('collapse',)
        }),
    )
    inlines = [ProposalLineItemInline, ProposalCommentInline]

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing
            return self.readonly_fields + ('total', 'subtotal', 'tax_amount')
        return self.readonly_fields
