# Generated by Django 2.1.8 on 2020-04-23 19:09

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='book',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='bookbigcategory',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='bookcategory',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='bookchaptercontent',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='bookchapters',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]