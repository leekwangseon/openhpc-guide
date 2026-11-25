# 파일 주고받기
다음 예제는 HOME이 작업에 허용된 공유 경로일 때만 사용합니다. 별도 프로젝트 경로가 있으면 그 경로에서 시작합니다.

```bash
mkdir -p "$HOME/work/first-test"
cd "$HOME/work/first-test"
pwd
df -h .
```

내 PC에서 작은 파일을 올리는 예제입니다. `YOUR_USER_HOME`은 `/home/개인계정` 등 관리자가 안내한 절대 경로로 바꿉니다.

```bash
scp -P YOUR_SSH_PORT ./input.dat YOUR_USER@YOUR_LOGIN_HOST:YOUR_USER_HOME/work/first-test/
```

결과를 내 PC의 현재 폴더로 내려받습니다.

```bash
scp -P YOUR_SSH_PORT YOUR_USER@YOUR_LOGIN_HOST:YOUR_USER_HOME/work/first-test/result.dat ./
```

SSH는 소문자 `-p`, SCP는 대문자 `-P`로 포트를 지정합니다. GUI 파일 전송에서는 SFTP를 선택하고 같은 주소·계정·SSH 포트를 사용합니다. 중계 접속이면 별도 SFTP 중계 설정이 필요할 수 있습니다.

대용량·다수 파일은 양쪽에 rsync가 제공될 때 사용할 수 있습니다. 재실행 시 이미 전송된 내용을 활용하며 `--partial`은 중단된 부분 파일을 보관합니다. 대상 경로와 덮어쓰기 여부를 먼저 확인합니다.

```bash
rsync -av --partial --progress -e 'ssh -p YOUR_SSH_PORT' ./inputs/ YOUR_USER@YOUR_LOGIN_HOST:YOUR_USER_HOME/work/first-test/inputs/
```

이 예제에는 파일 삭제 옵션을 넣지 않았습니다. 중요한 결과는 현장 백업·보관 정책에 따라 별도 보존합니다.
