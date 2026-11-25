# 계산 노드 추가·교체·정보 변경

## 1. 신규·교체 노드 확인표

노드명, 관리 NIC MAC·포트, 관리 IP, 고속망 IP·장치, BMC, CPU·메모리·GPU, UEFI/Legacy·Secure Boot, 부팅 이미지·커널, 로컬 디스크 보존 범위를 확인합니다. MAC과 IP 중복은 기존 노드 통신·DHCP에 영향을 줄 수 있습니다.

교체 시 기존 노드의 직접 작업·예약·스케줄러 상태를 확인하고 사용 제외합니다. 등록 정보 변경과 로컬 디스크 초기화는 별도 작업입니다. 새 노드 등록만으로 디스크 포맷을 승인한 것으로 보지 않습니다.

## 2. Warewulf 3 등록 형태

배포 대상 버전과 옵션은 `wwsh` 도움말에서 확인합니다. 아래는 기존 이미지·bootstrap을 재사용하는 형태입니다.

```bash
wwsh node list
wwsh vnfs list
wwsh bootstrap list
wwsh file list
wwsh node new YOUR_NODE --netdev YOUR_MGMT_NIC \
  --ipaddr=YOUR_MGMT_IP --hwaddr=YOUR_MGMT_MAC \
  --netmask=YOUR_MGMT_NETMASK --gateway=YOUR_MGMT_GATEWAY
wwsh provision set YOUR_NODE --vnfs=YOUR_VNFS \
  --bootstrap=YOUR_BOOTSTRAP --files=YOUR_APPROVED_FILE_LIST
wwsh node print YOUR_NODE
wwsh provision print YOUR_NODE
```

배포 파일 목록에는 실제 인증·네트워크 구성에 필요한 승인 파일만 지정합니다. 과거 예제의 shadow 포함 목록을 그대로 복사하지 않습니다. IB 등 추가 인터페이스는 별도 등록·템플릿 설정으로 반영하고 관리망과 혼동하지 않습니다.

기존 노드의 NIC 교체·IP 변경은 신규 중복 객체를 만들지 말고 해당 버전의 node set 등 변경 명령을 확인합니다. 수정 전 기존 값을 보관하고 대상 한 대를 다시 조회합니다.

## 3. DHCP·PXE 반영

등록 정보를 확인한 뒤 현장의 PXE 설정을 생성합니다.

```bash
wwsh pxe update
```

DHCP 구성 검증·갱신·서비스 reload/restart는 사용하는 DHCP 서버의 실제 설정에 따라 수행합니다. 관리망 인터페이스와 서비스 범위를 확인하고 외부망에 새 DHCP 서비스를 잘못 제공하지 않습니다. 여러 노드 등록 중 반복 재시작으로 서비스가 실패 상태가 되지 않는지도 확인합니다.

Warewulf 4는 `wwctl`의 이미지·노드·프로파일·overlay 절차로 수행합니다. 버전 3 명령을 그대로 적용하지 않습니다.

## 4. 부팅 검증

1. PXE할 NIC·UEFI/Legacy·Secure Boot 정책을 확인합니다.
2. 승인된 정상 기동 또는 1회 부팅 설정으로 대표 노드를 부팅합니다.
3. DHCP → bootloader → 커널/initramfs → 이미지 전송 → 초기화 순서의 로그를 확인합니다.
4. SSH·계정·IP·IB·시간 동기화·공유 마운트·서비스를 확인합니다.
5. 일반 사용자 계산·멀티노드·필요한 라이선스 시험을 합니다.
6. 재부팅해 영구 부팅 경로와 구성이 유지되는지 확인합니다.

전원 On이나 DHCP 응답만으로 OS 부팅 완료로 표시하지 않습니다. 하드웨어 POST가 길거나 멈춘 경우 BMC 콘솔·이벤트 시각을 함께 확인합니다.

## 5. 스케줄러와 자원 등록

Slurm 사용 시 노드의 `slurmd -C` 등으로 실제 CPU 토폴로지·메모리를 확인하고 OS·RAM 루트 여유를 고려해 설정합니다. 새 노드명·NodeAddr·Partition·GRES·인증·회계 필요 사항을 반영하고 시험 작업으로 등록을 검증합니다. 기존 노드와 CPU 세대·GPU·메모리가 다르면 Feature·Partition 등 정책을 검토합니다.

사용자 안내·모니터링·하드웨어 대응표·예약 체계도 갱신합니다. 교체한 노드의 예전 키·인증 정보는 현장 절차로 회수합니다.
