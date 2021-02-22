# Generated by Django 3.0.11 on 2021-01-18 16:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('sessions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=254, null=True, unique=True, verbose_name='email')),
                ('firstname', models.CharField(max_length=30)),
                ('lastname', models.CharField(max_length=30)),
                ('streetname', models.CharField(max_length=30)),
                ('housenr', models.CharField(max_length=30)),
                ('postalcode', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=30)),
                ('country', models.CharField(max_length=30)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('session', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sessions.Session')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(choices=[('Wit', 'Wit'), ('Blauw', 'Blauw'), ('Oranje', 'Oranje'), ('Paars', 'Paars'), ('Roze', 'Roze'), ('Rood', 'Rood'), ('Parel', 'Parel'), ('Edelsteen', 'Edelsteen'), ('Beige', 'Beige'), ('Groen', 'Groen'), ('Geel', 'Geel')], max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Diy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('description', models.TextField()),
                ('jewelry_type', models.CharField(choices=[('Armband', 'Armband'), ('Ketting', 'Ketting'), ('Oorbellen', 'Oorbellen')], max_length=30)),
                ('look', models.CharField(choices=[('Kralen', 'Kralen'), ('Schakelketting', 'Schakelketting')], max_length=30)),
                ('metal_type', models.CharField(choices=[('Goud', 'Goud'), ('Zilver', 'Zilver')], max_length=30)),
                ('color', models.ManyToManyField(to='webshop.Color')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product_images/')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('date_added', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('in_stock', models.BooleanField(default=True)),
                ('description', models.TextField()),
                ('limited_edition', models.BooleanField(default=False)),
                ('jewelry_type', models.CharField(choices=[('Armband', 'Armband'), ('Ketting', 'Ketting'), ('Oorbellen', 'Oorbellen')], max_length=30)),
                ('look', models.CharField(choices=[('Kralen', 'Kralen'), ('Schakelketting', 'Schakelketting')], max_length=30)),
                ('metal_type', models.CharField(choices=[('Goud', 'Goud'), ('Zilver', 'Zilver')], max_length=30)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('image', models.ImageField(upload_to='product_images/')),
                ('size', models.IntegerField()),
                ('left', models.IntegerField()),
                ('sale', models.BooleanField(default=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('color', models.ManyToManyField(to='webshop.Color')),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('ordered', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('diyproduct', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='webshop.Diy')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='webshop.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_ordered', models.DateField()),
                ('status', models.CharField(choices=[('Verzonden', 'Verzonden'), ('In behandeling', 'In behandeling'), ('Ontvangen', 'Ontvangen')], max_length=30)),
                ('total', models.DecimalField(decimal_places=2, max_digits=5)),
                ('comment', models.TextField()),
                ('shipping', models.CharField(choices=[('Brievenbuspakketje', 'Brievenbuspakketje'), ('Met Track & Trace', 'Met Track & Trace')], max_length=50)),
                ('free_shipping', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('orderproduct', models.ManyToManyField(to='webshop.OrderProduct')),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('favoriteproduct', models.ManyToManyField(to='webshop.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20)),
                ('active', models.BooleanField(default=True)),
                ('expiry_date', models.DateTimeField()),
                ('discount_type', models.CharField(choices=[('Vast bedrag', 'Vast bedrag'), ('Percentage', 'Percentage')], max_length=30)),
                ('discount_amount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
