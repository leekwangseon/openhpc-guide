# Docker 사용하기

Docker가 제공·허용된 노드에서만 사용합니다. 일반 Docker daemon 접근 권한은 root 수준의 권한을 줄 수 있으며 `--user`는 daemon 접근 권한 자체를 제한하지 않습니다. Docker 그룹 가입, rootless 구성, GPU 실행 권한은 관리자가 정합니다.

## 1. 사용 환경 확인

```bash
docker version
docker info
id
```

Client만 보이거나 daemon 연결·권한 오류가 나면 담당자에게 문의합니다. `/var/run/docker.sock` 권한을 넓히거나 승인 없이 sudo로 우회하지 않습니다. Rootless Docker는 별도 구성과 기능 제한이 있습니다.

## 2. 이미지 선택과 내려받기

```bash
IMAGE=YOUR_APPROVED_IMAGE
docker pull "$IMAGE"
docker image ls
docker image inspect "$IMAGE"
```

프로젝트가 검증한 저장소·태그·가능하면 digest를 기록합니다. `latest`나 같은 태그의 내용은 바뀔 수 있습니다. 이미지의 OS·CPU·Python·프레임워크·CUDA 버전과 라이선스를 확인합니다. 큰 이미지는 다운로드·로컬 저장 용량을 먼저 확인합니다.

## 3. 기본 실행과 작업 폴더 연결

현재 폴더를 컨테이너의 `/work`로 연결합니다. 컨테이너 안에서 호스트의 HOME·사용자명이 자동으로 같은 의미가 되지는 않습니다.

```bash
docker run --rm --user "$(id -u):$(id -g)" \
  --mount "type=bind,src=$PWD,dst=/work" -w /work \
  "$IMAGE" python -c 'import sys; print(sys.version)'
```

이미지가 숫자 UID 실행을 지원해야 합니다. 프로젝트가 추가 그룹이나 쓰기 가능한 HOME을 요구하면 관리자와 이미지 설정을 확인합니다. 입력 전용 경로는 read-only 바인드를 사용할 수 있습니다. 시스템 디렉터리 전체를 임의로 연결하지 않습니다.

```bash
docker run --rm --user "$(id -u):$(id -g)" \
  --mount "type=bind,src=$PWD,dst=/work" -w /work \
  "$IMAGE" python /work/your_program.py
```

`--rm`은 종료된 컨테이너를 제거하지만 바인드된 작업 폴더의 파일은 남습니다. 컨테이너 내부의 임시 변경은 결과 보관 경로가 아닙니다.

## 4. 대화형 사용·상태·로그·종료

```bash
docker run --name research-shell -it \
  --user "$(id -u):$(id -g)" \
  --mount "type=bind,src=$PWD,dst=/work" -w /work "$IMAGE" sh
docker ps
docker ps -a
docker logs research-shell
docker exec -it research-shell sh
docker stop research-shell
docker rm research-shell
```

대화형 셸을 나간 다음 같은 컨테이너 이름을 다시 쓰려면 기존 컨테이너를 정리합니다. `docker exec`는 실행 중인 컨테이너에만 사용합니다. 종료는 본인 컨테이너와 결과 저장을 확인한 뒤 수행합니다. 다른 사용자의 컨테이너를 조작하거나 일괄 prune하지 않습니다.

## 5. GPU 실행

지원 드라이버와 NVIDIA Container Toolkit이 구성되어 있어야 합니다. 직접 실행이 허용된 환경에서 승인받은 GPU만 지정하는 예제입니다.

```bash
docker run --rm --gpus 'device=YOUR_ASSIGNED_GPU_ID' "$IMAGE" nvidia-smi
```

기존 `--runtime=nvidia` 방식과 현재 `--gpus` 방식은 설치 구성에 따라 다릅니다. 과거 예제를 무조건 대체 적용하지 않습니다. Slurm의 `CUDA_VISIBLE_DEVICES`는 컨테이너/호스트의 GPU 번호와 그대로 대응하지 않을 수 있으므로 스케줄러가 제공하는 컨테이너 연동을 사용합니다. `--gpus all`로 할당 외 GPU를 사용하지 않습니다.

## 6. 셸 스크립트로 반복 실행

```bash
cat > run-container.sh <<'EOF'
#!/bin/bash
set -euo pipefail
IMAGE=YOUR_APPROVED_IMAGE
docker run --rm --user "$(id -u):$(id -g)" \
  --mount "type=bind,src=$PWD,dst=/work" -w /work \
  "$IMAGE" python /work/your_program.py
EOF
bash -n run-container.sh
bash run-container.sh > container-run.log 2>&1
```

## 7. 이미지 만들기와 재사용

대화형 변경만 남기기보다 Dockerfile과 환경 파일을 기록합니다. 다음은 별도로 준비한 requirements.txt를 이미지에 추가하는 형태입니다.

```dockerfile
FROM YOUR_APPROVED_BASE_IMAGE
WORKDIR /work
COPY requirements.txt /tmp/requirements.txt
RUN python -m pip install --no-cache-dir -r /tmp/requirements.txt
```

```bash
docker build -t local/research-demo:1 .
docker image ls
```

`docker commit`은 대화형 컨테이너 변경을 이미지로 만들 수 있으나 이력 재현이 어렵고 비밀정보가 들어갈 수 있습니다. Dockerfile을 우선하고 이미지 레이어에도 비밀값을 넣지 않습니다. 저장소로 배포할 때는 승인된 namespace로 `docker tag`·`docker push`하고 인증정보는 이미지에 포함하지 않습니다. 여러 컨테이너 조합은 `docker compose`가 제공·허용된 경우 별도 프로젝트 설정으로 관리합니다.

## 8. 정리와 HPC 사용 시 유의점

본인 프로젝트가 사용하지 않는 이미지인지 확인한 뒤 `docker image rm YOUR_IMAGE_ID`로 정리합니다. 실행 중인 컨테이너와 공유 이미지의 영향을 먼저 확인합니다.

이미지는 노드별 로컬 저장소에 있어야 할 수 있고 RAM 기반 노드에서는 재부팅으로 사라질 수 있습니다. 계산 전에 승인된 방식으로 준비하거나 Apptainer/Singularity의 공유 이미지 방식을 검토합니다. 파일 소유권·메모리·공유 메모리·GPU·네트워크 정책은 현장 설정을 따릅니다.

참고: [Docker 실행](https://docs.docker.com/engine/containers/run/), [권한 안내](https://docs.docker.com/engine/install/linux-postinstall/)
