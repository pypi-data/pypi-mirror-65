import logging

import azure.functions as func

import os
import sys
import xml.etree.ElementTree as ET
from typing import Dict, List
from azure.storage.blob import BlockBlobService
from distutils.dir_util import copy_tree


access_dict = {'DefaultEndpointsProtocol': 'https',
               'AccountName': 'cristhianmurciastorage',
               'AccountKey': '0EKaL1sYt3QzmXmFB4WZ2KiqmNcyj5yl8bRDlMcZuAdxHqYKVDcUyVHLkouS2fBlkhtsM48+A3gb1EvsOpC4qA=='
              }


def replace_attributes(tag_attributes: Dict, tag_elements: List):
    """
    Replaces the values of the input tag_attributes dictionary.
    Args:
        tag_attributes: Python dictionary containing the tag attributes.
        tag_elements: List containing tuples that will be used to update the input tag_attributes dictionary. Each tuple
        contains the following elements:
            attribute_name: Strings that represent the name of the attribute whose value will be replaced.
            original_value: String representing the current attribute value to be replaced. In case of being assigned to
            an empty string, any original value will be replaced with the new_value.
            new_value: String representing the value that will replace the original attribute value.
    Returns:
        Python dict containing the updated tag_attributes.
    """
    for attribute_name, original_value, new_value in tag_elements:
        attribute_value = tag_attributes.get(attribute_name)
        # if the original value is assigned to an empty string, any original value will be replaced with the new_value.
        if attribute_value and original_value == '':
            tag_attributes[attribute_name] = new_value
        # matching attribute values will be replaced with the new values
        elif attribute_value and (original_value == attribute_value):
            tag_attributes[attribute_name] = new_value
    return tag_attributes


def update_xml_file_tag(xml_path: str, tag_elements: List):
    """
    Updates a xml file tag with the input tag_elements.
    Args:
        xml_path: Path pointing to the xml file.
        tag_elements: List containing tuples that will be used to update the input tag_attributes dictionary. Each tuple
        should contain the following elements: attribute_name, original_value, new_value.
    Returns:
        None.
    """
    try:
        tree = ET.parse(xml_path)
        for tag in tree.iter():
            original = tag.attrib
            tag_attributes = replace_attributes(original, tag_elements)
            tag.attrib = tag_attributes
        tree.write(xml_path)
    except IOError:
        sys.exit(f"Something went wrong while opening the {xml_path} file.")


def copy_blobs(blob_service_client, source_container, destination_container, blobs=[]):
    """
    Copies a set of blobs from the source container to the destination container.
    Args:
        blob_service_client: Azure objects used for the azure storage resource connection.
        source_container: String representing the container where the blobs to be copied are stored.
        destination_container: String representing the  destination container.
        blobs: List containing the blob names to be copied.

    Returns:
        None
    """
    if not blobs:
        blobs = [b.name for b in blob_service_client.list_blobs(source_container)]

    for blob in blobs:
        blob_url = blob_service_client.make_blob_url(source_container, blob)
        blob_service_client.copy_blob(destination_container, blob, blob_url)


def download_blobs(blob_service_client, source_path, container, blobs=[]):
    """
    Copies a set of blobs from the source container to the destination container.
    Args:
        blob_service_client: Azure objects used for the azure storage resource connection.
        source_path: String representing the local path where the file will be downloaded.
        container: String representing the container where the blobs will be pulled from.
        blobs: List containing the blob names to be downloaded.

    Returns:
        None
    """
    if not blobs:
        blobs = [b.name for b in blob_service_client.list_blobs(container) if b.name.endswith('.xml')]
    # download files to be edited locally
    for blob in blobs:
        downloaded_file_path = os.path.join(source_path, str.replace(blob, '.xml', '_DOWNLOADED.xml'))
        blob_service_client.get_blob_to_path(container, blob, downloaded_file_path)


def upload_files(blob_service_client, source_path, container, files=[]):
    """
    Uploads a set of files from the local source to the destination container.
    Args:
        blob_service_client: Azure objects used for the azure storage resource connection.
        source_path: String representing the local path locating the files to be uploaded.
        container: String representing the container where the blobs will be pulled from.
        blobs: List containing the blob names to be downloaded.

    Returns:
        None
    """
    if not files:
        files = [f for f in os.listdir(source_path) if f.endswith('_DOWNLOADED.xml')]

    # uploading files to the container
    for f in files:
        full_path_to_file = os.path.join(source_path, f)
        blob_service_client.create_blob_from_path(container,
                                                  str.replace(f, '_DOWNLOADED.xml', '.xml'),
                                                  full_path_to_file)


def elastic_cube_automation(credentials, source_container, destination_container):
    """
    Orchestrates the deployment of elastic cubes
    Args:
        credentials: Dictionary containing the Azure storage resource credentials.
        source_container: Name of the azure container which has the cubes to be deployed.
        destination_container: Name of the azure container that will host the deployed cubes.

    Returns:
        None.
    """
    print('Connecting to azure web storage.')
    blob_service_client = BlockBlobService(account_name=credentials.get('AccountName'),
                                           account_key=credentials.get('AccountKey'))
    print('Connected to azure web storage.')

    # 1. Backup production files.
    print('Creating backup for production cubes')
    copy_blobs(blob_service_client, 'production', 'backup-production')

    # 2. Copy the files to be deployed from development to production
    print('Copying cubes to be deployed from development to production')
    source_container, destination_container = 'development', 'production'
    copy_blobs(blob_service_client, source_container, destination_container)

    # 3. Downloads the files to be edited locally.
    local_path, container = '.', 'production'
    download_blobs(blob_service_client, local_path, container, blobs=[])

    # 4. Edit files locally.
    tag_elements = [("Server", "stagingedwus01.zcdev.local", "somedwsql01.zerochaos.local"),
                    ("UserName", "", ""),
                    ("Password", "", ""),
                    ("EncryptConnection", "", "True"),
                    ("TrustServerCertificate", "", "True")]

    production_cubes = [os.path.join(local_path, file) for file in os.listdir(local_path) if
                        file.endswith('_DOWNLOADED.xml')]

    for p_c in production_cubes:
        update_xml_file_tag(p_c, tag_elements)

    # 5. Uploads the edited cubes to the production container
    upload_files(blob_service_client, local_path, container, files=[])