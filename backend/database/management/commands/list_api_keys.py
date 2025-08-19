from django.core.management.base import BaseCommand
from database.models import ApiAccessKey, User
from django.utils import timezone

class Command(BaseCommand):
    help = 'List all API keys in the database'

    def handle(self, *args, **options):
        self.stdout.write('Listing all API keys...\n')
        
        api_keys = ApiAccessKey.objects.all().select_related('user')
        
        if not api_keys.exists():
            self.stdout.write(self.style.WARNING('No API keys found in the database'))
            return
        
        self.stdout.write(f'Found {api_keys.count()} API key(s):\n')
        
        for key in api_keys:
            status = 'Active' if not key.expires_at or key.expires_at > timezone.now() else 'Expired'
            last_used = key.last_used.strftime('%Y-%m-%d %H:%M:%S') if key.last_used else 'Never'
            
            self.stdout.write(f'UUID: {key.uuid}')
            self.stdout.write(f'  Name: {key.token_name}')
            self.stdout.write(f'  User: {key.user.email} (ID: {key.user.id})')
            self.stdout.write(f'  Status: {status}')
            self.stdout.write(f'  Created: {key.created_at.strftime("%Y-%m-%d %H:%M:%S")}')
            self.stdout.write(f'  Expires: {key.expires_at.strftime("%Y-%m-%d %H:%M:%S") if key.expires_at else "Never"}')
            self.stdout.write(f'  Last Used: {last_used}')
            self.stdout.write(f'  Note: {key.note or "None"}')
            self.stdout.write('')
        
        # Also list users to see if any have API keys
        users = User.objects.all()
        self.stdout.write(f'Total users in database: {users.count()}')
        
        users_with_keys = User.objects.filter(api_keys__isnull=False).distinct()
        self.stdout.write(f'Users with API keys: {users_with_keys.count()}')
        
        if users_with_keys.exists():
            self.stdout.write('Users with API keys:')
            for user in users_with_keys:
                key_count = user.api_keys.count()
                self.stdout.write(f'  {user.email} (ID: {user.id}) - {key_count} key(s)') 