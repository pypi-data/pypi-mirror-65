#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import codecs
import copy
import json
import multiprocessing.pool
import os
import shutil
import textwrap
import zipfile

import six

import requests
from taxii2client import v20, v21

__version__ = "1.0"
__author__ = "emmanvg"


def download_file(item):
    """Download file based on the given url, save to disk with the provided filename."""
    filename, url = item
    if os.path.isfile(filename) is False:
        print("Downloading {}...".format(url))
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(filename, mode="wb") as outfile:
                    for chunk in response:
                        outfile.write(chunk)
                print("Finished saving file '{}'".format(filename))
            else:
                response.raise_for_status()
        except requests.exceptions.SSLError as e:
            print("Please check if you are behind a proxy, request was unsuccessful...")
            print(e)
    else:
        print("File {} is already present...".format(filename))
    return filename


def process_json_object(collection, filename):
    """Open the file and send it to the server. Save the status resource returned by the server to disk."""
    with codecs.open(filename, mode="r", encoding="utf8") as infile:
        status = collection.add_objects(json.load(infile), timeout=0)
        status = status._raw

    status_filename = status["id"] + ".json"
    with codecs.open(status_filename, mode="w", encoding="utf8") as out_status:
        output = json.dumps(status, ensure_ascii=False, indent=4, separators=(',', ': '))
        out_status.write(six.text_type(output))
    print("Wrote status response in '{}' for {}".format(status_filename, filename))
    return status_filename


def post_to_taxii_server(item):
    """Method called by each item in the web_locations list in preparation to be added to server."""
    filename, url, collection, delete_download, delete_status = item
    print("Adding objects from '{}'...".format(filename))

    if zipfile.is_zipfile(filename):
        z = zipfile.ZipFile(filename)
        status_filenames = []
        for zip_member in z.namelist():
            if zip_member.endswith(".json"):
                location = z.extract(member=zip_member)
                status = process_json_object(collection, location)
                status_filenames.append(status)
        if delete_status:
            for s in status_filenames:
                remove_file(s)
        if delete_download:
            for item in sorted(z.NameToInfo.keys(), reverse=True):
                remove_file(item)
        z.close()
        if delete_download:
            remove_file(filename)

    elif filename.endswith(".json"):
        status = process_json_object(collection, filename)
        if delete_status:
            remove_file(status)
        if delete_download:
            remove_file(filename)


def print_json_message(message):
    """Used in the interactive session to print messages received from TAXII Server."""
    print("{:*^50}".format("RESPONSE BEGIN"))
    print(json.dumps(message, indent=4))
    print("{:*^50}".format("RESPONSE END"))


def get_collection_for_post(url, username, password, version):
    """Interactive session to select an available collection to insert the downloaded
    data to."""
    if version == "2.1":
        server = v21.Server(url + "taxii2/", user=username, password=password)
    else:
        server = v20.Server(url + "taxii/", user=username, password=password)
    print_json_message(server._raw)

    count_apiroot = len(server.api_roots)
    if count_apiroot > 0:
        select_apiroot = input("Select an ApiRoot (1 - {}): ".format(count_apiroot))
        api_root = server.api_roots[int(select_apiroot) - 1]
    else:
        raise RuntimeError("No ApiRoots available...")

    count_collections = len(api_root.collections)
    if count_collections > 0:
        print_json_message({"collections": [x._raw for x in api_root.collections]})
        select_collection = input("Select Collection to POST (1 - {}): ".format(count_collections))
        collection = api_root.collections[int(select_collection) - 1]
    else:
        raise RuntimeError("No collections available...")

    return collection


def remove_file(path):
    """Check if the file exists, then remove it. Works only on the current directory where"""
    full_path = os.path.join(os.getcwd(), path)
    if os.path.isfile(full_path):
        os.remove(full_path)
        print("Deleted file {}...".format(full_path))
    elif os.path.isdir(full_path):
        shutil.rmtree(full_path, ignore_errors=True)
        print("Deleted directory {}...".format(full_path))


