import os

from PySide2 import QtCore, QtWidgets

from hyperborea.preferences import *

from .ui_preferences import Ui_PreferencesDialog


class PreferencesDialog(QtWidgets.QDialog, Ui_PreferencesDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.settings = QtCore.QSettings()

        self.setupUi(self)

        # this is easily forgotten in Qt Designer
        self.tabWidget.setCurrentIndex(0)

        self.accepted.connect(self.write_settings)
        self.browseButton.clicked.connect(self.browse_cb)

        self.read_settings()

    def browse_cb(self):
        base_dir = self.outputLocation.text()
        base_dir = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                              dir=base_dir)

        if base_dir:
            self.outputLocation.setText(base_dir)

    def read_settings(self):
        self.unitPreferences.read_settings()

        base_dir = self.settings.value("BasePath")
        if not base_dir:
            documents_path = QtCore.QStandardPaths.writableLocation(
                QtCore.QStandardPaths.DocumentsLocation)
            app_name = QtWidgets.QApplication.applicationName()
            base_dir = os.path.join(documents_path, app_name + " Data")
        self.outputLocation.setText(base_dir)
        self.outputLocation.setCursorPosition(0)

        auto_rgb = read_bool_setting(self.settings, "AutoRGB", True)
        self.automaticRGBCheckBox.setChecked(auto_rgb)

        downsample = read_bool_setting(self.settings, "Downsample", True)
        self.downsampleCheckBox.setChecked(downsample)

        compression_level = read_int_setting(self.settings,
                                             "CompressionLevel", 6)
        self.compressionLevel.setValue(compression_level)

        self.settings.beginGroup("Upload")
        upload_enabled = read_bool_setting(self.settings, "Enabled", False)
        self.enableUpload.setChecked(upload_enabled)
        s3_bucket = self.settings.value("S3Bucket")
        if s3_bucket:
            self.s3Bucket.setText(s3_bucket.strip())
        aws_region = self.settings.value("AWSRegion")
        if aws_region:
            self.awsRegion.setText(aws_region.strip())
        upload_directory = self.settings.value("Directory")
        if upload_directory:
            self.uploadDirectory.setText(upload_directory.strip())
        access_key_id = self.settings.value("AccessKeyID")
        if access_key_id:
            self.uploadAccessKeyID.setText(access_key_id.strip())
        secret_access_key = self.settings.value("SecretAccessKey")
        if secret_access_key:
            self.uploadSecretAccessKey.setText(secret_access_key.strip())
        delete_original = read_bool_setting(self.settings, "DeleteOriginal",
                                            False)
        self.uploadDeleteOriginal.setChecked(delete_original)
        self.settings.endGroup()

    def write_settings(self):
        self.unitPreferences.write_settings()

        base_dir = self.outputLocation.text()
        self.settings.setValue("BasePath", base_dir)

        auto_rgb = self.automaticRGBCheckBox.isChecked()
        write_bool_setting(self.settings, "AutoRGB", auto_rgb)

        downsample = self.downsampleCheckBox.isChecked()
        write_bool_setting(self.settings, "Downsample", downsample)

        compression_level = self.compressionLevel.value()
        self.settings.setValue("CompressionLevel", compression_level)

        self.settings.beginGroup("Upload")
        upload_enabled = self.enableUpload.isChecked()
        write_bool_setting(self.settings, "Enabled", upload_enabled)
        s3_bucket = self.s3Bucket.text().strip()
        self.settings.setValue("S3Bucket", s3_bucket)
        aws_region = self.awsRegion.text().strip()
        self.settings.setValue("AWSRegion", aws_region)
        upload_directory = self.uploadDirectory.text().strip()
        self.settings.setValue("Directory", upload_directory)
        access_key_id = self.uploadAccessKeyID.text().strip()
        self.settings.setValue("AccessKeyID", access_key_id)
        secret_access_key = self.uploadSecretAccessKey.text().strip()
        self.settings.setValue("SecretAccessKey", secret_access_key)
        delete_original = self.uploadDeleteOriginal.isChecked()
        write_bool_setting(self.settings, "DeleteOriginal", delete_original)
        self.settings.endGroup()
