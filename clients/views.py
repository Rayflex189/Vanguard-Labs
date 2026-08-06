from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Client, ClientContact, ClientProject, ClientNote
from .forms import ClientForm, ClientContactForm, ClientProjectForm, ClientNoteForm

class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'clients/client_list.html'
    context_object_name = 'clients'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) |
                Q(primary_contact_email__icontains=q) |
                Q(industry__icontains=q)
            )
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Client.STATUS_CHOICES
        return context

class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'clients/client_detail.html'
    context_object_name = 'client'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = self.object.projects.all()
        context['contacts'] = self.object.contacts.all()
        context['notes'] = self.object.notes.all().order_by('-created_at')
        return context

class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('clients:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, f"Client '{form.instance.name}' created successfully.")
        return super().form_valid(form)

class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'

    def get_success_url(self):
        return reverse_lazy('clients:detail', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        messages.success(self.request, f"Client '{form.instance.name}' updated.")
        return super().form_valid(form)

class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'clients/client_confirm_delete.html'
    success_url = reverse_lazy('clients:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Client deleted successfully.")
        return super().delete(request, *args, **kwargs)

# --- Contact views ---
class ClientContactCreateView(LoginRequiredMixin, CreateView):
    model = ClientContact
    form_class = ClientContactForm
    template_name = 'clients/contact_form.html'

    def form_valid(self, form):
        client_slug = self.kwargs.get('slug')
        client = get_object_or_404(Client, slug=client_slug)
        form.instance.client = client
        messages.success(self.request, "Contact added successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('clients:detail', kwargs={'slug': self.kwargs['slug']})

class ClientContactUpdateView(LoginRequiredMixin, UpdateView):
    model = ClientContact
    form_class = ClientContactForm
    template_name = 'clients/contact_form.html'

    def get_success_url(self):
        return reverse_lazy('clients:detail', kwargs={'slug': self.object.client.slug})

class ClientContactDeleteView(LoginRequiredMixin, DeleteView):
    model = ClientContact
    template_name = 'clients/contact_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('clients:detail', kwargs={'slug': self.object.client.slug})

# --- Project views (client-specific) ---
class ClientProjectCreateView(LoginRequiredMixin, CreateView):
    model = ClientProject
    form_class = ClientProjectForm
    template_name = 'clients/project_form.html'

    def form_valid(self, form):
        client_slug = self.kwargs.get('slug')
        client = get_object_or_404(Client, slug=client_slug)
        form.instance.client = client
        messages.success(self.request, "Project added successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('clients:detail', kwargs={'slug': self.kwargs['slug']})

# Similarly you can add update/delete for projects and notes.
