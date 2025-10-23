# Generated manually
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_alter_book_options_alter_comment_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='capa_url',
            field=models.URLField(
                blank=True,
                help_text='Cole o link do Google Drive no formato: https://drive.google.com/uc?export=view&id=SEU_ID',
                max_length=500,
                null=True,
                verbose_name='Link da Capa (Google Drive)'
            ),
        ),
    ]
