# Generated by Django 2.2.5 on 2019-09-27 13:54

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone
import paper_uploads.models.image


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('upload', 'Can upload files'), ('change', 'Can change files'), ('delete', 'Can delete files')),
                'managed': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='CollectionItemBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.IntegerField()),
                ('item_type', models.CharField(db_index=True, editable=False, max_length=32, verbose_name='type')),
                ('order', models.IntegerField(default=0, editable=False, verbose_name='order')),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_paper_uploads.collectionitembase_set+', to='contenttypes.ContentType')),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='file name')),
                ('extension', models.CharField(editable=False, help_text='Lowercase string without leading dot', max_length=32, verbose_name='file extension')),
                ('size', models.PositiveIntegerField(default=0, editable=False, verbose_name='file size')),
                ('hash', models.CharField(editable=False, help_text='SHA-1 hash of the file contents', max_length=40, verbose_name='file hash')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='created at')),
                ('uploaded_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='uploaded at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='changed at')),
                ('owner_app_label', models.CharField(editable=False, max_length=100)),
                ('owner_model_name', models.CharField(editable=False, max_length=100)),
                ('owner_fieldname', models.CharField(editable=False, max_length=255)),
                ('file', models.FileField(max_length=255, storage=django.core.files.storage.FileSystemStorage(), upload_to='files/%Y-%m-%d', verbose_name='file')),
                ('display_name', models.CharField(blank=True, max_length=255, verbose_name='display name')),
            ],
            options={
                'verbose_name': 'file',
                'verbose_name_plural': 'files',
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='UploadedImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='file name')),
                ('extension', models.CharField(editable=False, help_text='Lowercase string without leading dot', max_length=32, verbose_name='file extension')),
                ('size', models.PositiveIntegerField(default=0, editable=False, verbose_name='file size')),
                ('hash', models.CharField(editable=False, help_text='SHA-1 hash of the file contents', max_length=40, verbose_name='file hash')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='created at')),
                ('uploaded_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='uploaded at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='changed at')),
                ('owner_app_label', models.CharField(editable=False, max_length=100)),
                ('owner_model_name', models.CharField(editable=False, max_length=100)),
                ('owner_fieldname', models.CharField(editable=False, max_length=255)),
                ('alt', models.CharField(blank=True, help_text='This text will be used by screen readers, search engines, or when the image cannot be loaded', max_length=255, verbose_name='alternate text')),
                ('title', models.CharField(blank=True, help_text='The title is used as a tooltip when the user hovers the mouse over the image', max_length=255, verbose_name='title')),
                ('width', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='width')),
                ('height', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='height')),
                ('cropregion', models.CharField(blank=True, editable=False, max_length=24, verbose_name='crop region')),
                ('file', paper_uploads.models.image.VariationalFileField(max_length=255, storage=django.core.files.storage.FileSystemStorage(), upload_to='images/%Y-%m-%d', verbose_name='file')),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='FileItem',
            fields=[
                ('collectionitembase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='paper_uploads.CollectionItemBase')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='file name')),
                ('extension', models.CharField(editable=False, help_text='Lowercase string without leading dot', max_length=32, verbose_name='file extension')),
                ('size', models.PositiveIntegerField(default=0, editable=False, verbose_name='file size')),
                ('hash', models.CharField(editable=False, help_text='SHA-1 hash of the file contents', max_length=40, verbose_name='file hash')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='created at')),
                ('uploaded_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='uploaded at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='changed at')),
                ('file', models.FileField(max_length=255, storage=django.core.files.storage.FileSystemStorage(), upload_to='gallery/files/%Y-%m-%d', verbose_name='file')),
                ('display_name', models.CharField(blank=True, max_length=255, verbose_name='display name')),
                ('preview', models.CharField(blank=True, editable=False, max_length=255, verbose_name='preview URL')),
            ],
            options={
                'verbose_name': 'file',
                'verbose_name_plural': 'files',
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('paper_uploads.collectionitembase', models.Model),
        ),
        migrations.CreateModel(
            name='ImageItem',
            fields=[
                ('collectionitembase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='paper_uploads.CollectionItemBase')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='file name')),
                ('extension', models.CharField(editable=False, help_text='Lowercase string without leading dot', max_length=32, verbose_name='file extension')),
                ('size', models.PositiveIntegerField(default=0, editable=False, verbose_name='file size')),
                ('hash', models.CharField(editable=False, help_text='SHA-1 hash of the file contents', max_length=40, verbose_name='file hash')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='created at')),
                ('uploaded_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='uploaded at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='changed at')),
                ('alt', models.CharField(blank=True, help_text='This text will be used by screen readers, search engines, or when the image cannot be loaded', max_length=255, verbose_name='alternate text')),
                ('title', models.CharField(blank=True, help_text='The title is used as a tooltip when the user hovers the mouse over the image', max_length=255, verbose_name='title')),
                ('width', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='width')),
                ('height', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='height')),
                ('cropregion', models.CharField(blank=True, editable=False, max_length=24, verbose_name='crop region')),
                ('file', paper_uploads.models.image.VariationalFileField(max_length=255, storage=django.core.files.storage.FileSystemStorage(), upload_to='gallery/images/%Y-%m-%d', verbose_name='file')),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('paper_uploads.collectionitembase', models.Model),
        ),
        migrations.CreateModel(
            name='SVGItem',
            fields=[
                ('collectionitembase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='paper_uploads.CollectionItemBase')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='file name')),
                ('extension', models.CharField(editable=False, help_text='Lowercase string without leading dot', max_length=32, verbose_name='file extension')),
                ('size', models.PositiveIntegerField(default=0, editable=False, verbose_name='file size')),
                ('hash', models.CharField(editable=False, help_text='SHA-1 hash of the file contents', max_length=40, verbose_name='file hash')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='created at')),
                ('uploaded_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='uploaded at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='changed at')),
                ('file', models.FileField(max_length=255, storage=django.core.files.storage.FileSystemStorage(), upload_to='gallery/files/%Y-%m-%d', verbose_name='file')),
                ('display_name', models.CharField(blank=True, max_length=255, verbose_name='display name')),
            ],
            options={
                'verbose_name': 'SVG-file',
                'verbose_name_plural': 'SVG-files',
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('paper_uploads.collectionitembase', models.Model),
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner_app_label', models.CharField(editable=False, max_length=100)),
                ('owner_model_name', models.CharField(editable=False, max_length=100)),
                ('owner_fieldname', models.CharField(editable=False, max_length=255)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='created at')),
                ('collection_content_type', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType')),
                ('cover', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='paper_uploads.ImageItem', verbose_name='cover image')),
            ],
            options={
                'proxy': False,
                'default_manager_name': 'default_mgr',
            },
            managers=[
                ('default_mgr', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ImageCollection',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('paper_uploads.collection',),
            managers=[
                ('default_mgr', django.db.models.manager.Manager()),
            ],
        ),
    ]
