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


class RetrieveUpdateDestroyAPIView[T](
    mixins.RetrieveUpdateDestroyModelMixin,
    MethodView
):
    def get(self, *args, **kwargs) -> T:
        return self.retrieve(*args, **kwargs)

    def put(self, *args, **kwargs) -> T:
        return self.update(*args, **kwargs)

    def delete(self, *args, **kwargs) -> None:
        self.destroy(*args, **kwargs)
