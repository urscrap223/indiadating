# coding=utf-8
import json

import config
import requests

headers = {
    'app_version': '6.9.4',
    'platform': 'ios',
    "content-type": "application/json",
    "User-agent": "Tinder/9.0.0 (iPhone; iOS 10.3.2; Scale/2.00)",
}


def get_auth_token(fb_auth_token, fb_user_id):
    if "error" in fb_auth_token:
        return {"error": "could not retrieve fb_auth_token"}
    if "error" in fb_user_id:
        return {"error": "could not retrieve fb_user_id"}
    url = "https://api.gotinder.com/v2/auth/login/facebook"
    req = requests.post(url,
                        headers=headers,
                        data=json.dumps(
                            {'token': fb_auth_token, 'facebook_id': fb_user_id})
                        )
    try:
        print(req.json())
        tinder_auth_token = req.json()["data"]["api_token"]
        headers.update({"X-Auth-Token": tinder_auth_token})
        print("You have been successfully authorized!")
        return tinder_auth_token
    except Exception as e:
        print(e)
        return {"error": "Something went wrong. Sorry, but we could not authorize you."}


def authverif():
    res = get_auth_token(config.fb_access_token, config.fb_user_id)
    if "error" in res:
        return False
    return True


def get_recommendations():
    '''
    Returns a list of users that you can swipe on
    '''
    try:
        r = requests.get('https://api.gotinder.com/user/recs', headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong with getting recomendations:", e)


def get_updates(last_activity_date=""):
    '''
    Returns all updates since the given activity date.
    The last activity date is defaulted at the beginning of time.
    Format for last_activity_date: "2017-07-09T10:28:13.392Z"
    '''
    try:
        url = config.host + '/updates'
        r = requests.post(url,
                          headers=headers,
                          data=json.dumps({"last_activity_date": last_activity_date}))
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong with getting updates:", e)


def get_self():
    '''
    Returns your own profile data
    '''
    try:
        url = config.host + '/profile'
        r = requests.get(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not get your data:", e)


def get_meta():
    '''
    Returns meta data on yourself. Including the following keys:
    ['globals', 'client_resources', 'versions', 'purchases',
    'status', 'groups', 'products', 'rating', 'tutorials',
    'travel', 'notifications', 'user']
    '''
    try:
        url = config.host + '/meta'
        r = requests.get(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not get your metadata:", e)

def update_location(lat, lon):
    '''
    Updates your location to the given float inputs
    Note: Requires a passport / Tinder Plus
    '''
    try:
        url = config.host + '/passport/user/travel'
        r = requests.post(url, headers=headers, data=json.dumps({"lat": lat, "lon": lon}))
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not update your location:", e)

def reset_real_location():
    try:
        url = config.host + '/passport/user/reset'
        r = requests.post(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not update your location:", e)


def get_recs_v2():
    '''
    This works more consistently then the normal get_recommendations becuase it seeems to check new location
    '''
    try:
        url = config.host + '/v2/recs/core?locale=en-US'
        r = requests.get(url, headers=headers)
        return r.json()
    except Exception as e:
        print('excepted')

def set_webprofileusername(username):
    '''
    Sets the username for the webprofile: https://www.gotinder.com/@YOURUSERNAME
    '''
    try:
        url = config.host + '/profile/username'
        r = requests.put(url, headers=headers,
                         data=json.dumps({"username": username}))
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not set webprofile username:", e)

def reset_webprofileusername(username):
    '''
    Resets the username for the webprofile
    '''
    try:
        url = config.host + '/profile/username'
        r = requests.delete(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not delete webprofile username:", e)

def get_person(id):
    '''
    Gets a user's profile via their id
    '''
    try:
        url = config.host + '/user/%s' % id
        r = requests.get(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not get that person:", e)


def send_msg(match_id, msg):
    try:
        url = config.host + '/user/matches/%s' % match_id
        r = requests.post(url, headers=headers,
                          data=json.dumps({"message": msg}))
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not send your message:", e)


def superlike(person_id):
    try:
        url = config.host + '/like/%s/super' % person_id
        r = requests.post(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not superlike:", e)


def like(person_id):
    try:
        url = config.host + '/like/%s' % person_id
        r = requests.get(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not like:", e)


def dislike(person_id):
    try:
        url = config.host + '/pass/%s' % person_id
        r = requests.get(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not dislike:", e)


def report(person_id, cause, explanation=''):
    '''
    There are three options for cause:
        0 : Other and requires an explanation
        1 : Feels like spam and no explanation
        4 : Inappropriate Photos and no explanation
    '''
    try:
        url = config.host + '/report/%s' % person_id
        r = requests.post(url, headers=headers, data={
                          "cause": cause, "text": explanation})
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not report:", e)


def match_info(match_id):
    try:
        url = config.host + '/matches/%s' % match_id
        r = requests.get(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not get your match info:", e)

def all_matches():
    try:
        url = config.host + '/v2/matches'
        r = requests.get(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not get your match info:", e)
