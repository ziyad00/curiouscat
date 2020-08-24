from django.db import models

class QA(models.Model):
    question = models.TextField()
    answer = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    


    class Meta:
        ordering = ['-created']

 