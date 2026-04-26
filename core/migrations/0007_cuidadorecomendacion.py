from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_fichacapilar_marca_shampoo'),
    ]

    operations = [
        migrations.CreateModel(
            name='CuidadoRecomendacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(blank=True, null=True)),
                ('recomendacion_casa', models.TextField()),
                ('producto_recomendado', models.TextField()),
                ('modo_uso', models.TextField()),
                ('frecuencia', models.TextField()),
                ('fecha_inicio', models.DateField(blank=True, null=True)),
                ('fecha_termino', models.DateField(blank=True, null=True)),
                ('cliente', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cuidados_recomendaciones', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
