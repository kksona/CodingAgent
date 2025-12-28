import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
import datetime

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



log_file = "agent_session_logs.md"
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open(log_file, "a", encoding="utf-8") as f:
    f.write(f"\n# Session Log: {timestamp}\n")
    f.write(f"**Initial Prompt:** {args.user_prompt}\n\n")
    f.write("## Detailed Thought Process & Tool Usage:\n")
    
    for msg in messages:
        role = msg.role
        for part in msg.parts:
            # 1. Log Model's text thoughts
            if hasattr(part, 'text') and part.text:
                f.write(f"> **{role.capitalize()}**: {part.text}\n\n")
            
            # 2. Log Tool Calls (The "Command")
            if hasattr(part, 'function_call') and part.function_call:
                f.write(f"- 🛠️ **Tool Call**: `{part.function_call.name}` with args: `{part.function_call.args}`\n")
            
            # 3. Log Tool Responses (The "Output") - FIXED ATTRIBUTE HERE
            if hasattr(part, 'function_response') and part.function_response:
                # The SDK uses .response to store the tool's output
                tool_output = getattr(part.function_response, 'response', 'No output')
                f.write(f"- 📤 **Tool Result**: \n```json\n{tool_output}\n```\n\n")
                
    f.write("\n" + "="*40 + "\n")

print(f"\n[Detailed history logged to {log_file}]")