import argparse
import boto3
import os
import subprocess
import logging

# AWS Lambda Imports
from botocore.vendored import requests

# Imports local version of nmap
from res import nmap

# Sets Logger
logger = logging.getLogger('network_mapper')
logger.setLevel(logging.INFO)


# Makes the NMAP Binary Executable Ready For The Lambda
def make_nmap_binary_executable():
    command = 'cp res/nmap_x64_binary /tmp/nmap; chmod 755 /tmp/nmap'
    logger.info(subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT))
    logger.info(os.access('/tmp/nmap', os.R_OK))  # Check for read access
    logger.info(os.access('/tmp/nmap', os.W_OK))  # Check for write access
    logger.info(os.access('/tmp/nmap', os.X_OK))  # Check for execution access
    logger.info(os.access('/tmp/nmap', os.F_OK))  # Check for existence of file


# Calls Nmap Binary & Scans IP Address Provided
def scan_for_connected_clients(ip_address):
    scanner = nmap.PortScanner()
    logger.info("Running Nmap Scan Against: " + ip_address)
    scan_dict = scanner.scan(ip_address, arguments='-sP')
    return scan_dict.get("scan")


# Port Scan Connected Devices
def port_scan_connected_clients(ip_address):
    scanner = nmap.PortScanner()
    logger.info("Running Nmap Port Scan Against: " + ip_address)
    port_scanner = scanner.scan(ip_address)
    return port_scanner.get("scan")


# Push Data To DynamoDB
def post_data_to_dynamo_db(data, table):
    return 0


# Main Function To Be Called By Lambda When Running
def lambda_handler(event, context):
    make_nmap_binary_executable()
    type_of_scan = event["detail"]["type_of_scan"]
    if type_of_scan == 'connected_clients_scan':
        scan_results = scan_for_connected_clients(event["detail"]["ip_address"])
        post_data_to_dynamo_db(scan_results, type_of_scan)
    elif type_of_scan == "port_scan":
        scan_results = port_scan_connected_clients(event["detail"]["ip_address"])
        post_data_to_dynamo_db(scan_results, type_of_scan)
    return


# Function Used To Run This Program Locally
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Checks for connected clients in a subnet or portscans a subnet")
    parser.add_argument("scan_type", help="Type of scan to be performed e.g PortScan or ConnectedClients", type=str)
    parser.add_argument("ip_address", help="Ip Address of subnet to be scanned", type=str)
    args = parser.parse_args()
    if args.scan_type == 'ConnectedClients':
        results = scan_for_connected_clients(args.ip_address)
        print(results)
    elif args.scan_type == "PortScan":
        results = port_scan_connected_clients(args.ip_address)
        print(results)
