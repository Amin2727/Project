# Generated by Django 4.0.4 on 2022-05-07 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='thumbmail',
            new_name='thumbnail',
        ),
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.CharField(choices=[('d', 'Draft'), ('p', 'Published')], max_length=1),
        ),
    ]
