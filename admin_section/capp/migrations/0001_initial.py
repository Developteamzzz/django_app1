# Generated by Django 5.0.3 on 2024-03-19 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='register',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regno', models.CharField(max_length=100)),
                ('image', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('name', models.CharField(max_length=100)),
                ('gname', models.CharField(max_length=100)),
                ('dob', models.DateField()),
                ('age', models.IntegerField()),
                ('category', models.CharField(max_length=100)),
                ('maritalstatus', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=100)),
                ('qualification', models.CharField(max_length=100)),
                ('contactno', models.IntegerField()),
                ('gcontactno', models.IntegerField()),
                ('whatsapp', models.IntegerField()),
                ('email', models.CharField(max_length=100)),
                ('occupation', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('post', models.CharField(max_length=100)),
                ('pin', models.IntegerField()),
                ('course', models.CharField(max_length=100)),
                ('duration', models.CharField(max_length=100)),
                ('dateofjoin', models.DateField()),
                ('batch', models.CharField(max_length=100)),
                ('coursemode', models.CharField(max_length=100)),
            ],
        ),
    ]
