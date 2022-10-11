#!/usr/bin/env python3

import json
import argparse
import getpass
import os
import datetime
import csv
import re
from textwrap import indent

from adnuntius.api import Api
from adnuntius.api import ApiClient
from adnuntius.util import generate_alphanum_id, date_to_string, id_reference


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


def list_sites(api):
    print('Querying all Line Items...')
    sites = api.sites.query()['results']
    sports = []
    ids = []
    for site in sites:
        print(site)
        fullName = ''
        if 'earningsAccount' in site:
            fullName = site['earningsAccount']['name']

        print(fullName)
        if('Norges ' in fullName):
            forbund = re.sub('s?forbund.*', "", fullName)
            sport = forbund.replace("Norges ", "")
            sports.append(sport)
            ids.append(site['id'])
    return sports, ids


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Adnuntius API example which creates and updates a line item")
    parser.add_argument('--api', dest='api_url', default='https://api.adnuntius.com/api')
    parser.add_argument('--network', dest='network', default='df')
    parser.add_argument('--user', dest='user', default='theodor.bergersen@gmail.com')
    parser.add_argument('--file', dest='file', default='navn_og_nummer.csv')
    parser.add_argument('--password', dest='password', required=False)
    parser.add_argument('--masquerade', dest='masquerade', required=False)

    args = parser.parse_args()
    password = 'Theodoradnuntius98'
    print(args.network)
    api = Api(args.user, password, args.api_url,
              context= args.network, masquerade_user=args.masquerade)

    adunits, ids = list_sites(api)
    print(adunits)
    print(ids)
