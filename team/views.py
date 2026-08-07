from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import TeamMember, TeamRole

class TeamListView(ListView):
    model = TeamMember
    template_name = 'team/team_list.html'
    context_object_name = 'members'
    paginate_by = 12

    def get_queryset(self):
        qs = super().get_queryset().filter(is_active=True)
        # Role filter
        role_slug = self.kwargs.get('role_slug')
        if role_slug:
            self.role = TeamRole.objects.get(slug=role_slug)
            qs = qs.filter(role=self.role)
        else:
            self.role = None
        # Search
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(bio__icontains=q) | Q(skills__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['roles'] = TeamRole.objects.all()
        context['current_role'] = getattr(self, 'role', None)
        return context

class TeamDetailView(DetailView):
    model = TeamMember
    template_name = 'team/team_detail.html'
    context_object_name = 'member'

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
