with open('nexuslang.py', 'r') as f:
    content = f.read()

# Fix the datetime.strptime issue
content = content.replace("'strptime': datetime.strptime", "'strptime': lambda fmt,s: __import__('datetime').datetime.strptime(s,fmt)")

with open('nexuslang.py', 'w') as f:
    f.write(content)

print("✅ Fixed!")
