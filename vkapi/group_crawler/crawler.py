from .execute_database import *
from .recommendations import *
from .parameters import *
 
def just_recommendations(public_id):
    session = vk.Session()
    api = vk.API(session)
    dbo = ExecuteDataBaseOperator(api, access_token, user_token, version)
    return get_recommendations(public_id, dbo, members_to_proceed=200, top=100, output=True)

