from django.db import models

# Create your models here.
class Page(models.Model):
	title = models.CharField(unique=True, max_length=128)
	content = models.TextField()
	author = models.EmailField()
	update_date = models.DateTimeField(auto_now_add=True, blank=True)

