from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=200, null=True, verbose_name='Owner')),
                ('year', models.IntegerField(null=True, verbose_name='Year')),
                ('licence_plate', models.CharField(max_length=200, verbose_name='Licence plate')),
                ('vin_code', models.CharField(max_length=200, verbose_name='VIN code')),
            ],
            options={
                'verbose_name': 'Car',
                'verbose_name_plural': 'Cars',
            },
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manufacturer', models.CharField(max_length=200, verbose_name='Manufacturer')),
                ('model', models.CharField(max_length=200, verbose_name='Model')),
            ],
            options={
                'verbose_name': 'Car Model',
                'verbose_name_plural': 'Car Models',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('due_date', models.DateTimeField(blank=True, null=True, verbose_name='Due Date')),
                ('car', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='autoservice.car', verbose_name='Car')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('price', models.FloatField(verbose_name='Price')),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
            },
        ),
        migrations.CreateModel(
            name='OrderLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(verbose_name='Quantity')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lines', to='autoservice.order', verbose_name='Order')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='autoservice.service', verbose_name='Service')),
            ],
            options={
                'verbose_name': 'Order Line',
                'verbose_name_plural': 'Order Lines',
            },
        ),
        migrations.AddField(
            model_name='car',
            name='car_model',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='autoservice.carmodel', verbose_name='Model'),
        ),
    ]