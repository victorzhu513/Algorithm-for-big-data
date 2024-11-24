import os
import requests

cwd = dir_path = os.path.dirname(os.path.realpath(__file__))
gunControlImages = cwd + "\\data\\images\\gun_control"
abortonImages = cwd + "\\data\\images\\abortion"

gunControlTweets = cwd + "\\data\\gun_control_train"
abortionTweets = cwd + "\\data\\abortion_train"


# Configure your Ollama API endpoints and keys
OLLAMA_API_URL = "http://localhost:11434/api/chat"
API_KEY = "~/.ollama/id_ed25519.pub"

# Helper function to call the Ollama API for text analysis
def analyze_text(content):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "type": "text",
        "content": content,
        "model": "llama3.2",
    }

    response = requests.post(OLLAMA_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Helper function to call the Ollama API for image analysis
def analyze_image(image_path):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
    }
    files = {
        "file": open(image_path, "rb"),
    }
    response = requests.post(OLLAMA_API_URL, headers=headers, files=files)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Function to determine stance and persuasiveness
def evaluate_content(tweet_text, image_path=None):
    # Analyze the text of the tweet
    text_analysis = analyze_text(tweet_text)
    if not text_analysis:
        return None

    image_analysis = None
    # Analyze the image if provided
    if image_path:
        image_analysis = analyze_image(image_path)
        if not image_analysis:
            return None

    # Compile results
    results = {
        "text_analysis": text_analysis,
        "image_analysis": image_analysis if image_path else "No image analyzed",
    }

    return results

# Example Usage
if __name__ == "__main__":


    prompt = "We want you to analyze tweets and images to see if they are pro-gun reform or anti-gun reform as well as if the tweet was persuasive or not"

    image_path = None
    # Example tweet text
    test = analyze_text(prompt)
    



    tweet = "We need stricter gun control laws to ensure public safety!"

    # Example image path (leave None if no image)

    analysis_results = evaluate_content(tweet, image_path)

    

    if analysis_results:
        print("Analysis Results:")
        print("Text Analysis:", analysis_results["text_analysis"])
        print("Image Analysis:", analysis_results["image_analysis"])
    else:
        print("Failed to analyze the content.")