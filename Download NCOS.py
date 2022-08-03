import requests

api_keys = {'X-CP-API-ID': 'your',
			'X-CP-API-KEY': 'api',
			'X-ECM-API-ID': 'keys',
			'X-ECM-API-KEY': 'here'}
device_base_url = 'https://www.cradlepointecm.com/api/v2/firmwares/?limit=500&version='
firmware_base_url = 'https://d251cfg5d9gyuq.cloudfront.net'


def app():
	firmware_version = input('Which version of firmware are you looking for? (ex: 7.22.60) - ')
	device_list_url = device_base_url + firmware_version
	device_list = requests.get(device_list_url, headers=api_keys).json()['data']
	model = input('What model router are you looking for? (ex: ibr900) - ')
	model_list = []
	for i in device_list:
		if str.upper(model) in i['url']:
			model_list.append(i['url'])

	index = 0
	for i in model_list:
		print(f'{index} - {i.replace("/", "")}')
		index += 1

	confirm_firmware = input('Please confirm your firmware ID number (ex: 0) - ')
	model_url = str(model_list[int(confirm_firmware)])
	firmware_url = firmware_base_url + model_url

	firmware_image = requests.get(firmware_url, headers=api_keys)
	with open(f'NCOS/{model}-{firmware_version}.bin', "wb") as f:
		f.write(firmware_image.content)
	value = input('Would you like to run the script again? (ex: y) - ')
	run_again(value)


def run_again(value):
	if 'Y' in value.upper():
		app()
	else:
		exit()


if __name__ == "__main__":
	app()
