# 접속하기

담당자에게 받은 **서버 주소·SSH 포트·개인 계정**을 준비합니다. 아래 명령의 `YOUR_LOGIN_HOST`, `YOUR_SSH_PORT`, `YOUR_USER`를 각각 그 값으로 바꿔 입력하세요. 값을 받지 못했다면 먼저 담당자에게 문의해 주세요.
### 내 PC에서 실행

Windows는 PowerShell/OpenSSH 또는 조직에서 허용한 SSH 클라이언트를, macOS·Linux는 터미널을 사용할 수 있습니다. 클라이언트별 기능·라이선스는 해당 배포처에서 확인합니다.

```bash
ssh -p YOUR_SSH_PORT YOUR_USER@YOUR_LOGIN_HOST
```

처음 접속할 때 표시되는 호스트 키 지문은 관리자에게 받은 지문과 비교합니다. 호스트 키가 변경되었다는 경고가 나오면 재설치·교체 여부를 확인합니다. 경고를 우회하거나 기존 키를 무조건 삭제하지 않습니다.

비밀번호 입력 중 화면에 글자가 보이지 않는 것은 정상입니다. 비밀번호·다중 인증·키 인증 중 현장에서 지정한 방법을 사용합니다.

중계 서버·VPN이 필요한 현장에서는 관리자에게 받은 전용 접속 절차를 사용합니다. **중계 서버의 `127.0.0.1`과 내 PC의 `127.0.0.1`은 다른 대상입니다.** 리버스 유지보수 통로를 일반 사용자 접속 경로로 임의 사용하지 않습니다.

## 운영체제별 접속 준비

### Windows: MobaXterm 또는 OpenSSH

MobaXterm을 사용하는 경우 Session → SSH에서 Remote host, Specify username, Port를 입력합니다. 터미널의 SSH 명령으로도 접속할 수 있습니다. SFTP 패널은 세션·인증 설정에 따라 제공되며 패널에서 파일을 올리기 전에 대상 폴더를 확인합니다. 조직 정책과 해당 에디션의 사용 조건을 확인합니다.

PowerShell의 OpenSSH는 `ssh -V`로 설치 여부를 확인할 수 있습니다. GUI 화면 전달이 필요하면 별도 X 서버가 필요하며, MobaXterm에서는 내장 X 서버 기능을 사용할 수 있습니다.

Windows 사용자명·경로에 한글이 있어 클라이언트 오류가 발생하면 오류 메시지와 버전을 확인하고 지원되는 최신 버전·작업 경로 설정을 담당자에게 문의합니다. 기존 `.bashrc`를 덮어쓰거나 시스템 ssh_config를 무조건 치환하지 않습니다.

### macOS: Terminal과 선택적 XQuartz

터미널의 SSH로 접속할 수 있습니다. 텍스트 접속에는 XQuartz가 필요하지 않습니다. X11 GUI를 사용하는 경우 [XQuartz](https://www.xquartz.org/)를 설치·실행하고 새 터미널에서 `ssh -X`를 사용합니다. 필요 시 로그아웃 후 다시 로그인하는 등 설치 안내를 따릅니다.

### Linux: Terminal

SSH 클라이언트가 있는지 `ssh -V`로 확인합니다. X11 전달에는 로컬 X 서버와 서버의 전달 허용·인증 도구 등이 필요합니다. headless 환경에서 별도 준비 없이 GUI가 열린다고 가정하지 않습니다.

## GUI 접속과 터널

```bash
ssh -X -p YOUR_SSH_PORT YOUR_USER@YOUR_LOGIN_HOST
```

`-X`는 X11 전달, `-C`는 압축, `-Y`는 신뢰하는 X11 전달 옵션입니다. 일반 접속에 모두 필요하지는 않습니다. 신뢰하는 서버에서 제품이 요구할 때만 관리자에게 `-Y` 사용을 확인합니다. GUI가 안 열리면 `echo "$DISPLAY"`와 X 서버·전달 설정을 확인하고 [GUI 안내](optional.md)를 참고합니다.

승인된 중계 서버를 거치는 ProxyJump 형태는 다음과 같습니다. 중계 SSH 포트와 최종 SSH 포트는 별개입니다.

```bash
ssh -J YOUR_JUMP_USER@YOUR_JUMP_HOST:YOUR_JUMP_PORT \
  -p YOUR_TARGET_PORT YOUR_USER@YOUR_TARGET_HOST
```

리버스 터널 유지보수 포트를 사용하는 현장은 별도 안내를 받습니다. 접속 편의를 위해 에이전트 전달이나 호스트 키 검사를 일괄 해제하지 않습니다.

## 접속한 서버에서 확인

```bash
hostname
whoami
pwd
```

현장 안내서의 로그인 노드 이름과 개인 계정이 표시되는지 확인합니다. 계산 노드 접속이 별도로 필요한 경우에만 승인된 방식으로 이동합니다.

추가로 `w`, `uptime`, `free -h`, `df -h .`로 상황을 확인할 수 있습니다. `nvidia-smi`는 GPU와 드라이버가 제공된 노드에서 사용합니다. 이 명령들이 사용 예약을 대신하지는 않습니다.

## 자주 접속하는 서버 저장

개인 PC의 `~/.ssh/config`에 별칭을 등록할 수 있습니다. Windows OpenSSH는 보통 사용자 프로필의 `.ssh/config`를 사용합니다.

```text
Host research-cluster
    HostName YOUR_LOGIN_HOST
    User YOUR_USER
    Port YOUR_SSH_PORT
    ServerAliveInterval 30
    ServerAliveCountMax 3
```

실제 값으로 바꾼 후 `ssh research-cluster`로 접속합니다. 설정 파일에는 비밀번호를 넣지 않습니다. 연결 확인 옵션은 죽은 연결 감지에 도움이 되지만 실행 작업을 자동 복구하지는 않습니다.
