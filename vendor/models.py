from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification

# Create your models here.


class vendor(models.Model):
    user = models.OneToOneField(User, related_name="user", on_delete=models.CASCADE)
    user_profile = models.OneToOneField(
        UserProfile, related_name="user_profile", on_delete=models.CASCADE
    )
    vendor_name = models.CharField(max_length=200)
    vendor_license = models.ImageField(upload_to="vendor/license")
    is_approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # update
            previous_state = vendor.objects.get(pk=self.pk)
            if previous_state.is_approved != self.is_approved:
                mail_template = "accounts/emails/admin_approval_email.html"
                data = {"user": self.user, "is_approved": self.is_approved}
                if self.is_approved == True:
                    mail_subject = "Restaurant Approval"
                    send_notification(mail_subject, mail_template, data)
                else:
                    mail_subject = "Restaurant License uapproved"
                    send_notification(mail_subject, mail_template, data)
        return super(vendor, self).save(*args, **kwargs)
