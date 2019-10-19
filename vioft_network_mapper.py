from flask import Flask, jsonify, request
import nmap
import requests
import sys, os, subprocess
from zappa.asynchronous import task
app = Flask(__name__)

@task
def scan_connected_clients(ip_addr):
    command = 'cp ./nmaps /tmp/nmap; chmod 755 /tmp/nmap'
    print(subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)) 
    print(os.access('/tmp/nmap', os.R_OK))  # Check for read access
    print(os.access('/tmp/nmap', os.W_OK))  # Check for write access
    print(os.access('/tmp/nmap', os.X_OK))  # Check for execution access
    print(os.access('/tmp/nmap', os.F_OK))  # Check for existence of file
    scanner = nmap.PortScanner()
    scan_dict = scanner.scan(ip_addr, arguments='-sP')
    #return jsonify({"Connected Clients": scan_dict.get("scan")})
    return scan_dict.get("scan")

@app.route('/nmap', methods=['GET'])
def test_nmap():
    command = 'cp ./nmaps /tmp/nmap; chmod 755 /tmp/nmap'
    print(subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT))
    scanner = nmap.PortScanner()
    return 'Nmap Done'

@app.route('/clients/list', methods=['POST'])
def get_connected_clients():
    ip_addr = request.json['ipaddr']+'/24'
    scan_connected_clients(ip_addr)
    return "Scan Is Initiated"

@app.route('/clients/portscan', methods=['POST'])
def port_scan_router():
    scanner = nmap.PortScanner()
    port_scanner = scanner.scan(request.json['ipaddr']+'/24')
    return jsonify({"Port-Scan-Results": port_scanner.get("scan")})

@app.route('/hello', methods=['GET'])
def hello_chump():
    return 'Hello World!', 200

@app.route('/ping', methods=['GET'])
def hello_dump():
    r = requests.get("https://www.google.com")
    return str(r)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
