import csv
import json

def csv_to_json(csv_file_path, json_file_path):
    # Open the CSV file for reading
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        # Read the CSV file
        csv_reader = csv.DictReader(csv_file)
        
        # Create a list to hold the formatted JSON data
        data = []
        
        # Process each row in the CSV
        for row in csv_reader:
            # Construct the desired JSON structure for each row
            json_object = {
                "input": {
                    "text": row['tweet_text'],  # Assuming column name is 'tweet_text'
                    "image": f"data/images/gun_control/{row['tweet_id']}.jpg"
                },
                "output": {
                    "Persuasion": row['persuasiveness'],  # Assuming column name is 'persuasiveness'
                    "Stance": row['stance']  # Assuming column name is 'stance'
                }
            }
            data.append(json_object)
    
    # Write the JSON data to a file
    with open(json_file_path, mode='w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4)

# Example usage
csv_file = 'gun_control_train.csv'  # Path to your CSV file
json_file = 'gun_control_train.json'    # Path where the JSON file will be saved

csv_to_json(csv_file, json_file)
