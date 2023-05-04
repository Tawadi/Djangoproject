# Generated by Django 4.1.5 on 2023-03-18 14:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseModel',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MedicineCategory',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.basemodel')),
                ('category_name', models.CharField(max_length=100)),
            ],
            bases=('home.basemodel',),
        ),
        migrations.CreateModel(
            name='Medicines',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.basemodel')),
                ('medicine_name', models.CharField(max_length=100)),
                ('price', models.IntegerField(default=100)),
                ('images', models.ImageField(upload_to='medicine')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medicines', to='home.medicinecategory')),
            ],
            bases=('home.basemodel',),
        ),
        migrations.CreateModel(
            name='Carts',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.basemodel')),
                ('is_paid', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='carts', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('home.basemodel',),
        ),
        migrations.CreateModel(
            name='CartItems',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.basemodel')),
                ('thecart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='home.carts')),
                ('themedicine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.medicines')),
            ],
            bases=('home.basemodel',),
        ),
    ]
