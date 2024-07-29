from django.db import models
from django.contrib.auth import get_user_model

class ImageCaption(models.Model):
    image = models.ImageField(upload_to='images/')
    caption = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(get_user_model(), related_name='liked_images', blank=True)

    def like(self, user):
        if not self.likes.filter(pk=user.pk).exists():
            self.likes.add(user)
            self.save()

    def unlike(self, user):
        if self.likes.filter(pk=user.pk).exists():
            self.likes.remove(user)
            self.save()

    @property
    def count_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.caption
