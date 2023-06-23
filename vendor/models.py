from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification
from datetime import time, date, datetime

# Create your models here.


class Vendor(models.Model):
    user = models.OneToOneField(User, related_name="user", on_delete=models.CASCADE)
    user_profile = models.OneToOneField(
        UserProfile, related_name="user_profile", on_delete=models.CASCADE
    )
    vendor_name = models.CharField(max_length=200)
    vendor_slug = models.SlugField(max_length=300, unique=True)
    vendor_license = models.ImageField(upload_to="vendor/license")
    is_approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name

    def is_open(self):
        today = date.today().isoweekday()
        current_opening_hour = OpeningHour.objects.filter(vendor=self, day=today)

        current_time = datetime.now().strftime("%H:%M:%S")
        is_open = None
        for data in current_opening_hour:
            if not data.is_closed:
                start = str(datetime.strptime(data.from_hour, "%I:%M %p").time())
                end = str(datetime.strptime(data.to_hour, "%I:%M %p").time())
                if current_time > start and current_time < end:
                    is_open = True
                else:
                    is_open = False
        return is_open

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # update
            previous_state = Vendor.objects.get(pk=self.pk)

            if previous_state.is_approved != self.is_approved:
                mail_template = "accounts/emails/admin_approval_email.html"
                data = {"user": self.user, "is_approved": self.is_approved}
                if self.is_approved == True:
                    mail_subject = "Restaurant Approval"
                    send_notification(mail_subject, mail_template, data)
                else:
                    mail_subject = "Restaurant License uapproved"
                    send_notification(mail_subject, mail_template, data)
        return super(Vendor, self).save(*args, **kwargs)


class OpeningHour(models.Model):
    Days = [
        (0, "Sunday"),
        (1, "Monday"),
        (2, "Tuesday"),
        (3, "Wednesday"),
        (4, "Thursday"),
        (5, "Friday"),
        (6, "Saturday"),
    ]

    HOURS_OF_DAYS = [
        ("12:00 AM", "12:00 AM"),
        ("12:15 AM", "12:15 AM"),
        ("12:30 AM", "12:30 AM"),
        ("12:45 AM", "12:45 AM"),
        ("01:00 AM", "01:00 AM"),
        ("01:15 AM", "01:15 AM"),
        ("01:30 AM", "01:30 AM"),
        ("01:45 AM", "01:45 AM"),
        ("02:00 AM", "02:00 AM"),
        ("02:15 AM", "02:15 AM"),
        ("02:30 AM", "02:30 AM"),
        ("02:45 AM", "02:45 AM"),
        ("03:00 AM", "03:00 AM"),
        ("03:15 AM", "03:15 AM"),
        ("03:30 AM", "03:30 AM"),
        ("03:45 AM", "03:45 AM"),
        ("04:00 AM", "04:00 AM"),
        ("04:15 AM", "04:15 AM"),
        ("04:30 AM", "04:30 AM"),
        ("04:45 AM", "04:45 AM"),
        ("05:00 AM", "05:00 AM"),
        ("05:15 AM", "05:15 AM"),
        ("05:30 AM", "05:30 AM"),
        ("05:45 AM", "05:45 AM"),
        ("06:00 AM", "06:00 AM"),
        ("06:15 AM", "06:15 AM"),
        ("06:30 AM", "06:30 AM"),
        ("06:45 AM", "06:45 AM"),
        ("07:00 AM", "07:00 AM"),
        ("07:15 AM", "07:15 AM"),
        ("07:30 AM", "07:30 AM"),
        ("07:45 AM", "07:45 AM"),
        ("08:00 AM", "08:00 AM"),
        ("08:15 AM", "08:15 AM"),
        ("08:30 AM", "08:30 AM"),
        ("08:45 AM", "08:45 AM"),
        ("09:00 AM", "09:00 AM"),
        ("09:15 AM", "09:15 AM"),
        ("09:30 AM", "09:30 AM"),
        ("09:45 AM", "09:45 AM"),
        ("10:00 AM", "10:00 AM"),
        ("10:15 AM", "10:15 AM"),
        ("10:30 AM", "10:30 AM"),
        ("10:45 AM", "10:45 AM"),
        ("11:00 AM", "11:00 AM"),
        ("11:15 AM", "11:15 AM"),
        ("11:30 AM", "11:30 AM"),
        ("11:45 AM", "11:45 AM"),
        ("12:00 PM", "12:00 PM"),
        ("12:15 PM", "12:15 PM"),
        ("12:30 PM", "12:30 PM"),
        ("12:45 PM", "12:45 PM"),
        ("01:00 PM", "01:00 PM"),
        ("01:15 PM", "01:15 PM"),
        ("01:30 PM", "01:30 PM"),
        ("01:45 PM", "01:45 PM"),
        ("02:00 PM", "02:00 PM"),
        ("02:15 PM", "02:15 PM"),
        ("02:30 PM", "02:30 PM"),
        ("02:45 PM", "02:45 PM"),
        ("03:00 PM", "03:00 PM"),
        ("03:15 PM", "03:15 PM"),
        ("03:30 PM", "03:30 PM"),
        ("03:45 PM", "03:45 PM"),
        ("04:00 PM", "04:00 PM"),
        ("04:15 PM", "04:15 PM"),
        ("04:30 PM", "04:30 PM"),
        ("04:45 PM", "04:45 PM"),
        ("05:00 PM", "05:00 PM"),
        ("05:15 PM", "05:15 PM"),
        ("05:30 PM", "05:30 PM"),
        ("05:45 PM", "05:45 PM"),
        ("06:00 PM", "06:00 PM"),
        ("06:15 PM", "06:15 PM"),
        ("06:30 PM", "06:30 PM"),
        ("06:45 PM", "06:45 PM"),
        ("07:00 PM", "07:00 PM"),
        ("07:15 PM", "07:15 PM"),
        ("07:30 PM", "07:30 PM"),
        ("07:45 PM", "07:45 PM"),
        ("08:00 PM", "08:00 PM"),
        ("08:15 PM", "08:15 PM"),
        ("08:30 PM", "08:30 PM"),
        ("08:45 PM", "08:45 PM"),
        ("09:00 PM", "09:00 PM"),
        ("09:15 PM", "09:15 PM"),
        ("09:30 PM", "09:30 PM"),
        ("09:45 PM", "09:45 PM"),
        ("10:00 PM", "10:00 PM"),
        ("10:15 PM", "10:15 PM"),
        ("10:30 PM", "10:30 PM"),
        ("10:45 PM", "10:45 PM"),
        ("11:00 PM", "11:00 PM"),
        ("11:15 PM", "11:15 PM"),
        ("11:30 PM", "11:30 PM"),
        ("11:45 PM", "11:45 PM"),
    ]

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    day = models.IntegerField(choices=Days)
    from_hour = models.CharField(
        choices=HOURS_OF_DAYS, max_length=50, blank=True, null=True
    )
    to_hour = models.CharField(
        choices=HOURS_OF_DAYS, max_length=50, blank=True, null=True
    )
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ("day", "from_hour")
        constraints = [
            models.UniqueConstraint(
                fields=["vendor", "day", "from_hour", "to_hour"], name="day_hour_unique"
            )
        ]

    def __str__(self):
        return self.get_day_display()
