# Generated by Django 4.1.3 on 2023-01-07 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_alter_tag_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredient',
            name='unit',
            field=models.CharField(choices=[(0, 'GRAMM'), (1, 'MILLiLITR'), (2, 'DONA')], max_length=221),
        ),
    ]
