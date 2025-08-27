# Copyright (c) 2022, Riverbank Computing Limited
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


import os
import toml

from ... import (AbstractPyQtComponent, ComponentOption, ExtensionModule,
        PythonModule, PythonPackage)


# All the parts that can be provided by the component.
_ALL_PARTS = {
    'PyQt6': PythonModule(deps='Python:pkgutil'),
    'PyQt6.QAxContainer':
        ExtensionModule(target='win', deps='PyQt6.QtWidgets',
                libs='-lQAxContainer', qmake_qt='axcontainer'),
    'PyQt6.Qt': ExtensionModule(deps='PyQt6', libs='-lQt'),
    'PyQt6.QtAndroidExtras':
        ExtensionModule(target='android', deps='PyQt6.QtCore',
                libs='-lQtAndroidExtras', qmake_qt='androidextras'),
    'PyQt6.QtBluetooth':
        ExtensionModule(deps='PyQt6.QtCore', libs='-lQtBluetooth',
                qmake_qt='bluetooth'),
    'PyQt6.QtCore':
        ExtensionModule(deps=('SIP:PyQt6.sip', 'PyQt6'), libs='-lQtCore'),
    'PyQt6.QtDBus':
        ExtensionModule(deps='PyQt6.QtCore', libs='-lQtDBus', qmake_qt='dbus'),
    'PyQt6.QtGui': ExtensionModule(deps='PyQt6.QtCore', libs='-lQtGui'),
    'PyQt6.QtHelp':
        ExtensionModule(deps='PyQt6.QtWidgets', libs='-lQtHelp',
                qmake_qt='help'),
    'PyQt6.QtLocation':
        ExtensionModule(deps='PyQt6.QtPositioning', libs='-lQtLocation',
                qmake_qt='location'),
    'PyQt6.QtMacExtras':
        ExtensionModule(target='ios|macos', deps='PyQt6.QtGui',
                libs='-lQtMacExtras', qmake_qt='macextras'),
    'PyQt6.QtMultimedia':
        ExtensionModule(deps=('PyQt6.QtGui', 'PyQt6.QtNetwork'),
                libs='-lQtMultimedia', qmake_qt='multimedia'),
    'PyQt6.QtMultimediaWidgets':
        ExtensionModule(deps=('PyQt6.QtMultimedia', 'PyQt6.QtWidgets'),
                libs='-lQtMultimediaWidgets', qmake_qt='multimediawidgets'),
    'PyQt6.QtNetwork':
        ExtensionModule(deps='PyQt6.QtCore', libs='-lQtNetwork',
                qmake_qt='network'),
    'PyQt6.QtNetworkAuth':
        ExtensionModule(deps='PyQt6.QtNetwork', libs='-lQtNetworkAuth',
                qmake_qt=('network', 'networkauth')),
    'PyQt6.QtNfc':
        ExtensionModule(deps='PyQt6.QtCore', libs='-lQtNfc', qmake_qt='nfc'),
    'PyQt6.QtOpenGL':
        ExtensionModule(deps='PyQt6.QtWidgets', libs='-lQtOpenGL',
                qmake_qt='opengl'),
    'PyQt6.QtPositioning':
        ExtensionModule(deps='PyQt6.QtCore', libs='-lQtPositioning',
                qmake_qt='positioning'),
    'PyQt6.QtPrintSupport':
        ExtensionModule(target='!ios', deps='PyQt6.QtWidgets',
                libs='-lQtPrintSupport', qmake_qt='printsupport'),
    'PyQt6.QtQml':
        ExtensionModule(deps='PyQt6.QtNetwork', libs='-lQtQml',
                qmake_qt='qml'),
    'PyQt6.QtQuick':
        ExtensionModule(deps=('PyQt6.QtGui', 'PyQt6.QtQml'), libs='-lQtQuick',
                qmake_qt='quick'),
    'PyQt6.QtQuick3D':
        ExtensionModule(min_version=(5, 15),
                deps=('PyQt6.QtGui', 'PyQt6.QtQml'), libs='-lQtQuick3D',
                qmake_qt='quick3d'),
    'PyQt6.QtQuickWidgets':
        ExtensionModule(deps=('PyQt6.QtQuick', 'PyQt6.QtWidgets'),
                libs='-lQtQuickWidgets', qmake_qt='quickwidgets'),
    'PyQt6.QtRemoteObjects':
        ExtensionModule(deps='PyQt6.QtCore', libs='-lQtRemoteObjects',
                qmake_qt='remoteobjects'),
    'PyQt6.QtSensors':
        ExtensionModule(deps='PyQt6.QtCore', libs='-lQtSensors',
                qmake_qt='sensors'),
    'PyQt6.QtSerialPort':
        ExtensionModule(deps='PyQt6.QtCore', libs='-lQtSerialPort',
                qmake_qt='serialport'),
    'PyQt6.QtSql':
        ExtensionModule(deps='PyQt6.QtWidgets', libs='-lQtSql',
                qmake_qt='sql'),
    'PyQt6.QtSvg':
        ExtensionModule(deps='PyQt6.QtWidgets', libs='-lQtSvg',
                qmake_qt='svg'),
    'PyQt6.QtTest':
        ExtensionModule(deps='PyQt6.QtWidgets', libs='-lQtTest',
                qmake_qt='testlib'),
    'PyQt6.QtTextToSpeech':
        ExtensionModule(min_version=(5, 15, 1), deps='PyQt6.QtCore',
                libs='-lQtTextToSpeech', qmake_qt='texttospeech'),
    'PyQt6.QtWebChannel':
        ExtensionModule(deps='PyQt6.QtCore', libs='-lQtWebChannel',
                qmake_qt='webchannel'),
    'PyQt6.QtWebSockets':
        ExtensionModule(deps='PyQt6.QtNetwork', libs='-lQtWebSockets',
                qmake_qt='websockets'),
    'PyQt6.QtWidgets':
        ExtensionModule(deps='PyQt6.QtGui', libs='-lQtWidgets',
                qmake_qt='widgets'),
    'PyQt6.QtWinExtras':
        ExtensionModule(target='win', deps='PyQt6.QtWidgets',
                libs='-lQtWinExtras', qmake_qt='winextras'),
    'PyQt6.QtX11Extras':
        ExtensionModule(target='linux', deps='PyQt6.QtCore',
                libs='-lQtX11Extras', qmake_qt='x11extras'),
    'PyQt6.QtXml':
        ExtensionModule(deps='PyQt6.QtCore', libs='-lQtXml', qmake_qt='xml'),
    'PyQt6.QtXmlPatterns':
        ExtensionModule(deps='PyQt6.QtNetwork', libs='-lQtXmlPatterns',
                qmake_qt='xmlpatterns'),
    'PyQt6._QOpenGLFunctions_2_0':
        ExtensionModule(deps='PyQt6.QtGui', libs='-l_QOpenGLFunctions_2_0'),
    'PyQt6._QOpenGLFunctions_2_1':
        ExtensionModule(deps='PyQt6.QtGui', libs='-l_QOpenGLFunctions_2_1'),
    'PyQt6._QOpenGLFunctions_4_1_Core':
        ExtensionModule(deps='PyQt6.QtGui',
                libs='-l_QOpenGLFunctions_4_1_Core'),
    'PyQt6._QOpenGLFunctions_ES2':
        ExtensionModule(deps='PyQt6.QtGui', libs='-l_QOpenGLFunctions_ES2'),
    'PyQt6.uic':
        PythonPackage(
                deps=('Python:io', 'Python:logging', 'Python:os', 'Python:re',
                        'Python:traceback', 'Python:xml.etree.ElementTree'),
                exclusions=('port_v2', 'pyuic.py')),
}


