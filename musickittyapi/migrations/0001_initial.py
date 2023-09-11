# Generated by Django 4.2.5 on 2023-09-11 16:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('age', models.CharField(max_length=255)),
                ('sex', models.CharField(max_length=255)),
                ('bio', models.TextField()),
                ('image', models.CharField(max_length=255)),
                ('adopted', models.BooleanField()),
                ('gets_along_with_cats', models.BooleanField()),
                ('gets_along_with_dogs', models.BooleanField()),
                ('gets_along_with_children', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='CatFavorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorited_by_profiles', to='musickittyapi.cat')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=255)),
                ('opening_hours', models.CharField(max_length=255)),
                ('closing_hours', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('image', models.CharField(blank=True, max_length=255)),
                ('bio', models.CharField(blank=True, max_length=255)),
                ('has_cats', models.BooleanField(default=False)),
                ('has_dogs', models.BooleanField(default=False)),
                ('has_children', models.BooleanField(default=False)),
                ('approved_to_adopt', models.BooleanField(default=False)),
                ('favorited_cats', models.ManyToManyField(through='musickittyapi.CatFavorite', to='musickittyapi.cat')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('number_of_guests', models.IntegerField()),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musickittyapi.location')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musickittyapi.profile')),
            ],
        ),
        migrations.CreateModel(
            name='ProfileAdoption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adoption_date', models.DateField()),
                ('status', models.CharField(max_length=255)),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musickittyapi.cat')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musickittyapi.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('price', models.FloatField()),
                ('image', models.CharField(max_length=255)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musickittyapi.location')),
            ],
        ),
        migrations.AddField(
            model_name='catfavorite',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_relationships', to='musickittyapi.profile'),
        ),
        migrations.AddField(
            model_name='cat',
            name='favoried_by',
            field=models.ManyToManyField(related_name='favorited_cats_through', through='musickittyapi.CatFavorite', to='musickittyapi.profile'),
        ),
        migrations.AddField(
            model_name='cat',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musickittyapi.location'),
        ),
    ]
