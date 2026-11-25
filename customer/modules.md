# Module로 공유 프로그램 사용하기

## 1. 기본 명령

Module은 관리자 설치본의 PATH·라이브러리 경로 등을 세션에 반영합니다. 프로그램 자체를 새로 설치하는 명령이 아닙니다. Lmod와 Environment Modules의 기능은 일부 다르므로 제공되는 도구를 확인합니다.

```bash
type module
module --version
module list
module avail
module show YOUR_MODULE
module load YOUR_MODULE
module unload YOUR_MODULE
```

Lmod에서 `ml`은 짧은 명령으로 사용할 수 있습니다. `module spider YOUR_KEYWORD`는 계층형 모듈의 검색에 유용하며 모든 구현에 있는 기능은 아닙니다.

## 2. 버전 선택과 전환

```bash
module avail
module load YOUR_COMPILER_MODULE
command -v gcc
gcc --version
module swap YOUR_COMPILER_MODULE YOUR_OTHER_COMPILER_MODULE
module list
```

CUDA는 제공되는 NVIDIA GPU와 개발 도구가 필요한 경우에만 사용합니다. `nvidia-smi`의 CUDA 표시와 `nvcc --version`은 각각 드라이버 지원 수준과 개발 툴킷 정보를 보여주므로 같지 않을 수 있습니다.

```bash
module load YOUR_CUDA_MODULE
command -v nvcc
nvcc --version
```

컴파일러·MPI·수치 라이브러리는 호환되는 조합으로 사용합니다. GNU용 MPI와 다른 컴파일러로 만든 바이너리를 임의로 섞지 않습니다. ANSYS 등 제품이 제공하는 MPI는 제품별 안내를 따릅니다.

## 3. 환경 변화 확인

```bash
printf '%s\n' "$PATH"
printf '%s\n' "${LD_LIBRARY_PATH:-}"
module show YOUR_MODULE
command -v YOUR_COMMAND
```

`module purge`는 현재 모듈을 내립니다. Lmod의 sticky 모듈이나 현장 기본값은 남거나 다시 로드될 수 있습니다. `module reset`의 제공 여부와 기본 모듈도 확인합니다. 알 수 없는 충돌을 해결하려고 사용자 환경 전체를 무조건 삭제하지 않습니다.

## 4. 실행 스크립트

```bash
cat > module-check.sh <<'EOF'
#!/bin/bash
set -euo pipefail
# module 명령이 비대화형 셸에도 제공되는지 확인합니다.
type module
module load YOUR_MODULE
module list
YOUR_COMMAND --version
EOF
bash -n module-check.sh
bash module-check.sh
```

module이 없으면 관리자가 지정한 초기화 스크립트를 먼저 source합니다. 특정 `/etc/profile.d` 파일이 모든 현장에 있다고 가정하지 않습니다.

## 5. 기본 환경과 저장 공간

Lmod에서는 `module save YOUR_COLLECTION`, `module restore YOUR_COLLECTION`으로 환경을 저장·복원할 수 있습니다. 이름이 바뀐 모듈은 복원에 실패할 수 있습니다. `.bashrc`에 모듈을 넣는 경우 기존 파일을 보관하고 승인된 모듈만 추가합니다. 설치되지 않은 CUDA나 특정 버전을 모든 로그인에 강제하지 않습니다.

공유 프로그램을 사용하면 개인 환경의 중복 설치를 줄일 수 있습니다. 개인 사용량은 `du -sh "$HOME"`, 저장소 여유는 `df -h "$HOME"`로 확인합니다. 사용자 quota는 현장 파일시스템에 맞는 도구·안내를 사용합니다.

참고: [Lmod 사용자 안내](https://lmod.readthedocs.io/en/latest/010_user.html)
