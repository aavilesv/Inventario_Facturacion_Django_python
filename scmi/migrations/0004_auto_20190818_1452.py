# Generated by Django 2.1 on 2019-08-18 19:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scmi', '0003_auto_20190813_2001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='fecha',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 8, 18, 14, 52, 5, 566957)),
        ),
        migrations.AlterField(
            model_name='factura',
            name='fecventa',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 18, 14, 52, 5, 573959)),
        ),
        migrations.AlterField(
            model_name='inventario',
            name='fechaingreso',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 8, 18, 14, 52, 5, 564958)),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='fecentrega',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 18, 14, 52, 5, 571959)),
        ),
    ]