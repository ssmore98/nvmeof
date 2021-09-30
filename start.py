#!/usr/bin/python3

from pprint import pprint
import libvirt
import sys
import xml.etree.ElementTree
import io
import uuid
import xmltodict

POOL = "pool"

"""
def xml2dict(xmldef):
    def x2d(node):
        retval = {}
        for attr in node.attrib:
            retval[attr] = node.attrib[attr]
        for child in node.getchildren():
            retval[child.tag] = x2d(child)
        if len(retval) < 1:
            retval = node.text
        return retval
    print(xmldef)
    with io.StringIO(xmldef) as sfp:
        parser = xml.etree.ElementTree.parse(sfp)
    root = parser.getroot()
    retval = {}
    retval[root.tag] = x2d(root)
    return retval
"""

try:
    conn = libvirt.open()
except libvirt.libvirtError:
    print('Failed to open connection to the hypervisor')
    sys.exit(1)

for pool in conn.listAllStoragePools():
    dpool = xmltodict.parse(pool.XMLDesc())
    if dpool['pool']['name'] == POOL:
        for v in pool.listAllVolumes():
            print(v.XMLDesc())
        break
exit(0)

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
    elif child.tag == 'devices':
        for grandchild in child.getchildren():
            if grandchild.tag == 'disk' and grandchild.attrib['type'] == 'block' \
                and grandchild.attrib['device'] == 'disk':
                for greatgrandchild in grandchild.getchildren():
                    if greatgrandchild.tag == 'source':
                        print(greatgrandchild.attrib['dev'])
with io.BytesIO() as sfp:
    parser.write(sfp)
    xmlconfig = sfp.getvalue().decode()
exit(0)
conn.createXML(xmlconfig)
