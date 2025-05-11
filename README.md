# 🛡️ Fail-SafeBox

안전한 파일 암호화 및 자동 삭제 기능을 제공하는 보안 도구입니다. AES-256 암호화를 사용하여 파일을 안전하게 보호하고, 실패한 복호화 시도가 일정 횟수를 초과하면 자동으로 파일을 파기하는 기능을 제공합니다.

## 프로젝트 구조

```
fail-safebox/
├── vault/               # 핵심 암호화 모듈
│   ├── crypto.py       # 암호화/복호화 구현
│   ├── autodestruct.py # 자동 파기 기능
│   ├── operations.py   # 파일 작업 처리
│   └── lock.py         # 잠금 메커니즘
├── gui.py              # GUI 인터페이스
├── main.py            # CLI 인터페이스
└── config.py          # 설정 파일
```

## 주요 기능

### 암호화 및 보안
- AES-256 CBC 모드 암호화
- PBKDF2를 통한 안전한 키 유도 (4096회 반복)
- 안전한 파일 처리 및 메모리 관리
- 실패한 복호화 시도 추적 및 자동 파기
- 안전한 파일 삭제 (무작위 데이터로 덮어쓰기 후 삭제)

### 사용자 인터페이스
- 직관적인 GUI 인터페이스
- 명령줄(CLI) 인터페이스 지원
- 자동 삭제 옵션 (복호화 후 원본 파일 자동 삭제)

## 시스템 요구사항

- Python 3.6 이상
- pycryptodome 라이브러리
- customtkinter (GUI 인터페이스용)

## 사용 방법

### GUI 모드

```bash
python gui.py
```

GUI 애플리케이션을 통해 직관적으로 파일을 암호화하고 복호화할 수 있습니다:
- 파일 선택 버튼으로 암호화/복호화할 파일 선택
- 비밀번호 입력
- 암호화/복호화 모드 선택
- 자동 삭제 옵션 선택 (선택사항)

### CLI 모드

파일 암호화:
```bash
python main.py encrypt <파일_경로>
```

파일 복호화:
```bash
python main.py decrypt <파일_경로>
```

자동 삭제 옵션 사용:
```bash
python main.py decrypt <파일_경로> --autodelete
```