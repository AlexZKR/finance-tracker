# Generated by Django 5.1.2 on 2024-11-04 20:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance_api', '0006_remove_usercategory_unique_category_for_user_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='usercategory',
            name='unique category for user',
        ),
        migrations.AlterUniqueTogether(
            name='categorybudget',
            unique_together=set(),
        ),
    ]
