
import requests
import webbrowser
import json

TOKEN_URL = 'https://www.bungie.net/platform/app/oauth/token/'
API_KEY = '35df7ca970834f178dd261d181eedaea'
CLIENT_ID = '48220'
REDIRECT_URI = 'https://someonesvault.github.io/'
AUTH_URL = f'https://www.bungie.net/en/OAuth/Authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}'
CLIENT_SECRET = 'VCMsXHZ0TmTHj-Vb1IoF4mMMCzqwjfgwUolpubYR5rA'
BASE_URL = 'https://www.bungie.net/Platform/Destiny2/'

# Open the authorization URL in the user's browser (most important)
webbrowser.open(AUTH_URL)

TOKEN_URL = 'https://www.bungie.net/platform/app/oauth/token/'

HEADERS = {
    'X-API-Key': API_KEY
}

def get_destiny_manifest(api_key):
    # Function to get and save Destiny manifest
    url = "https://www.bungie.net/Platform/Destiny2/Manifest/"
    headers = {
        "X-API-Key": API_KEY
    }
    response = requests.get(url, headers=headers)
    return response.json()

def get_item_data(manifest, api_key, item_type):
    item_data = []
    for key, value in manifest['Response']['jsonWorldComponentContentPaths']['en'].items():
        if 'DestinyInventoryItemDefinition' in key:
            url = f"https://www.bungie.net{value}"
            headers = {
                "X-API-Key": api_key
            }
            response = requests.get(url, headers=headers)
            items = response.json()
            for item in items.values():
                if item.get('itemType') == item_type:
                    item_data.append((item['hash'], item['displayProperties']['name']))
    return item_data

def save_item_data(item_data, filename):
    with open(filename, 'w') as f:
        for item_number, name in item_data:
            f.write(f"{item_number}: {name}\n")

#Stating what the class is, making it more user friendly.
CLASS_TYPE_MAP = {
    0: "Titan",
    1: "Hunter",
    2: "Warlock"
}

# Fetch the manifest
manifest = get_destiny_manifest(API_KEY)

# Extract weapon data
weapon_data = get_item_data(manifest, API_KEY, 3)
save_item_data(weapon_data, 'destiny2_weapons.txt')

# Extract armor data
armor_data = get_item_data(manifest, API_KEY, 2)
save_item_data(armor_data, 'destiny2_armor.txt')

TestVar = get_destiny_manifest(API_KEY)

# Save the manifest to a json file
with open('test.json', 'w') as f:
    json.dump(TestVar, f, indent=4)

def get_access_token(auth_code):
    payload = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI
    }
    
    response = requests.post(TOKEN_URL, data= payload)

    if response.status_code == 200:
        token_data = response.json()
        if 'access_token' in token_data:
            return token_data['access_token']
        else:
            print("Error: 'access_token' not found in the response.")
            print(token_data)
            return None
    else:
        print(f"Error: Received status code {response.status_code}")
        print(response.json())
        return None

auth_code = input("Enter the URL Code: ")
access_token = get_access_token(auth_code)

if access_token:
    def get_user_info(access_token):
        url = 'https://www.bungie.net/Platform/User/GetMembershipsForCurrentUser/'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'X-API-Key': API_KEY
        }
        response = requests.get(url, headers=headers)
        return response.json()

    user_info = get_user_info(access_token)
    membership_id = user_info['Response']['destinyMemberships'][0]['membershipId']
    membership_type = user_info['Response']['destinyMemberships'][0]['membershipType']
    print(f"Membership ID: {membership_id}")
    print(f"Membership Type: {membership_type}")

    def get_character_info(membership_id, membership_type, access_token):
        url = f'https://www.bungie.net/Platform/Destiny2/{membership_type}/Profile/{membership_id}/?components=200'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'X-API-Key': API_KEY
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            profile_data = response.json()
            characters = profile_data['Response']['characters']['data']
            character_info = []
            for character_id, character in characters.items():
                class_type = CLASS_TYPE_MAP.get(character['classType'], "Unknown")
                power_level = character['light']
                character_info.append((character_id, class_type, power_level))
            return character_info
        else:
            print(f"Error: Received status code {response.status_code}")
            print(response.json())
            return None

    character_info = get_character_info(membership_id, membership_type, access_token)
    if character_info:
        for char_id, class_type, power_level in character_info:
            print(f"Character ID: {char_id}, Class Type: {class_type}, Power Level: {power_level}")
    else:
        print("Failed to retrieve character information.")
else:
    print("Failed to obtain access token.")

def pullfrompost(item_instance_id, char_id, membership_type):
    payload = {
        'itemReferenceHash': item_instance_id,
        'stackSize' : 1,
        'itemId': item_instance_id,
        'characterId': char_id,
        'membershipType': membership_type
    }

#now we in the moneyy


##def load_weapons(file_path):
 #       weapons = {}
 #       with open(file_path, 'r') as file:
 #           for line in file:
 #               item_instance_id, name = line.strip().split(',')
 #               weapons[name.lower()] = item_instance_id
 #       return weapons
#
 #   def transfer_weapon(item_instance_id, from_character_id, to_character_id=None):
 #       url = 'https://www.bungie.net/Platform/Destiny2/Actions/Items/TransferItem/'
 #       headers = {
 #           'X-API-Key': API_KEY,
 #           'Authorization': f'Bearer {access_token}',
 #           'Content-Type': 'application/json'
 #       }
 #       payload = {
 #           'itemReferenceHash': item_instance_id,
 #           'stackSize': 1,
 #           'transferToVault': to_character_id is None,
 #           'itemId': item_instance_id,
 #           'characterId': from_character_id,
 #           'membershipType': membership_type
 #       }
 #       if to_character_id:
 #           payload['transferToVault'] = False
 #           payload['characterId'] = to_character_id
#
 #       response = requests.post(url, headers=headers, json=payload)
 #       return response.json()
 #   
#
 #   def main():
 #       weapons = load_weapons('destiny2_weapons.txt')
 #       weapon_name = input("Enter the name of the weapon: ").lower()
 #       from_character_id = input("Enter the ID of the character to take the weapon from: ")
 #       to_character_id = input("Enter the ID of the character to transfer the weapon to (or 'vault' to transfer to the vault): ")
#
 #       item_instance_id = weapons.get(weapon_name)
 #       if not item_instance_id:
 #           print("Weapon not found.")
 #           return
#
 #       if to_character_id.lower() == 'vault':
 #           to_character_id = None
#
 #       result = transfer_weapon(item_instance_id, from_character_id, to_character_id)
 #       print(result)
