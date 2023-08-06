import engora
import sys
import json
import csv
#import argparse
#TODO: Use a proper argument parser

def help(url, cert_path):
    print("""Usage: engora [command]
    Command can be one of
        login: Interactively fetch new API credentials and save to your config
        find_or_create [name] [description]: Create a new dataset.
        add [dataset ID] [version|"latest"] [item]: Add a JSON-formatted item to an existing dataset.  If version=="latest", get the latest version and add the item to that.
        upload [dataset ID] [version|"latest"] [CSV path]: Upload a CSV to a dataset.  If version=="latest", get the latest version.
        download [dataset ID] [version|"latest"] [CSV path]: Download a dataset as a CSV file.  If version=="latest", get the latest version.
        watch: Watch a dataset version; when a new item is added, execute a given command.
""")

def login(url, cert_path):
    if url!=None:
        client = engora.Client(url=url, cert_path=cert_path)
    else:
        client = engora.Client()
    client.create_and_save_token()

def create(url, cert_path):
    #parse the command line args
    name = sys.argv[2]
    description = sys.argv[3]
    if url!=None:
        client = engora.Client(url=url, cert_path=cert_path)
    else:
        client = engora.Client()
    ds = client.find_or_create(name, description=description)
    print(ds.dataset_id)

def add(url, cert_path):
    #parse the command line args
    dataset_id = sys.argv[2]
    version = sys.argv[3]
    datum = sys.argv[4]
    if url!=None:
        client = engora.Client(url=url, cert_path=cert_path)
    else:
        client = engora.Client()
    if version!="latest":
        ds = client.dataset(dataset_id, version=version)
    else:
        ds = client.dataset(dataset_id)
        ds.version()
    ds.add(json.loads(datum))

def upload(url, cert_path):
    #parse the command line args
    dataset_id = sys.argv[2]
    version = sys.argv[3]
    path = sys.argv[4]
    if url!=None:
        client = engora.Client(url=url, cert_path=cert_path)
    else:
        client = engora.Client()
    if version!="latest":
        ds = client.dataset(dataset_id, version=version)
    else:
        ds = client.dataset(dataset_id)
        ds.version()
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        for r in reader:
            ds.add(r)

def download(url, cert_path):
    #parse the command line args
    dataset_id = sys.argv[2]
    version = sys.argv[3]
    path = sys.argv[4]
    if url!=None:
        client = engora.Client(url=url, cert_path=cert_path)
    else:
        client = engora.Client()
    if version!="latest":
        ds = client.dataset(dataset_id, version=version)
    else:
        ds = client.dataset(dataset_id)
        ds.version()
    data = list(ds)
    keys = set()
    for d in data:
        if type(d) == dict:
            [keys.add(k) for k in d.keys()]
    keys = sorted(list(keys))
    with open(path, 'w') as f:
        writer = csv.DictWriter(f, keys)
        writer.writeheader()
        for d in data:
            writer.writerow(d)

def watch():
    print("Not implemented yet!")

def main():
    name = sys.argv[0]
    cmd = sys.argv[1]
    url = None
    cert_path = None
    for i in range(len(sys.argv)):
        if sys.argv[i] == '--url' or sys.argv[i] == '-u':
            url = sys.argv[i+1]
        if sys.argv[i] == '--cert' or sys.argv[i] == '-c':
            cert_path = sys.argv[i+1]
            if cert_path == "False":
                cert_path = False
    cmds = {"help":help, "login":login, "find_or_create":create, "add":add, "upload":upload, "download":download, "watch":watch}
    if cmd in cmds.keys():
        cmds[cmd](url, cert_path)
    else:
        print("Command not recognized: {}".format(cmd))
        help()

