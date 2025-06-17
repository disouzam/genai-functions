from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL
import json
from functions import get_my_location, get_current_weather

client = OpenAI(api_key=OPENAI_API_KEY)

def create_function_definitions():
    """
    Define the function schemas for the assistant to use.

    Returns:
        list: A list of function definitions.
    """
    functions = [
        {
            "type": "function",
            "name": "get_my_location",
            "description": "Get my latitude and longitude location",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "type": "function",
            "name": "get_current_weather",
            "description": "Get current temperature for provided coordinates in celsius.",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "number"},
                    "longitude": {"type": "number"}
                },
                "required": ["latitude", "longitude"],
                "additionalProperties": False
            },
        },
    ]
    return functions

# Observation
def process_user_message(messages):
    while True:
        # Reasoning
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            functions=create_function_definitions(),
        )

        response_message = response.choices[0].message

        # Action
        if response_message.function_call:
            function_name = response_message.function_call.name
            arguments = json.loads(response_message.function_call.arguments)

            if function_name == "get_current_weather":
                function_response = get_current_weather(
                    arguments["latitude"], arguments["longitude"]
                )
            elif function_name == "get_my_location":
                function_response = get_my_location()
            else:
                raise ValueError(f"Unknown function name: {function_name}")

            # Result
            messages.append(response_message)
            messages.append({
                "role": "function",
                "name": function_name,
                "content": json.dumps(function_response),
            })
        else:
            # Final Answer
            return response_message.content

