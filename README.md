# Autonomous AI Coding Agent

An autonomous, multi-turn AI agent built with Python and the Google Gemini 2.0 Flash API. This system enables an LLM to navigate, analyze, and modify a local codebase through a self-correcting "Plan-Act-Observe" feedback loop.

## Key Features

* **Autonomous Feedback Loop**: Implements a robust cycle where the model uses tool outputs (including error messages) to inform its next decision, allowing for multi-step problem solving.
* **Secure Code Execution**: Runs Python code in a controlled subprocess with a 30-second timeout and strict directory sandboxing to prevent resource exhaustion.
* **Toolbox Architecture**: Uses JSON Schema declarations via `types.FunctionDeclaration` to expose local Python functions to the LLM.
* **Stateful Memory**: Manages a complex conversation history of `FunctionCalls` and `FunctionResponses`, enabling the agent to "remember" findings from previous steps.
* **Security Sandboxing**: Prevents directory traversal attacks by normalizing paths and validating them against a permitted working directory.

## Technical Stack

* **Language**: Python 3.10+
* **LLM**: Google Gemini 2.0 Flash
* **API**: Google Generative AI SDK (`google-genai`)
* **Environment Management**: `python-dotenv`

## Project Structure

```text
├── functions/
│   ├── get_files_info.py     # Maps directory structure and metadata
│   ├── get_file_content.py   # Securely reads file contents
│   ├── write_file.py         # Writes or overwrites file data
│   ├── run_python_file.py    # Executes Python code via subprocess
│   └── call_function.py      # The "Dispatcher" and Tool definitions
├── prompts.py                # System instructions and Agent behavior
├── main.py                   # The core agentic loop logic
└── .env                      # API Credentials (ignored by git)