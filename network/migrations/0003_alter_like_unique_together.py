# Generated by Django 3.2.8 on 2022-01-15 20:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_follow_like_post'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('user', 'post')},
        ),
    ]
