import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from functions.call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Autonomous Coding Agent")
parser.add_argument("user_prompt", type=str)
parser.add_argument("--verbose", action="store_true")
args = parser.parse_args()

# Initialize the conversation history
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

MAX_ITERATIONS = 20

# --- THE FEEDBACK LOOP ---
for i in range(MAX_ITERATIONS):
    try:
        # 1. Call the LLM with the full conversation history
        response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
            )
        )

        # 2. Add the Model's thoughts/calls to the conversation history
        for candidate in response.candidates:
            messages.append(candidate.content)

        # 3. Check if the model is finished
        # It's finished if there are NO function calls AND it gave us text
        if not response.function_calls and response.text:
            print(f"\nFinal Response:\n{response.text}")
            break

        # 4. If there are function calls, execute them
        if response.function_calls:
            results_parts = []
            for function_call in response.function_calls:
                # Call the function (validation happens inside call_function)
                function_call_result = call_function(function_call, verbose=args.verbose)
                
                # Append the Part object (which contains the FunctionResponse)
                results_parts.append(function_call_result.parts[0])

            # 5. Add the Tool results back to history with the role of 'user'
            # (Note: In some SDK versions, the role is 'tool'; use what your SDK expects)
            messages.append(types.Content(role="user", parts=results_parts))

    except Exception as e:
        print(f"Error during iteration {i}: {e}")
        break
else:
    print(f"Reached maximum iterations ({MAX_ITERATIONS}). Stopping.")