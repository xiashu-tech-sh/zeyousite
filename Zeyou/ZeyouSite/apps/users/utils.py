import re


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    print(user.department)
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username,
        'department': user.department,
        "status": 200
    }
