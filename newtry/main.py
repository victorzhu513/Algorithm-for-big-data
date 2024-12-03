import requests
import json
import csv

# Ollama server settings
url = "http://localhost:11434/api/chat"
headers = {"Content-Type": "application/json"}

# Initialize the conversation history
conversation = [
    {"role": "user", "content": "Hello!"}
]


# Function to send a message and get a response
def send_message(new_message, count):
    # Add the new message to the conversation
    conversation.append({"role": "user", "content": new_message})

    # Make the API call
    response = requests.post(url, headers=headers, json={
        "model": "llama3",
        "messages": conversation,
        "stream": False,
        "options": {
            "num_ctx": count
        }
    })

    # Get the bot's response
    if response.status_code == 200:
        bot_message = response.json()["message"]["content"]
        # Add the bot's response to the conversation
        conversation.append({"role": "assistant", "content": bot_message})
        return bot_message
    else:
        print("Error:", response.status_code, response.text)
        return None

# Path to your JSON file
file_path = "abortion_train.json"

# Read the JSON file and convert it to a string
with open(file_path, "r") as file:
    json_data = json.load(file)  # Load JSON as Python object
    json_string = json.dumps(json_data)  # Convert Python object to JSON string


baseprompt = "Given the data gave you, find the persuasiveness and stance of the statement, give an answer in this exact format: persuasiveness: [yes/no], stance: [oppose/support]. Dont give anything else just simply what i ask for. this should be in json format ALWAYS -- Statement: "

#First prompt to give the llm info
print(send_message("Here are examples of persuasive and stance evaluations for statements for the topic of abortion. Use this to guide your future responses:\n" + json_string,12000))

# Get the test info
# Path to your CSV file
csv_file_path = 'abortion_test.csv'

# Open the file and convert it to a dictionary
with open(csv_file_path, mode='r',encoding='utf-8', errors='ignore') as file:
    # Create a CSV reader object
    csv_reader = csv.DictReader(file)

    # Convert to a list of dictionaries
    abortion_test_data = [row for row in csv_reader]

correct_persuasiveness_count = 0
correct_stance_count = 0
total = 0

for row in abortion_test_data:
    tweet_text = row['tweet_text']
    correct_persuasiveness = row['persuasiveness']
    correct_stance = row['stance']

    response_json = send_message(baseprompt + tweet_text,4096)
    try:
        # Attempt to parse the JSON string
        response_dict = json.loads(response_json)
        if response_dict['persuasiveness'] == correct_persuasiveness:
            correct_persuasiveness_count += 1

        if response_dict['stance'] == correct_stance:
            correct_stance_count += 1
    except json.JSONDecodeError as e:
        # Handle JSON decoding errors
        print(f"Failed to parse JSON: {e}")
    except Exception as e:
        # Handle other unexpected errors
        print(f"An unexpected error occurred: {e}")
    print(total)
    total += 1

print("Correct on persuasiveness: " + str(correct_persuasiveness_count/total * 100) + "%")
print("Correct on stance: " + str(correct_stance_count/total * 100) + "%")

