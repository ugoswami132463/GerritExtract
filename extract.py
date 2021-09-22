import argparse
import csv
import json
import pandas as pd
import re
import requests
from requests.auth import HTTPDigestAuth

headers = {"Content-Type" : "application/json"}

base_url = "https://review-android.quicinc.com/a/changes/?q=ownerin:usb.reviewers+status:merged"
kernel_49_url = "https://review-android.quicinc.com/a/changes/?q=ownerin:pcie.reviewers+branch:msm-4.9+status:merged"
my_changes_url = "https://review-android.quicinc.com/a/changes/?q=owner:sallenki+status:open"
kernel_414_url = "https://review-android.quicinc.com/a/changes/?q=ownerin:pcie.reviewers+branch:msm-4.14+status:merged"

current_rev_file = "&o=CURRENT_REVISION&o=CURRENT_FILES"

args = {}
p1_branch = ""
p2_branch = ""

def parse_params():

    parser = argparse. ArgumentParser(
                    description = 'Indentify missing kernel changes')
    parser.add_argument("-u",
                    dest = "username",
                    help = "(REQUIRED) Gerrit Id",
                    default = "",
                    required = True)

    parser.add_argument("-p",
                    dest = "http_key",
                    help = "(REQUIRED) Gerrit HTTP key",
                    default = "",
                    required = True)

    parser.add_argument("-f",
                    dest = "file_path",
                    help = "(OPTIONAL) Path to a kernel driver",
                    default = "",
                    required = False)

    parser.add_argument("-p1",
                    dest = "project1",
                    help = "(REQUIRED) Set 1 -Project:Branch for comparison",
                    default = "",
                    required = True)

    parser.add_argument("-p2",
                    dest = "project2",
                    help = "(REQUIRED) Set 2 - Project:Branch for comparison",
                    default = "",
                    required = True)

    return parser.parse_args()

def get_list_of_files(change):
    current_rev_id = change["current_revision"]
    current_rev = change["revisions"][current_rev_id]
    return current_rev["files"].keys()

def create_and_populate_items(change, is_p1):
    new_item = {}
    new_item[p1_branch[1]] = is_p1
    new_item[p2_branch[1]] = (not is_p1)
    new_item["subject"] = change["subject"]
    new_item["files"] = get_list_of_files(change)
    new_item["change_id"] = change["change_id"]
    new_item["owner"] = change["owner"]["name"]
    return new_item

def get_parsed_changes_dict(changes_dict, parsed_dict, is_49):
    r = re.compile(args.file_path)
    for change in changes_dict:
        if change["change_id"] in parsed_dict:
            parsed_dict[change["change_id"]][p2_branch[1]] = (not is_49)
        elif len(list(filter(r.match, get_list_of_files(change)))):
            parsed_dict[change["change_id"]] = create_and_populate_items(change, is_49)

def get_changes_dict(project, branch):
    request_url = base_url + "+project:" + project + "+branch:" + branch
    changes_list = requests.get(request_url + current_rev_file,
                            headers = headers,
                            verify = False,
                            auth = HTTPDigestAuth(args.username, args.http_key)).text

    return json.loads(changes_list[5:])

args = parse_params()

p1_branch = args.project1.split(":")
p2_branch = args.project2.split(":")

changes_p1_dict = get_changes_dict(p1_branch[0], p1_branch[1])
changes_p2_dict = get_changes_dict(p2_branch[0], p2_branch[1])

changes_dict = {}

get_parsed_changes_dict(changes_p1_dict, changes_dict, True)
get_parsed_changes_dict(changes_p2_dict, changes_dict, False)

df = pd.DataFrame.from_dict(changes_dict, orient = 'index')
columns = ["subject", "change_id", "owner", "files", p1_branch[1], p2_branch[1]]
df.to_csv('compare.csv', index=False, columns = columns)
