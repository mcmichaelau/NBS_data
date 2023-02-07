import requests
import pandas as pd

property_type = 'APARTMENT'
postal_code = '24502'
api_key = 'cd29fb3fc17be3b59290c4493b087661'
num_properties = 10


def get_properties(api_key, postal_code, property_type, page_size):

    headers = {
        'Accept': 'application/json, application/json',
        'apikey': api_key,
    }

    params = {
        'postalcode': postal_code,
        'propertytype': property_type,
        'page': '3',
        'pagesize': page_size,
    }

    response = requests.get('https://api.gateway.attomdata.com/propertyapi/v1.0.0/property/address', params=params, headers=headers)

    return response


def get_property_info(api_key, property_id):

    headers = {
        'Accept': 'application/json, application/json',
        'apikey': api_key,
    }

    params = {
        'attomid': property_id,
    }

    response = requests.get('https://api.gateway.attomdata.com/propertyapi/v1.0.0/property/detail', params=params, headers=headers)

    return response


def get_owner(api_key, property_id):

    headers = {
        'Accept': 'application/json',
        'apikey': api_key,
    }

    params = {
        'attomid': property_id,
    }

    response = requests.get(
        'https://api.gateway.attomdata.com/propertyapi/v1.0.0/property/detailowner',
        params=params,
        headers=headers,
    )

    return response


def try_info(data, key):
    try:
        # loop through each key
        for i in range(len(key)):
            key[i] = str(key[i])
            data = data[key[i]]
        return data

    except:
        return 'N/A'


properties_list = get_properties(api_key, postal_code, property_type, num_properties).json()['property']
print(f'properties_list: {properties_list}')

# create property output dictionary
property_output = {}

for i in range(len(properties_list)):

    address = try_info(properties_list[i],['address','oneLine'])
    property_output.setdefault(i, {}).setdefault('Address', address)

    id = try_info(properties_list[i],['identifier','Id'])
    property_output.setdefault(i, {}).update({'ID': id})

    # get property info for each property
    property_info = get_property_info(api_key, id).json()['property'][0]
    print(f'property_info: {property_info}')

    levels = try_info(property_info,['building','summary','levels'])
    property_output.setdefault(i, {}).update({'Levels': levels})

    # number of beds
    rooms = try_info(property_info,['building','rooms','roomsTotal'])
    property_output.setdefault(i, {}).update({'Rooms': rooms})

    # lot size in acres
    lot_size = try_info(property_info, ['lot','lotsize1'])
    property_output.setdefault(i, {}).update({'Lot Size (acres)': lot_size})

    # total building size
    building_size = try_info(property_info,['building','size','bldgsize'])
    property_output.setdefault(i, {}).update({'Total Building Area (sq. ft.)': building_size})

    # living size
    living_size = try_info(property_info,['building','size','livingsize'])
    property_output.setdefault(i, {}).update({'Living Area (sq. ft.)': living_size})

    # get owner info for each property
    owner_info = get_owner(api_key, id).json()['property'][0]
    print(f'owner_info: {owner_info}')

    # get owner last name
    last_name = try_info(owner_info,['owner','owner1','lastname'])
    property_output.setdefault(i, {}).update({'Owner Last Name': last_name})

    # get owner first name for each property
    first_name = try_info(owner_info, ['owner', 'owner1', 'firstnameandmi'])
    property_output.setdefault(i, {}).update({'Owner First Name': first_name})

print(property_output)

df = pd.DataFrame(property_output)

# transpose dataframe
df = df.T

df.to_excel('data.xlsx', index=True, sheet_name='Sheet1')



# owner_test = get_owner(api_key, '210426523')

# print(owner_test.json()['property'][0]['owner'])
