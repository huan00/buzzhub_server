# Generated by Django 4.1.6 on 2023-02-27 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_post_userpicturepath'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='video',
            field=models.FileField(default='', upload_to='video/'),
        ),
    ]