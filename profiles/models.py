from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    A user profile model for maintaining default delivery information
    and order history.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    referred_by = models.ForeignKey(User, on_delete=models.SET_NULL,
                                    null=True, blank=True,
                                    related_name='referred_profiles')
    full_name = models.CharField(max_length=50, default='')
    email = models.EmailField(default='')

    def save(self, *args, **kwargs):
        """Ensure email and full_name are always set
        based on the User model."""
        if not self.email:
            # Set email if not provided
            self.email = self.user.email
        if not self.full_name:
            # Set full_name if not provided
            self.full_name = self.user.username
        super().save(*args, **kwargs)

    # Address fields
    street_address1 = models.CharField(max_length=80, default='Main Street')
    street_address2 = models.CharField(max_length=80, blank=True, null=True)
    town_or_city = models.CharField(max_length=40, default='City')
    county = models.CharField(max_length=80, blank=True, null=True)
    postcode = models.CharField(max_length=20, default='00000')
    country = models.CharField(max_length=40, default='US')
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    # Points system for the user
    points = models.IntegerField(default=0)

    def __str__(self):
        # Return the username as the string representation of the profile
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile whenever a User instance is saved.
    This ensures every user has a corresponding UserProfile.
    """
    if created:
        # Create a new profile for the new user
        UserProfile.objects.create(user=instance)
    # Save the profile if it already exists
    instance.userprofile.save()
