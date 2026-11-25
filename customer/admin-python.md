# 공유 Python 설치와 Module 제공

기존 시스템 Python을 교체하지 않고 버전별 공유 설치본을 제공하는 절차입니다. OS 관리 도구가 사용하는 Python과 연구용 Python을 분리합니다. Conda로 제공할지 소스 빌드할지 먼저 결정합니다.

## 1. 버전·경로·빌드 환경

지원 중인 Python 릴리스, 사용하는 OS·OpenSSL·컴파일러와 대상 노드의 CPU 범위를 확인합니다. 오래된 Python 3.5 예제는 현재 기본 설치 기준으로 사용하지 않습니다. 아래의 버전·경로 자리표시는 승인된 값으로 바꿉니다.

```bash
PYVER=YOUR_APPROVED_PYTHON_VERSION
PREFIX=/YOUR_SHARED_SOFTWARE_ROOT/python/$PYVER
```

빌드는 부하를 허용한 관리·빌드 서버에서 수행합니다. 특정 CPU의 `-march=native`로 만든 바이너리가 다른 세대 노드에서 실패하지 않는지 확인합니다. 설치 경로는 기존 버전과 분리합니다.

## 2. 빌드 의존성

Enterprise Linux 계열의 패키지 형태입니다. 저장소와 Python 버전에 따라 추가 의존성이 필요할 수 있습니다.

```bash
dnf install gcc make zlib-devel bzip2-devel xz-devel \
  readline-devel sqlite-devel openssl-devel libffi-devel
```

Ubuntu·SUSE 등 다른 배포판에는 해당 배포판의 개발 패키지 이름을 사용합니다. OpenSSL·시스템 라이브러리를 전체 노드에서 임의로 교체하지 않습니다.

## 3. 소스 검증·빌드·설치

```bash
mkdir -p "$HOME/python-build"
cd "$HOME/python-build"
curl -fLO "https://www.python.org/ftp/python/$PYVER/Python-$PYVER.tgz"
sha256sum "Python-$PYVER.tgz"
```

[Python 공식 배포](https://www.python.org/downloads/source/)의 체크섬·검증 절차와 비교한 후 압축을 풉니다.

```bash
tar -xzf "Python-$PYVER.tgz"
cd "Python-$PYVER"
./configure --prefix="$PREFIX" --with-ensurepip=install --enable-shared
make -j2
make test
make altinstall
```

각 단계의 성공을 확인하고 테스트가 실패하면 원인을 검토합니다. 실제 설치 권한은 prefix에만 필요한 범위로 사용합니다. 공유 라이브러리를 사용하면 시험 실행에도 해당 lib 경로가 필요할 수 있습니다. altinstall의 버전 있는 실행파일 이름을 확인하고 시스템 `/usr/bin/python*` 링크를 바꾸지 않습니다.

## 4. Lua Module 파일

Lmod가 제공되는 경우의 파일 형태입니다. 실제 설치 경로·버전을 입력해 현장의 모듈 트리에 `python/YOUR_VERSION.lua`로 저장합니다.

```lua
help([[Shared research Python. Use the versioned executable or a project venv.]])
whatis("Name: Python")
whatis("Version: YOUR_VERSION")
conflict("python")
local root = "/YOUR_SHARED_SOFTWARE_ROOT/python/YOUR_VERSION"
prepend_path("PATH", pathJoin(root, "bin"))
prepend_path("LD_LIBRARY_PATH", pathJoin(root, "lib"))
```

현장이 Tcl 기반 Environment Modules를 사용하면 맞는 형식으로 작성합니다. 모듈 파일은 사용자에게 읽혀야 하며 관리자가 수정합니다. 모듈 캐시는 현장의 Lmod 버전과 정책에 따라 갱신하고 다른 사용자의 캐시를 일괄 삭제하지 않습니다.

## 5. 일반 사용자·노드 검증

```bash
module avail
module show python/YOUR_VERSION
module load python/YOUR_VERSION
command -v YOUR_VERSIONED_PYTHON
YOUR_VERSIONED_PYTHON --version
YOUR_VERSIONED_PYTHON -c 'import ssl, sqlite3, bz2, lzma, ctypes; print(ssl.OPENSSL_VERSION)'
YOUR_VERSIONED_PYTHON -m pip --version
```

설치된 실제 실행파일 이름으로 바꿉니다. 일반 사용자로 여러 노드에서 같은 버전·동적 라이브러리 로드·패키지 import를 확인합니다. 시스템 Python과 개인 Conda 환경이 바뀌지 않았는지도 확인합니다.

개인 패키지는 프로젝트 venv 또는 Conda 환경에 설치하게 합니다. 공용 Python에 모든 사용자의 패키지를 즉흥적으로 추가하지 않습니다. 공용 패키지 변경은 버전·환경 파일·시험 결과를 기록하고 이전 정상 버전을 유지합니다.
