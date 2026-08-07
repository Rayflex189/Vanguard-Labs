from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q, Count, Sum, Avg
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Lead, Opportunity, Interaction, Task, Note
from .forms import LeadForm, InteractionForm, TaskForm, NoteForm, OpportunityForm

@login_required
def crm_dashboard(request):
    """Simple CRM dashboard with stats."""
    context = {
        'total_leads': Lead.objects.count(),
        'new_leads': Lead.objects.filter(status='new').count(),
        'won_leads': Lead.objects.filter(status='won').count(),
        'lost_leads': Lead.objects.filter(status='lost').count(),
        'my_tasks': Task.objects.filter(assigned_to=request.user, completed=False).count(),
        'recent_interactions': Interaction.objects.filter(user=request.user).order_by('-date')[:5],
        'opportunities_by_stage': Opportunity.objects.values('stage').annotate(count=Count('id')),
        'lead_status_counts': Lead.objects.values('status').annotate(count=Count('id')),
    }
    return render(request, 'crm/dashboard.html', context)

class LeadListView(LoginRequiredMixin, ListView):
    model = Lead
    template_name = 'crm/lead_list.html'
    context_object_name = 'leads'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)
        # Search
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q) |
                Q(email__icontains=q) |
                Q(company__icontains=q) |
                Q(phone__icontains=q)
            )
        # Assigned to me
        if self.request.GET.get('assigned_to_me'):
            qs = qs.filter(assigned_to=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Lead.STATUS_CHOICES
        context['status_counts'] = Lead.objects.values('status').annotate(count=Count('id'))
        return context

class LeadDetailView(LoginRequiredMixin, DetailView):
    model = Lead
    template_name = 'crm/lead_detail.html'
    context_object_name = 'lead'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['interactions'] = self.object.interactions.all().order_by('-date')[:10]
        context['tasks'] = self.object.tasks.all().order_by('due_date')
        context['notes'] = self.object.notes.all().order_by('-created_at')
        context['opportunities'] = self.object.opportunities.all()
        return context

class LeadCreateView(LoginRequiredMixin, CreateView):
    model = Lead
    form_class = LeadForm
    template_name = 'crm/lead_form.html'
    success_url = reverse_lazy('crm:lead_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Lead created successfully.")
        return super().form_valid(form)

class LeadUpdateView(LoginRequiredMixin, UpdateView):
    model = Lead
    form_class = LeadForm
    template_name = 'crm/lead_form.html'

    def get_success_url(self):
        return reverse_lazy('crm:lead_detail', kwargs={'pk': self.object.pk})

class LeadDeleteView(LoginRequiredMixin, DeleteView):
    model = Lead
    template_name = 'crm/lead_confirm_delete.html'
    success_url = reverse_lazy('crm:lead_list')

class LeadConvertView(LoginRequiredMixin, UpdateView):
    model = Lead
    template_name = 'crm/lead_convert.html'
    fields = []  # We'll handle logic manually

    def post(self, request, *args, **kwargs):
        lead = self.get_object()
        if lead.status == 'won':
            client = lead.convert_to_client()
            if client:
                messages.success(request, f"Lead converted to client: {client.name}")
            else:
                messages.error(request, "Lead must be 'won' before conversion.")
        else:
            messages.error(request, "Lead status must be 'won' to convert.")
        return redirect('crm:lead_detail', pk=lead.pk)

# Similar views for Opportunity, Task, Interaction, Note...
# For brevity, we'll include a few sample:

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'crm/task_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        # If lead_id in URL, associate
        lead_id = self.kwargs.get('lead_id')
        if lead_id:
            form.instance.lead = get_object_or_404(Lead, pk=lead_id)
        messages.success(self.request, "Task created.")
        return super().form_valid(form)

    def get_success_url(self):
        if self.object.lead:
            return reverse_lazy('crm:lead_detail', kwargs={'pk': self.object.lead.pk})
        return reverse_lazy('crm:task_list')

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'crm/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.GET.get('mine'):
            qs = qs.filter(assigned_to=self.request.user)
        if self.request.GET.get('incomplete'):
            qs = qs.filter(completed=False)
        return qs
