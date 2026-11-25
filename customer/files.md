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

## 폴더 전체 전송

SCP는 `-r`로 폴더를 전송합니다. 현재 PC에서 실행하는 예입니다.

```bash
scp -r -P YOUR_SSH_PORT ./inputs YOUR_USER@YOUR_LOGIN_HOST:YOUR_USER_HOME/work/first-test/
```

서버 간 직접 전송은 양쪽 인증과 통신 경로가 필요합니다. 어떤 장비를 경유하는지는 SCP 버전·옵션에 따라 달라지므로 승인된 전송 방법을 확인합니다. 비밀키를 임시로 여러 서버에 복사하지 않습니다.

## SFTP에서 파일 전송

```bash
sftp -P YOUR_SSH_PORT YOUR_USER@YOUR_LOGIN_HOST
```

접속 후 `pwd`·`ls`는 원격 경로를, `lpwd`·`lls`는 내 PC 경로를 확인합니다. `cd`·`lcd`로 각각 이동하고 `put input.dat`, `get result.dat`로 전송합니다. 종료는 `bye`입니다. GUI에서는 서버·포트·계정·인증 방식을 동일하게 지정합니다.

## rsync로 반복·대용량 전송

`source/`는 폴더 안의 내용, `source`는 폴더 자체를 복사하는 차이가 있습니다. 전송 전 경로를 미리 확인합니다.

```bash
rsync -av --dry-run -e 'ssh -p YOUR_SSH_PORT' ./inputs/ \
  YOUR_USER@YOUR_LOGIN_HOST:YOUR_USER_HOME/work/first-test/inputs/
```

출력을 확인한 후 `--dry-run`을 빼고 `--partial --progress`를 추가해 전송합니다. 이미 압축된 데이터는 `-z` 압축이 도움이 되지 않을 수 있습니다. rsync의 재실행은 이미 같은 파일을 건너뛰거나 차이를 활용할 수 있으나, 모든 프로그램·모든 파일 형식에서 무조건 이어받기를 보장하는 표현으로 이해하지 않습니다.

`--delete`는 대상의 파일을 제거할 수 있으므로 일상 복사 예제에는 사용하지 않습니다. 입력·결과 경로를 뒤집거나 공유 폴더 루트를 대상으로 잡지 않습니다.

## 전송 결과 검증과 권한

```bash
ls -lh input.dat
sha256sum input.dat
```

중요 파일은 전송 전후 체크섬을 비교합니다. 파일 개수·크기뿐 아니라 프로그램에서 읽히는지도 확인합니다. `Permission denied`는 파일·상위 폴더 권한과 대상 계정을, 용량 오류는 `df`·quota를 확인합니다. 권한을 일괄 777로 바꾸지 않습니다. 대규모 작은 파일은 저장소 부하를 고려해 담당자와 묶음 전송 방식을 협의합니다.
