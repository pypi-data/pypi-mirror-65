# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 16:23:13 2018

@author: samschott
"""

# system imports
import logging

# external packages
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtCore import Qt

# local imports
from .resources import RELINK_DIALOG_PATH, APP_ICON_PATH
from .utils import get_scaled_font, icon_to_pixmap
from .utils import BackgroundTask

logger = logging.getLogger(__name__)


# noinspection PyArgumentList
class RelinkDialog(QtWidgets.QDialog):
    """A dialog to show when Maestral's Dropbox access has expired or has been revoked."""

    VALID_MSG = "Verified. Restarting Maestral..."
    INVALID_MSG = "Invalid token"
    CONNECTION_ERR_MSG = "Connection failed"

    EXPIRED = 0
    REVOKED = 1

    def __init__(self, parent, reason=EXPIRED):
        super().__init__()
        uic.loadUi(RELINK_DIALOG_PATH, self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint
                            | Qt.WindowTitleHint | Qt.CustomizeWindowHint)

        # import OAuth2Session here because of ~40 MB memory footprint
        from maestral.oauth import OAuth2Session

        self._parent = parent
        self.auth_session = OAuth2Session(self._parent.mdbx.config_name)

        # format text labels
        if reason is self.EXPIRED:
            self.titleLabel.setText("Dropbox Access Expired")
            formatted_text = self.infoLabel.text().format(
                "has expired", self.auth_session.get_auth_url())
        elif reason is self.REVOKED:
            self.titleLabel.setText("Dropbox Access Revoked")
            formatted_text = self.infoLabel.text().format(
                "has been revoked", self.auth_session.get_auth_url())
        else:
            raise ValueError("'reason' must be RelinkDialog.EXPIRED or "
                             "RelinkDialog.REVOKED.")
        self.infoLabel.setText(formatted_text)
        self.titleLabel.setFont(get_scaled_font(bold=True))
        self.infoLabel.setFont(get_scaled_font(scaling=0.9))

        # add app icon
        icon = QtGui.QIcon(APP_ICON_PATH)
        pixmap = icon_to_pixmap(icon, self.iconLabel.width(), self.iconLabel.height())
        self.iconLabel.setPixmap(pixmap)

        # format line edit
        self.lineEditAuthCode.setTextMargins(3, 0, 0, 0)

        # connect callbacks
        self.lineEditAuthCode.textChanged.connect(self._set_text_style)
        self.pushButtonCancel.clicked.connect(self._parent.quit)
        self.pushButtonUnlink.clicked.connect(self.delete_creds_and_quit)
        self.pushButtonLink.clicked.connect(self.on_link_clicked)

        # other
        self.pushButtonCancel.setFocus()
        self.adjustSize()

    @QtCore.pyqtSlot()
    def delete_creds_and_quit(self):
        self.auth_session.delete_creds()
        self._parent.quit(stop_daemon=True)

    @QtCore.pyqtSlot(str)
    def _set_text_style(self, text):
        if text == "":
            self.pushButtonLink.setEnabled(False)
            self.lineEditAuthCode.setStyleSheet("")
        elif text == self.INVALID_MSG:
            self.pushButtonLink.setEnabled(False)
            self.lineEditAuthCode.setStyleSheet("color: rgb(205, 0, 0); font: bold;")
        elif text == self.CONNECTION_ERR_MSG:
            self.pushButtonLink.setEnabled(False)
            self.lineEditAuthCode.setStyleSheet("color: rgb(205, 0, 0); font: bold;")
        elif text == self.VALID_MSG:
            self.pushButtonLink.setEnabled(False)
            self.pushButtonUnlink.setEnabled(False)
            self.pushButtonCancel.setEnabled(False)
            self.lineEditAuthCode.setStyleSheet("color: rgb(0, 129, 0); font: bold;")
        else:
            self.pushButtonLink.setEnabled(True)
            self.lineEditAuthCode.setStyleSheet("")

    @QtCore.pyqtSlot()
    def on_link_clicked(self):
        token = self.lineEditAuthCode.text()
        if token == "":
            # this should not occur because link button will be inactivate when there
            # is no text in QLineEdit
            return

        self.set_ui_busy()

        self.auth_task = BackgroundTask(
            parent=self,
            target=self.auth_session.verify_auth_token,
            args=(token,)
        )
        self.auth_task.sig_done.connect(self.on_verify_token_finished)

    @QtCore.pyqtSlot(object)
    def on_verify_token_finished(self, res):

        from maestral.oauth import OAuth2Session

        if res == OAuth2Session.Success:
            self.auth_session.save_creds()
            self.lineEditAuthCode.setText(self.VALID_MSG)
            QtWidgets.QApplication.processEvents()
            QtCore.QTimer.singleShot(200, self._parent.restart)
        elif res == OAuth2Session.InvalidToken:
            self.lineEditAuthCode.setText(self.INVALID_MSG)
            self.set_ui_idle()
        elif res == OAuth2Session.ConnectionFailed:
            self.lineEditAuthCode.setText(self.CONNECTION_ERR_MSG)
            self.set_ui_idle()

    def set_ui_busy(self):
        self.progressIndicator.startAnimation()
        self.lineEditAuthCode.setEnabled(False)
        self.pushButtonLink.setEnabled(False)
        self.pushButtonUnlink.setEnabled(False)
        self.pushButtonCancel.setEnabled(False)

    def set_ui_idle(self):
        self.progressIndicator.stopAnimation()
        self.lineEditAuthCode.setEnabled(True)
        self.pushButtonLink.setEnabled(True)
        self.pushButtonUnlink.setEnabled(True)
        self.pushButtonCancel.setEnabled(True)
