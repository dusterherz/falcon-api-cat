import falcon
from falcon import media
from middleware import SqlAlchemySessionManager, SqlAlchemyMediaHandler, Session
import resources

handlers = media.Handlers({
    'application/json': SqlAlchemyMediaHandler,
})
app = falcon.API(
    middleware=[SqlAlchemySessionManager(Session)])
app.resp_options.media_handlers = handlers
app.add_route('/cats', resources.CatsRessource())
app.add_route('/cats/{id}', resources.CatRessource())
