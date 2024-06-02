import requests
from flask import json
import sys
import os

SCRIPT_DIRP = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIRP))

BASE = "http://127.0.0.1:5000"

from application import db 

#--------------------------------------------------- EscalateTicketAPI -----------------------------------------------------------

url_escalate = BASE + "/api/escalate_to_gspace"

def test_ticket_escalate_success_200():
    input_dict = {"ticket_id": 1, "role_id" : 2, "is_escalated" : 0}  
    headers = {'Content-Type': 'application/json'}
    request=requests.post(url = url_escalate,json = input_dict, headers=headers) 
    response = request.json()
    assert request.status_code == 200
    assert response['message'] == "Ticket escalated successfully"
    
def test_ticket_escalate_id_missing_400():
    input_dict = {"ticket_id": None, "role_id" : 2, "is_escalated" : 1}
    headers = {'Content-Type': 'application/json'}
    request=requests.post(url = url_escalate,json = input_dict, headers=headers)
    response = request.json()
    assert request.status_code == 400
    assert response['error'] == "Ticket ID is required"

def test_ticket_already_escalated_201():
    input_dict = {"ticket_id": 2, "role_id" : 2, "is_escalated" : 1}
    headers = {'Content-Type': 'application/json'}
    request=requests.post(url = url_escalate,json = input_dict, headers=headers) 
    response = request.json()
    assert request.status_code == 201
    assert response['message'] == "Ticket is already escalated"

#--------------------------------------------- UnresolvedTicketsNotification -----------------------------------------------------

url_unresolve_ticket_notification_get = BASE + "/api/notifications/unresolved_tickets"

def test_unresolved_ticket_notification_200():
    header={"Content-Type":"application/json"}
    request = requests.get(url_unresolve_ticket_notification_get,headers=header)   
    assert request.status_code == 200
    assert type(request.json()["notifications"]) == list

#---------------------------------------------- EscalatedTicketNotification ------------------------------------------------------
    
url_escalate_notify = BASE + "/api/notifications/escalated_tickets"

def test_escalate_notify_200():
    header={"Content-Type":"application/json"}
    response = requests.get(url_escalate_notify,headers=header)
    assert response.status_code == 200
    assert type(response.json()["notifications"]) == list # Check if the response is the same data type as expected
    
# #--------------------------------------------------- FetchPotentialBan -----------------------------------------------------------
    
url_potential_ban_get = BASE + "/api/get_flagged_users"

def test_potential_ban_200():
    header={"Content-Type":"application/json"}
    request = requests.get(url_potential_ban_get,headers=header)
    assert request.status_code == 200
    assert type(request.json()) == list # Check if the response is the same data type as expected

# #---------------------------------------------------- ViewFlaggedPost ------------------------------------------------------------
    
url_flag_get = BASE + "/api/get_flagged_posts"
url_flag_post = BASE + "/api/get_flagged_posts"

def token_login_support_agent():
    url=BASE+"/login"
    data={"email":"admin@gmail.com","password":"pass@1234"}
    response=requests.post(url,data=data)
    return response.json()["token"]
    
def test_view_flag_post_400():
    header={"secret_authtoken":token_login_support_agent(),"Content-Type":"application/json"}
    response = requests.get(url_flag_get,headers=header)        
    assert response.status_code == 400    
    response_data = response.json()
    assert response_data["error"] == "User ID is required"

def test_view_flag_post_200():
    header={"secret_authtoken":token_login_support_agent(),"Content-Type":"application/json"}
    params = {'user_id': 1} 
    request = requests.get(url_flag_post,params=params,headers=header)  
    assert request.status_code == 200
    assert type(request.json()) == list # Check if the response is the same data type as expected

#------------------------------------------------- BanUsersNotifications ---------------------------------------------------------

url_ban_user = BASE + "/api/ban_user"

def test_ban_user_200():
    input_dict = {"user_id": 4}  
    headers = {'Content-Type': 'application/json'}
    request=requests.post(url = url_ban_user,json = input_dict, headers=headers) 
    response = request.json()
    assert request.status_code == 200
    assert response["message"] == "User blocked and login disabled successfully"

def test_ban_user_400():
    input_dict = {"user_id": None}
    headers = {'Content-Type': 'application/json'}
    request=requests.post(url = url_ban_user,json = input_dict, headers=headers)
    response = request.json()
    assert request.status_code == 400
    assert response["message"] == "User ID is required"

def test_ban_user_404():
    input_dict = {"user_id": 100}  
    headers = {'Content-Type': 'application/json'}
    request=requests.post(url = url_ban_user,json = input_dict, headers=headers) 
    response = request.json()
    assert request.status_code == 404
    assert response["message"] == "User not found"

#--------------------------------------------------- DiscourseTopicAPI -----------------------------------------------------------
    
url_discourse_topic = BASE + "/api/discourse/topics"

def test_discourse_topic_200():
    input_dict = {
        "created_by": 3,
        "ticket_id": 9993,
        "title": "9993",
        "raw": "asjdhkajshajsf"
    }
    headers = {'Content-Type': 'application/json; charset=utf-8', 'Accept':'/'}
    request = requests.post(url=url_discourse_topic, json = input_dict, headers=headers)
    response = request.json()
    assert request.status_code == 200

def test_discourse_topic_201():
    input_dict = {
        "created_by": 7,
        "ticket_id": 9,
        "title": "first post testing",
        "raw": "abcdefghijklmnopqrstuv"
    }
    headers = {'Content-Type': 'application/json; charset=utf-8', 'Accept':'/'}
    request = requests.post(url=url_discourse_topic, json = input_dict, headers=headers)
    response = request.json()
    assert request.status_code == 201

def test_discourse_topic_403():
    input_dict = {
        "created_by": 3,
        "ticket_id": None,
        "title": "first post testing",
        "raw": "abcdefghijklmnopqrstuv"
    }
    headers = {'Content-Type': 'application/json; charset=utf-8', 'Accept':'/'}
    request = requests.post(url=url_discourse_topic, json = input_dict, headers=headers)
    response = request.json()
    assert request.status_code == 403
