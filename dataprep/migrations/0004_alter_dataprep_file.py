# Generated by Django 4.0.5 on 2022-06-08 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataprep', '0003_remove_dataprep_filepath_dataprep_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataprep',
            name='file',
            field=models.FileField(default='/User/', upload_to=''),
        ),
    ]