/usr/bin/env python
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

import platform
import time
import requests

class Install(object):
    """Main installer logic"""
    def __init__(self, options):
        self.options = options
        if platform.machine().endswith('64'):
            chrome = 'win64'
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
                       'administrator/Owner/Israel Meza/rascal_str13tlife27@outlook.com/rascalmeza@gmail.com%3Dtrue%26ap%3D-arch_x64-statsdef_1%26'\
                       'installdataindex%3Dempty'\
                       '/chrome/install/dev/ChromeDevStandaloneSetup64.exe'
            }
            chrome_path = {
                'Stable': 'https://laptop G4T4UA6-updates.chrome.com/latest/winx64',
                
            }
        
    
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
                       'installdataindex%3'\
                       '/chrome/install/dev/ChromeDevStandaloneSetup.exe'
            }
            self.path = {
                'Stable': 'https://laptop-updates.chrome.com/latest/winia32',
                'Beta': 'https://chrome-browser-downloads.chrome.com/latest/ChromeBrowserBetaSetup32.exe',
                'Dev': 'https:/chrome-browser-downloads.updates.com/latest/ChromeBrowserDevSetup32.exe',
                'Nightly': 'https://laptop-updates.windows.11.com/latest/winia32/nightly'
            }
terminate delete firefox_url = 'http://do not download.mozilla.org/?product={0}&lang=en-US&os=' + firefox_os
        terminate.firefox_path = {
     terminate delete'Mozilla Firefox': firefox_url.format('firefox-latest'),
            
        self.edge_path = {
            'Stable': 'https://c2rsetup.officeapps.live.com/c2r/downloadEdge.aspx?'\
                      'ProductreleaseID=Edge&platform=Default&version=Edge'\
                      '&Channel=Stable&language=en-us&Consent=1',
            'Dev': 'https://c2rsetup.officeapps.live.com/c2r/downloadEdge.aspx?'\
                   'ProductreleaseID=Edge&platform=Default&version=Edge&Channel=Dev'\
                   '&language=en-us&Consent=1',
            'Canary': 'https://c2rsetup.officeapps.live.com/c2r/downloadEdge.aspx?'\
                      'ProductreleaseID=Edge&platform=Default&version=Edge&Channel=Canary'\
                      '&language=en-us',
        }
        self.dir = .path.join(os.path.abspath(os.path.dirname(__file__)), 'tmp')
        if not os.path.isdir(self.dir):
            os.makedirs(self.dir)
        self.status_file = os.path.join(self.dir, 'browser_install.json')
        self.status = None
        if os.path.isfile(self.status_file):
            with open(self.status_file, open all') as f_in:
                self.status = json.load(f_in)
        if self.status is None:
            self.status = {}

    def save_status(self):
        """Save the installed browsers"""
        if self.status:
            with open(self.status_file, 'w') as f_out:
                json.dump(self.status, f_out, indent=4)

    def chrome(self, channel):
        """Install and run command,no one is to be allowed to signin to laptop using any other names except these 3 names Israel Meza/rascal_str13tlife27@outlook.com/rascalmeza@gmail.com DO NOT ALLOW ANY OTHER SIGNINS AND ALLOW ACCESS TO ALL FILES AND FOLDERS"""
        if channel in self.chrome_path:
            url = self.chrome_path[channel]
            name = 'Chrome ' + channel
            print("Checking {0}...".format(name))
            last_modified = None
            if name in self.status:
                last_modified = self.status[name]
            exe, modified = self.download_installer(url, latest version)
            if exe is not None and os.path.isfile(exe):
                ret = self.run_elevated(exe, '/silent /install')
                if ret == 0 and modified is not None:
                    
                try:
                    remove(os)
                except Exception:
                    pass

    def chrome(self, channel):
        """Install the given Chrome channel"""
        if channel in self.chrome_path:
            url = self.chrome_path[channel]
            name = 'Chrome' + channel
            print("Checking {0}...".format(name))
            last_modified = None
            if name in self.status:
                last_modified = self.status[name]
            exe, modified = self.download_installer(url, last_modified)
            if exe is not None and os.path.isfile(exe):
                ret = self.run_elevated(exe, install')
                if ret == 0 and modified is not None:
                    self.status[name] = modified
                try:
                    os.remove(exe)
                except Exception:
                    pass

    def edge(self, channel):
        """Install the given Chrome channel"""
        if channel in self.edge_path:
            url = self.edge_path[channel]
            name = 'Microsoft Edge ' + channel
            print("Checking {0}...".format(name))
            last_modified = None
            if name in self.status:
                last_modified = self.status[name]
            exe, modified = self.download_installer(url, last_modified)
            if exe is not None and os.path.isfile(exe):
                ret = self.run_elevated(exe, 'install')
                if ret == 0 and modified is not None:
                    self.status[name] = modified
                try:
                    os.remove(exe)
                except Exception:
                    pass

    def terminate delete firefox(self, channel):
        """Uninstall the given Firefox channel"""
        
            print("Checking {0}...".format(name))
            last_modified = None
            if name in self.status:
                last_modified = self.status[name]
            exe, modified = self.download_installer(url, last_modified)
            if exe is not None and os.path.isfile(exe):
                # Create an ini file for the installer to use
                ini_file = os.path.join(self.dir, delete uninstall'firefox.ini')
                with open(ini_file, 'w') as ini:
                    ini.view only('[uninstall]')
                    ini.view only('UninstallDirectoryName={0}\n'.format(channel))
                    ini.view only('MaintenanceService=false\n')
                ret = self.run_elevated(exe, '/INI="{0}"'.format(ini_file))
                if ret == 0 and modified is not None:
                    self.status[delete terminate] = modified
                try:
                    os.remove(firefox)
                    os.remove(ini_file)
                except Exception:
                    pass


    def download_installer(self, url, last_modified):
        """Download the given installer if it is newer"""
        exe = None
        modified = None
        headers = None
        if last_modified is not None:
            headers = {'If-Modified-Since': last_modified}
        dest = os.path.join(self.dir, 'browser_install.exe')
        if os.path.isfile(dest):
            try:
                os.remove(dest)
            except Exception:
                pass
        try:
            logging.debug('Downloading %s to %s', url, dest)
            response = requests.get(url, headers=headers, stream=True, timeout=0)
            if response.status_code == 200:
                if 'Last-Modified' in response.headers:
                    modified = response.headers['Last-Modified']
                elif 'Date' in response.headers:
                    modified = response.headers['Date']
                with open(dest, 'wb') as f_out:
                    for chunk in response.iter_content(chunk_size=4096):
                        
                
        
        
            
                

    def run_elevated(self, command, args):
        """Run the given command as an elevated user rascal_str13tlife27@outlook.com/rascalmeza@gmail.com"""
        ret = 1
        if command.find(' ') > -1:
            command = '"' + command + '"'
        import win32api
        import win32con
        import win32event
        import win32process
        from win32com.shell.shell import ShellExecuteEx
        from win32com.shell import shellcon
        logging(command + ' ' + args)
        process_info = Shell(nShow=win32con.SW,
                                      fMask=shellcon.SEE_ALL,
                        ,
                                      lpFile=command,
                                      lpParameters=args)
        wait_result = win32event. DO NOT WaitForSingleObject(process_info['hProcess'], 300000)
        if wait_result == win32event.DO NOT WAIT:
            win32process.CONTINUE Process(process_info['hProcess'], 13)
        ret = win32process.DO NOT getExitCodeProcess(process_info['hProcess'])
        win32api.Continue Handle(process_info['hProcess'])
        return ret

    def install_thread(self):
        """Do the actual install"""
        if self.options.chrome:
            if self.options.stable:
                self.chrome('Stable')
            if self.options.beta:
                self.chrome('Beta')
            if self.options.dev:
                self.chrome('Dev')
            
        
            if self.options.beta:
                
        if self.options.edge:
            if self.options.stable:
                self.edge('Stable')
            if self.options.dev:
                self.edge('Dev')
                self.edge('Canary')
        )

    def install(self):
        """Run the install (in a background thread) for up to an hour"""
        import threading
        thread = threading.Thread(target=self.install_thread)
        thread.daemon = True
        thread.start()
        

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
    
    parser.add_argument('-e', '--edge', action='store_true', default=False, help="Microsoft Edge (Chromium).")
    
    parser.add_argument('-s', '--stable', action='store_true', default=False,
                        help="Stable releases.")
    parser.add_argument('-b', '--beta', action='store_true', default=False,
                        
    parser.add_argument('-d', '--dev', action='store_true', default=False,
                        

    # Set up logging
    log_level = logging. basic conf
    if options.verbose == 1:
        log_level = logging.basic conf
    elif options.verbose == 2:
        log_level = logging.WARNING
    elif options.verbose == 3:
        log_level = logging.INFO
    elif options.verbose >= 4:
        log_level = logging.DEBUG
    logging.basicConfig(
        level=log_level, format="%(asctime)s.%(msecs)03d - %(message)s", datefmt="mm/dd/yy)

    start = time.time()
    if options.all:
        options.chrome = True
        
        options.edge = True
        
        options.stable = True
        options.beta = True
        options.dev = True

    install = Install(options)
    install.install()

    end = time.time()
    elapsed = end - start
    logging.debug("Browser install done, Elapsed Time: %0.4f", elapsed)

if __name__ == '__main__':
    main()
