from django.db import models
from django.contrib.auth.models import User
# from django.core.urlresolvers import reverse
from django.utils import timezone



class Todo(models.Model):
    description = models.CharField(max_length=128, default='')
    content= models.TextField(max_length=500, default='')
    medium = (
        ('easy', 'Easy'),
        ('moderate', 'moderate'),
        ('complex', 'complex'),
        )
    tesk_medium = models.CharField(max_length=13, choices=medium, default=True)
    mark_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    finished_at = models.DateTimeField(null=True)
    is_finished = models.BooleanField(default=False)
    creator = models.ForeignKey(User, null=True, related_name='todos', on_delete=models.CASCADE)
    answered_by = models.ForeignKey(User, null=True, related_name='answerd', on_delete=models.CASCADE)


    # def get_absolute_url(self):
    #     return reverse("lists:index")

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.description

    def close(self):
        self.is_finished = True
        self.finished_at = timezone.now()
        self.save()

    def reopen(self):
        self.is_finished = False
        self.finished_at = None
        self.save()
