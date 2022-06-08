from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from django.urls import reverse


USER = get_user_model()


class BaseModel(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True)
    active = models.BooleanField(default=True)
    slug = models.SlugField(null=False, blank=False, unique=True)
    created_by = models.ForeignKey(USER, null=False, blank=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MainTask(BaseModel):
    title = models.CharField(max_length=50, null=False, blank=False, unique=True)

    class Meta:
        ordering = ['title']
        verbose_name = "Maintask"
        verbose_name_plural = "Maintasks"
    
    def __str__(self) -> str:
        return self.title[:25]
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title) if not self.slug else self.slug
        super(MainTask, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('maintask-detail', kwargs={'slug': self.slug})


class SubTask(BaseModel):
    maintask = models.ForeignKey(MainTask, null=False, blank=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        ordering = ['maintask', 'title']
        constraints = [
            models.UniqueConstraint(fields=['maintask', 'title'], name='unique-task-constraint'),
        ]
        verbose_name = 'Subtask'
        verbose_name_plural = 'Subtasks'

    def __str__(self) -> str:
        return self.title[:25]
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.maintask.title, self.title) if not self.slug else self.slug
        super(SubTask, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('subtask-detail', kwargs={'slug': self.slug})