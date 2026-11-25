# Apptainer와 Singularity

과학 계산용 컨테이너 실행기입니다. 같은 계열이라도 제품·버전에 따라 옵션과 보안 설정이 다릅니다. 아래 예제는 `apptainer`를 사용하며 Singularity만 제공되는 현장은 담당자가 확인한 대응 명령으로 바꿉니다.

## 1. 제공 여부 확인

```bash
module avail
command -v apptainer
apptainer --version
```

모듈 방식이면 현장에서 안내받은 모듈을 먼저 불러옵니다. 컨테이너라고 모든 권한 문제가 사라지는 것은 아닙니다. 호스트 파일·바인드·네트워크·GPU 접근은 사용자 권한과 관리자 정책에 따릅니다.

## 2. 이미지 가져오기와 기본 실행

```bash
apptainer pull research.sif docker://YOUR_APPROVED_IMAGE
ls -lh research.sif
apptainer inspect research.sif
apptainer exec research.sif cat /etc/os-release
apptainer shell research.sif
```

셸 종료는 `exit`입니다. 이미지 안에 Python이 있는 경우:

```bash
apptainer exec research.sif python --version
apptainer exec --bind "$PWD:/work" --pwd /work research.sif python /work/your_program.py
```

HOME·현재 폴더 등의 기본 바인드 범위는 버전·설정에 따라 달라집니다. 데이터·출력 경로를 확인하고 명시적으로 연결합니다. 바인드된 호스트 파일은 컨테이너 안에서 변경할 수도 있으므로 필요하면 `:ro`로 제한합니다.

## 3. GPU와 공용 라이브러리

```bash
apptainer exec --nv research.sif nvidia-smi
```

GPU 사용이 할당된 노드에서 실행합니다. `--nv`가 모든 프레임워크·CUDA 조합의 호환성을 보장하지는 않습니다. 이미지의 프레임워크 런타임과 호스트 드라이버 조합을 확인합니다.

관리자가 승인한 공용 라이브러리 경로를 바인드해야 하는 경우의 형태입니다.

```bash
apptainer exec --nv --bind YOUR_SHARED_SOFTWARE_PATH:/software:ro \
  research.sif sh -c 'printf "%s\n" "$LD_LIBRARY_PATH"; ls /software'
```

환경변수를 컨테이너 안에서 확인할 때는 `sh -c '...'`처럼 셸을 명시합니다. 호스트에서 먼저 확장된 변수값을 보고 컨테이너 내부 값이라고 판단하지 않습니다. 라이브러리 바인드만으로 ABI나 MPI 호환성이 해결되지는 않습니다.

## 4. 이미지 빌드·수정

SIF 이미지를 직접 수정하지 않는 방식이 일반적이지만, 이미지 생성·수정이 불가능하다는 뜻은 아닙니다. 정의 파일·sandbox·overlay 지원과 권한을 확인합니다.

```text
Bootstrap: docker
From: YOUR_APPROVED_BASE_IMAGE

%post
    echo "Add only approved package-install commands for this image OS."

%runscript
    exec python "$@"
```

위 형태를 `research.def`로 저장하고 승인된 빌드 환경에서 생성합니다.

```bash
apptainer build research.sif research.def
```

필요한 권한이나 fakeroot·원격 빌드가 제공되지 않으면 관리자에게 요청합니다. sandbox를 지원하고 수정이 허용된 경우:

```bash
apptainer build --sandbox research-sandbox research.sif
apptainer shell --writable research-sandbox
apptainer build research-repacked.sif research-sandbox
```

`--writable`이 일반 사용자에게 root 권한을 주지는 않습니다. 영구 변경은 정의 파일에 기록해 재현하고, 동시 쓰기 중인 sandbox를 공유 작업에서 사용하지 않습니다.

## 5. 실행 스크립트

```bash
cat > run-apptainer.sh <<'EOF'
#!/bin/bash
set -euo pipefail
apptainer exec --bind "$PWD:/work" --pwd /work \
  ./research.sif python /work/your_program.py
EOF
bash -n run-apptainer.sh
bash run-apptainer.sh > apptainer-run.log 2>&1
```

GPU가 필요하면 자원 할당을 먼저 확인하고 `--nv`를 추가합니다. Slurm에서는 [작업 예제](slurm.md)의 자원 요청과 함께 사용합니다.

## 6. Jupyter 실행

Jupyter가 설치된 이미지에서 실행하고 호스트의 작업 폴더를 바인드합니다.

```bash
apptainer exec --bind "$PWD:/work" --pwd /work research.sif \
  jupyter lab --no-browser --ip=127.0.0.1 --port=8888
```

[GUI·터널 안내](optional.md)의 SSH 포트 전달로 내 PC 브라우저에서 접속합니다. X11 브라우저 실행이 필수인 것은 아닙니다. 계산 노드에서 실행할 때는 노드 할당과 해당 노드까지의 터널 경로를 확인합니다.

참고: [Apptainer 이미지 빌드](https://apptainer.org/docs/user/main/build_a_container.html), [GPU 지원](https://apptainer.org/docs/user/main/gpu.html)
