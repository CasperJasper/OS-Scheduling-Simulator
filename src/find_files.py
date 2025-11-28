# find_files.py
import os


def find_json_files():
    """Search for JSON files in the project"""
    print("Searching for JSON files...")

    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.json'):
                full_path = os.path.join(root, file)
                file_size = os.path.getsize(full_path)
                print(f"Found: {full_path} ({file_size} bytes)")


if __name__ == "__main__":
    find_json_files()