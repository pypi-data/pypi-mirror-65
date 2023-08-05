#!/usr/bin/env python3

"""
Deploy Qt
"""

import sys
import os
import stat
import shutil
import argparse
from urllib.request import urlopen
import hashlib
import re
import subprocess
import logging

import cuteci


WORKING_DIR = os.getcwd()
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
MD5SUMS_FILENAME = "md5sums.txt"
DEFAULT_INSTALL_SCRIPT = os.path.join(CURRENT_DIR, "install-qt.qs")
UNEXISTING_PROXY = "192.168.0.100:44444"

EXIT_OK = 0
EXIT_ERROR = 1


log = logging.getLogger()
log.setLevel(logging.DEBUG)
console = logging.StreamHandler(sys.stdout)
console.setFormatter(
    logging.Formatter(fmt=("%(asctime)s " "[%(levelname)s] " "%(message)s"), datefmt="%Y-%m-%dT%H:%M:%S%z")
)
log.addHandler(console)


def _get_version(path):
    # qt-opensource-windows-x86-5.12.2.exe
    # qt-opensource-mac-x64-5.12.2.dmg
    # qt-opensource-linux-x64-5.12.2.run
    basename = os.path.basename(path)
    res = re.search(r"-(\d+\.\d+.\d+)\.", basename)
    if res is None:
        raise Exception(
            "Cannot get version from `{}` filename (expects name like: `qt-opensource-linux-x64-5.12.2.run`)".format(
                basename
            )
        )
    res.group(1)
    return res.group(1)


def _get_major_minor_ver(path):
    return ".".join(_get_version(path).split(".")[:1])


def _get_install_script(version):
    path = os.path.join(CURRENT_DIR, "install-qt-{}.qs".format(version))
    if not os.path.exists(path):
        log.info("No specific install script found, fallback to %s", DEFAULT_INSTALL_SCRIPT)
        path = DEFAULT_INSTALL_SCRIPT
    return path


