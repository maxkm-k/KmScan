[app]

# (str) Title of your application
title = Km Scan

# (str) Package name
package.name = kmscan

# (str) Package domain (needed for android packaging)
package.domain = org.km

# (str) Source files to include (let it include py and kv)
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
# python3, kivy, and netifaces (for auto-fetching local IP)
requirements = python3,kivy,netifaces

# (str) Supported orientations
orientation = portrait

# (list) Permissions
android.permissions = INTERNET, ACCESS_WIFI_STATE, ACCESS_NETWORK_STATE, CHANGE_WIFI_STATE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android APK extralibs/ndk choice
android.ndk = 25b

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
