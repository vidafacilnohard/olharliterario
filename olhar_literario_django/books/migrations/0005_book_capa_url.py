# Generated manually
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_book_destaque'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='capa_url',
            field=models.URLField(
                blank=True,
                help_text='Cole o link compartilhado do Google Drive (será convertido automaticamente). Ex: https://drive.google.com/file/d/ABC123/view',
                max_length=500,
                null=True,
                verbose_name='Link da Capa (Google Drive)'
            ),
        ),
    ]