class DeployQt:
    """
    Class in charge of Qt deployment
    """

    def __init__(self, show_ui, rm_installer, qt_installer, timeout):
        self.verbose = False
        self.show_ui = show_ui
        self.rm_installer = rm_installer
        self.timeout = timeout
        if qt_installer.startswith("http"):
            self.installer_path = None
            self.installer_url = qt_installer
        else:
            self.installer_path = qt_installer
            self.installer_url = None

    def _run_installer(self, env):
        # Set a fake proxy, then credentials are not required in the installer
        env.update({"http_proxy": UNEXISTING_PROXY, "https_proxy": UNEXISTING_PROXY})
        assert self.installer_path
        version = _get_major_minor_ver(self.installer_path)
        install_script = _get_install_script(version)
        cmd = [self.installer_path, "--script", install_script]
        if not self.show_ui:
            cmd.extend(["--platform", "minimal"])
        if self.verbose:
            cmd.extend(["--verbose"])
        log.info("Running installer %s", cmd)
        proc = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr, env=env)
        try:
            ret = proc.wait(self.timeout)
            if ret != 0 and ret != 3:  # 3: Installer has been exited nicely
                raise Exception("Installer neither returned 0 nor 3 exit code: {}".format(ret))
        except subprocess.TimeoutExpired:
            proc.kill()
            raise Exception("Timeout while waiting for the installer (waited {}s), kill it".format(self.timeout))

    def _cleanup(self):
        if self.rm_installer:
            assert self.installer_path
            log.info("Removing %s", self.installer_path)
            os.remove(self.installer_path)

    def _ensure_executable(self):
        assert self.installer_path
        os.chmod(self.installer_path, os.stat(self.installer_path).st_mode | stat.S_IEXEC)

    def download_qt(self):
        """
        Download Qt if possible, also verify checksums.

        :raises Exception: in case of failure
        """
        if not self.installer_url:
            log.info("Skip download: no url provided")
            return
        qt_url = self.installer_url
        filename = qt_url[qt_url.rfind("/") + 1 :]
        md5sums_url = qt_url[: qt_url.rfind("/")] + "/" + MD5SUMS_FILENAME

        self.installer_path = os.path.join(WORKING_DIR, filename)

        # Download Qt
        log.info("Download Qt %s", qt_url)

        def print_progress(size, length):
            # Print progress every 10%
            if not hasattr(print_progress, "prev"):
                print_progress.prev = -1  # Then 0% is printed
            percent = int(size * 100 / length)
            progress = percent - percent % 10
            if progress != print_progress.prev:
                log.info("Fetched %s%", progress)
                print_progress.prev = progress

        hash_md5 = hashlib.md5()
        with open(self.installer_path, "wb") as installer_file:
            req = urlopen(qt_url)
            length = int(req.getheader("content-length", 1500000000))
            size = 0
            while True:
                chunk = req.read(4096)
                if not chunk:
                    break
                size += len(chunk)
                hash_md5.update(chunk)
                installer_file.write(chunk)
                print_progress(size, length)

        # Download md5sums and check
        log.info("Download md5sums %s", md5sums_url)
        response = urlopen(md5sums_url)
        log.info("Check md5sums")
        if hash_md5.hexdigest() not in str(response.read()):
            log.error("Checksums do not match")
            return EXIT_ERROR
        log.info("Download OK %s", self.installer_path)

    def list_packages(self):
        """
        List available packages in Qt Installer.

        :raises Exception: in case of failure
        """
        self._ensure_executable()
        self.verbose = True  # Listing needs to be verbose
        env = os.environ.copy()
        env["LIST_PACKAGE_ONLY"] = "1"
        self._run_installer(env)
        self._cleanup()

    def install(self, packages, destdir, keep_tools, verbose):
        """
        Install Qt.

        :param list: packages to install
        :param str destdir: install directory
        :param keep_tools: if True, keep Qt Tools after installation
        :param bool verbose: enable verbosity
        :raises Exception: in case of failure
        """
        self._ensure_executable()
        self.verbose = verbose
        env = os.environ.copy()
        env["PACKAGES"] = packages
        env["DESTDIR"] = destdir
        self._run_installer(env)
        self._cleanup()

        if not keep_tools:
            log.info("Cleaning destdir")
            files = os.listdir(destdir)
            for name in files:
                fullpath = os.path.join(destdir, name)
                if re.match(r"\d+\.\d+.\d+", name):
                    # Qt stands in X.Y.Z dir, skip it
                    log.info("Keep %s", fullpath)
                    continue
                if os.path.isdir(fullpath):
                    shutil.rmtree(fullpath)
                else:
                    os.remove(fullpath)
                log.info("Remove %s", fullpath)


def main():
    """
    Command line tool to deploy Qt
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--version", action="version", version="{} {}".format(cuteci.__application__, cuteci.__version__)
    )
    parser.add_argument("--ui", action="store_true", default=False, help="Installer UI displayed")
    parser.add_argument("--rm", action="store_true", default=False, help="Remove Qt installer")
    parser.add_argument("--installer", required=True, help="Path or url to Qt installer")
    parser.add_argument("--timeout", type=int, default=180, help="Timeout in seconds, default 180")

    subparsers = parser.add_subparsers(dest="action")
    subparsers.required = True

    subparsers.add_parser(name="list")

    install_parser = subparsers.add_parser(name="install")
    install_parser.add_argument("--packages", required=True, help="Comma separated list of package to install")
    install_parser.add_argument("--destdir", required=True, help="Path to install Qt, e.g.: /opt/Qt")
    install_parser.add_argument("--keep-tools", action="store_true", default=False, help="Keep tools, samples, doc etc")
    install_parser.add_argument("--verbose", action="store_true", default=False, help="Print debug info")

    args = parser.parse_args()
    action = args.action

    deployer = DeployQt(args.ui, args.rm, args.installer, args.timeout)

    try:
        deployer.download_qt()
        log.info("Download OK - Qt Installer is ready")

        if action == "list":
            deployer.list_packages()
            log.info("Listing OK - available packages are printed above")
        else:
            deployer.install(args.packages, args.destdir, args.keep_tools, args.verbose)
            log.info("Installation OK")
    except Exception as exception:
        log.error("FAIL %s", str(exception))
        return EXIT_ERROR
    log.info("OK")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
