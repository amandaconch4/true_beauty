from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_fichacapilar_detalles'),
    ]

    operations = [
        migrations.AddField(
            model_name='fichacapilar',
            name='marca_shampoo',
            field=models.CharField(blank=True, max_length=25),
        ),
    ]
