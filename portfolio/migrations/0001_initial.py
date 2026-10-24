from django.db import migrations, models
class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name="GalleryItem", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("title", models.CharField(max_length=180)),
            ("description", models.TextField(blank=True)),
            ("kind", models.CharField(choices=[("image","Image"),("video","Video"),("pdf","PDF"),("note","Note")], default="pdf", max_length=12)),
            ("file", models.FileField(upload_to="gallery/")),
            ("created_at", models.DateTimeField(auto_now_add=True)),
            ("is_public", models.BooleanField(default=True)),
        ]),
        migrations.CreateModel(name="ContactMessage", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("name", models.CharField(max_length=120)),
            ("email", models.EmailField(max_length=254)),
            ("subject", models.CharField(blank=True, max_length=180)),
            ("message", models.TextField()),
            ("created_at", models.DateTimeField(auto_now_add=True)),
        ])]
