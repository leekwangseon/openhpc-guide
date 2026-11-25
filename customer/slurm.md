# Slurm 작업 제출과 자원 정책

Slurm을 실제로 사용하는 현장을 위한 안내입니다. 직접 실행이 지정된 현장은 [직접 실행 안내](run.md)를 사용합니다. Slurm 밖에서 시작한 작업은 Slurm 대기열에 자동으로 표시되지 않습니다.

## 1. 자원과 대기열

Partition은 노드의 논리적 묶음, Job은 자원 요청과 실행 단위입니다. `--ntasks`는 프로세스 수, `--cpus-per-task`는 프로세스당 CPU 수입니다. 메모리는 `--mem` 또는 `--mem-per-cpu` 등 현장이 사용하는 정책을 확인합니다. 요청량이 크거나 제한을 넘으면 자원이 남아 보여도 작업이 대기할 수 있습니다.

Backfill은 먼저 예정된 작업을 지연시키지 않는 범위에서 빈 시간에 다른 작업을 실행하는 방식입니다. 작업 시작 순서는 단순 제출 순서만이 아니라 예약·파티션·우선순위·필요 자원의 영향을 받습니다.

## 2. 노드·작업 상태 확인

```bash
sinfo
sinfo -Nel
squeue -u "$USER"
squeue -u "$USER" -o '%.18i %.12P %.24j %.8T %.10M %.6D %R'
scontrol show job YOUR_JOB_ID
```

| 노드 상태 | 의미 |
|---|---|
| idle | Slurm 기준 미할당. 직접 실행 작업 유무는 별도 |
| mix | 일부 자원이 할당된 상태 |
| alloc | 자원이 할당된 상태 |
| drain / down | 새 작업 배정 제외 / 사용 불가 상태 |
| completing | 작업 종료·정리 중 |
| 상태 뒤 `*` | 응답하지 않는 노드 표시. 관리자 확인 필요 |

| 작업 상태 | 확인할 점 |
|---|---|
| PENDING | `%R` 또는 Reason 필드의 대기 이유 |
| RUNNING | 실행 노드·시간·출력 로그 |
| COMPLETED | 종료 코드와 실제 결과를 함께 확인 |
| FAILED / OUT_OF_MEMORY / TIMEOUT | 프로그램 오류 / 메모리 / 시간 제한 |
| CANCELLED | 사용자 또는 운영 정책에 의한 취소 |

`sinfolong`, `squeuelong`은 표준 Slurm 명령이 아니라 현장별 별칭일 수 있습니다. 없는 경우 위 표준 명령과 출력 형식을 사용합니다.

## 3. 대화형 작업

```bash
srun -p YOUR_PARTITION --nodes=1 --ntasks=1 --cpus-per-task=2 \
  --mem=2G --time=00:10:00 --pty bash
hostname
printf '%s\n' "${SLURM_JOB_ID:-}" "${SLURM_CPUS_PER_TASK:-}"
exit
```

셸을 열기 전에 자원 배정을 기다릴 수 있습니다. 대화형 셸을 닫아야 자원을 반환합니다. 반면 `srun ... hostname`처럼 명령을 직접 지정하면 명령이 끝날 때 종료됩니다. 시간 제한은 배정 단계에서 지정합니다.

GPU 노드가 제공되고 해당 파티션에서 GRES를 사용하는 경우 `--gres=gpu:1` 같은 요청을 추가합니다. GPU 종류·개수 요청 형식은 현장 설정을 따릅니다. 할당 후 `nvidia-smi`와 프레임워크 GPU 인식을 확인합니다.

## 4. 첫 배치 작업

공유 작업 폴더에서 파일을 작성합니다. 아래 예제는 2분 안에 호스트명과 날짜를 출력합니다.

```bash
cat > hello.slurm <<'EOF'
#!/bin/bash
#SBATCH --job-name=hello
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:02:00
#SBATCH --output=hello-%j.out
#SBATCH --error=hello-%j.err
set -euo pipefail
hostname
date --iso-8601=seconds
EOF
sbatch -p YOUR_PARTITION hello.slurm
```

