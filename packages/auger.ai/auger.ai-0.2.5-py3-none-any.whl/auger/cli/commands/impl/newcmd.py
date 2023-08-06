import os
import sys
import errno
from auger.api.dataset import DataSet
from auger.api.cloud.utils.exception import AugerException
from auger.cli.utils.template import Template
from auger.cli.utils.config import AugerConfig


class NewCmd(object):

    def __init__(self, ctx, project_name, target, source, model_type):
        self.ctx = ctx
        self.project_name = project_name
        self.target = target
        self.source = source
        self.model_type = model_type

    def mk_project_folder(self):
        if os.path.exists(os.path.join(os.getcwd(), 'auger.yaml')):
            raise AugerException("Can't create '%s' inside a project."
                         " './auger.yaml' already exists" % self.project_name)
        project_path = os.path.join(os.getcwd(), self.project_name)
        try:
            os.makedirs(project_path)
        except OSError as e:
            if e.errno == errno.EEXIST:
                raise AugerException(
                    "Can't create '%s'. Folder already exists." %
                    self.project_name)
        self.ctx.log('Created project folder %s', self.project_name)
        return project_path

    def create_project(self):
        try:
            project_path = self.mk_project_folder()
        except AugerException as e:
            self.ctx.log(str(e))
            sys.exit(1)
        Template.copy_config_files(project_path)

        self.ctx.config.load(project_path)
        if self.source:
            try:
                self.source = DataSet.verify(self.source)[0]
            except Exception as e:
                self.ctx.log(str(e))
                sys.exit(1)

        AugerConfig(self.ctx).config(
            target=self.target,
            source=self.source,
            model_type=self.model_type,
            project_name=self.project_name)

        self.ctx.log(
            "Next, please go to project dir: cd %s\n"
            "Select or create data set on Auger Cloud: "
            "augerai dataset create|select\n"
            "Configure your experiment by editing auger.yaml\n"
            "And run the experiment: augerai experiment start\n"
            "After that you can use your model: augerai model deploy && "
            "augerai model predict <target_data>" % self.project_name)
