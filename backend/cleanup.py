import os
import shutil

def cleanup():
    # Remove all __pycache__ directories
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            print(f"Removing {pycache_path}")
            shutil.rmtree(pycache_path)
        
        # If we're in a migrations folder
        if 'migrations' in root:
            for file in files:
                # Keep __init__.py, remove all other migration files
                if file != '__init__.py' and file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    print(f"Removing {file_path}")
                    os.remove(file_path)

if __name__ == '__main__':
    cleanup() 