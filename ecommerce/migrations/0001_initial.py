# Generated by Django 3.2.5 on 2021-08-05 03:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cursos', '0001_initial'),
        ('info_User', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cupon',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('codigo_cupon', models.CharField(max_length=10)),
                ('descuento', models.DecimalField(decimal_places=2, max_digits=6)),
                ('fecha_fin', models.DateField()),
                ('en_uso', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Cupon',
                'verbose_name_plural': 'Cupones',
                'db_table': 'cupon',
            },
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_of_sale', models.DateField(auto_now_add=True)),
                ('codigo', models.CharField(max_length=200)),
                ('cantidad', models.IntegerField(default=1)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=6)),
                ('cupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecommerce.cupon')),
                ('postulante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info_User.infouser')),
            ],
            options={
                'verbose_name': 'Venta',
                'verbose_name_plural': 'Ventas',
                'db_table': 'venta',
            },
        ),
        migrations.CreateModel(
            name='Detalle_Venta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField(default=1)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('programa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.curso')),
                ('venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.venta')),
            ],
            options={
                'verbose_name': 'Detalle Venta',
                'verbose_name_plural': 'Detalle Ventas',
                'db_table': 'detalle_orden',
            },
        ),
        migrations.CreateModel(
            name='Carrito',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField(default=1)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('programa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cursos.curso')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='info_User.infouser')),
            ],
            options={
                'verbose_name': 'Carrito de Compra',
                'verbose_name_plural': 'Carrito de Compras',
                'db_table': 'carrito',
            },
        ),
    ]
