# PDF 번역기

> **저장소**: https://github.com/JEWOOCHO/translate

## 🌐 웹 버전 (바로 사용)

**서버 설치 없이 브라우저에서 바로 실행:**

👉 **https://jewoocho.github.io/translate/**

PDF 파일을 업로드하면 영어 텍스트를 한글로 번역하고, TXT / PDF / DOCX 형식으로 저장하는 Flask 웹 애플리케이션.

## 주요 기능

- PDF 업로드 → 텍스트 자동 추출 (pdfplumber)
- OpenRouter API (upstage/solar-pro-3:free) 로 영→한 번역
- paraphrase-MiniLM-L6-v2 임베딩으로 번역 유사도 품질 평가
- TXT / PDF / DOCX 형식으로 다운로드
- 페이지 범위 지정, 일시 중단/재개, 재번역 지원

## 설치

```bash
pip install flask pdfplumber python-dotenv sentence-transformers scikit-learn fpdf2 python-docx requests
```

## 환경 변수 설정

`.env.example`을 복사하여 `.env`를 만들고 API 키를 입력합니다.

```bash
cp .env.example .env
# .env 파일을 열어 openrouter_API_KEY=sk-or-v1-... 입력
```

OpenRouter API 키 발급: https://openrouter.ai/keys

## 폰트 설치 (PDF 출력용)

PDF 내보내기에 한글 폰트가 필요합니다. macOS의 경우:

```bash
mkdir -p fonts
cp /Library/Fonts/Arial\ Unicode.ttf fonts/ArialUnicode.ttf
```

다른 OS에서는 한글을 지원하는 TTF 폰트를 `fonts/ArialUnicode.ttf` 경로에 복사하세요.

## 실행

```bash
python app.py
```

브라우저에서 http://localhost:5000 접속.

## 아키텍처

```
Step 1: PDF 업로드 → pdfplumber로 텍스트 추출
Step 2: OpenRouter API 번역 + 유사도 계산
Step 3: TXT / PDF / DOCX 파일 생성 및 다운로드
```

| 파일 | 역할 |
|---|---|
| `app.py` | Flask 라우터 (`/upload`, `/translate_page`, `/export`) |
| `translator.py` | OpenRouter 번역 API 호출 + 유사도 계산 |
| `exporter.py` | TXT / PDF / DOCX 파일 생성 |
| `config.py` | `.env`에서 API 키 로드 |
| `templates/index.html` | 단일 페이지 UI |
| `fonts/ArialUnicode.ttf` | PDF 한글 렌더링용 폰트 (별도 복사 필요) |

## macOS 데스크톱 앱 빌드

```bash
bash macos/create_app.sh
```

결과물: `macos/dist/PDF번역기.app`

## Windows 실행

`windows/PDF번역기.bat` 더블클릭 (Python 설치 필요)
