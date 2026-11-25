# Conda와 Python 환경

## 1. 사용 가능 여부와 설치

이미 제공되는 Conda 모듈·설치본이 있는지 먼저 확인합니다. 없다면 담당자가 승인한 배포판·채널과 현재 라이선스 조건을 확인합니다. Anaconda Distribution과 Miniconda 등은 구성·배포 조건이 다릅니다.

```bash
command -v conda
conda --version
conda env list
```

직접 설치가 허용된 경우 [공식 배포 안내](https://docs.conda.io/projects/conda/en/stable/user-guide/install/index.html)에서 CPU 아키텍처에 맞는 설치 스크립트와 체크섬을 확인합니다. 서버에 브라우저가 없으면 내 PC에서 링크를 확인해 내려받거나 파일을 전송합니다.

```bash
cd "$HOME"
curl -fL 'YOUR_APPROVED_INSTALLER_URL' -o conda-installer.sh
sha256sum conda-installer.sh
bash conda-installer.sh
```

체크섬을 배포처의 값과 비교한 후 설치합니다. 관리자 승인 없이 root로 실행하지 않습니다. 초기화가 필요한 셸은 설치 안내에 따라 `conda init bash`를 적용하고 새 셸을 엽니다. 기존 `.bashrc`를 통째로 덮어쓰지 않습니다.

```bash
conda config --set auto_activate_base false
conda info
```

Conda 자체 업데이트는 관리되는 공유 설치본인지 먼저 확인합니다. 개인 설치본에서 승인된 경우 `conda update -n base conda`를 사용하되, 작업 도중 환경을 바꾸지 않습니다.

## 2. 환경 생성·활성화·종료

Python 버전은 응용프로그램 지원 조건에 맞춰 선택합니다. 아래 3.11은 예시이며 모든 제품의 요구 버전은 아닙니다.

```bash
conda create -n research-demo python=3.11 pip
conda activate research-demo
command -v python
python --version
python -m pip --version
python -m pip install numpy
python -c 'import numpy; print(numpy.__version__)'
conda deactivate
```

환경 안에서 `python -m pip`를 쓰면 대상 Python을 분명히 할 수 있습니다. 시스템 Python에 패키지를 설치하지 않습니다. 여러 노드에서 공유 환경을 동시에 변경하지 않습니다.

## 3. TensorFlow와 CUDA 환경

GPU 드라이버, Python, TensorFlow, CUDA 런타임의 호환 조합을 먼저 확인합니다. 오래된 TensorFlow 1.x·Python 3.6·CUDA 9 예제는 레거시 조합이며 현재 장비용 기본 설치 명령이 아닙니다. 기존 연구의 재현이 필요하면 격리된 환경·컨테이너와 원래 요구사항을 담당자에게 확인합니다.

현재 Linux용 TensorFlow가 지원하는 조건을 만족하고 해당 GPU 자원 사용이 승인된 경우의 설치 형태입니다. 버전을 생략해 자동으로 바뀌게 두기보다 프로젝트에서 검증한 값을 지정합니다.

```bash
conda activate research-demo
python -m pip install 'tensorflow[and-cuda]==YOUR_SUPPORTED_TF_VERSION'
python -c 'import tensorflow as tf; print(tf.__version__); print(tf.config.list_physical_devices("GPU"))'
```

CPU용 설치는 지원 버전의 `tensorflow` 패키지를 사용합니다. 다른 버전의 시스템 CUDA·Module·pip 런타임을 무조건 함께 올리지 않습니다. [TensorFlow 설치 문서](https://www.tensorflow.org/install/pip)를 기준으로 OS·GPU·드라이버를 확인합니다.

## 4. 스크립트와 배치 실행

일괄 실행에서는 `.bashrc`에만 의존하지 말고 Conda 설치 경로를 명시합니다. `YOUR_CONDA_ROOT`를 실제 경로로 바꿉니다.

```bash
cat > run-python.sh <<'EOF'
#!/bin/bash
set -euo pipefail
source YOUR_CONDA_ROOT/etc/profile.d/conda.sh
conda activate research-demo
python -u ./your_program.py > python-run.log 2>&1
EOF
bash -n run-python.sh
bash run-python.sh
```

계산 노드와 자원을 배정받은 후 실행합니다. 단일 명령에는 `conda run -n research-demo python your_program.py`도 사용할 수 있습니다. Slurm 예제는 [작업 제출 안내](slurm.md)를 확인합니다.

## 5. 환경 내보내기·복원·제거

```bash
conda env export -n research-demo > environment-full.yml
conda env export -n research-demo --from-history > environment-history.yml
conda list -n research-demo --explicit > environment-explicit.txt
conda env create -n research-rebuild -f environment-history.yml
conda activate research-rebuild
python --version
conda deactivate
```

전체 YAML은 설치된 의존성까지, history는 직접 요청한 항목 중심으로 기록합니다. explicit 목록은 같은 플랫폼의 재현에 적합합니다. 채널·플랫폼·pip 의존성·빌드가 달라지면 동일 결과가 보장되지 않습니다. 내보낸 파일의 개인 경로·사설 채널 인증정보를 확인한 뒤 공유합니다.

사용하지 않는 환경은 실행 중인 작업이 없는지 확인한 후 제거합니다.

```bash
conda deactivate
conda env remove -n research-rebuild
conda env list
```

로그인 때 특정 환경을 자동 활성화할 수 있으나, 다른 프로그램·MPI와 충돌할 수 있습니다. 기본 자동 활성화보다는 실행 스크립트에서 환경을 지정하는 방법을 권합니다. 자동화가 필요하면 `.bashrc`의 기존 Conda 초기화 부분을 보존하고 사용자 추가 부분만 수정합니다.
