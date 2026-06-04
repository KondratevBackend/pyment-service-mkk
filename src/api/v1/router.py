import fastapi


class V1Router:
    def __init__(self):
        pass

    @property
    def router(self) -> fastapi.APIRouter:
        router = fastapi.APIRouter(prefix="/v1")
        self._update_routes(router=router)
        return router

    def _update_routes(self, router: fastapi.APIRouter) -> None:
        pass
