#!/usr/bin/env python
"""
Copyright 2016 Google Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import json
import logging
import os
import platform
import time
import requests

class Install(object):
    """Main installer logic"""
    def __init__(self):
        if platform.machine().endswith('64'):
            firefox_os = 'win64'
            self.chrome_path = {
                'Stable': 'https://dl.google.com/tag/s/'\
                          'appguid%3D%7B8A69D345-D564-463C-AFF1-A69D9E530F96%7D%26'\
                          'iid%3D%7B3C078BAD-5ACB-D945-6C84-7F778A6383F1%7D%26lang%3Den%26'\
                          'browser%3D4%26usagestats%3D0%26appname%3DGoogle%2520Chrome%26'\
                          'needsadmin%3Dtrue%26ap%3Dx64-stable-statsdef_1%26'\
                          'installdataindex%3Ddefaultbrowser'\
                          '/chrome/install/ChromeStandaloneSetup64.exe',
                'Beta': 'https://dl.google.com/tag/s/'\
                        'appguid%3D%7B8237E44A-0054-442C-B6B6-EA0509993955%7D%26'\
                        'iid%3D%7B8F94C426-F48E-944F-58B4-56AC548C0A6F%7D%26lang%3Den%26'\
                        'browser%3D4%26usagestats%3D0%26appname%3DChrome%2520Beta%26'\
                        'needsadmin%3Dtrue%26ap%3D-arch_x64-statsdef_1%26'\
                        'installdataindex%3Dempty'\
                        '/chrome/install/beta/ChromeBetaStandaloneSetup64.exe',
                'Dev': 'https://dl.google.com/tag/s/'\
                       'appguid%3D%7B401C381F-E0DE-4B85-8BD8-3F3F14FBDA57%7D%26'\
                       'iid%3D%7B3C078BAD-5ACB-D945-6C84-7F778A6383F1%7D%26lang%3Den%26'\
                       'browser%3D4%26usagestats%3D0%26appname%3DGoogle%2520Chrome%2520Dev%26'\
                       'needsadmin%3Dtrue%26ap%3D-arch_x64-statsdef_1%26'\
                       'installdataindex%3Dempty'\
                       '/chrome/install/dev/ChromeDevStandaloneSetup64.exe'
            }
        else:
            self.chrome_path = {
                'Stable': 'https://dl.google.com/tag/s/'\
                          'appguid%3D%7B8A69D345-D564-463C-AFF1-A69D9E530F96%7D%26'\
                          'iid%3D%7B3C078BAD-5ACB-D945-6C84-7F778A6383F1%7D%26lang%3D'\
                          'en%26browser%3D4%26usagestats%3D0%26appname%3DGoogle%2520Chrome%26'\
                          'needsadmin%3Dtrue%26ap%3Dstable-arch_x86-statsdef_1%26'\
                          'installdataindex%3Ddefaultbrowser'\
                          '/chrome/install/ChromeStandaloneSetup.exe',
                'Beta': 'https://dl.google.com/tag/s/'\
                        'appguid%3D%7B8237E44A-0054-442C-B6B6-EA0509993955%7D%26'\
                        'iid%3D%7B8F94C426-F48E-944F-58B4-56AC548C0A6F%7D%26lang%3Den%26'\
                        'browser%3D4%26usagestats%3D0%26appname%3DChrome%2520Beta%26'\
                        'needsadmin%3Dtrue%26ap%3D-arch_x86-statsdef_1%26'\
                        'installdataindex%3Dempty'\
                        '/chrome/install/beta/ChromeBetaStandaloneSetup.exe',
                'Dev': 'https://dl.google.com/tag/s/'\
                       'appguid%3D%7B401C381F-E0DE-4B85-8BD8-3F3F14FBDA57%7D%26'\
                       'iid%3D%7B3C078BAD-5ACB-D945-6C84-7F778A6383F1%7D%26lang%3Den%26'\
                       'browser%3D4%26usagestats%3D0%26appname%3DGoogle%2520Chrome%2520Dev%26'\
                       'needsadmin%3Dtrue%26ap%3D-arch_x86-statsdef_1%26'\
                       'installdataindex%3Dempty'\
                       '/chrome/install/dev/ChromeDevStandaloneSetup.exe'
            }
            firefox_os = 'win'

        firefox_url = 'http://download.mozilla.org/?product={0}&lang=en-US&os=' + firefox_os
        self.firefox_path = {
            'Mozilla Firefox': firefox_url.format('firefox-latest'),
            'Mozilla Firefox ESR': firefox_url.format('firefox-esr-latest'),
            'Mozilla Firefox Beta': firefox_url.format('firefox-beta-latest'),
            'Mozilla Firefox Dev': firefox_url.format('firefox-devedition-latest'),
            'Nightly': firefox_url.format('firefox-nightly-latest')
        }
        self.dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'tmp')
        if not os.path.isdir(self.dir):
            os.makedirs(self.dir)
        self.status_file = os.path.join(self.dir, 'browser_install.json')
        self.status = None
        if os.path.isfile(self.status_file):
            with open(self.status_file, 'rb') as f_in:
                self.status = json.load(f_in)
        if self.status is None:
            self.status = {}

    def save_status(self):
        """Save the installed state of the various browsers"""
        if self.status:
            with open(self.status_file, 'wb') as f_out:
                json.dump(self.status, f_out, indent=4)

    def chrome(self, channel):
        """Install the given Chrome channel"""
        if channel in self.chrome_path:
            url = self.chrome_path[channel]
            name = 'Chrome ' + channel
            print "Checking {0}...".format(name)
            last_modified = None
            if name in self.status:
                last_modified = self.status[name]
            exe, modified = self.download_installer(url, last_modified)
            if exe is not None and os.path.isfile(exe):
                ret = self.run_elevated(exe, '/silent /install')
                if ret == 0 and modified is not None:
                    self.status[name] = modified
                try:
                    os.remove(exe)
                except Exception:
                    pass

    def firefox(self, channel):
        """Install the given Firefox channel"""
        if channel in self.firefox_path:
            url = self.firefox_path[channel]
            name = channel
            print "Checking {0}...".format(name)
            last_modified = None
            if name in self.status:
                last_modified = self.status[name]
            exe, modified = self.download_installer(url, last_modified)
            if exe is not None and os.path.isfile(exe):
                # Create an ini file for the installer to use
                ini_file = os.path.join(self.dir, 'firefox.ini')
                with open(ini_file, 'wb') as ini:
                    ini.write("[Install]\n")
                    ini.write("InstallDirectoryName={0}\n".format(channel))
                    ini.write("MaintenanceService=false\n")
                ret = self.run_elevated(exe, '/INI="{0}"'.format(ini_file))
                if ret == 0 and modified is not None:
                    self.status[name] = modified
                try:
                    os.remove(exe)
                    os.remove(ini_file)
                except Exception:
                    pass


    def download_installer(self, url, last_modified):
        """Download the given installer if it is newer"""
        exe = None
        modified = None
        headers = {'If-Modified-Since': last_modified}
        dest = os.path.join(self.dir, 'browser_install.exe')
        if os.path.isfile(dest):
            try:
                os.remove(dest)
            except Exception:
                pass
        try:
            logging.debug('Downloading %s to %s', url, dest)
            response = requests.get(url, headers=headers, stream=True)
            if response.status_code == 200:
                modified = response.headers['Last-Modified']
                with open(dest, 'wb') as f_out:
                    for chunk in response.iter_content(chunk_size=4096):
                        f_out.write(chunk)
                exe = dest
        except Exception as err:
            msg = ''
            if err is not None and err.__str__() is not None:
                msg = err.__str__()
            logging.exception("Download failed: %s", msg)
        return exe, modified

    def run_elevated(self, command, args):
        """Run the given command as an elevated user and wait for it to return"""
        ret = 1
        if command.find(' ') > -1:
            command = '"' + command + '"'
        import win32api
        import win32con
        import win32event
        import win32process
        from win32com.shell.shell import ShellExecuteEx
        from win32com.shell import shellcon
        logging.debug(command + ' ' + args)
        process_info = ShellExecuteEx(nShow=win32con.SW_HIDE,
                                      fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
                                      lpVerb='runas',
                                      lpFile=command,
                                      lpParameters=args)
        wait_result = win32event.WaitForSingleObject(process_info['hProcess'], 300000)
        if wait_result == win32event.WAIT_TIMEOUT:
            win32process.TerminateProcess(process_info['hProcess'], 13)
        ret = win32process.GetExitCodeProcess(process_info['hProcess'])
        win32api.CloseHandle(process_info['hProcess'])
        return ret

##########################################################################
#   Main Entry Point
##########################################################################
def main():
    """Main entry point"""
    import argparse
    parser = argparse.ArgumentParser(description='Automated browser installer/updater.',
                                     prog='browser_install')
    parser.add_argument('-v', '--verbose', action='count',
                        help="Increase verbosity (specify multiple times for more)."\
                        " -vvvv for full debug output.")
    parser.add_argument('-a', '--all', action='store_true', default=False,
                        help="All supported browsers.")
    parser.add_argument('-c', '--chrome', action='store_true', default=False, help="Chrome.")
    parser.add_argument('-f', '--firefox', action='store_true', default=False, help="Firefox.")
    parser.add_argument('-s', '--stable', action='store_true', default=False,
                        help="Stable releases (includes ESR and dev edition for Firefox).")
    parser.add_argument('-b', '--beta', action='store_true', default=False, help="Beta releases.")
    parser.add_argument('-d', '--dev', action='store_true', default=False,
                        help="Dev releases (Nightly for Firefox, Dev channel for Chrome).")
    options, _ = parser.parse_known_args()

    # Set up logging
    log_level = logging.CRITICAL
    if options.verbose == 1:
        log_level = logging.ERROR
    elif options.verbose == 2:
        log_level = logging.WARNING
    elif options.verbose == 3:
        log_level = logging.INFO
    elif options.verbose >= 4:
        log_level = logging.DEBUG
    logging.basicConfig(
        level=log_level, format="%(asctime)s.%(msecs)03d - %(message)s", datefmt="%H:%M:%S")

    start = time.time()
    if options.all:
        options.chrome = True
        options.firefox = True
        options.stable = True
        options.beta = True
        options.dev = True

    install = Install()
    if options.chrome:
        if options.stable:
            install.chrome('Stable')
        if options.beta:
            install.chrome('Beta')
        if options.dev:
            install.chrome('Dev')
    if options.firefox:
        if options.stable:
            install.firefox('Mozilla Firefox')
            install.firefox('Mozilla Firefox ESR')
            install.firefox('Mozilla Firefox Dev')
        if options.beta:
            install.firefox('Mozilla Firefox Beta')
        if options.dev:
            install.firefox('Nightly')
    install.save_status()

    end = time.time()
    elapsed = end - start
    logging.debug("Browser install done, Elapsed Time: %0.4f", elapsed)

if __name__ == '__main__':
    main()
