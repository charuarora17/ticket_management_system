import requests
url = "http://localhost:4200/users.json"
headers = {"Accept": "*/*",
"Api-Username": "21f1004416",
"Api-Key": "7f85cd0f1ead062e623976cff7d98d47a3ce80f2be98a0fce7c7e424eba44b3f"}


users = [('Piyush','piyush@gmail.com','piyush@1234','piyush'),('Puravasu','puravasu@gmail.com','puravasu@1234','puravasu'),('Abhay','abhay@gmail.com','abhay@1234','abhay'),('Khushee','khushee@gmail.com','khushee@1234','khushee'),('Harshil','harshil@gmail.com','harshil@1234','harshil'),('Jigyasa','jigyasa@gmail.com','jigyasa@1234','jigyasa'),('Dhruv','dhruv@gmail.com','dhruv@1234','dhruv')]
for u in users:
    data = {
        "name":u[0],
        "email":u[1],
        "password":u[2],
        "username":u[3],
        "active":True
    }
    response = requests.post(url, headers=headers, json=data)
    print("\n\nStatus Code", response.status_code)
    if response.status_code != 200:
        print("JSON Response ", response.json())
