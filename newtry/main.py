import requests
import json
import csv
import base64
import os

# Ollama server settings
url = "http://localhost:11434/api/chat"
llava_url = "http://localhost:11434/api/generate"
headers = {"Content-Type": "application/json"}

# Initialize the conversation history
conversation = [
    {"role": "user", "content": "Hello!"}
]

def convert_to_base64(file_name):
    # Get the current working directory
    current_directory = os.getcwd()

    # Combine the current directory with the file name
    file_location = os.path.join(current_directory, file_name)
    with open(file_location, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string



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

# Function to send a message and get a response
def get_image_details(image):
    # Add the new message to the conversation

    # Make the API call
    response = requests.post(llava_url, headers=headers, json={
        "model": "llava",
        "prompt": "what is this photo? also extract any text from it",
        "images": [image],
        "stream": False
    })

    # Get the bot's response
    if response.status_code == 200:
        bot_message = response.json()["response"]
        # Add the bot's response to the conversation
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


baseprompt = "Given the data provided, find the stance using the statement and the description of the photo. To determine persuasion, only use the statement and dont use the description of the photo, give an answer in this exact format: {persuasiveness: [yes/no], stance: [oppose/support]}. Dont give anything else just simply what i ask for. make sure this returns a response in json format only - should be lowercase and have correct json format -- Statement: "

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
    tweet_id = row['tweet_id']

    # Convert image to base 64
    base64encodedString = convert_to_base64("data/images/abortion/" + tweet_id + ".jpg")
    image_description = get_image_details(base64encodedString)
    # print(image_description)
    if image_description is None:
        image_description = "No description available"
    response_json = send_message(baseprompt + tweet_text + "Description of photo: " + image_description,4096)
    print(response_json)
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

