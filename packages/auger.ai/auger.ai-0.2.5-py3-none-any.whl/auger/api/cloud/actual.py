from .base import AugerBaseApi


class AugerActualApi(AugerBaseApi):
    """Auger Trial API."""

    def __init__(self, ctx, pipeline_api, prediction_id=None):
        super(AugerActualApi, self).__init__(
            ctx, pipeline_api, prediction_id)
        assert pipeline_api is not None, 'Pipeline must be set for Actuals'

    def create(self, records):
        return self._call_create(params={
            'pipeline_id': self.parent_api.object_id,
            'actuals': records}, has_return_object=False)
