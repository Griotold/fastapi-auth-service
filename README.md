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

# sqlite 명령어

```bash
fastapi-auth-service-3.13) hs@griotoldui-MacBookAir fastapi-auth-service % sqlite3 sql_app.db
SQLite version 3.51.0 2025-06-12 13:14:41
Enter ".help" for usage hints.
sqlite> .tables
posts  users
sqlite> .schema users
CREATE TABLE users (
        id INTEGER NOT NULL, 
        email VARCHAR, 
        username VARCHAR, 
        password VARCHAR, 
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
        PRIMARY KEY (id)
);
CREATE UNIQUE INDEX ix_users_username ON users (username);
CREATE UNIQUE INDEX ix_users_email ON users (email);
sqlite> 
``` 

# pdm 으로 라이브러리 설치 방법
```bash
pdm add passlib bcrypt
```

## bcrypt → argon2로 변경한 이유

처음에는 `bcrypt`를 사용했으나, **argon2**로 변경했습니다.

### argon2가 더 나은 이유

| 항목 | bcrypt | argon2 |
|------|--------|--------|
| 개발 | 2006년 | 2015년 (Password Hashing Competition 우승) |
| 메모리 기반 방어 | ❌ | ✅ |
| GPU/ASIC 공격 저항 | 낮음 | 높음 |
| OWASP 권장 | 구식 | ✅ 차세대 표준 |
| Python 3.13 호환성 | ❌ 문제 있음 | ✅ 안정적 |

**결론**: argon2는 bcrypt보다 최신이고 더 강력한 보안을 제공합니다.

---

## 라이브러리 교체할 때 캐시 삭제하기

Python과 패키지 관리자는 성능 최적화를 위해 컴파일된 바이트코드를 캐시합니다. 라이브러리를 교체할 때 이 캐시가 남아있으면 예상치 못한 에러가 발생할 수 있습니다.

### 해결 방법

라이브러리를 변경한 후 반드시 이 순서대로 진행하세요:
```bash
# 1. 서버 완전 종료 (Ctrl+C)

# 2. 캐시 완전 제거
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete
rm -rf .pdm-build

# 3. venv 재생성
rm -rf .venv
pdm install

# 4. 서버 다시 시작
pdm run dev
```

### 왜 필요한가?
```
라이브러리 변경 (bcrypt → argon2)
        ↓
예전 bcrypt 바이트코드가 __pycache__에 남아있음
        ↓
Python이 새 라이브러리 대신 캐시된 구 버전을 읽음
        ↓
에러 발생 ("모듈을 찾을 수 없음" 등)
```