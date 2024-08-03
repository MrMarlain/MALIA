line = "Hello world!\n\0"
for char in line:
    print(f'{ord(char)}')
print(f'count: {len(line)}')