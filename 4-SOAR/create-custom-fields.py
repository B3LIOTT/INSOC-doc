import requests

# Configuration
API_URL = "http://IP:9000/api/customField"
API_KEY = "API_KEY"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


CUSTOM_FIELDS = [   
    {"name": "agent_name", "reference": "agent_name", "description": "Nom de l'agent", "type": "string", "mandatory": False},
    {"name": "agent_id", "reference": "agent_id", "description": "ID de l'agent", "type": "string", "mandatory": False},
    {"name": "agent_ip", "reference": "agent_ip", "description": "Adresse IP de l'agent", "type": "string", "mandatory": False},
    {"name": "src_ip", "reference": "src_ip", "description": "Adresse IP source", "type": "string", "mandatory": False},
    {"name": "src_port", "reference": "src_port", "description": "port source", "type": "string", "mandatory": False},
    {"name": "dest_ip", "reference": "dest_ip", "description": "Adresse IP de destination", "type": "string", "mandatory": False},
    {"name": "dest_port", "reference": "dest_port", "description": "port de destination", "type": "string", "mandatory": False},
    {"name": "protocol", "reference": "protocol", "description": "Protocol", "type": "string", "mandatory": False},
    {"name": "url", "reference": "url", "description": "url", "type": "string", "mandatory": False}
]


def create_custom_field(field):
    response = requests.post(API_URL, json=field, headers=HEADERS)

    if response.status_code == 201:
        print(f"[+] Custom field '{field['name']}' créé avec succès.")
    else:
        print(f"[!] Erreur ({response.status_code}) pour '{field['name']}': {response.text}")



if __name__ == "__main__":

    for field in CUSTOM_FIELDS:
        create_custom_field(field)
