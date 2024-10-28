# Generated by Django 4.2.11 on 2024-10-28 10:26

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Filmwork',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('creation_date', models.DateField(blank=True, verbose_name='creation_date')),
                ('rating', models.FloatField(blank=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='rating')),
                ('type', models.CharField(choices=[('movie', 'Movie'), ('tv_show', 'TV Show')], default='movie', max_length=10)),
            ],
            options={
                'verbose_name': 'filmfork',
                'verbose_name_plural': 'filmforks',
                'db_table': 'content"."film_work',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'genre',
                'verbose_name_plural': 'genres',
                'db_table': 'content"."genre',
            },
        ),
        migrations.CreateModel(
            name='GenreFilmwork',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'genre filmwork',
                'verbose_name_plural': 'genres filmworks',
                'db_table': 'content"."genre_film_work',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=255, verbose_name='full_name')),
            ],
            options={
                'verbose_name': 'person',
                'verbose_name_plural': 'persons',
                'db_table': 'content"."person',
            },
        ),
        migrations.CreateModel(
            name='PersonFilmwork',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('role', models.CharField(choices=[('director', 'Director'), ('writer', 'Writer'), ('actor', 'Actor')], default='actor', max_length=10, verbose_name='role')),
                ('film_work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person_filmwork', to='movies.filmwork', verbose_name='filmwork')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person_filmwork', to='movies.person', verbose_name='person')),
            ],
            options={
                'verbose_name': 'person filmwork',
                'verbose_name_plural': 'persons filmworks',
                'db_table': 'content"."person_film_work',
            },
        ),
        migrations.AddIndex(
            model_name='person',
            index=models.Index(fields=['full_name'], name='person_full_name_idx'),
        ),
        migrations.AddField(
            model_name='genrefilmwork',
            name='film_work',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='genre_filmwork', to='movies.filmwork', verbose_name='filmwork'),
        ),
        migrations.AddField(
            model_name='genrefilmwork',
            name='genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='genre_filmwork', to='movies.genre', verbose_name='genre'),
        ),
        migrations.AddField(
            model_name='filmwork',
            name='genres',
            field=models.ManyToManyField(through='movies.GenreFilmwork', to='movies.genre'),
        ),
        migrations.AddField(
            model_name='filmwork',
            name='persons',
            field=models.ManyToManyField(through='movies.PersonFilmwork', to='movies.person'),
        ),
        migrations.AddIndex(
            model_name='personfilmwork',
            index=models.Index(fields=['film_work', 'person', 'role'], name='person_role_film_work_idx_fk'),
        ),
        migrations.AddIndex(
            model_name='genrefilmwork',
            index=models.Index(fields=['film_work', 'genre'], name='genre_film_work_idx_fk'),
        ),
        migrations.AddIndex(
            model_name='filmwork',
            index=models.Index(fields=['id'], name='film_work_id_idx'),
        ),
        migrations.AddIndex(
            model_name='filmwork',
            index=models.Index(fields=['title'], name='film_work_title_idx'),
        ),
        migrations.AddIndex(
            model_name='filmwork',
            index=models.Index(fields=['creation_date'], name='film_work_creation_date_idx'),
        ),
        migrations.AddIndex(
            model_name='filmwork',
            index=models.Index(fields=['rating'], name='film_work_creation_idx'),
        ),
        migrations.AddIndex(
            model_name='filmwork',
            index=models.Index(fields=['type'], name='film_work_type_idx'),
        ),
    ]
