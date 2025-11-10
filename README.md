# 개발 환경 설정 

## 실행 명령어
```bash
pdm run dev
```

### pyproject.toml 에 작성한 스크립트 
```bash
[tool.pdm.scripts]
dev = {cmd = "uvicorn main:app --reload", env = {PYTHONPATH = "src"}}
```
- 동작 원리:

    - pdm run dev 명령어는 pyproject.toml의 [tool.pdm.scripts] 섹션에서 dev 스크립트를 찾음
    - dev 스크립트는 uvicorn main:app --reload 명령어를 실행
    - 동시에 PYTHONPATH=src 환경 변수를 자동으로 설정
    - 이를 통해 Python이 src 디렉토리를 모듈 경로로 인식하고 from app... import가 정상 작동

- 직접 실행 (선택사항)
    - 스크립트를 쓰지 않고 직접 실행하려면:
```bash
PYTHONPATH=src pdm run uvicorn main:app --reload
```

# 배포 환경 설정

- 배프로덕션 환경에서 실행하려면 pyproject.toml에 prod 스크립트를 추가하여 사용합니다:
```bash
[tool.pdm.scripts]
dev = ...
prod = {cmd = "uvicorn main:app --host 0.0.0.0 --port 8000", env = {PYTHONPATH = "src"}}

--- 

pdm run prod
```