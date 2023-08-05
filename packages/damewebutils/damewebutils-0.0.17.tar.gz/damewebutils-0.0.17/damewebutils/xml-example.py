from unittest import TestCase
from xml.dom import minidom
import xml.etree.ElementTree as ET

tree = ET.parse('files/rss.xml')

l = []
for elem in tree.iter():
    if (elem.tag == "title"):
        print(elem.text)
