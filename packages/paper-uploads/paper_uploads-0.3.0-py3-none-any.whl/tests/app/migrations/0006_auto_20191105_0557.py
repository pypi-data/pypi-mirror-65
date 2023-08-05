# Generated by Django 2.2.6 on 2019-11-05 05:57

from django.db import migrations
import django.db.models.deletion
import paper_uploads.cloudinary.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('paper_uploads_cloudinary', '0001_initial'),
        ('app', '0005_testcollection_testcollectionblocked_testcollectionoverride'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='cloud_file',
            field=paper_uploads.cloudinary.models.fields.CloudinaryFileField(blank=True, on_delete=django.db.models.deletion.SET_NULL, to='paper_uploads_cloudinary.CloudinaryFile', verbose_name='file'),
        ),
        migrations.AddField(
            model_name='page',
            name='cloud_image',
            field=paper_uploads.cloudinary.models.fields.CloudinaryImageField(blank=True, on_delete=django.db.models.deletion.SET_NULL, to='paper_uploads_cloudinary.CloudinaryImage', verbose_name='image'),
        ),
        migrations.AddField(
            model_name='page',
            name='cloud_video',
            field=paper_uploads.cloudinary.models.fields.CloudinaryMediaField(blank=True, on_delete=django.db.models.deletion.SET_NULL, to='paper_uploads_cloudinary.CloudinaryMedia', verbose_name='video'),
        ),
    ]
