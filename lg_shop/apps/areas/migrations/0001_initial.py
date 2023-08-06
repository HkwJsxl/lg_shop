# Generated by Django 3.2.20 on 2023-08-06 21:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Areas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='区划名称')),
                ('pid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subs', to='areas.areas', verbose_name='父级id')),
            ],
            options={
                'verbose_name': '三级区域',
                'verbose_name_plural': '三级区域',
                'db_table': 'lg_areas',
            },
        ),
    ]
