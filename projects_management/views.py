from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q, Count, Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Project, Task, Milestone, TimeLog, Comment, ActivityLog
from .forms import ProjectForm, TaskForm, MilestoneForm, TimeLogForm, CommentForm

# --- Project Views ---

class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects_management/project_list.html'
    context_object_name = 'projects'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)
        # Search
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Project.STATUS_CHOICES
        return context

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects_management/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = self.object.tasks.all().order_by('due_date')
        context['milestones'] = self.object.milestones.all().order_by('due_date')
        context['comments'] = self.object.comments.all().order_by('-created_at')[:10]
        context['time_logs'] = TimeLog.objects.filter(task__project=self.object).order_by('-date')[:10]
        return context

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects_management/project_form.html'

    def form_valid(self, form):
        form.instance.project_manager = self.request.user
        messages.success(self.request, "Project created successfully.")
        return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects_management/project_form.html'

    def get_success_url(self):
        return reverse_lazy('projects_management:project_detail', kwargs={'slug': self.object.slug})

class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'projects_management/project_confirm_delete.html'
    success_url = reverse_lazy('projects_management:project_list')

# --- Task Views ---

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'projects_management/task_form.html'

    def form_valid(self, form):
        project_slug = self.kwargs.get('project_slug')
        project = get_object_or_404(Project, slug=project_slug)
        form.instance.project = project
        form.instance.created_by = self.request.user
        messages.success(self.request, "Task created successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('projects_management:project_detail', kwargs={'slug': self.kwargs['project_slug']})

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'projects_management/task_form.html'

    def get_success_url(self):
        return reverse_lazy('projects_management:project_detail', kwargs={'slug': self.object.project.slug})

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'projects_management/task_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('projects_management:project_detail', kwargs={'slug': self.object.project.slug})

# --- Dashboard (overview) ---

@login_required
def dashboard(request):
    """Show project stats for the current user."""
    user = request.user
    # Get projects where user is manager or team member
    projects = Project.objects.filter(
        Q(project_manager=user) | Q(team_members__user=user)
    ).distinct()
    context = {
        'total_projects': projects.count(),
        'active_projects': projects.filter(status='active').count(),
        'completed_projects': projects.filter(status='completed').count(),
        'total_tasks': Task.objects.filter(project__in=projects).count(),
        'completed_tasks': Task.objects.filter(project__in=projects, status='completed').count(),
        'recent_activities': ActivityLog.objects.filter(project__in=projects).order_by('-created_at')[:10],
        'projects': projects[:5],
    }
    return render(request, 'projects_management/dashboard.html', context)
