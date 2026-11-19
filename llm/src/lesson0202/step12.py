# https://stepik.org/lesson/2075122/step/12?unit=2104233

def is_safe_request(messages: list) -> bool:
    has_msg_from_system_role: bool = False

    for message in messages:
        if type(message) != dict:
            return False
        elif 'role' not in message or 'content' not in message:
            return False
        elif not has_msg_from_system_role:
            has_msg_from_system_role = (message['role'] == 'system')

    return has_msg_from_system_role
