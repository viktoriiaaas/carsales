# Generated by Django 4.2 on 2024-12-19 20:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '__first__'),
        ('news', '0006_alter_newphoto_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newphoto',
            name='photo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cars.photo'),
        ),
    ]
