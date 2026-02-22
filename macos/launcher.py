"""
macOS 실행 진입점
- Flask 서버를 백그라운드 스레드로 실행
- 브라우저를 자동으로 열어 앱에 접속
"""
import sys
import os
import threading
import webbrowser
import time
import tempfile

if getattr(sys, 'frozen', False):
    ROOT = sys._MEIPASS
    exe_dir = os.path.dirname(sys.executable)
    bundle_dir = os.path.abspath(os.path.join(exe_dir, '..', '..', '..'))
    os.chdir(bundle_dir)
    UPLOAD_DIR = os.path.join(tempfile.gettempdir(), 'pdf_translator_uploads')
else:
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(ROOT)
    UPLOAD_DIR = os.path.join(ROOT, 'uploads')

sys.path.insert(0, ROOT)
os.environ['PDF_UPLOAD_FOLDER'] = UPLOAD_DIR
os.makedirs(UPLOAD_DIR, exist_ok=True)

from app import app

PORT = 5000

def _open_browser():
    time.sleep(2)
    webbrowser.open(f'http://127.0.0.1:{PORT}')

if __name__ == '__main__':
    threading.Thread(target=_open_browser, daemon=True).start()
    app.run(host='127.0.0.1', port=PORT, debug=False, threaded=True)
