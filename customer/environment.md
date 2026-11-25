# 실행 환경 준비

프로그램을 제공받은 방식에 따라 아래 상세 안내를 선택하세요. 모든 기능이 모든 클러스터에 설치되어 있는 것은 아닙니다.

| 제공 방식 | 상세 안내 | 주요 내용 |
|---|---|---|
| 개인 Python 환경 | [Conda·Python](conda.md) | 설치 확인, 환경 생성, GPU 런타임, 스크립트, 저장·복원 |
| 공유 프로그램 | [Module](modules.md) | 검색, 불러오기, 버전 전환, 환경 확인 |
| Docker 이미지 | [Docker](docker.md) | 이미지·컨테이너·볼륨·GPU·빌드·정리 |
| HPC 컨테이너 | [Apptainer·Singularity](apptainer.md) | SIF·바인드·GPU·빌드·Jupyter |
| GPU 시험 | [GPU·학습 실습](gpu.md) | 장치 확인, 행렬 계산, 짧은 GAN 학습 |
| 자원 배정 | [Slurm 상세 사용](slurm.md) | 대화형·배치·MPI·GPU·정책 조회 |
Module이 제공되는 현장에서만 사용합니다.

```bash
module list
module avail
module show YOUR_MODULE
module load YOUR_MODULE
```

`YOUR_MODULE`은 실제 목록에 있는 프로그램/버전으로 바꿉니다. 작업 기록에 프로그램 버전과 모듈 목록을 남깁니다. `module purge`는 현재 환경을 모두 내리므로 실행 중인 작업의 환경 설정을 임의로 바꾸지 않습니다.

Conda·Python·컨테이너는 제공되는 경우에만 사용합니다. 오래된 예제의 Python·CUDA·딥러닝 버전을 그대로 설치하지 말고 프로젝트 요구 버전과 지원 조합을 확인합니다. 시스템 Python을 덮어쓰거나 일반 사용자 작업에 `sudo pip`를 사용하지 않습니다.
