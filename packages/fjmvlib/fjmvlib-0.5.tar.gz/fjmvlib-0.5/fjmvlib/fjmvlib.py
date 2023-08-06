#!/usr/bin/env python3

"""
Copyright (c) 2018-2020 Cisco and/or its affiliates.
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import requests
import json


# Helper functions for Fire Jumper Mission Validation

def get_user_details(webex_token):

    url = "https://api.ciscospark.com/v1/people/me"
    headers = {"Authorization": f"Bearer {webex_token}", 'Content-Type':'application/json', 'Accept':'application/json'}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    user = response.json()

    return user


def post_submission(url, threatgrid_sha, threatgrid_sample_id,
                    threatgrid_sample_domains, umbrella_blacklist,
                    umbrella_blacklist_enforcement, ctr_observables,
                    ctr_response_url, webex_id):

    data = {
        "threatgrid_sha": threatgrid_sha,
        "threatgrid_sample_id": threatgrid_sample_id,
        "threatgrid_sample_domains": threatgrid_sample_domains,
        "umbrella_blacklist": umbrella_blacklist,
        "umbrella_blacklist_enforcement": umbrella_blacklist_enforcement,
        "ctr_observables": ctr_observables,
        "ctr_response_url": ctr_response_url,
        "webex_id": webex_id
    }
    headers = {'Content-Type':'application/json',
                'User-Agent': 'python-firejumper-mission-api'}

    response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
    response.raise_for_status()

    return response.json()