from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_perfilusuario_rol'),
    ]

    operations = [
        migrations.AddField(
            model_name='fichacapilar',
            name='cuero_cabelludo',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='fichacapilar',
            name='diagnostico_general',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name='fichacapilar',
            name='duracion_aproximada',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='fichacapilar',
            name='elasticidad',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='fichacapilar',
            name='grosor',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='fichacapilar',
            name='historial',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name='fichacapilar',
            name='porosidad',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='fichacapilar',
            name='textura',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
