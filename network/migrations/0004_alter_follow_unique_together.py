# Generated by Django 3.2.8 on 2022-01-16 17:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_alter_like_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together={('follower', 'following')},
        ),
    ]