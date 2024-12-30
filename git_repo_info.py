from datetime import datetime
import requests

def get_github_repo_info(owner, repo_name):
    base_url = "https://api.github.com/repos"
    commits_url = f"https://api.github.com/repos/{owner}/{repo_name}/commits"
    
    # 날짜 형식 변환 함수
    def format_datetime(iso_datetime):
        try:
            dt_object = datetime.strptime(iso_datetime, "%Y-%m-%dT%H:%M:%SZ")
            # 날짜와 시간 사이에 '/' 추가
            return dt_object.strftime("%Y-%m-%d / %H:%M:%S")
        except ValueError:
            return "N/A"
    
    try:
        # 저장소 정보 가져오기
        repo_response = requests.get(f"{base_url}/{owner}/{repo_name}")
        repo_response.raise_for_status()
        repo_data = repo_response.json()

        # 저장소 생성일 및 최근 업데이트
        created_at = format_datetime(repo_data.get("created_at", "N/A"))
        updated_at = format_datetime(repo_data.get("updated_at", "N/A"))
        
        # 전체 커밋 목록 가져오기
        commits_response = requests.get(commits_url)
        commits_response.raise_for_status()
        commits_data = commits_response.json()

        if commits_data:
            first_commit = commits_data[-1]
            last_commit = commits_data[0]
            
            first_commit_date = format_datetime(first_commit["commit"]["committer"]["date"])
            last_commit_date = format_datetime(last_commit["commit"]["committer"]["date"])
            
            total_commits = len(commits_data)
        else:
            first_commit_date = "N/A"
            last_commit_date = "N/A"
            total_commits = 0
        
        # 출력
        print(f"----------")
        print(f"소유자명: {owner}")
        print(f"저장소명: {repo_name}")
        print(f"----------")
        print(f"저장소 생성일: {created_at}")
        print(f"첫 커밋 일시: {first_commit_date}")
        print(f"총 커밋 수: {total_commits}")
        print(f"최근 커밋 일시: {last_commit_date}")
        print(f"최근 업데이트: {updated_at}")
    
    except requests.exceptions.RequestException as e:
        print(f"에러 발생: {e}")

if __name__ == "__main__":
    owner = input("소유자명을 입력하세요: ").strip()
    repo_name = input("저장소명을 입력하세요: ").strip()
    get_github_repo_info(owner, repo_name)
