#!/usr/bin/python

import dropbox
import time
import requests
import json

f = open('accessInfo.json', 'rb')
file_content = f.read()
access_info = json.loads(file_content)

client = dropbox.client.DropboxClient(access_info['dropboxAccessToken'])
url = access_info['bcnURL']

cursor = None
while True:
	result = client.delta(cursor)
	cursor = result['cursor']
	if result['reset']:
		print 'RESET'

	for path, metadata in result['entries']:
		if metadata is not None:
			print '%s was created/updated' % path
			if path == "/babylog.txt":
				baby_log_metadata = client.metadata('/babyLog.txt')
				if not baby_log_metadata['size'].startswith('0'):
					f, metadata = client.get_file_and_metadata('/babyLog.txt')
					baby_log_lines = f.readlines()
					for log_line in baby_log_lines:
						upload_line = {'email': access_info['email'], 'password': access_info['password'], 'kidId': access_info['kidId']}
						upload_line.update(json.loads(log_line))
						r = requests.post(url + '/diaper', json=upload_line)
					client.file_delete('/babyLog.txt')
					response = client.put_file('/babyLog.txt', '')
		else:
			print '%s was deleted' % path

		# if has_more is true, call delta again immediately
		if not result['has_more']:

			changes = False
		# poll until there are changes
		while not changes:
			response = requests.get('https://api-notify.dropbox.com/1/longpoll_delta',
			params={
				'cursor': cursor, # latest cursor from delta call
				'timeout': 120 # default is 30 seconds
			})
			data = response.json()

			changes = data['changes']
		if not changes:
			print 'Timeout, polling again...'

		backoff = data.get('backoff', None)
		if backoff is not None:
			print 'Backoff requested. Sleeping for %d seconds...' % backoff
			time.sleep(backoff)
		print 'Resuming polling...'
