from functions.get_file_content import get_file_content

def run_test(label, working_dir, path):
    print(f"--- {label} ---")
    result = get_file_content(working_dir, path)
    
    # Special handling for lorem test to avoid wall of text
    if "lorem.txt" in path and "Error:" not in result:
        print(f"Content Length: {len(result)} characters")
        print(f"Ends with: {result[-60:].strip()}")
    else:
        print(result)
    print("\n")

# 1. Truncation Test
run_test("Testing lorem.txt truncation", "calculator", "lorem.txt")

# 2. Regular File Tests
run_test("Testing main.py", "calculator", "main.py")
run_test("Testing pkg/calculator.py", "calculator", "pkg/calculator.py")

# 3. Security Test
run_test("Testing /bin/cat (Outside Dir)", "calculator", "/bin/cat")

# 4. Missing File Test
run_test("Testing non-existent file", "calculator", "pkg/does_not_exist.py")