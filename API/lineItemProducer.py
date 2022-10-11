#!/usr/bin/env python3

import json
import argparse
import getpass
import os
import datetime
import csv
from textwrap import indent

from adnuntius.api import Api
from adnuntius.api import ApiClient
from adnuntius.util import generate_alphanum_id, date_to_string, id_reference



def list_teams(api):
    print('Querying all Line Items...')
    line_items = api.orders.query()['results']
    print(json.dumps(line_items, indent=4))

def make_adunit(api, minW, minH, maxW, maxH, name, target, site):
    id = generate_alphanum_id()
    adUnit = api.ad_units.update({
        'id': id,
        "objectState": "ACTIVE",
        "name": name + ' ' + target,
        "site": id_reference(site),
        "floorPrice": {
            "currency": "NOK",
            "amount": 200
        },
        "matchingLabels": [
            target
        ],
        "width": maxW,
        "height": maxH,
        "minWidth": minW,
        "minHeight": minH,
        "pageSize": 1
    })
    print(json.dumps(adUnit, indent=4))

def create_full(api, name, orgNm, url):

    #Preemptively create IDs for all assets which are to be made. So Those IDs can be reused for other aspects.
    EA_id = generate_alphanum_id()
    team_id = generate_alphanum_id()
    site_id = generate_alphanum_id()

    short_url = url.split("//")[1]

    #Retrieve User network and roles from the same ID as the user logged in. Allows for setting of roles later once the team is created
    allUsers = api.users.query()['results']
    #j7nylvvlccbsjrpc is Admin ID
    network = next((x['userRoles']['rolesByNetwork'][0]['network'] for x in allUsers if x['id'] == 'j7nylvvlccbsjrpc'), None)
    currentRoles = next((x['userRoles']['rolesByNetwork'][0]['roles'] for x in allUsers if x['id'] == 'j7nylvvlccbsjrpc'), None)

    #Create unfinished Team, in order to use for creation of EA and site
    team = api.teams.update({
        'id': team_id,
        'name': name,
        'type': 'STANDARD'
    })

    #Produce EA, with standard values, name , genereated ID and Organisational number for external referance
    EA = api.earnings_accounts.update({
        'id': EA_id,
        'name': name,
        'externalReference': str('Org nr: '+ orgNm),
        'revenueShare': 50.0,
        'team': id_reference(team)
    })
    
    site = api.sites.update({
        'id': site_id,
        'name': short_url,
        'siteUrl': url,
        'earningsAccount': id_reference(EA),
        'siteGroup': { 'id': 'gsn7lq2rjqbry72h'}, #Bonefish sitegroup ID
        'teams': [id_reference(team)]
    })

    currentRoles.append({
        'team': id_reference(team),
        "role": {
            "id": "adopsrole",
            "name": "Ad Ops",
            "url": "/api/v1/roles/adopsrole",
            "application": "ADVERTISING"
        }
    })

    user = api.users.update({
        'id': 'j7nylvvlccbsjrpc',
        'userRoles': {
            'rolesByNetwork': [
                {
                'network': network,
                'roles': currentRoles
                }
            ]
        }
    })

    #Finalize Team, after site has been created
    team = api.teams.update({
        'objectState': 'ACTIVE',
        'id': team_id,
        'sites': [id_reference(site)]
    })


    print(json.dumps(user, indent=4))
    print(json.dumps(site, indent=4))
    print(json.dumps(EA, indent=4))
    print(json.dumps(team, indent=4))

    #We can then create Ad-Units using the site we have created
    make_adunit(api, 900, 225, 1800, 450, name, "4:1", site)
    make_adunit(api, 300, 600, 450, 900, name, "1:2", site)




def list_line_items_example(api):
    """
       Example of querying and printing results.
    """

    # Retrieve all line items for this network
    print('Querying all Line Items...')
    line_items = api.line_items.query()['results']
    for line_item in line_items:
        print('Name: ', line_item['name'])
        print('Id: ', line_item['id'])
        print('JSON:\n', json.dumps(line_item, indent=4))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Adnuntius API example which creates and updates a line item")
    parser.add_argument('--api', dest='api_url', default='https://api.adnuntius.com/api')
    parser.add_argument('--network', dest='network', default='df')
    parser.add_argument('--user', dest='user', default='theodor.bergersen@gmail.com')
    parser.add_argument('--file', dest='file', default='navn_og_nummer.csv')
    parser.add_argument('--password', dest='password', required=False)
    parser.add_argument('--masquerade', dest='masquerade', required=False)

    args = parser.parse_args()
    password = args.password
    print(args.network)
    if password is None:
        password = getpass.getpass('Enter password: ')
    api = Api(args.user, password, args.api_url,
              context=args.network, masquerade_user=args.masquerade)

    with open(args.file, newline='') as csvFile:
        reader = csv.reader(csvFile)
        next(reader) #skip header row
        for row in reader:
            create_full(api, row[0], row[1], row[2])
            
    #ssp_connections = ApiClient("sspconnections", api)
    #list_teams(api)