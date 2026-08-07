from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Proposal, ProposalStatus, ProposalLineItem
from .forms import ProposalForm, ProposalLineItemForm

class ProposalListView(LoginRequiredMixin, ListView):
    model = Proposal
    template_name = 'proposals/proposal_list.html'
    context_object_name = 'proposals'
    paginate_by = 15

    def get_queryset(self):
        qs = super().get_queryset()
        # Filter by status
        status_slug = self.kwargs.get('status_slug')
        if status_slug:
            self.status = get_object_or_404(ProposalStatus, slug=status_slug)
            qs = qs.filter(status=self.status)
        else:
            self.status = None
        # Search
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(proposal_number__icontains=q) |
                Q(title__icontains=q) |
                Q(client__name__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = ProposalStatus.objects.filter(is_active=True)
        context['current_status'] = getattr(self, 'status', None)
        return context

class ProposalDetailView(LoginRequiredMixin, DetailView):
    model = Proposal
    template_name = 'proposals/proposal_detail.html'
    context_object_name = 'proposal'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['line_items'] = self.object.line_items.all().order_by('order')
        context['comments'] = self.object.comments.all().order_by('created_at')
        return context

class ProposalCreateView(LoginRequiredMixin, CreateView):
    model = Proposal
    form_class = ProposalForm
    template_name = 'proposals/proposal_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Proposal created successfully.")
        return super().form_valid(form)

class ProposalUpdateView(LoginRequiredMixin, UpdateView):
    model = Proposal
    form_class = ProposalForm
    template_name = 'proposals/proposal_form.html'

    def get_success_url(self):
        return reverse_lazy('proposals:detail', kwargs={'slug': self.object.slug})

class ProposalDeleteView(LoginRequiredMixin, DeleteView):
    model = Proposal
    template_name = 'proposals/proposal_confirm_delete.html'
    success_url = reverse_lazy('proposals:list')

@login_required
def add_line_item(request, pk):
    proposal = get_object_or_404(Proposal, pk=pk)
    if request.method == 'POST':
        form = ProposalLineItemForm(request.POST)
        if form.is_valid():
            line = form.save(commit=False)
            line.proposal = proposal
            line.save()
            # Update proposal totals
            proposal.subtotal = proposal.line_items.aggregate(models.Sum('total'))['total__sum'] or 0
            proposal.tax_amount = proposal.subtotal * (proposal.tax_rate / 100)
            proposal.total = proposal.subtotal + proposal.tax_amount - proposal.discount
            proposal.save()
            messages.success(request, "Line item added.")
            return redirect('proposals:detail', slug=proposal.slug)
    else:
        form = ProposalLineItemForm()
    return render(request, 'proposals/line_item_form.html', {'proposal': proposal, 'form': form})

@login_required
def delete_line_item(request, pk, line_id):
    proposal = get_object_or_404(Proposal, pk=pk)
    line = get_object_or_404(ProposalLineItem, pk=line_id, proposal=proposal)
    line.delete()
    # Recalculate totals
    proposal.subtotal = proposal.line_items.aggregate(models.Sum('total'))['total__sum'] or 0
    proposal.tax_amount = proposal.subtotal * (proposal.tax_rate / 100)
    proposal.total = proposal.subtotal + proposal.tax_amount - proposal.discount
    proposal.save()
    messages.success(request, "Line item removed.")
    return redirect('proposals:detail', slug=proposal.slug)
