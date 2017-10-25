# browser-install
Automatically install and keep Chrome and Firefox browsers up to date with the latest releases (on Windows).

This can be run frequently (hourly or daily) as the browser is only downloaded and installed if the installer has changed since the last install.

UAC must be disabled (don't prompt) since the browser installs need to be run with administrator rights.

For Chrome, the following channels are supported:
* Stable
* Beta
* Dev

Canary is not supported for Chrome as there is no silent stand-alone installer for it.

For Firefox, the following channels are supported:
* Stable
* ESR
* Dev
* Beta
* Nightly

## Usage
To automatically install all of the supported browsers:
```
python browser_install.py --all
```

## Command-line options
* **-v, --verbose** : Increase verbosity (specify multiple times for more). -vvvv for full debug output.
* **-a, --all** : All supported browsers.
* **-c, --chrome** : Chrome.
* **-f, --firefox** : Firefox.
* **-s, --stable** : Stable releases (includes ESR and dev edition for Firefox).
* **-b, --beta** : Beta releases.
* **-d, --dev** : Dev releases (Nightly for Firefox, Dev channel for Chrome).
