cd /home/giuseppe/AndroidStudioProjects/DomoticsAI/android

./gradlew clean
./gradlew assembleDebug

adb install -r \
  /home/giuseppe/AndroidStudioProjects/DomoticsAI/android/app/build/outputs/apk/debug/app-debug.apk

adb shell monkey \
-p it.zara.domoticsai \
-c android.intent.category.LAUNCHER 1

adb shell am force-stop it.zara.domoticsai

adb shell am force-stop it.zara.domoticsai

adb shell monkey \
-p it.zara.domoticsai \
-c android.intent.category.LAUNCHER 1

adb logcat | grep DomoticsAI

