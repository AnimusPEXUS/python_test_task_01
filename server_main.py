
import bottle
import lxml.etree
import db_schemas
import schema_root
import sqlalchemy
import sqlalchemy.orm
import os


schema = lxml.etree.XMLSchema(schema_root.schema_root)


@bottle.post('/entity')
def entity():

    PY_TEST_SERVER_DB = os.environ['PY_TEST_SERVER_DB']

    print("PY_TEST_SERVER_DB ==", PY_TEST_SERVER_DB)

    engine = sqlalchemy.create_engine(
        'postgresql:///postgres:example@' + PY_TEST_SERVER_DB + '/postgres',
        echo=True
    )

    db_schemas.Base.create_all(engine)

    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()

    bottle_request_body = bytes(bottle.request.body)

    msg_r = db_schemas.Message()
    msg_r.text = str(bottle_request_body)

    session.add(msg_r)

    print("new message id ==", msg_r.id)

    # lxml suggests creating separate parser for each thread
    # see pydoc http://localhost:46213/lxml.etree.html#XMLParser
    parser = lxml.etree.XMLParser(schema=schema)

    try:
        parsed = lxml.etree.parse(bottle_request_body, parser)
    except lxml.etree.XMLSyntaxError as e:
        print("lxml.etree.XMLSyntaxError", e)
        msg_r.is_valid = False
        return
    finally:
        session.commit()

    msg_r.is_valid = True

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


print("TEST TASK PY XML SERVER")
sys.stdout.flush()
bottle.run(host='0.0.0.0', port=8080)
