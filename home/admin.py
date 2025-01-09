from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import path
from django.shortcuts import redirect
from .models import NewsletterSubscriber, NewsletterEmail, PageContent


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    """Admin configuration for NewsletterSubscriber model."""
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)
    list_filter = ('subscribed_at',)


@admin.register(NewsletterEmail)
class NewsletterEmailAdmin(admin.ModelAdmin):
    """Admin configuration for NewsletterEmail model."""
    list_display = ('subject', 'created_at')
    change_form_template = 'admin/newsletter_email_change_form.html'

    def get_urls(self):
        """Add custom URL for sending the newsletter."""
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:object_id>/send/',
                self.admin_site.admin_view(self.send_newsletter),
                name='home_newsletteremail_send_newsletter'),
        ]
        return custom_urls + urls

    def send_newsletter(self, request, object_id, *args, **kwargs):
        """Send the newsletter to all subscribers."""
        email = self.get_object(request, object_id)  # Get the email object
        subscribers = NewsletterSubscriber.objects.all()  # Get all subscribers
        for subscriber in subscribers:
            # Prepare HTML and plain text versions of the email
            html_message = render_to_string('emails/newsletter.html', {
                'content': email.content,
                'subject': email.subject
            })
            plain_message = strip_tags(html_message)
            # Send the email to each subscriber
            send_mail(
                email.subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [subscriber.email],
                html_message=html_message,
                fail_silently=False,
            )
        # Notify the admin that the email was sent successfully
        self.message_user(
            request, f"Newsletter '{email.subject}' sent successfully!")
        return redirect('..')


@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    """Admin configuration for PageContent model."""
    list_display = ('get_page_display', 'last_updated')
    list_filter = ('page',)
    search_fields = ('content',)
