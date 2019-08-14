

from lxml import etree


with open("schema.xsd", "br") as f:
    schema_root = etree.XML(f.read())
