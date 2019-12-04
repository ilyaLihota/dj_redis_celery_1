# Generated by Django 2.2.8 on 2019-12-04 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('languages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Framework',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('languages', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='frameworks', to='languages.Language')),
            ],
        ),
    ]
