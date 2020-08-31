# Generated by Django 3.1 on 2020-08-31 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tree_menu', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menu',
            old_name='m_named_url',
            new_name='named_url',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='name',
        ),
        migrations.AddField(
            model_name='menu',
            name='title',
            field=models.CharField(default='d', max_length=20, verbose_name='Menu title'),
            preserve_default=False,
        ),
    ]
