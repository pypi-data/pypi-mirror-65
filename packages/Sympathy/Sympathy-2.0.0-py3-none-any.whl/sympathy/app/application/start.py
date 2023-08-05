# This file is part of Sympathy for Data.
# Copyright (c) 2019 Combine Control Systems AB
#
# Sympathy for Data is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# Sympathy for Data is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sympathy for Data.  If not, see <http://www.gnu.org/licenses/>.
import sys
import os

# TODO: locating of icons is duplicated from sympathy.app.util.  Importing it
# is too expensive here. We should reorganize so that icon path and similar
# would be available without full sympathy.app.util and duplication.

_icon_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'Resources', 'icons'))


def create_gui_application(argv):
    import Qt.QtCore as QtCore
    import Qt.QtGui as QtGui
    import Qt.QtWidgets as QtWidgets
    from sympathy.platform import os_support as oss
    from sympathy.utils.prim import get_icon_path
    from .. import version

    oss.set_high_dpi_unaware()
    oss.set_application_id()

    app = QtWidgets.QApplication(argv)
    app.setApplicationName(version.application_name())
    QtCore.QLocale.setDefault(QtCore.QLocale('C'))

    ico = get_icon_path('application.png')
    app.setWindowIcon(QtGui.QIcon(ico))
    app.setApplicationVersion(version.version)
    return app


def create_cli_application(argv):
    # Using QApplication instead of QCoreApplication on
    # Windows to avoid QPixmap errors.
    import Qt.QtWidgets as QtWidgets
    import Qt.QtCore as QtCore
    from .. import version
    from .. import user_statistics

    user_statistics.user_started_sympathy('gui')

    if sys.platform == 'win32':
        app = QtWidgets.QApplication(argv)
    else:
        app = QtCore.QCoreApplication(argv)
    app.setApplicationName(version.application_name())
    app.setApplicationVersion(version.version)
    return app


def start_gui_application(parsed_args, argv):
    import Qt.QtWidgets as QtWidgets
    import Qt.QtGui as QtGui
    import Qt.QtCore as QtCore
    from .. import version
    from .. import user_statistics
    from .. windows import first_run
    from sympathy.platform import os_support
    from sympathy.utils.prim import get_icon_path
    user_statistics.user_started_sympathy('gui')
    os_support.set_application_name(version.application_name())

    app = create_gui_application(argv)
    teardown = [None]
    main_window = [None]

    def create_gui():
        from . import application
        main_window[0], teardown[0] = application.create_gui(parsed_args, argv)
        splash.finish(main_window[0])

        first_run.setup(main_window[0].closed)

        application.create_start_flow(main_window[0], parsed_args)

    # TODO: Replace with more suitable image.  Could be a more complex widget
    # but that would require something more complex since create_gui will block
    # the main thread.
    ico = get_icon_path('splash.png')
    pixmap = QtGui.QPixmap(ico)
    splash = QtWidgets.QSplashScreen(pixmap)
    splash.show()

    # Avoid rendering issues of splash on Linux.  Also, it looks better if the
    # splash does not flicker too quickly in case startup is very fast.
    # Symptom on Linux seems similar to:
    # https://bugreports.qt.io/browse/QTBUG-35757.  Though that issues is
    # marked as done, might be the same underlying problem shining through.
    QtCore.QTimer.singleShot(100, create_gui)
    polling_timer = user_statistics.create_polling_timer()
    polling_timer.start()
    try:
        return app.exec_()
    finally:
        polling_timer.stop()
        user_statistics.user_stopped_sympathy()
        if teardown[0]:
            teardown[0]()


def start_cli_application(parsed_args, argv):
    from . application import start_cli_application as start_cli
    # Ensure Q(Core)Application is live while the gui is executing.
    app = create_cli_application(argv)  # NOQA
    return start_cli(parsed_args, argv)
