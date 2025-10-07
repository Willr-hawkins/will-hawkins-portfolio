from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.http import JsonResponse
from .forms import ContactForm


def home(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        
        # Check if it's an AJAX request
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        if form.is_valid():
            # Save to database
            contact = form.save()
            
            # Prepare email content
            subject = f"New Portfolio Contact: {contact.full_name}"
            message_body = f"""
You have received a new contact form submission:

Name: {contact.full_name}
Email: {contact.email}
Phone: {contact.phone_number or 'Not provided'}

Message:
{contact.message}

Submitted at: {contact.created_at.strftime('%d/%m/%Y %H:%M')}
            """
            
            try:
                # Send email to yourself
                send_mail(
                    subject=subject,
                    message=message_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
                
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Thank you for your message! I will get back to you soon.'
                    })
                else:
                    messages.success(request, 'Thank you for your message! I will get back to you soon.')
                    return redirect('home')
                
            except BadHeaderError:
                if is_ajax:
                    return JsonResponse({
                        'success': False,
                        'message': 'Invalid header found. Please try again.'
                    })
                else:
                    messages.error(request, 'Invalid header found. Please try again.')
                    return redirect('home')
                    
            except Exception as e:
                if is_ajax:
                    return JsonResponse({
                        'success': False,
                        'message': 'There was an error sending your message. Please try again or email me directly.'
                    })
                else:
                    messages.error(request, 'There was an error sending your message. Please try again or email me directly.')
                    return redirect('home')
        else:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'message': 'Please correct the errors below.',
                    'errors': form.errors
                })
            else:
                messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'home/index.html', context)