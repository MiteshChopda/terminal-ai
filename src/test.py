from api_call import api_call

data ="a simple python file with 50 lines of code"
for role, content in api_call(data):
    print(role, content)
