#!/usr/bin/python3

from pprint import pprint
import libvirt
import sys
import xml.etree.ElementTree
import io
import uuid

try:
    conn = libvirt.open()
except libvirt.libvirtError:
    print('Failed to open connection to the hypervisor')
    sys.exit(1)

# for domain in conn.listAllDomains():
#     print("Domain: id %d running %s %s" % (domain.ID(), domain.OSType(), domain.info()))
#     xml = domain.XMLDesc()
#     break

parser = xml.etree.ElementTree.parse('template.xml')
root = parser.getroot()
if root.tag != 'domain':
    raise
for attr in root.attrib:
    if attr == 'type' and root.attrib[attr] != 'kvm':
        raise
for child in root.getchildren():
    if child.tag == 'name':
        child.text = 'sachin'
    elif child.tag == 'uuid':
        child.text = uuid.uuid4().hex
with io.BytesIO() as sfp:
    parser.write(sfp)
    xmlconfig = sfp.getvalue().decode()
conn.createXML(xmlconfig)
