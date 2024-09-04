import requests
import importlib_metadata as metadata

def check_latest_version(package_name):
    url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        latest_version = response.json()["info"]["version"]
        return latest_version
    except requests.RequestException:
        print("최신 버전 정보를 확인할 수 없습니다.")
        return None

def notify_if_new_version(package_name):
    try:
        installed_version = importlib.metadata.version(package_name)
        latest_version = check_latest_version(package_name)

        if latest_version and installed_version != latest_version:
            print(f"새 버전이 있습니다! (현재 버전: {installed_version}, 최신 버전: {latest_version})")
        else:
            print(f"현재 최신 버전을 사용 중입니다. (버전: {installed_version})")
    except importlib.metadata.PackageNotFoundError:
        print(f"{package_name} 패키지가 설치되어 있지 않습니다.")
