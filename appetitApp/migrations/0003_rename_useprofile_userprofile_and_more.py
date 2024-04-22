import django.db.models.deletion

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
<<<<<<< HEAD
=======

>>>>>>> main


class Migration(migrations.Migration):

    dependencies = [
        ('appetitApp', '0002_remove_directions_recipe_useprofile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UseProfile',
            new_name='UserProfile',
        ),
        migrations.AlterField(
            model_name='recipe',
            name='description',
            field=models.TextField(max_length=300),
        ),


        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=300)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appetitApp.recipe')),
            ],
        ),

    ]
