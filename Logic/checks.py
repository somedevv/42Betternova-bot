import os, requests

def get_user(userid):
    url = '{}/api/users/{}/login42'.format(os.environ['API_BASE_URL'], str(userid))
    hed = {'Authorization': 'Bearer {}'.format(os.environ["API_TOKEN"])}
    response = requests.get(url, headers=hed)
    if response.status_code == 200 and response.json()['login42'] is not None:
        return response.status_code, response.json()['login42']
    else:
        return response.status_code, None