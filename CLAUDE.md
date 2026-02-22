# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

PDF 파일을 업로드하면 영어 텍스트를 한글로 번역하고, TXT / PDF / DOCX 형식으로 저장하는 Flask 웹 애플리케이션.

## 실행 방법

```bash
python app.py
```

브라우저에서 http://localhost:5000 접속.

## 의존성 설치

```bash
pip install flask pdfplumber python-dotenv sentence-transformers scikit-learn fpdf2 python-docx requests
```

## 환경 변수

`.env` 파일에 OpenRouter API 키를 설정한다:

```
openrouter_API_KEY=your_key_here
```

## 아키텍처

### 파일 구조

| 파일 | 역할 |
|---|---|
| `app.py` | Flask 라우터 (`/upload`, `/translate_page`, `/export`) |
| `translator.py` | OpenRouter 번역 API 호출 + 유사도 계산 |
| `exporter.py` | TXT / PDF / DOCX 파일 생성 |
| `config.py` | `.env`에서 API 키 로드 |
| `templates/index.html` | 단일 페이지 UI |
| `fonts/ArialUnicode.ttf` | PDF 한글 렌더링용 폰트 |

### API 엔드포인트

- `POST /upload` — PDF 파일 수신, 텍스트 추출
- `POST /translate_page` — 번역 후 유사도 반환. 실패 시 3초 후 1회 재시도
- `POST /export` — 파일 생성 후 다운로드
