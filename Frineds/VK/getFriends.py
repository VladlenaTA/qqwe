import vk
from VK.auth_vk import auth_vk_token

V = '9.95'

session = auth_vk_token()
api = vk.API(session, v=V)


def get_friends(user_id):
    return api.friends.get(user_id=user_id)['items']


def get_name(user_id):
    userInfo = api.users.get(user_id=user_id)[0]

    return f"{userInfo['first_name']} {userInfo['last_name']}"
