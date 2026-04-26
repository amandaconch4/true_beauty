from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_fichacapilar_marca_shampoo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fichacapilar',
            name='marca_shampoo',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
