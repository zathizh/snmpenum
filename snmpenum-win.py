#! /usr/bin/python

import subprocess
import sys
import re

if len(sys.argv) < 2:
    print("Usage : snmpenum.py <ip address> <version: 1|2c|3> <community>")
    sys.exit(0)

remote_host = str(sys.argv[1])

#version 1|2c|3
_version = ""
try:
    _version = str(sys.argv[2])
except IndexError:
    _version = "1"

_pub_community = ""
try:
    _pub_community = sys.argv[3]
except IndexError:
    _pub_community = "public"

_users = "1.3.6.1.4.1.77.1.2.25"
_processes = "1.3.6.1.2.1.25.4.2.1.2"
_paths = "1.3.6.1.2.1.25.4.2.1.4"

P = {}

print("[+] SNMP Enumerator")
print

try:
    regex = re.compile(r"^iso.* = STRING: ")

    result1=filter(None,subprocess.check_output(["snmpwalk", "-c", _pub_community, "-v"+str(_version), remote_host, _users]).split("\n"))
    result2=filter(None,subprocess.check_output(["snmpwalk", "-c", _pub_community, "-v"+str(_version), remote_host, _processes]).split("\n"))
    result3=filter(None,subprocess.check_output(["snmpwalk", "-c", _pub_community, "-v"+str(_version), remote_host, _paths]).split("\n"))

    print(" USERS :--: "),
    for result in result1:
        names = regex.sub('', result.strip().replace("\"",""))
        print(" | "),
        print(names),

    print
    print

    for result in result2:
        procs = result.replace("iso.3.6.1.2.1.25.4.2.1.2.","").replace("STRING:", "").replace("\"","").split(" =  ")
        if len(procs) == 2:
            P[int(procs[0])]=procs[1]

    for result in result3:
        procs = result.replace("iso.3.6.1.2.1.25.4.2.1.4.","").replace("STRING:", "").replace("\\\\","\\").replace("\"","").replace(" = ","").split(" ")
        if len(procs) == 2 and int(procs[0]) in P.keys():
            P[int(procs[0])]=[P[int(procs[0])], procs[1]]

    keylist = P.keys()
    keylist.sort()
    for key in keylist:
        print("  "),
        print(str(key).rjust(5)),
        print("->"),
        if len(P[key]) == 2:
            print(P[key][0]),
            print("\t--  "),
            print(P[key][1])
        else:
            print(P[key])

except subprocess.CalledProcessError:
    print
    print("[-] Exiting SNMP Enumerator")
    sys.exit(0)

print
print("[-] Exiting SNMP Enumerator")
