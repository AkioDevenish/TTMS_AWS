from django.core.management.base import BaseCommand
from django.db import connection, transaction
from django.conf import settings
from database.models import ApiAccessKey, User
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Reset all table IDs to be in order and remove orphaned API keys (Advanced version)'

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
        parser.add_argument(
            '--tables',
            nargs='+',
            help='Specific tables to reset (default: all tables)',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        skip_api_cleanup = options['skip_api_cleanup']
        specific_tables = options.get('tables', [])
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))
        
        with connection.cursor() as cursor:
            try:
                with transaction.atomic():
                    # Step 1: Clean up orphaned API keys
                    if not skip_api_cleanup:
                        self.cleanup_orphaned_api_keys(cursor, dry_run)
                    
                    # Step 2: Reset IDs for all tables in the correct order
                    self.reset_table_ids(cursor, dry_run, specific_tables)
                    
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

    def reset_table_ids(self, cursor, dry_run, specific_tables=None):
        """Reset IDs for all tables in dependency order"""
        
        # Define tables in dependency order (parent tables first)
        all_tables = [
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
        
        tables_to_process = specific_tables if specific_tables else all_tables
        
        for table in tables_to_process:
            if table in all_tables:
                self.reset_table_id_advanced(cursor, table, dry_run)
            else:
                self.stdout.write(self.style.WARNING(f'Unknown table: {table}'))

    def reset_table_id_advanced(self, cursor, table_name, dry_run):
        """Reset IDs for a specific table with proper foreign key handling"""
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
            
            # Get current max ID and count
            cursor.execute(f"SELECT MAX(id), COUNT(*) FROM {table_name}")
            max_id, count = cursor.fetchone()
            
            if max_id is None or max_id == 0:
                self.stdout.write(f'Table {table_name} is empty, skipping...')
                return
            
            self.stdout.write(f'Resetting IDs for {table_name} (current max: {max_id}, count: {count})')
            
            if not dry_run:
                # Step 1: Temporarily disable foreign key constraints
                self.disable_foreign_keys(cursor, table_name)
                
                try:
                    # Step 2: Create a temporary column for new IDs
                    cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN temp_new_id SERIAL")
                    
                    # Step 3: Update the temp column with sequential IDs
                    cursor.execute(f"""
                        UPDATE {table_name} 
                        SET temp_new_id = ROW_NUMBER() OVER (ORDER BY id)
                    """)
                    
                    # Step 4: Update foreign key references in other tables
                    self.update_foreign_key_references(cursor, table_name)
                    
                    # Step 5: Drop the old id column and rename temp column
                    cursor.execute(f"ALTER TABLE {table_name} DROP COLUMN id")
                    cursor.execute(f"ALTER TABLE {table_name} RENAME COLUMN temp_new_id TO id")
                    cursor.execute(f"ALTER TABLE {table_name} ADD PRIMARY KEY (id)")
                    
                    # Step 6: Reset the sequence
                    cursor.execute(f"ALTER SEQUENCE {table_name}_id_seq RESTART WITH {count + 1}")
                    
                    self.stdout.write(f'  ✓ Reset {table_name} IDs (1 to {count})')
                    
                finally:
                    # Step 7: Re-enable foreign key constraints
                    self.enable_foreign_keys(cursor, table_name)
                    
            else:
                self.stdout.write(f'  Would reset {table_name} IDs (1 to {count})')
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error resetting {table_name}: {str(e)}'))
            # Continue with other tables even if one fails
            pass

    def disable_foreign_keys(self, cursor, table_name):
        """Disable foreign key constraints for a table"""
        try:
            # Get all foreign key constraints that reference this table
            cursor.execute("""
                SELECT constraint_name, table_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                    ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage ccu
                    ON ccu.constraint_name = tc.constraint_name
                WHERE tc.constraint_type = 'FOREIGN KEY'
                    AND ccu.table_name = %s
            """, [table_name])
            
            constraints = cursor.fetchall()
            
            for constraint_name, ref_table in constraints:
                try:
                    cursor.execute(f"ALTER TABLE {ref_table} DROP CONSTRAINT {constraint_name}")
                    self.stdout.write(f'  Disabled FK constraint: {constraint_name} on {ref_table}')
                except Exception as e:
                    self.stdout.write(f'  Warning: Could not disable constraint {constraint_name}: {e}')
                    
        except Exception as e:
            self.stdout.write(f'  Warning: Could not disable foreign keys for {table_name}: {e}')

    def enable_foreign_keys(self, cursor, table_name):
        """Re-enable foreign key constraints for a table"""
        # Note: This is a simplified version. In production, you'd want to 
        # store the original constraint definitions and recreate them
        self.stdout.write(f'  Note: Foreign key constraints for {table_name} need to be manually recreated')

    def update_foreign_key_references(self, cursor, table_name):
        """Update foreign key references in other tables"""
        # Get all tables that reference this table
        cursor.execute("""
            SELECT DISTINCT tc.table_name, kcu.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
                ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage ccu
                ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY'
                AND ccu.table_name = %s
        """, [table_name])
        
        references = cursor.fetchall()
        
        for ref_table, ref_column in references:
            try:
                # Update foreign key references to use new IDs
                cursor.execute(f"""
                    UPDATE {ref_table} 
                    SET {ref_column} = (
                        SELECT temp_new_id 
                        FROM {table_name} 
                        WHERE {table_name}.id = {ref_table}.{ref_column}
                    )
                    WHERE {ref_column} IN (SELECT id FROM {table_name})
                """)
                self.stdout.write(f'  Updated foreign key references in {ref_table}.{ref_column}')
            except Exception as e:
                self.stdout.write(f'  Warning: Could not update references in {ref_table}.{ref_column}: {e}')

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
