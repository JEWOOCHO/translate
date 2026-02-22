import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("openrouter_API_KEY")

if not OPENROUTER_API_KEY:
    raise EnvironmentError(".env 파일에 openrouter_API_KEY가 설정되지 않았습니다.")
