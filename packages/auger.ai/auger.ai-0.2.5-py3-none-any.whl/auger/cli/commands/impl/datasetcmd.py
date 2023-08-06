from auger.api.dataset import DataSet
from auger.cli.utils.config import AugerConfig
from auger.cli.utils.decorators import \
    error_handler, authenticated, with_project


class DataSetCmd(object):

    def __init__(self, ctx):
        self.ctx = ctx

    @error_handler
    @authenticated
    @with_project(autocreate=False)
    def list(self, project):
        count = 0
        selected = self.ctx.config.get('dataset', None)
        for dataset in iter(DataSet(self.ctx, project).list()):
            self.ctx.log(
                ('[%s] ' % ('x' if selected == dataset.get('name') else ' ')) +
                dataset.get('name')
            )
            count += 1
        self.ctx.log('%s DataSet(s) listed' % str(count))
        return {'datasets': DataSet(self.ctx, project).list()}

    @error_handler
    @authenticated
    @with_project(autocreate=True)
    def create(self, project, source = None):
        if source is None:
            source = self.ctx.config.get('source', None)
        dataset = DataSet(self.ctx, project).create(source)
        AugerConfig(self.ctx).set_data_set(dataset.name, source)
        self.ctx.log('Created DataSet %s' % dataset.name)
        return {'created': dataset.name}

    @error_handler
    @authenticated
    @with_project(autocreate=False)
    def delete(self, project, name):
        if name is None:
            name = self.ctx.config.get('dataset', None)
        DataSet(self.ctx, project, name).delete()
        if name == self.ctx.config.get('dataset', None):
            AugerConfig(self.ctx).set_data_set(None).set_experiment(None)
        self.ctx.log('Deleted dataset %s' % name)
        return {'deleted': name}

    @error_handler
    def select(self, name):
        old_name = self.ctx.config.get('dataset', None)
        if name != old_name:
            AugerConfig(self.ctx).set_data_set(name, '').set_experiment(None)
        self.ctx.log('Selected DataSet %s' % name)
        return {'selected': name}

    @error_handler
    @authenticated
    @with_project(autocreate=False)
    def download(self, project, name, path_to_download):
        if name is None:
            name = self.ctx.config.get('dataset', None)
        file_name = DataSet(self.ctx, project, name).download(path_to_download)
        self.ctx.log('Downloaded dataset %s to %s' % (name, file_name))
        return {'dowloaded': name, 'file': file_name}
