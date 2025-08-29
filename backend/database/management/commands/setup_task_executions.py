#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import TaskExecution
from django.utils import timezone
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Setup TaskExecution records for all scheduled tasks'

    def handle(self, *args, **options):
        # Define all scheduled tasks
        scheduled_tasks = [
            {
                'task_name': 'data_fetcher',
                'interval': 3600,  # 1 hour
                'status': 'success'
            },
            {
                'task_name': 'check_station_health',
                'interval': 60,  # 1 minute
                'status': 'success'
            },
            {
                'task_name': 'deactivate_expired_accounts',
                'interval': 60,  # 1 minute
                'status': 'success'
            },
            {
                'task_name': 'deactivate_expired_api_keys',
                'interval': 300,  # 5 minutes
                'status': 'success'
            }
        ]
        
        created_count = 0
        updated_count = 0
        
        for task_info in scheduled_tasks:
            task_execution, created = TaskExecution.objects.get_or_create(
                task_name=task_info['task_name'],
                defaults={
                    'status': task_info['status'],
                    'interval': task_info['interval'],
                    'last_run': timezone.now()
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created TaskExecution for {task_info["task_name"]}')
                )
            else:
                # Update existing record if needed
                if (task_execution.interval != task_info['interval'] or 
                    task_execution.status != task_info['status']):
                    task_execution.interval = task_info['interval']
                    task_execution.status = task_info['status']
                    task_execution.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.WARNING(f'Updated TaskExecution for {task_info["task_name"]}')
                    )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'TaskExecution setup complete: {created_count} created, {updated_count} updated'
            )
        )
        
        # Show current status
        self.stdout.write('\nCurrent TaskExecution records:')
        for task in TaskExecution.objects.all().order_by('task_name'):
            self.stdout.write(
                f'  - {task.task_name}: {task.status} (interval: {task.interval}s)'
            ) 