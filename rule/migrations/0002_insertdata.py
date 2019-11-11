
from django.db import migrations


def insert_data(apps, schema_editor):
    Rule = apps.get_model("rule", "Rule")
    new_rule = Rule(name="Approve confession", app="confession", model="Confession", value=50)
    new_rule.save()


class Migration(migrations.Migration):

    dependencies = [
        ("rule", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(insert_data),
    ]
