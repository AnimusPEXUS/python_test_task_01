
import bottle
import lxml.etree
import db_schemas
import schema_root

schema = lxml.etree.XMLSchema(schema_root.schema_root)


@bottle.post('/entity')
def entity():

    # lxml suggests creating separate parser for each thread
    # see pydoc http://localhost:46213/lxml.etree.html#XMLParser
    parser = lxml.etree.XMLParser(schema=schema)

    try:
        parsed = lxml.etree.parse(bottle.request.body, parser)
    except lxml.etree.XMLSyntaxError as e:
        print("lxml.etree.XMLSyntaxError", e)
        return

    name = parsed.find("Entity/Name")
    phone = parsed.find("Entity/Phone")
    email = parsed.find("Entity/Email")

    print('''
Entity
  Name    : {}
  Phone   : {}
  Email   : {}
  Services:'''.format(
        name.text,
        phone.text,
        email.text
    ))

    for i in parsed.find("Entity/Services").iter("Service"):
        main = ""
        if i.get("is_main") == "true":
            main = " (main)"
        print(
            "    {name}{main}"
            "\n      from: {b},"
            "\n      till: {e}".format(
                main=main,
                name=i.find("Name").text,
                b=i.find("Availability/From").text,
                e=i.find("Availability/To").text,
            )
        )

    return


bottle.run(host='localhost', port=8080)
