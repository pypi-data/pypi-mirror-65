from .base import AugerBaseApi


class AugerClusterTaskApi(AugerBaseApi):
    """Auger Cluster Task Api."""

    def __init__(self, ctx, project_api=None,
        cluster_task_name=None, cluster_task_id=None):
        super(AugerClusterTaskApi, self).__init__(
            ctx, project_api, cluster_task_name, cluster_task_id)
        assert project_api is not None, 'Project must be set for Cluster Task'

    def create(self, task_args):
        return self._call_create({
            'name': self.object_name,
            'project_id': self.parent_api.object_id,
            'args_encoded': task_args},
            ['pending', 'received', 'started', 'retry']).get('result')
