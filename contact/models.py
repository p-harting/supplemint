from django.db import models


class ContactMessage(models.Model):
    # Model to store contact messages submitted by users.
    # Captures details such as name, email, subject, message, and timestamp.

    name = models.CharField(max_length=100)
    # The name of the person sending the message.
    email = models.EmailField()
    # The email address of the person sending the message.
    subject = models.CharField(max_length=200)
    # The subject of the contact message.
    message = models.TextField()
    # The content of the contact message.
    created_at = models.DateTimeField(auto_now_add=True)
    # The timestamp when the message was created

    def __str__(self):
        # Return the subject of the message as its string representation.
        return self.subject
