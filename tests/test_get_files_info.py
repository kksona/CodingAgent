from functions.get_files_info import get_files_info

# Test 1: Current Directory
print('get_files_info("calculator", "."):')
print('Result for current directory:')
print(f"  {get_files_info('calculator', '.')}\n")

# Test 2: Subdirectory
print('get_files_info("calculator", "pkg"):')
print("Result for 'pkg' directory:")
print(f"  {get_files_info('calculator', 'pkg')}\n")

# Test 3: Outside Directory (Absolute-style)
print('get_files_info("calculator", "/bin"):')
print("Result for '/bin' directory:")
print(f"    {get_files_info('calculator', '/bin')}\n")

# Test 4: Path Traversal Attempt
print('get_files_info("calculator", "../"):')
print("Result for '../' directory:")
print(f"    {get_files_info('calculator', '../')}")

#Test 5: Unknown File Retrieval
print('get_files_info("calculator", "home.csv"):')
print("Result for 'home.csv' directory:")
print(f"    {get_files_info('calculator', 'home.csv')}")
