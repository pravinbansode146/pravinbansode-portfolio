from django.db import models

class GalleryItem(models.Model):
    KIND_CHOICES = [("image", "Image"), ("video", "Video"), ("pdf", "PDF"), ("note", "Note")]
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    kind = models.CharField(max_length=12, choices=KIND_CHOICES, default="pdf")
    file = models.FileField(upload_to="gallery/")
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)
    cover_image = models.ImageField(upload_to='gallery/covers/', blank=True, null=True)
    def __str__(self): return self.title

class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=180, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.name} — {self.subject or 'Contact'}"
