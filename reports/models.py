from django.db import models
from django.contrib.auth.models import User

class Report(models.Model):
    SPAM = 'spam'
    HARASSMENT = 'harassment'
    INAPPROPRIATE = 'inappropriate'
    OTHER = 'other'

    REPORT_CHOICES = [
        (SPAM, 'سبام'),
        (HARASSMENT, 'تحرش'),
        (INAPPROPRIATE, 'محتوى غير مناسب'),
        (OTHER, 'أخرى'),
    ]

    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_by', null=True, blank=True)
    reported_post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='reports', null=True, blank=True)
    reported_comment = models.ForeignKey('posts.Comment', on_delete=models.CASCADE, related_name='reports', null=True, blank=True)
    reason = models.CharField(max_length=20, choices=REPORT_CHOICES)
    description = models.TextField()
    status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'قيد المراجعة'),
        ('resolved', 'تم الحل'),
        ('dismissed', 'تم رفضه'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_reports')

    def clean(self):
        if not self.reported_user and not self.reported_post and not self.reported_comment:
            from django.core.exceptions import ValidationError
            raise ValidationError('A report must have at least one target (user, post, or comment).')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Report by {self.reporter.username} - {self.reason}"
