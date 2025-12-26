from functions.run_python_file import run_python_file

def print_test(title, result):
    print(f"--- {title} ---")
    print(result)
    print("-" * 40 + "\n")

# 1. Basic execution (usage instructions)
print_test("Test: main.py usage", 
           run_python_file("calculator", "main.py"))

# 2. Execution with arguments
print_test("Test: main.py with 3 + 5", 
           run_python_file("calculator", "main.py", ["3 + 5"]))

# 3. Running existing tests
print_test("Test: calculator tests.py", 
           run_python_file("calculator", "tests.py"))

# 4. Security: Path Traversal
print_test("Test: Security (Outside Dir)", 
           run_python_file("calculator", "../main.py"))

# 5. Existence check
print_test("Test: Non-existent file", 
           run_python_file("calculator", "nonexistent.py"))

# 6. File type check
print_test("Test: Non-python file", 
           run_python_file("calculator", "lorem.txt"))