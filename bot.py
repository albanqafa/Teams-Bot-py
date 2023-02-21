import requests
import msal
import time
import json


# Define credentials and id's
client_id = "" #Client ID for Azure App Registration
client_secret = "" #Client Secret for Azure App Registration
tenant = "" #Tenant URL
team_id = "" #Team ID
replyurl = "" #Teams channel incoming webhook endpoint
channel_name = "Test" #this is the channel we want to query for messages
scope = [ "https://graph.microsoft.com/.default" ] #Endpoint for MS Graph Authentication
token = ""
channel_id = ""
headers={}
timeout = time.time()


def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def get_token():
	global headers #so we can push token to global headers
	global timeout
	# Create a preferably long-lived app instance which maintains a token cache
	app = msal.ConfidentialClientApplication(
		client_id, authority=tenant,
		client_credential=client_secret,
		# token_cache=... 	# Default cache is in memory only.
							# You can learn how to use SerializableTokenCache from
							# https://msal-python.rtfd.io/en/latest/#msal.SerializableTokenCache
		)
	# The pattern to acquire a token looks like this.
	authentication = None
	# Firstly, looks up a token from cache
	# Since we are looking for token for the current app, NOT for an end user,
	# notice we give account parameter as None.
	authentication = app.acquire_token_silent(scope, account=None)
	if not authentication:
		print("No suitable token exists in cache. Let's get a new one from AAD -")
		authentication = app.acquire_token_for_client(scopes=scope)
	if "access_token" in authentication:
		print("Authentication Success:")
		print("")
		print("	Token expires in: " + str(authentication['expires_in']) + "s")
		print("")
		timeout = time.time() + authentication['expires_in']   # Time we have valid key until
		#print(timeout)
		# Update global token variable
		token = authentication['access_token']
		headers = {'Authorization': 'Bearer ' + token}
	else:
		print("Authentication error:")
		print(authentication.get("error"))
		print(authentication.get("error_description"))
		print(authentication.get("correlation_id"))  # You may need this when reporting a bug
		exit()



def get_channelid():
	global channel_id #use global channel_id not a local one
	# Lets read off channel names in the IT Department channel and print the channel_id for Test
	team_url = f"https://graph.microsoft.com/beta/teams/{team_id}/channels"
	team_response = requests.get(team_url, headers=headers)
	if team_response.status_code == 200:
		channels = team_response.json()["value"]
		for channel in channels:
			if channel["displayName"] == channel_name:
				channel_id = channel["id"]
	else:
		print("Failed to get channel_id")
		print(team_response)

def connector():
	#global headers
	# Define the Teams API endpoint for reading messages in a channel (we are specifying only the latest message)
	url = f"https://graph.microsoft.com/beta/teams/{team_id}/channels/{channel_id}/messages?top=1"
	replyheaders = {'Content-Type': 'application/json'}
	last_messageid = None
	while True:
		if float(time.time()) - float(timeout) >= 0.0: #when our token expires get a new one
			print("Token expired!")
			print("Getting new token...")
			get_token() #Get new token
		# Make a GET request to the Teams API to retrieve the latest message
		response = requests.get(url, headers=headers)
		if response.status_code == 200:
			messages = response.json()
			for message in messages["value"]:
				if last_messageid != message["id"]:
					print(message)
					print("")
					print(message["id"])
					if message["from"]["user"] is not None: #dont try to print raw channel messages from the bot or other non-users
						print(message["from"]["user"]["displayName"])
						print(remove_html_tags(message["body"]["content"]))
					print("")
					content_raw = remove_html_tags(message["body"]["content"])
					content = content_raw.split(" ")
					print(content)
					if content[0] == "/bot": #here we can set up a bot command syntax
						if content[1] == "hi": # second level command
							payload = {"text": "hey"}
							response = requests.post(replyurl, headers=replyheaders, data=json.dumps(payload))
						if content[1] == "sup": # second level command
							payload = {"text": "just being a robot dude"}
							response = requests.post(replyurl, headers=replyheaders, data=json.dumps(payload))
					last_messageid = message["id"]
		else:
			print("Failed to retrieve messages: " + str(response))
			

def main():
	get_token()
	get_channelid()
	connector()
	
main()
