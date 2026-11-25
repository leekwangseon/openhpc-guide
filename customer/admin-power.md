# 노드 전원 관리: IPMI·RACADM·WOL

전원 조작은 승인된 관리자만 수행합니다. 먼저 대상 노드와 BMC의 대응표를 확인하고 사용자 작업·저장소 쓰기·점검 시간을 검토합니다. 조회 → 정상 종료 → 전원 상태 확인 순서를 기본으로 합니다.

## 1. IPMI 상태 조회

ipmitool이 제공되고 승인된 BMC 관리망에서 접근하는 경우입니다. `-a`는 암호 입력을 요청하며 비밀번호를 명령 인수에 넣지 않습니다.

```bash
ipmitool -I lanplus -H YOUR_BMC_HOST -U YOUR_BMC_USER -a chassis power status
ipmitool -I lanplus -H YOUR_BMC_HOST -U YOUR_BMC_USER -a chassis status
ipmitool -I lanplus -H YOUR_BMC_HOST -U YOUR_BMC_USER -a sel elist last 10
```

전원 상태·하드웨어 오류·이벤트 시각을 확인합니다. IPMI망은 일반 사용자에게 공개하지 않습니다.

## 2. 정상 종료와 전원 켜기

OS에 접속 가능하면 해당 OS의 정상 종료 절차를 우선합니다. 승인된 대상 한 대에서 수행하는 예입니다.

```bash
ssh YOUR_ADMIN_USER@YOUR_CONFIRMED_NODE 'sudo systemctl poweroff'
```

OS가 ACPI 종료를 지원하는 경우 IPMI의 soft 요청을 사용할 수 있습니다.

```bash
ipmitool -I lanplus -H YOUR_BMC_HOST -U YOUR_BMC_USER -a chassis power soft
ipmitool -I lanplus -H YOUR_BMC_HOST -U YOUR_BMC_USER -a chassis power status
```

종료 완료와 전원 Off를 확인한 뒤 필요한 경우 켭니다.

```bash
ipmitool -I lanplus -H YOUR_BMC_HOST -U YOUR_BMC_USER -a chassis power on
```

`off`, `reset`, `cycle`은 정상 종료와 같지 않습니다. OS 불응 시의 장애 대응 절차에서 데이터 손상 위험과 승인을 확인한 후 사용합니다. 반복 전원 사이클을 원인 조사 대신 수행하지 않습니다.

## 3. PXE 부팅 대상 확인

```bash
ipmitool -I lanplus -H YOUR_BMC_HOST -U YOUR_BMC_USER -a chassis bootparam get 5
```

부팅 장치 변경은 UEFI/Legacy, 1회/영구 적용, PXE할 NIC와 로컬 디스크 보존 범위를 확인합니다. 명령이 성공해도 BMC가 실제 어떤 플래그를 저장했는지 다시 조회합니다. 모든 장비에 같은 raw 명령이나 부팅 옵션을 적용하지 않습니다.

## 4. Dell RACADM

해당 iDRAC 버전에서 지원되는 명령을 확인합니다. SSH 호스트 지문을 검증한 뒤 BMC에 로그인하는 방법은 비밀번호를 명령 인수에 넣는 원격 RACADM보다 노출을 줄일 수 있습니다.

```bash
ssh YOUR_BMC_USER@YOUR_BMC_HOST
```

BMC SSH 콘솔에서 지원되는 경우:

```text
racadm serveraction powerstatus
racadm serveraction graceshutdown
racadm serveraction powerup
```

`powerdown`·`powercycle`·`hardreset` 등은 정상 종료와 다를 수 있으므로 장비 문서와 장애 절차를 확인합니다. chassis 관리 장비는 추가 대상 지정 형식이 다를 수 있습니다.

## 5. Wake-on-LAN

NIC·BIOS·전원·스위치·네트워크에서 WOL을 지원하고 활성화한 경우에만 사용합니다. 부팅용 OS NIC의 승인된 MAC을 확인하며 BMC MAC과 혼동하지 않습니다.

```bash
wakeonlan YOUR_CONFIRMED_NIC_MAC
```

브로드캐스트·라우팅과 전원 상태에 따라 도달하지 않을 수 있습니다. 명령을 보냈다는 것만으로 기동 성공을 판단하지 말고 BMC·OS 부팅·서비스를 확인합니다.

## 6. 여러 노드 조작

pdsh 등의 도구가 있더라도 먼저 대상 범위의 `hostname` 같은 읽기 전용 명령으로 대응을 검증합니다. 작업 현황·정상 종료·동시 기동 전력·부팅 서버 부하를 검토하고 작은 묶음으로 적용합니다. 무조건 모든 노드에 강제 종료를 전달하는 예제는 사용하지 않습니다.

참고: [Dell RACADM serveraction](https://www.dell.com/support/manuals/en-us/poweredge-xe8640/idrac9_7.xx_racadm_pub/serveraction?guid=guid-16197034-e2a3-4174-a96d-7dae9afd66aa)