Job ID를 기록하고 `squeue -u "$USER"`로 확인합니다. 완료 후 `hello-작업번호.out`, `.err`를 읽습니다. 스크립트의 `#SBATCH`는 셸 명령이 아니므로 `$HOME` 같은 셸 변수가 그 위치에서 자동 확장된다고 가정하지 않습니다. `%j`는 Slurm의 Job ID 치환 표기입니다.

## 5. Conda·Module·컨테이너 작업 예제

다음 공통 템플릿의 실행 부분에서 **사용할 환경 한 가지**를 선택합니다. GPU가 필요한 작업에서만 현장에 맞는 GPU 요청을 추가합니다.

```bash
cat > research.slurm <<'EOF'
#!/bin/bash
#SBATCH --job-name=research
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --time=00:10:00
#SBATCH --output=research-%j.out
set -euo pipefail
echo "job=$SLURM_JOB_ID host=$(hostname)"
export OMP_NUM_THREADS="$SLURM_CPUS_PER_TASK"

# Conda 설치 경로와 프로그램을 실제 값으로 변경합니다.
source YOUR_CONDA_ROOT/etc/profile.d/conda.sh
conda activate research-demo
srun python -u ./your_program.py
EOF
sbatch -p YOUR_PARTITION research.slurm
```

Module을 쓰면 위 Conda 초기화·활성화·실행 부분을 다음으로 바꿉니다. 비대화형 셸의 module 초기화는 현장 절차를 따릅니다.

```bash
module load YOUR_MODULE
srun YOUR_APPLICATION YOUR_CONFIRMED_OPTIONS
```

Apptainer/Singularity를 쓰면 공유 이미지와 작업 폴더를 명시합니다.

```bash
srun apptainer exec --bind "$PWD:/work" --pwd /work \
  ./research.sif python /work/your_program.py
```

GPU가 배정된 작업에는 승인된 이미지 조합에서 `--nv`를 추가합니다. Docker는 현장의 Slurm 연동 방식과 GPU 장치 매핑을 받아 사용합니다. `srun docker run`만으로 컨테이너의 권한·자원 격리가 완성된다고 가정하지 않습니다. [Docker](docker.md)와 [Apptainer](apptainer.md) 안내를 함께 확인합니다.

## 6. MPI와 여러 노드

각 노드가 같은 실행파일·라이브러리·입력 경로를 읽을 수 있어야 합니다. 지원되는 MPI 모듈과 Slurm MPI plugin을 확인합니다.

```bash
module load YOUR_COMPILER_MODULE YOUR_MPI_MODULE
srun --mpi=list
mpicc -O2 -o mpi-hello mpi-hello.c
srun -p YOUR_PARTITION --nodes=2 --ntasks-per-node=2 \
  --time=00:02:00 --mpi=YOUR_SUPPORTED_PLUGIN ./mpi-hello
```

예제 소스는 [MPI 예제](../examples/mpi-hello.c)에 있습니다. PMIx/PMI2 등 현장이 지원하는 조합으로 바꾸며, 모든 MPI에 같은 `--mpi` 값을 적용하지 않습니다. MPI 라이브러리·IB 모듈·응용프로그램을 단계별로 시험합니다. ANSYS와 같은 제품은 제품 자체의 Slurm/MPI 연동 절차를 우선합니다.

## 7. 작업 취소·로그·실패 진단

```bash
scancel YOUR_JOB_ID
scontrol show job YOUR_JOB_ID
tail -n 50 research-YOUR_JOB_ID.out
```

회계 기능이 구성된 경우:

```bash
sacct -j YOUR_JOB_ID --format=JobID,JobName,State,Elapsed,ExitCode,MaxRSS
```

`squeue`에서 사라졌다는 사실만으로 성공을 판단하지 않습니다. 메모리 오류는 실제 MaxRSS·요청량·프로세스 수를, TIMEOUT은 시간 제한과 체크포인트를 확인합니다. 무조건 자원을 크게 늘려 재제출하기보다 실패 원인을 먼저 확인합니다.

같은 실행을 여러 입력으로 반복할 때는 현장에서 허용한 Job Array를 사용할 수 있습니다. `#SBATCH --array=1-5`와 `$SLURM_ARRAY_TASK_ID`, 출력 이름의 `%A_%a`를 조합하고 동시 실행 제한과 입력 대응을 확인합니다.

