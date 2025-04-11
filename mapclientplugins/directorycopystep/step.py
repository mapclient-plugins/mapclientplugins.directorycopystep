
"""
MAP Client Plugin Step
"""
import json
import os
import shutil

from PySide6 import QtGui
from packaging.version import Version

from mapclient.mountpoints.workflowstep import WorkflowStepMountPoint
from mapclient.settings.version import __version__ as mapclient_version
from mapclientplugins.directorycopystep.configuredialog import ConfigureDialog

if Version("0.24.0") <= Version(mapclient_version):
    from mapclient.core.utils import construct_configuration


class DirectoryCopyStep(WorkflowStepMountPoint):
    """
    Skeleton step which is intended to be a helpful starting point
    for new steps.
    """

    def __init__(self, location):
        super(DirectoryCopyStep, self).__init__('Directory Copy', location)
        self._configured = False  # A step cannot be executed until it has been configured.
        self._category = 'Sink'
        # Add any other initialisation code here:
        self._icon = QtGui.QImage(':/directorycopystep/images/data-sink.png')
        # Ports:
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#directory_location'))
        # Port data:
        self._portData0 = None  # http://physiomeproject.org/workflow/1.0/rdf-schema#directory_location
        # Config:
        self._config = {
            'identifier': '',
            'Recurse Directory Structure': True,
            'location': '',
            'previous_location': '',
        }
        self._relative_path_config_keys = ['location', 'previous_location']

    def execute(self):
        """
        Add your code here that will kick off the execution of the step.
        Make sure you call the _doneExecution() method when finished.  This method
        may be connected up to a button in a widget for example.
        """
        # Put your execute step code here before calling the '_doneExecution' method.
        def _list_files(path):
            for _file in os.listdir(path):
                if os.path.isfile(os.path.join(path, _file)):
                    yield os.path.join(path, _file)

        output_location = os.path.realpath(os.path.join(self._location, self._config['location']))
        if self._config['Recurse Directory Structure']:
            shutil.copytree(self._portData0, output_location, dirs_exist_ok=True)
        else:
            for file in _list_files(self._portData0):
                shutil.copy2(file, output_location)

        self._doneExecution()

    def setPortData(self, index, dataIn):
        """
        Add your code here that will set the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        uses port for this step then the index can be ignored.

        :param index: Index of the port to return.
        :param dataIn: The data to set for the port at the given index.
        """
        self._portData0 = dataIn  # http://physiomeproject.org/workflow/1.0/rdf-schema#directory_location

    def configure(self):
        """
        This function will be called when the configure icon on the step is
        clicked.  It is appropriate to display a configuration dialog at this
        time.  If the conditions for the configuration of this step are complete
        then set:
            self._configured = True
        """
        dlg = ConfigureDialog(self._main_window)
        dlg.set_workflow_location(self._location)
        dlg.identifierOccursCount = self._identifierOccursCount
        dlg.setConfig(self._config)
        dlg.validate()
        dlg.setModal(True)

        if dlg.exec_():
            self._config = dlg.getConfig()

        self._configured = dlg.validate()
        self._configuredObserver()

    def setConfiguration(self, configuration):
        keys = ['location', 'previous_location', 'Recurse Directory Structure']
        relative_keys = ['location', 'previous_location']
        identifier = self._config['identifier']
        self._config = construct_configuration(configuration, keys, relative_keys, self._location)
        self._config['identifier'] = identifier

    def relocateConfiguration(self, to_location):
        for key in self._relative_path_config_keys:
            value = self._config.get(key, '')
            if value:
                absolute_path = os.path.join(self._location, value)
                self._config[key] = os.path.relpath(absolute_path, to_location)

    def getIdentifier(self):
        """
        The identifier is a string that must be unique within a workflow.
        """
        return self._config['identifier']

    def setIdentifier(self, identifier):
        """
        The framework will set the identifier for this step when it is loaded.
        """
        self._config['identifier'] = identifier

    def serialize(self):
        """
        Add code to serialize this step to string.  This method should
        implement the opposite of 'deserialize'.
        """
        return json.dumps(self._config, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def deserialize(self, string):
        """
        Add code to deserialize this step from string.  This method should
        implement the opposite of 'serialize'.

        :param string: JSON representation of the configuration in a string.
        """
        self._config.update(json.loads(string))

        d = ConfigureDialog()
        d.set_workflow_location(self._location)
        d.identifierOccursCount = self._identifierOccursCount
        d.setConfig(self._config)
        self._configured = d.validate()
