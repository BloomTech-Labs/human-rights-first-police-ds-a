import requests
r = requests.post('http://127.0.0.1:8000/form_out', data={"form":1, "incident_id":1, "isChecked":"false", "link":"https://a.humanrightsfirst.dev/edit/1426290795267731463", "tweet_id":"1424511565932359685", "user_name":"witt_rowen"})

print(r.json())
