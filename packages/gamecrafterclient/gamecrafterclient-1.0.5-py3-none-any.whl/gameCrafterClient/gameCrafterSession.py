import aiohttp

class GameCrafterSession:
    def __init__ (sessionId, userId, httpSession):
        self.sessionId = sessionId
        self.userId = userId
        self.httpSession = httpSession

    def __del__ ():
        self.httpSession.close()