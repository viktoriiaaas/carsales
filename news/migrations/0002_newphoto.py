# Generated by Django 4.2 on 2024-12-09 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '__first__'),
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='new_photos', to='news.new')),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cars.photo')),
            ],
        ),
    ]