def _add_certs():
    """Helper method to add certs into certifi package. This method is not called by the script"""
    import certifi
    certifi_location = certifi.where()
    my_certs = "example.crt"  # update this filename as required

    with open(my_certs, "rb") as infile:
        customca = infile.read()

    # append the new certs to the
    with open(certifi_location, "ab") as outfile:
        outfile.write(customca)


class NewlinesHelpFormatter(argparse.RawDescriptionHelpFormatter):
    """Custom help formatter to insert newlines between argument help texts.
    """
    def _split_lines(self, text, width):
        text = self._whitespace_matcher.sub(" ", text).strip()
        txt = textwrap.wrap(text, width)
        txt[-1] += "\n"
        return txt


def _get_argparser():
    """Create and return an ``ArgumentParser`` instance for this application."""
    desc = "TAXII POST-ing script for bulk additions to a specific collection v{}".format(__version__)
    parser = argparse.ArgumentParser(
        description=desc,
        formatter_class=NewlinesHelpFormatter,
    )

    parser.add_argument(
        "-l",
        "--host",
        default="http://localhost:5000/",
        action="store",
        type=str,
        help="<url to TAXII Server or specific collection>"
    )

    parser.add_argument(
        "-u",
        "--user",
        default="admin",
        action="store",
        type=str,
        help="<username for basic auth>"
    )

    parser.add_argument(
        "-p",
        "--password",
        default="Password0",
        action="store",
        type=str,
        help="<password for basic auth>"
    )

    parser.add_argument(
        "--request-version",
        default="2.1",
        action="store",
        type=str,
        help="<client version to perform the request>"
    )

    parser.add_argument(
        "-w",
        "--web-locations",
        nargs="+",
        type=str,
        action="append",
        help="<web locations to download from> example: -w filename.json https://example.com/file.json -w filename2.json https://example2.com/file.json"
    )

    parser.add_argument(
        "--clean-downloads",
        default=False,
        action="store_true",
        help="<when flag is set, removes downloaded files>"
    )

    parser.add_argument(
        "--clean-statuses",
        default=False,
        action="store_true",
        help="<when flag is set, removes the status json files received from server>"
    )

    return parser


def main():
    parser = _get_argparser()
    tool_args = parser.parse_args()

    try:
        # v21.Connection()
        if tool_args.request_version == "2.1":
            selected_collection = v21.Collection(tool_args.host, user=tool_args.user, password=tool_args.password)
        else:
            selected_collection = v20.Collection(tool_args.host, user=tool_args.user, password=tool_args.password)
        selected_collection.refresh()
    except requests.HTTPError:
        selected_collection = get_collection_for_post(tool_args.host, tool_args.user, tool_args.password, tool_args.request_version)

    # these urls and filenames are used for downloading and populating the medallion backend
    web_locations = [
        ["enterprise-attack.json", "https://github.com/mitre/cti/raw/master/enterprise-attack/enterprise-attack.json"],
        ["mobile-attack.json", "https://github.com/mitre/cti/raw/master/mobile-attack/mobile-attack.json"],
        ["pre-attack.json", "https://github.com/mitre/cti/raw/master/pre-attack/pre-attack.json"],
        ["stix-capec.json", "https://github.com/mitre/cti/raw/master/capec/stix-capec.json"],
        ["cti-stix-elevator.zip", "https://github.com/oasis-open/cti-stix-elevator/archive/master.zip"],
    ]

    with multiprocessing.pool.ThreadPool() as threads:
        threads.imap_unordered(download_file, web_locations)
        threads.close()
        threads.join()

    for loc in web_locations:
        loc.append(copy.deepcopy(selected_collection))
        loc.append(tool_args.clean_downloads)
        loc.append(tool_args.clean_statuses)

    with multiprocessing.pool.ThreadPool() as threads:
        threads.imap_unordered(post_to_taxii_server, web_locations)
        threads.close()
        threads.join()


if __name__ == "__main__":
    main()
