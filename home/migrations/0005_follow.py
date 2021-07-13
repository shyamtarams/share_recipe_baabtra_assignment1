# Generated by Django 3.2 on 2021-07-11 03:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_post_access'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user who follows+', to='home.login')),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user who following+', to='home.login')),
            ],
        ),
    ]