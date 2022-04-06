# Generated by Django 4.0.3 on 2022-03-30 12:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('autoservice', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='photo',
            field=models.ImageField(null=True, upload_to='covers', verbose_name='Photo'),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('p', 'Approved'), ('v', 'In Progress'), ('a', 'Done'), ('t', 'Canceled')], default='p', help_text='Status', max_length=1),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.CreateModel(
            name='Profilis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nuotrauka', models.ImageField(default='default.png', upload_to='profile_pics')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('comment', models.TextField(max_length=2000, verbose_name='Comment')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to='autoservice.order', verbose_name='Order')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
        ),
    ]
