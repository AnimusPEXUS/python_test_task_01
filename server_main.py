
import os
import sys
import copy
import re
import queue
import threading

import bottle
import lxml.etree
import sqlalchemy
import sqlalchemy.orm
import yaml

import db_schemas
import schema_root


schema = lxml.etree.XMLSchema(schema_root.schema_root)


@bottle.post('/entity')
def entity():

    PY_TEST_SERVER_DB = os.environ['PY_TEST_SERVER_DB']

    print("PY_TEST_SERVER_DB ==", PY_TEST_SERVER_DB)

    engine_cmd = 'postgresql://postgres:example@' + PY_TEST_SERVER_DB + '/postgres'
    print("SQLAlchemy engine cmd:", engine_cmd)

    engine = sqlalchemy.create_engine(
        engine_cmd,
        echo=True
    )

    db_schemas.Base.metadata.create_all(engine)

    session = sqlalchemy.orm.sessionmaker(bind=engine)()

    bottle_request_body = copy.copy(bottle.request.body)

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

    print("new message id ==", msg_r.id)

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

    entity_r = db_schemas.Entity()
    entity_r.name = name.text
    entity_r.original_message_id = msg_r.id

    session.add(entity_r)
    session.commit()

    phone_r = db_schemas.Phone()
    phone_r.entity_id = entity_r.id
    phone_r.phone = phone.text

    # calculated in separate threads, as specified by task
    phone_r.is_mobile = False

    session.add(phone_r)

    email_r = db_schemas.Email()
    email_r.entity_id = entity_r.id
    email_r.email = email.text

    session.add(email_r)

    for i in parsed.find("Entity/Services").iter("Service"):

        serv_r = db_schemas.Service()
        serv_r.entity_id = entity_r.id
        serv_r.name = i.find("Name").text
        serv_r.is_main = i.get("is_main") == "true"
        serv_r.available_from = i.find("Availability/From").text
        serv_r.available_to = i.find("Availability/To").text

        session.add(serv_r)

    session.commit()

    q.put(phone_r.id)

    session.close()

    return


def check_phone_record():
    while True:
        record_id = q.get()

        engine = sqlalchemy.create_engine(
            engine_cmd,
            echo=True
        )

        session = sqlalchemy.orm.sessionmaker(bind=engine)()

        phone_r = session.\
            query(db_schemas.Phone).\
            filter_by(id=record_id).\
            first()
        phone_r.is_mobile = re.fullmatch("(\+7|8)\d{10}", phone_r.phone)
        session.commit()
        print("phone_r.is_mobile set to", phone_r.is_mobile)
        q.task_done()
        session.close()


print("TEST TASK PY XML SERVER")

with open("config.yml") as f:
    cfg = yaml.load(f.read(), Loader=yaml.SafeLoader)

print("Config:")
print("  threads: ", cfg['threads'])

q = queue.Queue()
threads = []
for i in range(cfg['threads']):
    t = threading.Thread(target=check_phone_record)
    t.start()
    threads.append(t)


bottle.run(host='0.0.0.0', port=8080)
