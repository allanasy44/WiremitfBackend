
# Generated manually
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pair', models.CharField(max_length=20, db_index=True)),
                ('rate', models.FloatField()),
                ('sources', models.JSONField(default=dict)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-timestamp']},
        ),
    ]
