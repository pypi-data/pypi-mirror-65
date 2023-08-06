from auger.api.model import Model
from auger.cli.utils.decorators import \
    error_handler, authenticated, with_project


class ModelCmd(object):

    def __init__(self, ctx):
        self.ctx = ctx

    @error_handler
    @authenticated
    @with_project(autocreate=False)
    def deploy(self, project, model_id, locally):
        model_id = Model(self.ctx, project).deploy(model_id, locally)
        return {'model_id': model_id}

    @error_handler
    @authenticated
    @with_project(autocreate=False)
    def predict(self, project, filename, model_id, threshold, locally):
        predicted = Model(self.ctx, project).predict(
            filename, model_id, threshold, locally)
        return {'predicted': predicted}

    @error_handler
    @authenticated
    @with_project(autocreate=False)
    def actual(self, project, filename, model_id):
        Model(self.ctx, project).actual(
            filename, model_id)
        return ''
