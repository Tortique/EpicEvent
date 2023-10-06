from django.db import migrations

from app.models import MANAGEMENT, SALES, SUPPORT


def create_teams(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    teams = apps.get_model("app", "Team")
    for name in [MANAGEMENT, SALES, SUPPORT]:
        teams.objects.using(db_alias).create(name=name)


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
        ("app", "0002_client_contract_event"),
    ]

    operations = [
        migrations.RunPython(create_teams),
    ]
