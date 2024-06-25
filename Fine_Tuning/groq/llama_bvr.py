import os
import json
from datetime import datetime
from groq import Groq 

client = Groq(
    api_key="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",
)

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
persona = "Teemu"
home_location = "Madrid"

schema = memory_schema = {
  "type": "object",
  "properties": {
    "date": {
      "type": "string",
      "description": "The current date (YYYY-MM-DD HH-MM-SS format)"
    },
    "me": {
      "type": "array",
      "description": "My name"
    },
    "people": {
      "type": "array",
      "description": "List of people involved in the event (optional)"
    },
    "feeling": {
      "type": "string",
      "description": "The main character's feeling during the event"
    },
    "short_description": {
      "type": "string",
      "description": "A brief description of the event"
    },
    "weather": {
      "type": "string",
      "description": "Current weather conditions (e.g., sunny, rainy, cloudy)"
    },
    "location": {
      "type": "string",
      "description": "Location name (e.g., city, town)"
    },
    "insight": {
      "type": "string",
      "description": "Additional details or insights about the event"
    },
    "memorable_because": {
      "type": "string",
      "description": "The reason why the event is memorable"
    }
  }
}

with open("my_schema.json", "w") as f:
  json.dump(schema, f)

with open("my_schema.json", "r") as f:
  my_schema = json.load(f)

prompt_by_user = "Today was sunny day and then rained, I went to city to have a dinner with friends and I ate the best Sushi I have ever tested in restaurant called Sushita Cafe, where my friend Paco is a chef."

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": f"You are helpful memory recorder.\nWrite outputs in JSON in schema: {my_schema}.\nCurrent time is {now}.\nI am {persona} living in {home_location} and events may take place in more specific places inside the home location or outside it, so record precisely.\n",
            #"content": "You are helpful memory recorder. Write outputs in JSON schema.\n",
            #f" The JSON object must use the schema: {json.dumps(my_schema.model_json_schema(), indent=1)}",
        },
        {
            "role": "user",
            "content": "Today was sunny day and then rained, I went to city to have a dinner with friends and I ate the best Sushi I have ever tested in restaurant called Sushita Cafe, where my friend Paco is a chef.",
        }
    ],
    model="llama3-70b-8192",
    response_format={"type": "json_object"},
)

print(chat_completion.choices[0].message.content)