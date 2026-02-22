# macOS 빌드 가이드

## 요구사항
- macOS 10.15 Catalina 이상
- Python 3.8+
- 인터넷 연결 (첫 실행 시 AI 모델 ~90MB 자동 다운로드)

## 빌드 방법

```bash
bash macos/create_app.sh
```

빌드 완료 후 `macos/dist/PDF번역기.app` 생성됨.

## 실행 방법

`PDF번역기.app`을 더블클릭하면 브라우저가 자동으로 열립니다.

## 주의사항

- **첫 실행 시** AI 유사도 모델(~90MB)이 자동 다운로드됩니다
- "개발자를 확인할 수 없습니다" 메시지: Finder에서 우클릭 → "열기" → "열기"
