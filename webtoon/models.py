from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Webtoon(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    rating = models.FloatField()
    image = models.TextField()
    webtoon_url = models.TextField()
    genre = models.CharField(max_length=200)
    week = models.CharField(max_length=20)
    
    def __str__(self):
        return f'{self.pk}: {self.title} - {self.week}'
class User_Webtoon(models.Model):
    webtoon = models.ForeignKey(Webtoon, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField()
    review = models.TextField(null=True)
    
    class Meta:
        constraints = [models.UniqueConstraint(fields=['webtoon', 'reviewer'], name='unique_review')]
