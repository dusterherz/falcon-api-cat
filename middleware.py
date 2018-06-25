import json
import six
from falcon.media import BaseHandler
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import DeclarativeMeta


db_engine = create_engine(
    'postgresql://postgres:catsareawesome@localhost:4321/postgres')

session_factory = sessionmaker(bind=db_engine)
Session = scoped_session(session_factory)


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_')
                          and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            return fields

        return json.JSONEncoder.default(self, obj)


class SqlAlchemyMediaHandler(BaseHandler):
    def serialize(obj):
        result = json.dumps(obj, cls=AlchemyEncoder, ensure_ascii=False)
        if six.PY3 or not isinstance(result, bytes):
            return result.encode('utf-8')
        return result


class SqlAlchemySessionManager:
    """
    Create a scoped session for every request and close it when the request
    ends.
    """

    def __init__(self, Session):
        self.Session = Session

    def process_resource(self, req, resp, resource, params):
        resource.session = self.Session()

    def process_response(self, req, resp, resource, req_succeeded):
        if hasattr(resource, 'session'):
            if not req_succeeded:
                resource.session.rollback()
            Session.remove()
