import taxjar
import requests

Google_Api_Endpoint = 'https://maps.googleapis.com/maps/api/geocode/json?address='
Google_Api_Key = 'YOUR_API_KEY_HERE'
TaxJar_Api_Key = 'YOUR_API_KEY_HERE'

client = taxjar.Client(api_key=TaxJar_Api_Key)


def google_maps_api_call(address):
    return Google_Api_Endpoint + address + '&key=' + Google_Api_Key


def get_rates(country, city, zipcode):
    rates = client.rates_for_location(zipcode, {
        'city': city,
        'country': country
    })
    return rates


def run_program():
    print('API Program v1.0.0.0')
    print('-------------------------------------------')

    address = input('Enter an address for the local tax rate: \n')
    address = address.replace(' ', '+')

    address_response = requests.get(google_maps_api_call(address))

    resp_json_payload = address_response.json()

    formatted_address = resp_json_payload['results'][0]['formatted_address']
    address_components = resp_json_payload['results'][0]['address_components']

    city = ""
    country = ""
    zipcode = ""
    for component in address_components:
        types = component['types']
        for t in types:
            if t == 'locality':
                city = component['long_name']
                break
            if t == 'country':
                country = component['short_name']
                break
            if t == 'postal_code':
                zipcode = component['long_name']
                break

    print('-------------------------------------------\n')
    print('Google API response: \n' + formatted_address)
    rates = get_rates(country, city, zipcode)
    print('\nTaxJar API response:')
    print('County: ' + rates.county + ' - Tax Rate: ' + str(rates.county_rate))
    print('State: ' + rates.state + ' - Tax Rate: ' + str(rates.state_rate))


run_program()
