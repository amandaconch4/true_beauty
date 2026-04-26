from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_cuidadorecomendacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuidadorecomendacion',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cuidados_recomendaciones', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterModelOptions(
            name='cuidadorecomendacion',
            options={'ordering': ['-fecha', '-id']},
        ),
    ]
