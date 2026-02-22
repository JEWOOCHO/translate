import os
import uuid
import pdfplumber
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from translator import translate_text, compute_similarity
from exporter import generate_txt, generate_pdf, generate_docx
import io

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20MB

UPLOAD_FOLDER = os.environ.get('PDF_UPLOAD_FOLDER') or os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': '파일이 없습니다.'}), 400

    file = request.files['file']

    if not file.filename or not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'PDF 파일만 업로드 가능합니다.'}), 400

    filename = f"{uuid.uuid4()}.pdf"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    try:
        pages = []
        with pdfplumber.open(filepath) as pdf:
            for i, page in enumerate(pdf.pages, 1):
                text = page.extract_text() or ''
                pages.append({'page': i, 'text': text.strip()})

        non_empty = [p for p in pages if p['text']]
        if not non_empty:
            return jsonify({
                'error': '텍스트를 추출할 수 없습니다. 이미지 기반(스캔본) PDF는 지원하지 않습니다.'
            }), 422

        return jsonify({
            'filename': file.filename,
            'page_count': len(pages),
            'pages': pages,
        })

    except Exception as e:
        return jsonify({'error': f'PDF 처리 중 오류가 발생했습니다: {str(e)}'}), 500

    finally:
        if os.path.exists(filepath):
            os.remove(filepath)


@app.route('/translate_page', methods=['POST'])
def translate_page():
    data = request.get_json()
    page_num = data.get('page')
    text = (data.get('text') or '').strip()

    if not text:
        return jsonify({'error': '번역할 텍스트가 없습니다.', 'page': page_num}), 400

    try:
        translated = translate_text(text)
        similarity = compute_similarity(text, translated)
        return jsonify({
            'page': page_num,
            'original': text,
            'translated': translated,
            'similarity': similarity,
        })
    except Exception as e:
        return jsonify({'error': str(e), 'page': page_num}), 500


@app.route('/export', methods=['POST'])
def export():
    data = request.get_json()
    fmt = data.get('format', 'txt').lower()
    results = data.get('results', [])
    original_filename = data.get('filename', 'document')

    base_name = os.path.splitext(original_filename)[0]
    date_str = datetime.now().strftime('%Y%m%d')
    download_name = f"{base_name}_번역_{date_str}"

    try:
        if fmt == 'txt':
            content = generate_txt(results)
            return send_file(
                io.BytesIO(content),
                mimetype='text/plain; charset=utf-8',
                as_attachment=True,
                attachment_filename=f"{download_name}.txt",
            )
        elif fmt == 'pdf':
            content = generate_pdf(results, original_filename)
            return send_file(
                io.BytesIO(content),
                mimetype='application/pdf',
                as_attachment=True,
                attachment_filename=f"{download_name}.pdf",
            )
        elif fmt == 'docx':
            content = generate_docx(results, original_filename)
            return send_file(
                io.BytesIO(content),
                mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                as_attachment=True,
                attachment_filename=f"{download_name}.docx",
            )
        else:
            return jsonify({'error': '지원하지 않는 형식입니다.'}), 400

    except Exception as e:
        return jsonify({'error': f'파일 생성 오류: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
