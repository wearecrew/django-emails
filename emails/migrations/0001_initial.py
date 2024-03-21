# Generated by Django 4.2.5 on 2023-10-03 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_email', models.CharField(max_length=255)),
                ('to_email', models.CharField(max_length=255)),
                ('subject', models.CharField(max_length=255)),
                ('text_content', models.TextField()),
                ('html_content', models.TextField()),
                ('message_id', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('sent_at', models.DateTimeField(blank=True, null=True)),
                ('metadata', models.TextField(blank=True)),
                ('data', models.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('subject', models.CharField(max_length=255)),
                ('text_template', models.TextField()),
                ('html_template', models.TextField()),
                ('preview_data', models.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.CharField(choices=[('queued', 'Queued'), ('sent', 'Sent'), ('rejected', 'Rejected'), ('failed', 'Failed'), ('bounced', 'Bounced'), ('deferred', 'Deferred'), ('delivered', 'Delivered'), ('opened', 'Opened'), ('clicked', 'Clicked'), ('unknown', 'Unknown')], max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emails.email')),
            ],
        ),
        migrations.AddField(
            model_name='email',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='emails.emailtemplate'),
        ),
    ]
