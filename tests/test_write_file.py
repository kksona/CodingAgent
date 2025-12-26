from functions.write_file import write_file

# Test 1: Overwrite existing file (lorem.txt)
print('Test 1: Overwriting lorem.txt')
print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
print("-" * 20)

# Test 2: Create new file in a subdirectory (pkg/morelorem.txt)
print('Test 2: Writing to a new subdirectory file')
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
print("-" * 20)

# Test 3: Security Test (Outside directory)
print('Test 3: Attempting to write outside working directory')
print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))