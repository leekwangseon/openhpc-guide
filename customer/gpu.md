# GPU 확인과 학습 실습

GPU가 제공되는 노드에서 사용 권한과 할당을 먼저 받습니다. 로그인 서버에 GPU가 없다고 전체 클러스터에 GPU가 없는 것은 아닙니다. GPU 없이 진행할 환경 시험과 GPU 계산 시험을 구분합니다.

## 1. 드라이버·사용량 확인

```bash
nvidia-smi
nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu --format=csv
printf '%s\n' "${CUDA_VISIBLE_DEVICES:-not-set}"
```

`gpustat`은 별도 설치된 경우에만 사용할 수 있습니다. 지속 확인은 `watch -n 2 nvidia-smi` 또는 `nvidia-smi --loop=2`를 사용하고 `Ctrl+c`로 마칩니다. 상태 조회가 자원 예약을 의미하지는 않습니다. 직접 실행 환경에서는 예약·사용 조정 정책을 따릅니다.

## 2. 작은 TensorFlow GPU 시험

실습 예제를 한 번에 받으려면 Git으로 이 가이드를 내려받을 수 있습니다. 받은 코드를 확인한 뒤 승인된 작업 공간에서 실행하세요.

```bash
git clone https://github.com/leekwangseon/openhpc-guide.git
cd openhpc-guide/examples
```

필요한 파일만 받을 때는 아래 curl 명령을 사용합니다.

검증된 [Conda 환경](conda.md), Module 또는 컨테이너 중 하나를 준비합니다. 예제는 외부 데이터를 내려받지 않는 작은 행렬 계산입니다.

```bash
curl -fLO https://leekwangseon.github.io/openhpc-guide/examples/tf-smoke.py
python tf-smoke.py
```

성공하면 TensorFlow 버전·보이는 GPU·실제 장치·체크섬이 출력됩니다. GPU가 없으면 CPU로 조용히 대체하지 않고 실패하도록 구성했습니다. GPU 목록이 비거나 라이브러리 로드가 실패하면 할당·드라이버·런타임 조합을 확인합니다.

## 3. 짧은 GAN 학습 시험

환경 확인을 위해 합성 데이터를 사용하는 작은 GAN 예제를 제공합니다. 기본 20 step이며 실제 연구용 모델이나 성능 측정용 기준이 아닙니다.

```bash
curl -fLO https://leekwangseon.github.io/openhpc-guide/examples/tf-gan-demo.py
python -u tf-gan-demo.py --steps 20 --require-gpu > gan.log 2>&1
tail -n 20 gan.log
```

완료하면 현재 작업 폴더에 `gan-synthetic-samples.npy`가 생성됩니다. GPU가 없는 환경의 짧은 CPU 시험은 `--require-gpu`를 빼고 자원 정책에 맞게 실행할 수 있습니다. 원본 입력·중요 결과와 별도 실습 폴더를 사용합니다.

## 4. 컨테이너에서 같은 예제 실행

TensorFlow가 있는 승인된 이미지와 배정받은 GPU를 사용합니다.

```bash
apptainer exec --nv --bind "$PWD:/work" --pwd /work research.sif \
  python /work/tf-smoke.py
```

Docker의 경우 [Docker 안내](docker.md)의 GPU 지정·작업 폴더 바인드를 사용합니다. Slurm 사용 환경에서는 [배치 스크립트](slurm.md)에 필요한 GPU 요청과 실행 부분을 반영합니다.

## 5. 오류가 날 때

실제 이미지 데이터의 DCGAN 학습까지 진행하려면 [TensorFlow 공식 DCGAN 예제](https://www.tensorflow.org/tutorials/generative/dcgan)를 참고해 데이터 다운로드 경로·출력·체크포인트·실행 시간을 확인합니다. 본 안내의 작은 합성 데이터 시험을 먼저 통과한 후 같은 환경에서 확장합니다. 기존 TensorFlow 1.x 외부 예제를 사용할 때는 해당 예제의 버전·라이선스·의존성을 검토하고 코드를 확인한 뒤 실행합니다.

| 증상 | 확인 |
|---|---|
| GPU를 찾을 수 없음 | 실제 실행 노드, GPU 배정, CUDA_VISIBLE_DEVICES, 컨테이너 GPU 전달 |
| CUDA 라이브러리 오류 | 드라이버·프레임워크 런타임 조합, 중복 모듈·경로 |
| Out of memory | GPU 실제 사용량, batch 크기, 다른 프로세스, 메모리 할당 정책 |
| no kernel image / unsupported architecture | GPU 세대와 해당 바이너리의 지원 범위 |
| GPU 사용률 0% | CPU 전처리·입출력 대기·실제 장치 선택·계산 규모 |

GPU 번호를 임의로 바꾸어 다른 사용자의 자원을 쓰거나 드라이버를 개인 작업으로 교체하지 않습니다. 모델 체크포인트와 환경 버전을 함께 보관하면 재현·복구에 도움이 됩니다.
