# Generated by Django 5.0.6 on 2024-07-01 11:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_alter_category_options_alter_newsmodel_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='FIO')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('message', models.TextField(verbose_name='Matn')),
            ],
        ),
        migrations.AlterField(
            model_name='newsmodel',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='news_cat', to='news.category', verbose_name='Kategoriya'),
        ),
    ]