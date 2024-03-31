# Generated by Django 5.0.2 on 2024-03-19 05:02

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Etsy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('contact', models.CharField(blank=True, max_length=50, null=True)),
                ('role_id', models.IntegerField(blank=True, null=True)),
                ('custom_user_role', models.IntegerField(blank=True, choices=[(1, 'Customer'), (2, 'Supplier'), (5, 'Store'), (7, 'Admin')], null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('status', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('fcm_token', models.CharField(blank=True, max_length=250, null=True, verbose_name='FCM Token')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_by_user', to='Etsy.customuser')),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deleted_by_user', to='Etsy.customuser')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updated_by_user', to='Etsy.customuser')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True, validators=[django.core.validators.RegexValidator(message='Please enter valid Email address.', regex='([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\\.[A-Z|a-z]{2,})+')])),
                ('first_name', models.CharField(blank=True, max_length=50, null=True, validators=[django.core.validators.RegexValidator(message="Some special characters like (~!#^`'$|{}<>*) are not allowed.", regex='^[a-zA-Z]+(?:\\s[a-zA-Z]+)*$')])),
                ('last_name', models.CharField(blank=True, max_length=50, null=True, validators=[django.core.validators.RegexValidator(message="Some special characters like (~!#^`'$|{}<>*) are not allowed.", regex='^[a-zA-Z]+(?:\\s[a-zA-Z]+)*$')])),
                ('phone_number', models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator(message='Enter a valid 10-digit mobile number +91 9999999999', regex='^(\\+\\d{1,3})?\\d{10}$')])),
                ('password', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Etsy.customuser')),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True, validators=[django.core.validators.RegexValidator(message='Please enter valid Email address.', regex='([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\\.[A-Z|a-z]{2,})+')])),
                ('first_name', models.CharField(blank=True, max_length=50, null=True, validators=[django.core.validators.RegexValidator(message="Some special characters like (~!#^`'$|{}<>*) are not allowed.", regex='^[a-zA-Z]+(?:\\s[a-zA-Z]+)*$')])),
                ('last_name', models.CharField(blank=True, max_length=50, null=True, validators=[django.core.validators.RegexValidator(message="Some special characters like (~!#^`'$|{}<>*) are not allowed.", regex='^[a-zA-Z]+(?:\\s[a-zA-Z]+)*$')])),
                ('phone_number', models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator(message='Enter a valid 10-digit mobile number +91 9999999999', regex='^(\\+\\d{1,3})?\\d{10}$')])),
                ('password', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Etsy.customuser')),
            ],
        ),
    ]
