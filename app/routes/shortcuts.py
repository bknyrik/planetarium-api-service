from flask.views import MethodView

from app.routes import mixins


class ListCreateAPIView[T](
    mixins.ListCreateModelMixin[T],
    MethodView
):

    def get(self, *args, **kwargs) -> list[T]:
        return self.list(*args, **kwargs)

    def post(self, *args, **kwargs) -> T:
        return self.create(*args, **kwargs)
