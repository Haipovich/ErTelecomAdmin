# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils.translation import gettext_lazy as _


class ApplicationStatus(models.TextChoices):
    PENDING = 'pending', _('Pending')
    UNDER_REVIEW = 'under_review', _('Under Review')
    INTERVIEW = 'interview', _('Interview')
    OFFER = 'offer', _('Offer')
    HIRED = 'hired', _('Hired')
    REJECTED = 'rejected', _('Rejected')
    WITHDRAWN = 'withdrawn', _('Withdrawn')


class JobType(models.TextChoices):
    INTERNSHIP = 'internship', _('Internship')
    VACANCY = 'vacancy', _('Vacancy')


class Activity(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    address = models.TextField(blank=True, null=True)
    target_audience = models.TextField(blank=True, null=True)
    is_active = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'activities'
        db_table_comment = 'Stores details about company events or activities'
        verbose_name_plural = "Activities"


class Application(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING)
    job = models.ForeignKey('Job', models.DO_NOTHING, blank=True, null=True)
    activity = models.ForeignKey(Activity, models.DO_NOTHING, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.PENDING,
        db_comment='Current status of the application'
    )
    hr_comment = models.TextField(blank=True, null=True)
    application_time = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'applications'
        db_table_comment = 'User applications for either jobs/internships OR activities'
        verbose_name_plural = "Applications"


class CompanyContact(models.Model):
    department = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'company_contacts'
        db_table_comment = 'General company contact information, possibly departmental'
        verbose_name_plural = "Company Contacts"


class Faq(models.Model):
    question = models.TextField()
    answer = models.TextField()
    display_order = models.IntegerField(db_comment='Order in which to display FAQs, lower numbers first')

    class Meta:
        managed = False
        db_table = 'faq'
        db_table_comment = 'Frequently Asked Questions and their answers'
        verbose_name_plural = "FAQ"


class HrContact(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255)
    phone = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'hr_contacts'
        db_table_comment = 'Contact information for HR personnel'
        verbose_name_plural = "HR Contacts"


class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(
        max_length=15,
        choices=JobType.choices
    )
    required_education = models.TextField(blank=True, null=True)
    required_experience = models.TextField(blank=True, null=True)
    required_skills = models.TextField(blank=True, null=True)
    additional_skills = models.TextField(blank=True, null=True)
    employment_type = models.CharField(max_length=100, blank=True, null=True)
    work_schedule = models.CharField(max_length=100, blank=True, null=True)
    workday_start = models.TimeField(blank=True, null=True)
    workday_end = models.TimeField(blank=True, null=True)
    salary = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    is_active = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'jobs'
        db_table_comment = 'Stores details about internships and job vacancies'
        verbose_name_plural = "Jobs"


class User(models.Model):
    id = models.BigIntegerField(primary_key=True, db_comment='Primary key, likely Telegram User ID')
    full_name = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    phone = models.CharField(unique=True, max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    work_experience = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    desired_salary = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    desired_employment = models.CharField(max_length=100, blank=True, null=True)
    relocation_readiness = models.BooleanField(blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)
    photo = models.BinaryField(blank=True, null=True, db_comment='Binary photo data. Consider storing a URL/path instead.')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'users'
        verbose_name_plural = "Users"


class ActivityReminder(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING)
    activity = models.ForeignKey('Activity', models.DO_NOTHING)
    reminder_type = models.CharField(max_length=10)
    sent_at = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'activity_reminders'
        unique_together = (('user', 'activity', 'reminder_type'),)
        verbose_name_plural = "Activity Reminders"
