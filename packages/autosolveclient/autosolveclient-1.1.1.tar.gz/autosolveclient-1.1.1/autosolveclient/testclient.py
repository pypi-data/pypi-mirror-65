from autosolveclient.autosolve import AutoSolve


def receiver_function(json_message):
    print("Task ID :: " + json_message['taskId'])
    print("Site Key :: " + json_message['siteKey'])
    print("Token :: " + json_message['token'])
    print("Created At :: " + json_message['createdAt'])
    print("Version :: " + str(json_message['version']))
    print("Action :: " + json_message['action'])

def cancel_function(json_message):
    print("Task ID :: " + json_message['taskId'])
    print("Site Key :: " + json_message['siteKey'])
    print("Token :: " + json_message['token'])
    print("Created At :: " + json_message['createdAt'])
    print("Version :: " + str(json_message['version']))
    print("Action :: " + json_message['action'])

try:
    auto_solve = AutoSolve({
        "access_token": "clientAccessToken",
        "api_key": "clientApiKey",
        "client_key": "yourClientKey",
        "receiver_function" : receiver_function,
        "should_alert_on_cancel" : cancel_function,
        "debug" : True
    })

    finished = auto_solve.initialized()
except Exception as s:
    print(s)

