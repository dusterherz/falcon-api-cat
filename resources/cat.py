import falcon
from models import Cat


class CatsRessource:
    def on_get(self, req, resp):
        cats = self.session.query(Cat).all()
        resp.media = cats
        resp.status = falcon.HTTP_OK

    def on_post(self, req, resp):
        name = req.media.get('name')
        if not name:
            raise falcon.HTTPBadRequest(
                'Missing name',
                'A name is required in the request body')
        cat = Cat(name=name)
        self.session.add(cat)
        self.session.commit()
        resp.media = cat
        resp.status = falcon.HTTP_OK


class CatRessource:
    def on_get(self, req, resp, id):
        cat = self.session.query(Cat).get(id)
        if cat is None:
            raise falcon.HTTPNotFound()
        resp.media = cat
        resp.status = falcon.HTTP_OK

    def on_delete(self, req, resp, id):
        cat = self.session.query(Cat).get(id)
        if cat is None:
            raise falcon.HTTPNotFound()
        self.session.delete(cat)
        self.session.commit()
        resp.media = cat
        resp.status = falcon.HTTP_OK
