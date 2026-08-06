from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent! We\'ll get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'pages/contact.html', {'form': form})
