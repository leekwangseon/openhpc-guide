# 참고 자료와 유지보수

## 문서 작성 기준

이 안내서는 운영 흐름을 새로 작성한 범용 문서입니다. 고객 서버의 설정·로그·연구 데이터·접속 정보는 포함하지 않습니다. 명령 예제의 `YOUR_*`은 미기입 값이며 `192.0.2.21`은 문서 예시용 주소입니다.

다산데이타 Open_HPC의 공개 관리자·사용자 가이드를 검토하여 목차 구성과 보완 주제를 참고했습니다. 원문·이미지·로고를 복제하지 않았습니다. 작성 시점의 GitHub 메타데이터에서 해당 저장소는 public이고 인식된 라이선스 값은 없었습니다. 공개 열람 가능성과 자유로운 재배포 허용은 별개이므로 원문을 재사용할 때는 원저작자의 라이선스·허가를 별도로 확인해야 합니다.

- [기존 관리자 가이드](https://github.com/dasandata/Open_HPC/tree/master/Document/Admin%20Guide)
- [기존 사용자 가이드](https://github.com/dasandata/Open_HPC/tree/master/Document/User%20Guide)

## 공식 문서

- [OpenHPC](https://openhpc.community/): 배포 구성·지원 버전별 설치 문서
- [Warewulf 4.6](https://warewulf.org/docs/v4.6.x/): `wwctl` 기반 절차. Warewulf 3에 그대로 적용하지 않음
- [Slurm 빠른 시작](https://slurm.schedmd.com/quickstart.html): 자원·작업·기본 명령
- [Slurm srun](https://slurm.schedmd.com/srun.html): 명령·대화형 작업 실행
- [OpenSSH ssh](https://man.openbsd.org/ssh.1): SSH 접속·호스트 인증·포트 전달
- [OpenSSH scp](https://man.openbsd.org/scp.1): 파일 전송·포트 옵션
- [Lmod 사용자 안내](https://lmod.readthedocs.io/en/latest/010_user.html): 모듈 환경 관리
- [Red Hat Enterprise Linux 8 서버 운영](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/8/html-single/deploying_different_types_of_servers/index): NFS·공유 권한
- [Docker 설치 후 권한 안내](https://docs.docker.com/engine/install/linux-postinstall/): Docker 그룹 권한
- [Docker rootless](https://docs.docker.com/engine/security/rootless/): 비특권 실행의 전제와 제한
- [Jupyter Server 운영 안내](https://jupyter-server.readthedocs.io/en/latest/operators/public-server.html): 서버 인증·접근 구성
- [tmux 문서](https://github.com/tmux/tmux/wiki): 세션 유지·재접속
- [rsync 매뉴얼](https://download.samba.org/pub/rsync/rsync.1): 전송 옵션과 부분 파일
- [문서 예시용 IPv4 주소 RFC 5737](https://www.rfc-editor.org/rfc/rfc5737): TEST-NET 대역

## 유지보수 원칙

각 현장의 OS·배포 도구·응용프로그램 버전이 바뀌면 관련 예제를 재검증합니다. 현장 안내서의 정책과 실제 상태가 범용 예제보다 우선합니다. 이 문서의 검토일은 모든 소프트웨어 조합의 인증 일자가 아닙니다.

수정 시 대상 독자·버전·실행 위치·전제조건·성공 기준·복구 방법을 함께 확인합니다. 새 기능은 기본 제공으로 단정하지 말고 선택 기능으로 표시합니다. 관리자 명령을 사용자 빠른 시작에 섞지 않습니다.

공개 전 다음을 확인합니다.

- 실제 고객명·연구실명·실제 서버 주소·계정·연락처·장비 식별정보 없음
- 비밀번호·키·토큰·라이선스 원문·구성 보관본·실제 로그 없음
- Git 이력에도 같은 민감정보가 없는지 확인
- 내부 문서로 연결되는 실제 URL·공유 링크 없음
- 코드 블록·문서 링크·오프라인 HTML의 탐색·인쇄 확인

## 저작권·재사용

별도의 재사용 라이선스는 이 저장소에 지정하지 않았습니다. 공개 게시만으로 복제·수정·재배포에 대한 포괄적인 허가가 부여된다고 해석하지 않습니다. 재사용 정책은 저장소 소유자가 결정하며, 각 외부 문서·제품·상표의 권리는 해당 권리자에게 있습니다.
