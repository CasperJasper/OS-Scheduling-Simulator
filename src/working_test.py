import os
import sys

# Get the absolute path to the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Current directory: {current_dir}")

# Add current directory to Python path
sys.path.insert(0, current_dir)

# List files to debug
print("Files in current directory:")
for file in os.listdir(current_dir):
    print(f"  {file}")

print("Files in models directory:")
models_path = os.path.join(current_dir, 'models')
if os.path.exists(models_path):
    for file in os.listdir(models_path):
        print(f"  {file}")
else:
    print("  models directory not found!")

# Try to import
try:
    from models.task import Task
    print("✓ Successfully imported Task")
except ImportError as e:
    print(f"✗ Failed to import Task: {e}")

try:
    from models.device import Device
    print("✓ Successfully imported Device")
except ImportError as e:
    print(f"✗ Failed to import Device: {e}")