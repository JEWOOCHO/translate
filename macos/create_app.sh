#!/bin/bash
# =============================================
#  PDF번역기 - macOS .app 번들 생성 스크립트
# =============================================
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"
DIST_DIR="$SCRIPT_DIR/dist"
APP_NAME="PDF번역기"
APP_BUNDLE="$DIST_DIR/$APP_NAME.app"
MACOS_BIN="$APP_BUNDLE/Contents/MacOS/$APP_NAME"

echo "============================================="
echo " PDF번역기 macOS .app 번들 생성"
echo "============================================="

rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"
mkdir -p "$APP_BUNDLE/Contents/MacOS"
mkdir -p "$APP_BUNDLE/Contents/Resources"

cat > "$APP_BUNDLE/Contents/Info.plist" << 'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key><string>PDF번역기</string>
    <key>CFBundleIdentifier</key><string>com.pdftranslator.app</string>
    <key>CFBundleName</key><string>PDF번역기</string>
    <key>CFBundleDisplayName</key><string>PDF번역기</string>
    <key>CFBundleVersion</key><string>1.0</string>
    <key>CFBundleShortVersionString</key><string>1.0</string>
    <key>CFBundlePackageType</key><string>APPL</string>
    <key>NSHighResolutionCapable</key><true/>
    <key>LSUIElement</key><false/>
</dict>
</plist>
PLIST

cat > "$MACOS_BIN" << 'SHELLSCRIPT'
#!/bin/bash
SCRIPT_PATH="$0"
MACOS_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
CONTENTS_DIR="$(cd "$MACOS_DIR/.." && pwd)"
APP_BUNDLE="$(cd "$CONTENTS_DIR/.." && pwd)"
DIST_DIR="$(cd "$APP_BUNDLE/.." && pwd)"

[ -z "$HOME" ] && HOME="$(eval echo ~$(whoami))"

PYTHON_CMD=""
for CANDIDATE in "$HOME/opt/anaconda3/bin/python" "$HOME/anaconda3/bin/python" "$HOME/miniconda3/bin/python" "/opt/anaconda3/bin/python" "/usr/local/bin/python3" "/usr/bin/python3"; do
    [ -x "$CANDIDATE" ] && PYTHON_CMD="$CANDIDATE" && break
done

[ -z "$PYTHON_CMD" ] && osascript -e 'display alert "Python을 찾을 수 없습니다."' && exit 1

/usr/sbin/lsof -ti :5000 &>/dev/null && open "http://127.0.0.1:5000" && exit 0

cd "$DIST_DIR"
"$PYTHON_CMD" launcher.py &
sleep 3
open "http://127.0.0.1:5000"
wait
SHELLSCRIPT

chmod +x "$MACOS_BIN"
xattr -rd com.apple.quarantine "$APP_BUNDLE" 2>/dev/null || true

echo "[*] 프로젝트 파일 복사 중..."
cp "$ROOT/app.py" "$ROOT/translator.py" "$ROOT/exporter.py" "$ROOT/config.py" "$DIST_DIR/"
cp "$SCRIPT_DIR/launcher.py" "$DIST_DIR/"
cp -r "$ROOT/templates" "$ROOT/fonts" "$DIST_DIR/"
[ -f "$ROOT/.env.example" ] && cp "$ROOT/.env.example" "$DIST_DIR/"

echo ""
echo "============================================="
echo " 빌드 완료: macos/dist/"
echo "============================================="
