# Generated by Django 5.0.7 on 2024-08-01 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_alter_blogpost_date_alter_blogpost_slug_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='img_url',
        ),
        migrations.RemoveField(
            model_name='user',
            name='profile_pic_url',
        ),
        migrations.AddField(
            model_name='blogpost',
            name='image',
            field=models.ImageField(null=True, upload_to='posts_pics'),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(null=True, upload_to='profile_pics'),
        ),
    ]
