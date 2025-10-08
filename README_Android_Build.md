# Taki Poker Tracker - Android APK Build Guide

This guide will help you convert your Kivy-based Taki Poker Tracker application into an Android APK file.

## Overview

Taki Poker Tracker is a Kivy application that helps manage poker game sessions by tracking:
- Player buy-ins and total purchases
- Player debts and chip counts
- Real-time calculations and summaries
- Date tracking for game sessions

## Prerequisites

### System Requirements
- **Linux** (recommended) or **WSL2 on Windows**
- Python 3.8 or higher
- At least 8GB RAM
- 20GB+ free disk space

### Required Tools
1. **Buildozer** - For building Android APKs from Python/Kivy apps
2. **Android SDK & NDK** - Will be automatically downloaded by Buildozer
3. **Java JDK** - Required for Android development

## Step-by-Step Installation

### 1. Install System Dependencies

#### On Ubuntu/Debian:
```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
```

#### On Windows (WSL2):
First install WSL2 with Ubuntu, then run the Ubuntu commands above.

### 2. Install Python Dependencies

```bash
# Install Buildozer
pip3 install --user buildozer

# Install Cython (required for Kivy compilation)
pip3 install --user cython

# Install Kivy (for testing locally)
pip3 install kivy
```

### 3. Set Environment Variables

Add these to your `~/.bashrc` or `~/.profile`:

```bash
export PATH=$PATH:~/.local/bin
export ANDROIDSDK="$HOME/.buildozer/android/platform/android-sdk"
export ANDROIDNDK="$HOME/.buildozer/android/platform/android-ndk-r25b"
export ANDROIDAPI="31"
export ANDROIDNDKVER="r25b"
```

Then reload your environment:
```bash
source ~/.bashrc
```

## Building the APK

### 1. Navigate to Project Directory
```bash
cd /path/to/your/Taki/project
```

### 2. Initialize Buildozer (First Time Only)
```bash
buildozer init
```

### 3. Build Debug APK
```bash
# This will take 30-60 minutes on first build as it downloads Android SDK/NDK
buildozer android debug
```

### 4. Build Release APK (Optional)
```bash
buildozer android release
```

## File Structure

Your project should have these files:
```
Taki/
├── taki.py              # Main Kivy application
├── main_kivy.py         # Entry point for Android build
├── buildozer.spec       # Buildozer configuration
├── requirements.txt     # Python dependencies
├── README_Android_Build.md  # This file
└── bin/                 # Generated APK files (after build)
```

## Configuration Details

### buildozer.spec Key Settings:
- **title**: Taki Poker Tracker
- **package.name**: takipoker
- **main.py**: main_kivy.py
- **requirements**: python3,kivy
- **orientation**: portrait
- **android.api**: 31 (Android 12)
- **android.minapi**: 21 (Android 5.0+)

## Troubleshooting

### Common Issues:

1. **"Command failed: ./gradlew assembleDebug"**
   - Solution: Ensure you have enough disk space (20GB+)
   - Try: `buildozer android clean` then rebuild

2. **"SDK not found"**
   - Solution: Let Buildozer download it automatically on first run
   - Or manually set ANDROIDSDK environment variable

3. **"NDK not found"**
   - Solution: Buildozer will download NDK r25b automatically
   - Ensure internet connection is stable

4. **"Java not found"**
   - Install OpenJDK 8: `sudo apt install openjdk-8-jdk`
   - Set JAVA_HOME: `export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64`

5. **Build takes too long**
   - First build can take 30-60 minutes
   - Subsequent builds are much faster (5-10 minutes)

### Memory Issues:
If you encounter out-of-memory errors:
```bash
export GRADLE_OPTS="-Xmx4096m -Dorg.gradle.jvmargs=-Xmx4096m"
```

## Testing the APK

### Install on Android Device:
1. Enable "Developer Options" on your Android device
2. Enable "USB Debugging" and "Install unknown apps"
3. Connect device via USB
4. Install APK:
   ```bash
   adb install bin/takipoker-0.1-debug.apk
   ```

### Or use Android Emulator:
1. Install Android Studio
2. Create an AVD (Android Virtual Device)
3. Drag and drop APK to emulator

## App Features on Android

The Android version will have the same functionality as the desktop version:
- ✅ Add players dynamically
- ✅ Track buy-ins with running totals
- ✅ Manage player debts and chip counts
- ✅ Real-time calculations
- ✅ Portrait orientation optimized for mobile
- ✅ Touch-friendly interface

## Customization

### Adding App Icon:
1. Create a 512x512 PNG icon
2. Save as `icon.png` in project root
3. Uncomment `icon.filename` in `buildozer.spec`

### Adding Splash Screen:
1. Create a splash screen image
2. Save as `presplash.png` in project root
3. Uncomment `presplash.filename` in `buildozer.spec`

### Changing Package Name:
Edit `buildozer.spec`:
```ini
package.name = your_app_name
package.domain = com.yourcompany
```

## Build Commands Reference

```bash
# Clean build files
buildozer android clean

# Build debug APK
buildozer android debug

# Build release APK
buildozer android release

# Build and install on connected device
buildozer android debug deploy run

# Build with verbose output
buildozer -v android debug
```

## Support

If you encounter issues:
1. Check the [Buildozer documentation](https://buildozer.readthedocs.io/)
2. Review [Kivy Android packaging guide](https://kivy.org/doc/stable/guide/packaging-android.html)
3. Search [Kivy community forums](https://github.com/kivy/kivy/discussions)

## Next Steps

After successful APK creation:
1. Test thoroughly on different Android devices
2. Consider publishing to Google Play Store
3. Add app signing for release builds
4. Implement crash reporting and analytics

---

**Note**: The first build will take significantly longer as Buildozer downloads and sets up the Android development environment. Be patient and ensure you have a stable internet connection.
