import os
import sys
from fastapi.testclient import TestClient
import pytest
import random
import string
from app.main import app

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

client = TestClient(app)

""" Testing all Gets"""

def test_get_bot_scripts():
    response = client.get("/select-all-from-bot-scripts")
    assert response.status_code == 200

def test_frankenbert():
    test = 'A women walked her dog down the street and cop waved to her'
    response = client.get(f'/frankenbert/{test}')
    assert response.status_code == 200
    response_body = response.json()
    assert 'Rank' in response_body['Rank'] 
    assert response_body['Rank'][5] in ['0', '1', '2', '3', '4', '5']
    assert '%' in response_body['Confidence'] 


def test_view_data():
    response = client.get('/view-data')
    assert response.status_code == 200
    response_body = response.json()
    assert len(response_body) == 5000


def test_to_approve():
    response = client.get('/view-data')
    assert response.status_code == 200


def test_advance_all():
    response = client.get('/advance-all')
    assert response.status_code == 200


"""Test all Posts"""

#yes
def test_form_in():
    response = client.post(
        '/form-in/',
        json={
                "city": "cHicago",
                "state": "ILLInoIs",
                "confidence": random.random(),
                "description": random_gen(0, 1000),
                "force_rank": "1",
                "incident_date": "09/09/2021", 
                "incident_id": 1224, #Most respect foriegn key constraint
                "lat": random.randint(0, 50),
                "long": random.randint(0, 50),
                "src": [f"https://twitter.com/{random_gen(0,20)}"],
                "status": "approved",
                "title": random_gen(0, 20),
                "tweet_id": random_gen(1, 19),
                "user_name": random_gen(0, 25)
        } 
    )
    assert response.status_code == 200

#yes
def test_form_out():
    response = client.post(
        '/form-out/',
        json={
            "form" : 1000,
            "incident_id" : 1224,
            "link": f"https://twitter.com/{random_gen(0,20)}",
            "tweet_id" : random_gen(1, 19),
            "user_name": random_gen(0, 25)
        }
    )
    assert response.status_code == 200

#yes
def test_approval_check():
    response = client.post(
        '/approval-check/',
        json={
            "tweet_id" : "1441464533348806658"
        }
    )
    assert response.status_code == 200

#yes
def test_approve_check():
    response = client.post(
        '/approve/',
        json={
            "tweet_id" : "1441464533348806658"
        }
    )

    assert response.status_code == 200

def test_approval_reconciliation():

    response1 = client.post(
        '/approval_reconciliation/',
        json={
            "incident_id": 1224, 
            "action": 1
        }
    )

    assert response1.status_code == 200


#yes
def test_add_script():
    response = client.post(
        '/add-script/',
        json={
            "script_id": random.randint(0,20),
            "script" : random_gen(0, 50),
            'convo_node': random.randint(0,20),
            "use_count": random.randint(0,10),
            "success_rate": random.randint(0,100),
            "active": True
        }
    )

    assert response.status_code == 200

#yes
def test_deactivate_script():
    #see script tracking file , not yet implemented
    pass

#yes
def test_activate_script():
    # see script tracking file, not yet implemented
    pass


def random_gen(type, nums):
    """type : 0 for letters, type : 1 for string_nums"""
    if type == 0:
        return f"{''.join(random.choice(string.ascii_letters) for i in range(nums))}"
    if type == 1:
        return f"{''.join(random.choice(string.digits) for i in range(nums))}"
    else:
        raise AssertionError('type option must be 0 or 1')

