from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0003_product_construction_product_product_type_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="is_verified_purchase",
            field=models.BooleanField(default=False),
        ),
    ]
