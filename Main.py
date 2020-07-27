#!/bin/python3
print("[Main] Script starting...")

# Do local imports
import configs 
import longpool

print('[Config] Token:', configs.token()) # Print your token

# Use longpool.listen() for return only message object
# or
# Use longpool.listen(True) for return updates object

for message in longpool.listen():
	print()
	print(message)
	print(f"\npeer_id: {message['peer_id']}\nText: {message['text']}")

# or

for updates in longpool.listen(True):
	print()
	print(updates)
