from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.db import models
from .models import Proposal, ProposalLineItem

def update_proposal_totals(proposal):
    """
    Recalculate subtotal, tax, and total for a proposal.
    """
    # Sum line item totals
    subtotal = proposal.line_items.aggregate(
        total_sum=models.Sum('total')
    )['total_sum'] or 0
    proposal.subtotal = subtotal

    # Calculate tax
    tax_amount = subtotal * (proposal.tax_rate / 100)
    proposal.tax_amount = tax_amount

    # Calculate final total (subtotal + tax - discount)
    total = subtotal + tax_amount - proposal.discount
    proposal.total = total

    # Save without triggering signals again
    proposal.save(update_fields=['subtotal', 'tax_amount', 'total'])

# --- Signals for ProposalLineItem changes ---
@receiver(post_save, sender=ProposalLineItem)
def line_item_saved(sender, instance, created, **kwargs):
    """
    When a line item is created or updated, recalc proposal totals.
    """
    update_proposal_totals(instance.proposal)

@receiver(post_delete, sender=ProposalLineItem)
def line_item_deleted(sender, instance, **kwargs):
    """
    When a line item is deleted, recalc proposal totals.
    """
    update_proposal_totals(instance.proposal)

# --- Signal for Proposal tax/discount changes ---
@receiver(pre_save, sender=Proposal)
def proposal_pre_save(sender, instance, **kwargs):
    """
    Before saving a proposal, recalc totals if tax_rate or discount changed.
    This ensures totals are correct even when line items haven't changed.
    """
    # If we're creating a new proposal, skip (totals will be set by line items)
    if not instance.pk:
        return

    # Get the current instance from DB to compare
    try:
        old = Proposal.objects.get(pk=instance.pk)
    except Proposal.DoesNotExist:
        return

    # If tax_rate or discount changed, recalc from existing line items
    if old.tax_rate != instance.tax_rate or old.discount != instance.discount:
        # Fetch the current line items from DB (they are already saved)
        # We need to recalc using the new tax/discount values.
        # Since we haven't saved yet, we need to recalc from DB line items.
        # We'll temporarily set the new tax/discount, then use helper.
        # But the helper uses instance's current fields, so it's fine.
        update_proposal_totals(instance)