## 8. 우선순위·시작 예상시간

```bash
squeue --start -u "$USER"
sprio -u "$USER"
sshare -l
```

기능과 권한이 제공되는 경우에 확인합니다. 예상 시작시각은 자원·정책·다른 작업의 종료에 따라 바뀌며 보장된 예약 시각이 아닙니다. Fairshare 정보가 없으면 회계·우선순위 plugin 구성을 담당자에게 확인합니다.

Age, Fairshare, JobSize, Partition, QoS, Association, TRES 등의 요인이 설정된 가중치에 따라 우선순위에 반영될 수 있습니다. 큰 숫자의 우선순위 하나만으로 다음 실행 작업을 결정할 수는 없습니다. 현장의 예약·선점·파티션 정책도 영향을 줍니다.

## 9. 사용자·그룹·QoS 제한 조회

SlurmDBD와 회계가 설정되어 있고 조회 권한이 있는 경우의 예입니다. 이 안내의 숫자를 운영 제한으로 간주하지 않습니다.

```bash
sacctmgr show cluster
sacctmgr show account
sacctmgr show association where user="$USER"
sacctmgr show qos format=Name,Priority,MaxWall,MaxJobsPU,MaxSubmitPU,MaxTRESPU
```

| 정책 | 의미 | 확인할 값 |
|---|---|---|
| MaxJobs / MaxJobsPU | 동시 실행 수 제한 | 현장 정책 |
| MaxSubmit / MaxSubmitPU | 실행·대기 등을 포함한 제출 수 제한 | 현장 정책 |
| MaxWall | 최대 실행시간 | 요청 가능 범위 |
| GrpTRES / MaxTRESPU | 그룹·사용자의 자원 제한 | CPU·메모리·GPU 등 |
| Fairshare / Shares | 사용량과 배분 기준 | 소속 Account·Association |
| QoS | 우선순위·상한·예외 정책 | 허용된 QoS와 기본값 |

제한 초과·라이선스 대기·노드 비가용 등 대기 사유를 확인하고 담당자에게 Job ID와 함께 문의합니다. 사용자가 회계·QoS 값을 임의로 수정하지 않습니다.

## 10. 파티션·노드·설정 확인

```bash
scontrol show partition YOUR_PARTITION
scontrol show node YOUR_NODE
scontrol show config
```

상세 출력의 CPU·메모리·GRES·시간 제한과 현장 안내를 비교합니다. 설정 파일은 `/etc/slurm/slurm.conf` 등의 현장 경로에 있고 configless 노드는 캐시·서비스 설정이 다를 수 있습니다. 사용자에게 공개되지 않는 값이 있으면 담당자에게 필요한 범위만 요청합니다. 조회와 설정 변경은 다른 권한입니다.

다음은 **정책 해석을 위한 가상의 예**이며 제공 중인 클러스터의 제한이 아닙니다.

| 구분 | 예시 | 해석 |
|---|---|---|
| 사용자 동시 실행 | 2개 | 세 번째 작업은 다른 조건이 충족되어도 대기할 수 있음 |
| 프로젝트 동시 GPU | 4개 | 같은 Account 사용자가 함께 사용하는 상한 |
| 일반 QoS | 최대 1일 | 더 긴 시간 요청은 거부·대기 사유가 될 수 있음 |
| 짧은 작업 QoS | 최대 30분 | 지정 조건을 만족하는 작업만 사용 |

`sbatch --account=YOUR_ACCOUNT --qos=YOUR_QOS -p YOUR_PARTITION job.slurm`처럼 승인된 조합을 사용합니다. 정책에 따라 허용된 기본값이 자동 적용될 수도 있습니다. Fairshare 사용량 감소 주기·우선순위 가중치·QoS 제한은 각 현장 값으로 확인합니다.

참고: [Slurm 빠른 시작](https://slurm.schedmd.com/quickstart.html), [squeue](https://slurm.schedmd.com/squeue.html), [우선순위](https://slurm.schedmd.com/priority_multifactor.html), [회계 조회](https://slurm.schedmd.com/sacctmgr.html)
