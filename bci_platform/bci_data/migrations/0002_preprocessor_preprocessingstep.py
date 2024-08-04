# Generated by Django 5.0.7 on 2024-07-15 01:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bci_data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Preprocessor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PreprocessingStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('step_type', models.CharField(max_length=50)),
                ('parameters', models.JSONField()),
                ('preprocessor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='bci_data.preprocessor')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]