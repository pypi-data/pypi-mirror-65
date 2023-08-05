import os
from math import ceil

from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0
import singer

DEFAULT_PER_PAGE = 100

CONFIG = {
    "domain": None,
    "non_interactive_client_id": None,
    "non_interactive_client_secret": None,
    "per_page": DEFAULT_PER_PAGE,
}

def get_auth0_client():
    get_token = GetToken(CONFIG['domain'])
    token = get_token.client_credentials(CONFIG['non_interactive_client_id'],
        CONFIG['non_interactive_client_secret'], 
        'https://{}/api/v2/'.format(CONFIG['domain']))
    mgmt_api_token = token['access_token']
    return Auth0(CONFIG['domain'], mgmt_api_token)

def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)

def load_schema(entity_name):
    schema = singer.utils.load_json(get_abs_path('schemas/{}.json'.format(entity_name)))
    return schema

def list_all_users():
    auth0 = get_auth0_client()
    users_schema = load_schema('users')
    singer.write_schema('users', users_schema, 'user_id')
    # Initial query to list first batch of users
    resp = auth0.users.list(per_page=CONFIG["per_page"])
    singer.write_records('users', resp["users"])
    # If additional users to list, query more
    if "total" in resp.keys() and resp["total"] > CONFIG["per_page"]:
        amount_of_additional_queries = ceil(resp["total"] / CONFIG["per_page"]) - 1
        if amount_of_additional_queries > 0:
            for i in range(amount_of_additional_queries):
                resp = auth0.users.list(per_page=CONFIG["per_page"], page=i+1)
                singer.write_records('users', resp["users"])

def main_impl():
    args = singer.utils.parse_args([
        "domain",
        "non_interactive_client_id",
        "non_interactive_client_secret"])
        
    CONFIG.update(args.config)

    list_all_users()
    
def main():
    try:
        main_impl()
    except Exception as exc:
        raise exc

if __name__ == '__main__':
    main()