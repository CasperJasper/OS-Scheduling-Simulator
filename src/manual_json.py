# manual_json_test.py
import json
import os


def test_json_write():
    """Test if we can write JSON files"""
    test_data = [
        {
            "scenario_id": 1,
            "scenario_name": "Test Scenario",
            "makespan": 100.5,
            "energy": 50.2,
            "offload_percentage": 45.0
        },
        {
            "scenario_id": 2,
            "scenario_name": "Another Test",
            "makespan": 200.3,
            "energy": 75.8,
            "offload_percentage": 60.0
        }
    ]

    # Create directory if it doesn't exist
    os.makedirs("data/output", exist_ok=True)

    output_file = "data/output/test_json.json"

    try:
        with open(output_file, 'w') as f:
            json.dump(test_data, f, indent=2)

        print(f"✓ Test JSON saved to: {output_file}")

        # Verify it can be read back
        with open(output_file, 'r') as f:
            read_data = json.load(f)
            print(f"✓ Successfully read back {len(read_data)} items")

    except Exception as e:
        print(f"✗ Error: {e}")


if __name__ == "__main__":
    test_json_write()