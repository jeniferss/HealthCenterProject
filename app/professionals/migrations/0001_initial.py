# Generated by Django 5.0.2 on 2024-03-04 23:11

import app.common.mixins
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('street', models.CharField(max_length=256, validators=[django.core.validators.RegexValidator(message='Field must be a minimum of a 2-letter string value with one space between each word.', regex="^[\\wà-ü']{2,}(\\s[\\wà-ü']{2,})*$")])),
                ('number', models.CharField(max_length=8, validators=[django.core.validators.RegexValidator(message='Field must either be a numeric value with a maximum of six digits or precisely match the "s/n" string.', regex='^(s\\/n|[1-9]\\d{1,6})$')])),
                ('neighborhood', models.CharField(max_length=256, validators=[django.core.validators.RegexValidator(message='Field must be a minimum of a 2-letter string value with one space between each word.', regex="^[\\wà-ü']{2,}(\\s[\\wà-ü']{2,})*$")])),
                ('zipcode', models.CharField(max_length=8, validators=[django.core.validators.RegexValidator(message='Field must be an 8-digit numeric value with non-repeating digits.', regex='^(\\d)(?!\x01+$)\\d{7}$')])),
                ('city', models.CharField(max_length=256, validators=[django.core.validators.RegexValidator(message='Field must be a minimum of a 2-letter string value with one space between each word.', regex="^[\\wà-ü']{2,}(\\s[\\wà-ü']{2,})*$")])),
                ('state', models.CharField(max_length=256, validators=[django.core.validators.RegexValidator(message='Field must be a minimum of a 2-letter string value with one space between each word.', regex="^[\\wà-ü']{2,}(\\s[\\wà-ü']{2,})*$")])),
                ('country', models.CharField(max_length=256, validators=[django.core.validators.RegexValidator(message='Field must be a minimum of a 2-letter string value with one space between each word.', regex="^[\\wà-ü']{2,}(\\s[\\wà-ü']{2,})*$")])),
            ],
            options={
                'db_table': 'tb_address',
            },
            bases=(models.Model, app.common.mixins.StripMixin),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('mobile_number', models.CharField(max_length=256, null=True, validators=[django.core.validators.RegexValidator(message="Field must contain only numeric digits, include the country and area codes, and for mobile numbers, it must include the digit '9'.", regex='^55\\d{2}9?\\d{4}\\d{4}$')])),
                ('comercial_number', models.CharField(max_length=256, null=True, validators=[django.core.validators.RegexValidator(message="Field must contain only numeric digits, include the country and area codes, and for mobile numbers, it must include the digit '9'.", regex='^55\\d{2}9?\\d{4}\\d{4}$')])),
                ('email', models.CharField(max_length=256, null=True, validators=[django.core.validators.RegexValidator(message='Field must begin with a letter, disallowing spaces or commas. After the @ symbol, only two consecutive periods, each followed by a word, are permitted.', regex='^([a-z])([\\w.-]+)@([a-z]+\\.[a-z]+){1,2}$')])),
            ],
            options={
                'db_table': 'tb_contact',
            },
            bases=(models.Model, app.common.mixins.StripMixin),
        ),
        migrations.CreateModel(
            name='Occupation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=256, null=True, validators=[django.core.validators.RegexValidator(message='Field must be a minimum of a 2-letter string value with one space between each word.', regex="^[\\wà-ü']{2,}(\\s[\\wà-ü']{2,})*$")])),
            ],
            options={
                'db_table': 'tb_occupation',
            },
            bases=(models.Model, app.common.mixins.StripMixin),
        ),
        migrations.CreateModel(
            name='Professional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('social_name', models.CharField(max_length=256, null=True, validators=[django.core.validators.RegexValidator(message='Field must be a minimum of a 2-letter string value with one space between each word.', regex="^[\\wà-ü']{2,}(\\s[\\wà-ü']{2,})*$")])),
                ('full_name', models.CharField(max_length=256, validators=[django.core.validators.RegexValidator(message='Field must be a minimum of a 2-letter string value with one space between each word.', regex="^[\\wà-ü']{2,}(\\s[\\wà-ü']{2,})*$")])),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='professionals.address')),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='professionals.contact')),
                ('occupation', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='professionals.occupation')),
            ],
            options={
                'db_table': 'tb_professional',
                'unique_together': {('full_name', 'occupation', 'address', 'contact')},
            },
            bases=(models.Model, app.common.mixins.StripMixin),
        ),
    ]
