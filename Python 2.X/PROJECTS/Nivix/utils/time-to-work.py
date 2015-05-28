import requests

def v(f):
	with open(f, 'r') as _FILE:
		s = _FILE.read()
	if s:
		return s.strip()
	else:
		print 'Could not find {}'.format(f)
		return False

KEY, HOME_ADDRESS, WORK_ADDRESS = map(v, ('google-direction-api.key', 'my-home-address.secret', 'my-work-address.secret', ))
if not all([KEY, HOME_ADDRESS, WORK_ADDRESS]):
	exit()

payload = {
	'origin': HOME_ADDRESS,
	'destination': WORK_ADDRESS,
	'key': KEY
}

base_url = 'https://maps.googleapis.com/maps/api/directions/json'

r = requests.get(base_url, params=payload)
if r.status_code == 200:
	print r.json()['routes'][0]['legs'][0]['duration']['text']
else:
	print "Error! Status code: {}".format(r.status_code)
	print u"\n{}".format(r.text)
