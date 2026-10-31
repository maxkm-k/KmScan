[app]

# (str) Title of your application
title = Km Scan

# (str) Package name
package.name = kmscan

# (str) Package domain (needed for android packaging)
package.domain = org.km

# (str) Version of the application
version = 0.1

# (str) Source files to include (let it include py and kv)
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
requirements = python3,kivy,netifaces

# (str) Supported orientations
orientation = portrait

# (list) Permissions
android.permissions = INTERNET, ACCESS_WIFI_STATE, ACCESS_NETWORK_STATE, CHANGE_WIFI_STATE

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK choice
android.ndk = 25b
# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android SDK build-tools version
android.build_tools_version = 33.0.2

# (int) Skip sdk license confirmation (accept automatically)
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
