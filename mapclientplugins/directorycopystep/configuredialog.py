import os

from PySide6 import QtWidgets
from mapclientplugins.directorycopystep.ui_configuredialog import Ui_ConfigureDialog

from mapclient.core.utils import to_exchangeable_path, to_system_path

INVALID_STYLE_SHEET = 'background-color: rgba(239, 0, 0, 50)'
DEFAULT_STYLE_SHEET = ''


class ConfigureDialog(QtWidgets.QDialog):
    """
    Configure dialog to present the user with the options to configure this step.
    """

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)

        self._ui = Ui_ConfigureDialog()
        self._ui.setupUi(self)

        # Keep track of the previous identifier so that we can track changes
        # and know how many occurrences of the current identifier there should
        # be.
        self._previousIdentifier = ''
        # Set a place holder for a callable that will get set from the step.
        # We will use this method to decide whether the identifier is unique.
        self.identifierOccursCount = None

        self._workflow_location = None
        self._previous_location = ''

        self._make_connections()

    def _make_connections(self):
        self._ui.lineEditIdentifier.textChanged.connect(self.validate)
        self._ui.lineEditDirectoryLocation.textChanged.connect(self.validate)
        self._ui.pushButtonDirectoryChooser.clicked.connect(self._directory_chooser_clicked)

    def _directory_chooser_clicked(self):
        location = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Directory', self._previous_location)

        if location:
            self._previous_location = location
            display_location = self._output_location(location)
            self._ui.lineEditDirectoryLocation.setText(display_location)

    def _output_location(self, location=None):
        if location is None:
            display_path = self._ui.lineEditDirectoryLocation.text()
        else:
            display_path = location
        if self._workflow_location and os.path.isabs(display_path):
            display_path = os.path.relpath(display_path, self._workflow_location)

        return display_path

    def accept(self):
        """
        Override the accept method so that we can confirm saving an
        invalid configuration.
        """
        result = QtWidgets.QMessageBox.StandardButton.Yes
        if not self.validate():
            result = QtWidgets.QMessageBox.warning(
                self, 'Invalid Configuration',
                'This configuration is invalid.  Unpredictable behaviour may result if you choose \'Yes\', are you sure you want to save this configuration?)',
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No, QtWidgets.QMessageBox.StandardButton.No)

        if result == QtWidgets.QMessageBox.StandardButton.Yes:
            QtWidgets.QDialog.accept(self)

    def set_workflow_location(self, location):
        self._workflow_location = location

    def validate(self):
        """
        Validate the configuration dialog fields.  For any field that is not valid
        set the style sheet to the INVALID_STYLE_SHEET.  Return the outcome of the
        overall validity of the configuration.
        """
        # Determine if the current identifier is unique throughout the workflow
        # The identifierOccursCount method is part of the interface to the workflow framework.
        value = self.identifierOccursCount(self._ui.lineEditIdentifier.text())
        valid = (value == 0) or (value == 1 and self._previousIdentifier == self._ui.lineEditIdentifier.text())
        self._ui.lineEditIdentifier.setStyleSheet(DEFAULT_STYLE_SHEET if valid else INVALID_STYLE_SHEET)

        non_empty = len(self._ui.lineEditDirectoryLocation.text())

        file_path = self._output_location()
        if self._workflow_location:
            file_path = os.path.join(self._workflow_location, file_path)
        location_valid = non_empty and os.path.isdir(file_path)
        self._ui.lineEditDirectoryLocation.setStyleSheet(DEFAULT_STYLE_SHEET if location_valid else INVALID_STYLE_SHEET)

        return valid and location_valid

    def getConfig(self):
        """
        Get the current value of the configuration from the dialog.  Also
        set the _previousIdentifier value so that we can check uniqueness of the
        identifier over the whole of the workflow.
        """
        self._previousIdentifier = self._ui.lineEditIdentifier.text()
        config = {
            'identifier': self._ui.lineEditIdentifier.text(),
            'Recurse Directory Structure': self._ui.checkBoxRecurse.isChecked(),
            'location': to_exchangeable_path(self._ui.lineEditDirectoryLocation.text()),
            'previous_location': to_exchangeable_path(self._previous_location),
        }
        return config

    def setConfig(self, config):
        """
        Set the current value of the configuration for the dialog.  Also
        set the _previousIdentifier value so that we can check uniqueness of the
        identifier over the whole of the workflow.
        """
        self._previousIdentifier = config['identifier']
        self._ui.lineEditIdentifier.setText(config['identifier'])
        self._ui.checkBoxRecurse.setChecked(config['Recurse Directory Structure'])
        self._ui.lineEditDirectoryLocation.setText(to_system_path(config['location']))
        self._previous_location = to_system_path(os.path.join(self._workflow_location, config['previous_location']))
