import os
import sys
import django
import MySQLdb

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.conf import settings

db_config = settings.DATABASES['default']

try:
    conn = MySQLdb.connect(
        host=db_config['HOST'],
        user=db_config['USER'],
        passwd=db_config['PASSWORD'],
        db=db_config['NAME'],
        port=int(db_config['PORT']),
    )
    cursor = conn.cursor()
    
    # Delete migration record
    cursor.execute("DELETE FROM django_migrations WHERE app='mainapp'")
    conn.commit()
    print("✓ Migration records deleted")
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
