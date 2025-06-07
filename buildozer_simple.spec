[app]

# (str) Title of your application
title = 大乐透预测系统

# (str) Package name
package.name = lottery_predictor

# (str) Package domain (needed for android/ios packaging)
package.domain = com.lottery.predictor

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy

# (str) Supported orientation (landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

[android]

# (int) Target Android API, should be as high as possible.
android.api = 34

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 27c

# (int) Android SDK version to use
android.sdk = 34

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually match android.minapi.
android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (bool) Accept SDK license
android.accept_sdk_license = True

# (str) Android entry point, default is ok for Kivy-based app
android.entrypoint = org.kivy.android.PythonActivity

# (str) Full name including package path of the Java class that implements Android Activity
android.activity_class_name = org.kivy.android.PythonActivity

# (str) Full name including package path of the Java class that implements Python Service
android.service_class_name = org.kivy.android.PythonService

# (list) Pattern to whitelist for the whole project
android.whitelist_src = False

# (str) Path to a custom whitelist file
android.whitelist = 

# (str) Path to a custom blacklist file
android.blacklist = 

# (list) List of Java .jar files to add to the libs so that pyjnius can access their classes. Don't add jars that you do not need, since extra jars can slow down the build process. Allows wildcards matching, for example: OUYA-ODK/libs/*.jar
android.add_jars = 

# (list) List of Java files to add to the android project (can be java or a directory containing the files)
android.add_src = 

# (str) OUYA Console category. Should be one of GAME or APP
android.ouya.category = GAME

# (str) Filename of OUYA Console icon. It must be a 732x412 png image.
android.ouya.icon_filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file to include as an intent filters in <activity> tag
android.manifest.intent_filters = 

# (str) launchMode to set for the main activity
android.manifest.launch_mode = standard

# (list) Android additional libraries to copy into libs/armeabi
android.add_libs_armeabi = 

# (list) Android additional libraries to copy into libs/armeabi-v7a
android.add_libs_armeabi_v7a = 

# (list) Android additional libraries to copy into libs/arm64-v8a
android.add_libs_arm64_v8a = 

# (list) Android additional libraries to copy into libs/x86
android.add_libs_x86 = 

# (list) Android additional libraries to copy into libs/x86_64
android.add_libs_x86_64 = 

# (bool) Indicate whether the screen should stay on
android.wakelock = False

# (list) Android application meta-data to set (key=value format)
android.meta_data = 

# (list) Android library project to add (will be added in the automatically imported in the build.xml)
android.library_references = 

# (str) Android logcat filters to use
android.add_activites = 

# (str) Android manifest placeholders to set (key=value format)
android.gradle_dependencies = 

# (list) Android gradle repositories (each line is a repository)
android.gradle_repositories = 

# (str) Android gradle plugins to apply (each line is a plugin)
android.gradle_plugins = 

# (str) Android gradle build script to include (each line is a build script)
android.gradle_build_script = 

# (str) Android gradle settings to include (each line is a setting)
android.gradle_settings = 

# (str) Android gradle properties to set (key=value format)
android.gradle_properties = 

# (str) Android gradle wrapper properties to set (key=value format)
android.gradle_wrapper_properties = 

# (str) Android gradle local properties to set (key=value format)
android.gradle_local_properties = 

# (bool) Enable AndroidX support. Enable when 'android.gradle_dependencies'
android.enable_androidx = False

# (bool) Enable Jetifier. Enable when 'android.enable_androidx' is True
android.enable_jetifier = False 