from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class ResumeAnalysis(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    resume_file = models.FileField(upload_to="resumes/")
    job_title = models.CharField(max_length=200)
    match_score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.job_title} - {self.match_score}"
