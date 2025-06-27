import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from available_functions import available_functions
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

print(sys.argv)

# Verificación de la existencia del prompt
if len(sys.argv) < 2:
    print("Message not provided")
    sys.exit(1)
    
user_prompt = sys.argv[1]

# Creación de la conversación    
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
for _ in range(0, 20):
    # Petición de la respuesta al prompt
    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages,
                                            config=types.GenerateContentConfig(tools=[available_functions], 
                                                                                system_instruction=system_prompt),)

    for candidate in response.candidates:
        messages.append(types.Content(role="model", parts=[types.Part(text=str(candidate.content.parts[0].text))]))
        
    if response.function_calls:
        function_result = call_function(response.function_calls[0], "--verbose" in sys.argv)
        if function_result.parts[0].function_response.response:
            print(f"-> {function_result.parts[0].function_response.response}")
            messages.append(types.Content(role="user", parts=[types.Part(text=str(function_result.parts[0].function_response.response))]))
        else:
            raise Exception("It was not posible to run the function")
    else:
        print(response.text)

    if "--verbose" in sys.argv:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")