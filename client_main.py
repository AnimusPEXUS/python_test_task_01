
import bottle
import lxml.etree
# import db_schemas
import http.client
import sys
import example


def main():
    client = http.client.HTTPConnection(sys.argv[1])
    client.request("POST", "/entity", body=example.example_text)


main()
