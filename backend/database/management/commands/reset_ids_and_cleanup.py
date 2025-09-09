from django.core.management.base import BaseCommand
from django.db import connection, transaction
from django.conf import settings
from database.models import ApiAccessKey, User
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Reset all table IDs to be in order and remove orphaned API keys'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without actually doing it',
        )
        parser.add_argument(
            '--skip-api-cleanup',
            action='store_true',
            help='Skip cleaning up orphaned API keys',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        skip_api_cleanup = options['skip_api_cleanup']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))
        
        with connection.cursor() as cursor:
            try:
                with transaction.atomic():
                    # Step 1: Clean up orphaned API keys
                    if not skip_api_cleanup:
                        self.cleanup_orphaned_api_keys(cursor, dry_run)
                    
                    # Step 2: Reset IDs for all tables in the correct order
                    self.reset_table_ids(cursor, dry_run)
                    
                    if not dry_run:
                        self.stdout.write(self.style.SUCCESS('Successfully reset all IDs and cleaned up orphaned data'))
                    else:
                        self.stdout.write(self.style.SUCCESS('Dry run completed successfully'))
                        
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error occurred: {str(e)}'))
                raise

    def cleanup_orphaned_api_keys(self, cursor, dry_run):
        """Remove API keys that don't have associated users"""
        self.stdout.write('Cleaning up orphaned API keys...')
        
        # Find orphaned API keys
        cursor.execute("""
            SELECT id, uuid, token_name 
            FROM api_access_keys 
            WHERE user_id NOT IN (SELECT id FROM users)
        """)
        
        orphaned_keys = cursor.fetchall()
        
        if orphaned_keys:
            self.stdout.write(f'Found {len(orphaned_keys)} orphaned API keys:')
            for key_id, uuid, token_name in orphaned_keys:
                self.stdout.write(f'  - ID: {key_id}, UUID: {uuid}, Name: {token_name}')
            
            if not dry_run:
                # Delete orphaned API keys
                cursor.execute("""
                    DELETE FROM api_access_keys 
                    WHERE user_id NOT IN (SELECT id FROM users)
                """)
                self.stdout.write(f'Deleted {len(orphaned_keys)} orphaned API keys')
            else:
                self.stdout.write(f'Would delete {len(orphaned_keys)} orphaned API keys')
        else:
            self.stdout.write('No orphaned API keys found')

    def reset_table_ids(self, cursor, dry_run):
        """Reset IDs for all tables in dependency order"""
        
        # Define tables in dependency order (parent tables first)
        tables = [
            'users',
            'brands', 
            'sensors',
            'stations',
            'api_access_keys',
            'api_access_key_stations',
            'station_sensors',
            'measurements',
            'station_health_logs',
            'notifications',
            'chats',
            'messages',
            'bills',
            'task_executions',
            'api_key_usage_logs',
            'system_logs'
        ]
        
        for table in tables:
            self.reset_table_id(cursor, table, dry_run)

    def reset_table_id(self, cursor, table_name, dry_run):
        """Reset IDs for a specific table"""
        try:
            # Check if table exists
            cursor.execute(f"""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = '{table_name}'
                )
            """)
            
            if not cursor.fetchone()[0]:
                self.stdout.write(f'Table {table_name} does not exist, skipping...')
                return
            
            # Get current max ID
            cursor.execute(f"SELECT MAX(id) FROM {table_name}")
            max_id = cursor.fetchone()[0]
            
            if max_id is None or max_id == 0:
                self.stdout.write(f'Table {table_name} is empty, skipping...')
                return
            
            # Get current count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            
            self.stdout.write(f'Resetting IDs for {table_name} (current max: {max_id}, count: {count})')
            
            if not dry_run:
                # Reset the sequence to start from 1
                cursor.execute(f"ALTER SEQUENCE {table_name}_id_seq RESTART WITH 1")
                
                # Update all IDs to be sequential starting from 1
                # We need to do this carefully to avoid conflicts
                cursor.execute(f"""
                    WITH numbered AS (
                        SELECT id, ROW_NUMBER() OVER (ORDER BY id) as new_id
                        FROM {table_name}
                    )
                    UPDATE {table_name} 
                    SET id = numbered.new_id
                    FROM numbered
                    WHERE {table_name}.id = numbered.id
                """)
                
                # Update the sequence to continue from the next available ID
                cursor.execute(f"SELECT setval('{table_name}_id_seq', {count}, true)")
                
                self.stdout.write(f'  ✓ Reset {table_name} IDs (1 to {count})')
            else:
                self.stdout.write(f'  Would reset {table_name} IDs (1 to {count})')
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error resetting {table_name}: {str(e)}'))
            # Continue with other tables even if one fails
            pass

    def get_table_foreign_keys(self, cursor, table_name):
        """Get foreign key constraints for a table"""
        cursor.execute("""
            SELECT 
                tc.constraint_name, 
                tc.table_name, 
                kcu.column_name, 
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name 
            FROM 
                information_schema.table_constraints AS tc 
                JOIN information_schema.key_column_usage AS kcu
                  ON tc.constraint_name = kcu.constraint_name
                  AND tc.table_schema = kcu.table_schema
                JOIN information_schema.constraint_column_usage AS ccu
                  ON ccu.constraint_name = tc.constraint_name
                  AND ccu.table_schema = tc.table_schema
            WHERE tc.constraint_type = 'FOREIGN KEY' 
              AND tc.table_name = %s
        """, [table_name])
        
        return cursor.fetchall()
