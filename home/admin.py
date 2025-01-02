from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import path
from django.shortcuts import redirect
from .models import NewsletterSubscriber, NewsletterEmail

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)
    list_filter = ('subscribed_at',)

@admin.register(NewsletterEmail)
class NewsletterEmailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'created_at')
    change_form_template = 'admin/newsletter_email_change_form.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/send/', self.admin_site.admin_view(self.send_newsletter), name='home_newsletteremail_send_newsletter'),
        ]
        return custom_urls + urls

    def send_newsletter(self, request, object_id, *args, **kwargs):
        email = self.get_object(request, object_id)
        subscribers = NewsletterSubscriber.objects.all()
        for subscriber in subscribers:
            html_message = render_to_string('emails/newsletter.html', {
                'content': email.content,
                'subject': email.subject
            })
            plain_message = strip_tags(html_message)
            send_mail(
                email.subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [subscriber.email],
                html_message=html_message,
                fail_silently=False,
            )
        self.message_user(request, f"Newsletter '{email.subject}' sent successfully!")
        return redirect('..')
