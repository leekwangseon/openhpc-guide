# 사용자 계정 추가·동기화·제거

이 장의 변경 명령은 관리 노드에서 권한 있는 담당자가 실행합니다. 로컬 파일 기반과 LDAP/AD/SSSD 같은 중앙 인증 방식을 구분합니다. 아래 예제의 `YOUR_*`는 승인된 실제 값으로 바꿉니다.

## 1. 추가 전 확인

사용자명·UID·기본 그룹·보조 그룹·사용 기간·프로젝트·저장 공간을 승인받습니다. 모든 노드와 저장소에서 UID/GID가 일관되어야 합니다.

```bash
getent passwd YOUR_USER
getent passwd YOUR_UID
getent group YOUR_GROUP
```

이미 있는 사용자·UID·그룹을 덮어쓰지 않습니다. 중앙 인증 사용자는 디렉터리 서비스에서 관리하고 동일 이름의 로컬 계정을 임의로 만들지 않습니다.

## 2. 로컬 사용자 예제

기본 그룹이 준비된 경우:

```bash
useradd -m -u YOUR_UID -g YOUR_GROUP -s /bin/bash YOUR_USER
passwd YOUR_USER
id YOUR_USER
getent passwd YOUR_USER
```

기본 그룹도 새로 만들 필요가 있으면 승인된 미사용 GID로 `groupadd -g YOUR_GID YOUR_GROUP`을 먼저 수행합니다. 비밀번호는 프롬프트나 승인된 초기 인증 전달 방식으로 설정합니다. 공용 문서·명령 인수에 비밀번호를 넣지 않습니다.

## 3. 계산 노드 계정 매핑

인증 방식에 맞춰 passwd/group의 사용자 매핑, SSH 공개키·인증 서비스·PAM 정책, 홈 마운트와 그룹 권한을 반영합니다. 마스터의 시스템 계정 파일을 통째로 덮어쓰면 이미지의 서비스 UID/GID와 충돌할 수 있습니다. 신규 계정만 반영하거나 충돌을 검증한 관리 파일을 사용합니다.

Warewulf 3에서 **이미 등록·할당된 배포 파일**을 갱신하는 형태입니다. 먼저 파일 목록과 각 노드 배포 대상을 확인합니다.

```bash
wwsh file list
wwsh provision print YOUR_NODE
wwsh file resync
```

`resync`가 어떤 등록 파일을 갱신하는지 먼저 검토합니다. `shadow`·`gshadow`·비밀키를 무조건 배포하는 절차로 사용하지 않습니다. 이미지의 재부팅 후 상태와 실행 중 노드의 갱신을 따로 확인합니다. 현장에 wwgetfiles가 구성된 경우 갱신 주기를 기다리거나 승인된 수동 갱신 절차를 사용합니다. 캐시 디렉터리의 무차별 삭제는 기본 절차로 넣지 않습니다.

여러 노드 조회에 pdsh가 제공되는 경우:

```bash
pdsh -R ssh -w 'YOUR_APPROVED_NODE_RANGE' 'hostname; getent passwd YOUR_USER'
```

호스트 범위 확장 형식과 실제 대상 목록을 확인합니다. root 키의 호스트 검증을 끄거나 관리자 비밀키를 노드에 배포하지 않습니다. Warewulf 4는 해당 버전의 syncuser·overlay 관리 방식을 사용합니다.

## 4. 인수 시험

해당 사용자로 실제 로그인·계산 노드 접근·공유 폴더 생성·파일 소유권·그룹 공유·프로그램 실행을 확인합니다. Slurm 회계를 쓰면 사용자·Account·Association·허용 QoS도 별도로 등록·검증합니다. OS 계정 생성만으로 Slurm 프로젝트 권한이 자동 생성된다고 가정하지 않습니다.

## 5. 계정 비활성화와 제거

실행 중 직접 작업·Slurm 작업, 공동 프로젝트 파일·예약·자동 실행을 조사합니다. 승인에 따라 비밀번호·SSH 키·중앙 인증·접속 정책 등 실제 인증 경로를 차단합니다. `usermod -L` 같은 비밀번호 잠금만으로 키 로그인까지 막히는 것은 아닙니다.

보존 정책과 인수인계를 확인한 후 로컬 계정을 제거하는 형태입니다.

```bash
userdel YOUR_USER
```

이 예제는 홈 삭제 옵션을 사용하지 않습니다. 사용자 데이터 삭제·소유권 이전·UID 재사용은 별도 판단·승인 후 수행합니다. 계산 노드·이미지·인증 서비스·Slurm의 관련 권한도 동기화하고 재로그인·재부팅 후 상태를 확인합니다.
