from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
 
class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        ordering = ('title',)
