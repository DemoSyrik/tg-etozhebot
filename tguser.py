from pony.orm import Database, Required, PrimaryKey, db_session, select, delete

__author__ = 'Semyon'

db = Database("sqlite", "users.sqlite",
              create_db=True)


class TGUser(db.Entity):
    id = PrimaryKey(int, auto=True)
    tgid = Required(int)
    username = Required(str)


@db_session
def add_user(id, name):
    TGUser(tgid=id, username=name)


@db_session
def get_user_by_id(id):
    res = select(u for u in TGUser if u.tgid == id)
    if len(res) > 0:
        return list(res)[0]
    else:
        return None


@db_session
def remove_user(tg_user):
    delete(u for u in TGUser if u.tgid == tg_user.tgid)


@db_session
def get_all():
    return select(u for u in TGUser)[:]


db.generate_mapping(create_tables=True)

db.create_tables()
