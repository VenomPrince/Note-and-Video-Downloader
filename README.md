# Dev Companion

## 🚀 Overview
Dev Companion is a versatile desktop application offering advanced Text Pad and Media Downloading capabilities.

## ✨ Features
- 📝 Advanced Text Pad
  * Smart text editing
  * Bullet point handling
  * Save/load functionality

- 🎥 Media Downloader
  * Multi-platform support
  * Download options:
    - Video + Audio
    - Video Only
    - Audio Only (MP3/WAV)
    - Thumbnail/Cover
  * Quality selection (4K to 360p)
  * Flexible download organization

## 🖥️ System Requirements

### Windows
- Windows 10 or later
- Python 3.7+ (64-bit)
- Minimum 200MB free disk space

### macOS
- macOS 10.14+ (Mojave or later)
- Python 3.7+ 
- Minimum 200MB free disk space

## 🔧 Prerequisites

### FFmpeg Installation (Recommended)

#### Windows
1. Download FFmpeg from official site:
   - Visit: https://ffmpeg.org/download.html
   - Choose Windows build (https://github.com/BtbN/FFmpeg-Builds/releases)
   - Download `ffmpeg-master-latest-win64-gpl.zip`

2. Installation Steps:
   ```bash
   # Extract downloaded zip
   # Copy ffmpeg.exe to a permanent location, e.g.:
   C:\Program Files\FFmpeg\bin
   ```

3. Add to System PATH:
   - Open "Edit the system environment variables"
   - Click "Environment Variables"
   - Under "System variables", edit "Path"
   - Add: `C:\Program Files\FFmpeg\bin`
   - Click OK on all dialogs

#### macOS
1. Install via Homebrew:
   ```bash
   # Install Homebrew if not already installed
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

   # Install FFmpeg
   brew install ffmpeg
   ```

#### Linux
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install ffmpeg

# Fedora
sudo dnf install ffmpeg

# Arch Linux
sudo pacman -S ffmpeg
```

## 🛠️ Installation

### Method 1: Run from Source

#### Windows/macOS
1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/dev-companion.git
   cd dev-companion
   ```

2. Create Virtual Environment (Recommended)
   ```bash
   python -m venv venv
   # Activate:
   # Windows: venv\Scripts\activate
   # macOS/Linux: source venv/bin/activate
   ```

3. Install Dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Application
   ```bash
   python cli_app.py
   ```

### Method 2: Use Executable

#### Windows
1. Download `DevCompanion.exe` from Releases
2. Double-click to run

#### macOS
1. Download `DevCompanion.app` from Releases
2. Drag to Applications folder
3. Right-click > Open (first time may require security override)

## 🔨 Building Executable

### Windows
```bash
python build_exe.py
# Executable created in: dist/DevCompanion.exe
```

### macOS
```bash
python build_exe.py
# Application bundle created in: dist/DevCompanion.app
```

## 🐛 Troubleshooting

### Common Issues
- Ensure Python is in system PATH
- Check FFmpeg installation
- Verify all dependencies are installed
- Run with administrator/sudo privileges if permission issues occur

### Dependency Conflicts
- Use virtual environment
- Upgrade pip: `python -m pip install --upgrade pip`
- Reinstall dependencies if conflicts arise

## 📋 Supported Platforms
- Windows 10/11 (64-bit)
- macOS 10.14+ 
- Linux (with Tkinter support)

## 🔒 Security
- No sensitive data storage
- Basic input validation
- Regular dependency updates recommended

## 📜 License
MIT License

## 🤝 Contributing
1. Fork the repository
2. Create your feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## 📞 Support
- Open GitHub Issues for bug reports
- Email: support@devcompanion.com

## 🌟 Acknowledgments
- yt-dlp Team
- Python Software Foundation
- Open Source Community
