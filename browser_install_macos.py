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
import subprocess
import time
import requests

class Install(object):
    """Main installer logic"""
    def __init__(self):
        cpu = subprocess.check_output(['uname', '-m'], universal_newlines=True)
        rosetta = subprocess.check_output(['sysctl', '-in', 'sysctl.proc_translated'], universal_newlines=True)
        logging.debug("CPU Platform: %s, Translated: %s", cpu.strip(), rosetta.strip())
        if cpu.startswith('arm') or int(rosetta) == 1:
            self.chrome_path = {
                'Stable': 'https://dl.google.com/chrome/mac/universal/stable/GGRO/googlechrome.dmg',
                'Beta': 'https://dl.google.com/chrome/mac/universal/beta/googlechromebeta.dmg',
                'Dev': 'https://dl.google.com/chrome/mac/universal/dev/googlechromedev.dmg',
                'Canary': 'https://dl.google.com/chrome/mac/universal/canary/googlechromecanary.dmg'
            }
        else:
            self.chrome_path = {
                'Stable': 'https://dl.google.com/chrome/mac/stable/GGRO/googlechrome.dmg',
                'Beta': 'https://dl.google.com/chrome/mac/beta/googlechromebeta.dmg',
                'Dev': 'https://dl.google.com/chrome/mac/dev/googlechromedev.dmg',
                'Canary': 'https://dl.google.com/chrome/mac/canary/googlechromecanary.dmg'
            }
        self.firefox_path = {
            'Mozilla Firefox': 'https://download.mozilla.org/?product=firefox-latest-ssl&os=osx&lang=en-US',
        }
        self.dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'tmp')
        if not os.path.isdir(self.dir):
            os.makedirs(self.dir)
        self.status_file = os.path.join(self.dir, 'browser_install.json')
        self.status = None
        if os.path.isfile(self.status_file):
            with open(self.status_file, 'r') as f_in:
                self.status = json.load(f_in)
        if self.status is None:
            self.status = {}

    def save_status(self):
        """Save the installed state of the various browsers"""
        if self.status:
            with open(self.status_file, 'w') as f_out:
                json.dump(self.status, f_out, indent=4)

    def chrome(self, channel):
        """Install the given Chrome channel"""
        if channel in self.chrome_path:
            url = self.chrome_path[channel]
            name = 'Chrome ' + channel
            print("Checking {0}...".format(name))
            last_modified = None
            if name in self.status:
                last_modified = self.status[name]
            dmg, modified = self.download_installer(url, last_modified, 'dmg')
            if dmg is not None and os.path.isfile(dmg):
                ret = self.install_dmg(dmg, 'Google Chrome')
                if ret == 0 and modified is not None:
                    self.status[name] = modified
                try:
                    os.remove(dmg)
                except Exception:
                    pass

    def firefox(self, channel):
        """Install the given Firefox channel"""
        if channel in self.firefox_path:
            url = self.firefox_path[channel]
            name = 'Firefox ' + channel
            print("Checking {0}...".format(name))
            last_modified = None
            if name in self.status:
                last_modified = self.status[name]
            dmg, modified = self.download_installer(url, last_modified, 'dmg')
            if dmg is not None and os.path.isfile(dmg):
                ret = self.install_dmg(dmg, 'Firefox')
                if ret == 0 and modified is not None:
                    self.status[name] = modified
                try:
                    os.remove(dmg)
                except Exception:
                    pass

    def download_installer(self, url, last_modified, extension):
        """Download the given installer if it is newer"""
        exe = None
        modified = None
        headers = None
        if last_modified is not None:
            headers = {'If-Modified-Since': last_modified}
        dest = os.path.join(self.dir, 'browser.{}'.format(extension))
        if os.path.isfile(dest):
            try:
                os.remove(dest)
            except Exception:
                pass
        try:
            logging.debug('Downloading %s to %s', url, dest)
            response = requests.get(url, headers=headers, stream=True, timeout=300)
            if response.status_code == 200:
                if 'Last-Modified' in response.headers:
                    modified = response.headers['Last-Modified']
                elif 'Date' in response.headers:
                    modified = response.headers['Date']
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

    def install_dmg(self, dmg, mount_prefix):
        """Install a browser from a dmg file"""
        self.unmount(mount_prefix)
        subprocess.call(['sudo', 'hdiutil', 'attach', dmg])
        # Figure out the volume name where it mounted
        for volume in os.listdir('/Volumes'):
            if volume.startswith(mount_prefix):
                volume_path = os.path.join('/Volumes', volume)
                for app in os.listdir(volume_path):
                    if app.endswith('app'):
                        app_path = os.path.join(volume_path, app)
                        subprocess.call(['sudo', 'cp', '-R', app_path, '/Applications/'])
        self.unmount(mount_prefix)
    
    def unmount(self, mount_prefix):
        """Unmount all volumes with the given prefix"""
        for volume in os.listdir('/Volumes'):
            if volume.startswith(mount_prefix):
                subprocess.call(['sudo', 'hdiutil', 'detach', os.path.join('/Volumes', volume)])

    def install_thread(self):
        """Do the actual install"""
        for channel in self.chrome_path:
            self.chrome(channel)
        for channel in self.firefox_path:
            self.firefox(channel)
        self.save_status()

    def install(self):
        """Run the install (in a background thread) for up to an hour"""
        import threading
        thread = threading.Thread(target=self.install_thread)
        thread.daemon = True
        thread.start()
        thread.join(3600)

##########################################################################
#   Main Entry Point
##########################################################################
def main():
    """Main entry point"""
    # Set up logging
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s.%(msecs)03d - %(message)s", datefmt="%H:%M:%S")

    start = time.time()
    install = Install()
    install.install()

    end = time.time()
    elapsed = end - start
    logging.debug("Browser install done, Elapsed Time: %0.4f", elapsed)

if __name__ == '__main__':
    main()
