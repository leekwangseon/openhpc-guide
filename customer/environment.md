# 실행 환경 준비
Module이 제공되는 현장에서만 사용합니다.

```bash
module list
module avail
module show YOUR_MODULE
module load YOUR_MODULE
```

`YOUR_MODULE`은 실제 목록에 있는 프로그램/버전으로 바꿉니다. 작업 기록에 프로그램 버전과 모듈 목록을 남깁니다. `module purge`는 현재 환경을 모두 내리므로 실행 중인 작업의 환경 설정을 임의로 바꾸지 않습니다.

Conda·Python·컨테이너는 제공되는 경우에만 사용합니다. 오래된 예제의 Python·CUDA·딥러닝 버전을 그대로 설치하지 말고 프로젝트 요구 버전과 지원 조합을 확인합니다. 시스템 Python을 덮어쓰거나 일반 사용자 작업에 `sudo pip`를 사용하지 않습니다.