class PyQtComponent(AbstractPyQtComponent):
    """ The PyQt component. """

    # The list of components that, if specified, should be installed before
    # this one.
    preinstalls = ['Python', 'Qt', 'SIP']

    def get_archive_name(self):
        """ Return the filename of the source archive. """

        if self._license_file is not None:
            #osh return 'PyQt6_commercial-{}.tar.gz'.format(self.version)
            return 'PyQt6_commercial-{}.tar.gz'.format(self.version)

        #osh return 'PyQt6-{}.tar.gz'.format(self.version)
        return 'PyQt6-{}.tar.gz'.format(self.version)

    def get_archive_urls(self):
        """ Return the list of URLs where the source archive might be
        downloaded from.
        """

        if self._license_file is not None:
            return super().get_archive_urls()

        return self.get_pypi_urls('PyQt6')

    def get_options(self):
        """ Return a list of ComponentOption objects that define the components
        configurable options.
        """

        options = super().get_options()

        options.append(
                ComponentOption('disabled_features', type=list,
                        help="The features that are disabled."))

        valid_modules = sorted(
                [name[len('PyQt6.'):]
                        for name in _ALL_PARTS
                                if name not in ('PyQt6', 'PyQt6.uic')])

        options.append(
                ComponentOption('installed_modules', type=list, required=True,
                        values=valid_modules,
                        help="The extension modules to be installed."))

        return options

    def install(self):
        """ Install for the target. """

        # See if there is a license file.
        self._license_file = self.get_file('pyqt-commercial.sip')

        # Unpack the source.
        self.unpack_archive(self.get_archive())

        # Copy any license file.
        if self._license_file is not None:
            self.copy_file(self._license_file, 'sip')

        # Configure the project and bindings.
        project_config = {
            'confirm-license': True,
            'designer-plugin': False,
            'qml-plugin': False,
            'dbus-python': False,
            'tools': False,
        }

        bindings_config = {
            'disabled-features': self.disabled_features,
        }

        self.install_pyqt_component(self, project=project_config,
                bindings=bindings_config, enable=self.installed_modules)

    def install_pyqt_component(self, component, project=None, bindings=None,
            enable=None):
        """ Install a PyQt-based component. """

        # Load the component's pyproject.toml file.
        try:
            pyproject = toml.load('pyproject.toml')
        except FileNotFoundError:
            component.error("Unable to find 'pyproject.toml'")
        except Exception as e:
            component.error("There was an error loading 'pyproject.toml'",
                    detail=str(e))

        # Get the relevent sections.
        project_section = self._get_section('tool.sip.project', pyproject)
        bindings_section = self._get_section('tool.sip.bindings', pyproject)

        # Re-configure the build.
        python = self.get_component('Python')

        project_section['py-platform'] = self.pyqt_platform
        project_section['py-major-version'] = python.version.major
        project_section['py-minor-version'] = python.version.minor
        project_section['py-include-dir'] = python.target_py_include_dir
        project_section['py-pylib-dir'] = component.target_lib_dir
        project_section['py-pylib-lib'] = python.target_py_lib
        project_section['target-dir'] = python.target_sitepackages_dir

        # See if a limited set of modules are being installed.
        if enable is not None:
            project_section['enable'] = enable

            # Make sure there is a section so that we can configure it later.
            for module in enable:
                if module not in bindings_section:
                    bindings_section[module] = {}

        # Apply any additional component-specific values.
        if project is not None:
            project_section.update(project)

        for module in bindings_section.values():
            if isinstance(module, dict):
                module['static'] = True

                # Apply any additional component-specific values.
                if bindings is not None:
                    module.update(bindings)

        # Save the modified pyproject.toml file.
        try:
            with open('pyproject.toml', 'w') as f:
                toml.dump(pyproject, f)
        except Exception as e:
            component.error("Unable to write modified 'pyproject.toml'",
                    detail=str(e))

        # Run sip-install.
        args = [
            'sip-install',
            '--qmake', self.get_component('Qt').host_qmake,
            '--no-distinfo',
            '--concatenate', '2',
            '--no-docstrings'
        ]

        if self.target_platform_name == 'android':
            args.append('--android-abi')
            args.append(self.android_abi)

        if self.verbose_enabled:
            args.append('--verbose')

        self.run(*args)

    @property
    def provides(self):
        """ The dict of parts provided by the component. """

        parts = {
            'PyQt6': _ALL_PARTS['PyQt6'],
            'PyQt6.uic': _ALL_PARTS['PyQt6.uic'],
        }

        for name in self.installed_modules:
            name = 'PyQt6.' + name

            part = _ALL_PARTS[name]

            if name == 'PyQt6.QtCore':
                lib_dir = os.path.join(
                        self.get_component('Python').target_sitepackages_dir,
                        'PyQt6')

                part.libs = ('-L' + lib_dir,) + part.libs

            parts[name] = part

        return parts

    @property
    def pyqt_platform(self):
        """ The target platform name as recognised by PyQt. """

        pyqt_platform = self.target_platform_name

        if pyqt_platform == 'android':
            pyqt_platform = 'linux'
        elif pyqt_platform in ('ios', 'macos'):
            pyqt_platform = 'darwin'
        elif pyqt_platform == 'win':
            pyqt_platform = 'win32'

        return pyqt_platform

    def verify(self):
        """ Verify the component. """

        # v5.14 is the first version supported by SIP v5.
        if self.version < (5, 14):
            self.unsupported()

        if self.version > (5, 15):
            self.untested()

        # Note that we should read the minimum versions from pyproject.toml.
        self.verify_pyqt_component(self.version,
                min_sipbuild_version=(6, 6, 2), min_pyqtbuild_version=(1, 9))

        # This is needed by dependent components.
        if not self.get_component('Qt').ssl:
            self.disabled_features.append('PyQt_SSL')

    def verify_pyqt_component(self, min_pyqt_version, min_sipbuild_version,
            min_pyqtbuild_version):
        """ Verify a PyQt-based component.  All versions are minimum versions.
        """

        # Check the name of the sip module and the ABI version that are being
        # provided by the SIP component.
        sip = self.get_component('SIP')

        #osh sip_module = 'PyQt6.sip'
        sip_module = 'PyQt6.sip'

        print(sip.module_name) #osh
        print("----")
        print(sip_module) #osh
        
        if sip.module_name != sip_module:
            #osh  component.error(
            self.error(
                    "sip module '{0}' is required but '{1}' is provided".format(
                            sip_module, sip.module_name))

        #osh abi_major_version = 12
        abi_major_version = 13

        if abi_major_version != sip.abi_major_version:
            #osh component.error(
            self.error(
                    "sip module ABI v{0} is required but v{1} is provided".format(
                            abi_major_version, sip.abi_major_version))

        # Check the minimum PyQt requirement, ignoring the patch version and
        # making sure it is the same major version.
        min_pyqt_version = self.parse_version_number(min_pyqt_version)

        if min_pyqt_version.major != self.version.major or min_pyqt_version.minor > self.version.minor:
            self.error(
                    "PyQt v{} or later is required".format(min_pyqt_version))

        # Check the minimum SIP and PyQt-builder requirement.
        # TODO: this assumes that pyqtdeploy and PyQt-builder are installed in
        # the same venv which may not be the case.  Therefore we either need a
        # way of querying the version of PyQt-builder from the command line.
        min_sipbuild_version = self.parse_version_number(min_sipbuild_version)

        if min_sipbuild_version.major == 5 and sip.version.major in (5, 6):
            # We assume that all PyQt dependent projects don't use features
            # deprecated in SIP v6.
            pass
        elif min_sipbuild_version.major != sip.version.major:
            self.error(
                    "SIP v{} is required".format(min_sipbuild_version.major))

        if min_sipbuild_version > sip.version:
            self.error(
                    "SIP v{} or later is required".format(
                            min_sipbuild_version))

        # Check the minimum PyQt-builder requirement, making sure it is the
        # same major version.
        min_pyqtbuild_version = self.parse_version_number(
                min_pyqtbuild_version)

        try:
            from pyqtbuild import PYQTBUILD_VERSION
        except ImportError:
            PYQTBUILD_VERSION = 0

        pyqtbuild_version = self.parse_version_number(PYQTBUILD_VERSION)

        if min_pyqtbuild_version.major != pyqtbuild_version.major or min_pyqtbuild_version > pyqtbuild_version:
            self.error(
                    "PyQt-builder v{} or later is required".format(
                            min_pyqtbuild_version))

    @staticmethod
    def _get_section(name, pyproject):
        """ Return a dict containing the named section from a pyproject.toml
        file.
        """

        section = pyproject

        for section_name in name.split('.'):
            # A section might be missing so make sure it is there (and empty).
            if section_name not in section:
                section[section_name] = {}

            section = section[section_name]

            if not isinstance(section, dict):
                return {}

        return section
