本节开始把 Chapter 10 的 API Automation Framework 应用于真实 REST API. 

我们不会绕过现有架构, 也不会重新创建项目结构. 

继续使用: 

```
Workflow
    ↓
Service Layer
    ↓
API Client
    ↓
HTTP
    ↓
GitHub REST API
```

## Theory

在 Chapter 10 中, 我们使用的是教学 API. 它的目标是解释 HTTP、Endpoint、Payload、Service Layer 和 API Client. 

Chapter 11 开始使用真实 API. 

真实 API 与教学 API 最大的区别是: 

```
真实 API 有正式 Documentation. 
真实 API 有真实 Resource Model. 
真实 API 有真实 Query Parameters. 
真实 API 有真实 Response Payload. 
真实 API 有真实 Rate Limit. 
```

因此本节的目标不是“发送一个 GET Request”. 

而是建立一个业务接口: 

```python
repository_service.collect_user_repositories()
```

让 Workflow 通过业务语义获取 Repository Inventory. 

## Engineering Discussion

GitHub Documentation 中的 Endpoint 是: 

`GET /users/{username}/repos`

这表示: 

>读取某个 User Resource 下的 Repository Collection

但是 Workflow 不应该看到: 

```
GET
/users/{username}/repos
per_page
sort
direction
```

这些属于 Service Layer 与 API Client 之间的细节. 

Workflow 应该只看到: 

```python
repositories = repository_service.collect_user_repositories(
    username="octocat"
)
```

这样 Workflow 面向业务动作, 而不是面向 HTTP. 

## Hands-on Lab

### Step 1: 更新 API Configuration

文件: 

`configs/api.yaml`
内容调整为: 

```yaml
timeout: 10
verify_ssl: true
base_url: "https://api.github.com"

default_headers:
  Accept: "application/vnd.github+json"
  X-GitHub-Api-Version: "2022-11-28"
  User-Agent: "ccie-ei-automation-workbook"

authentication:
  enabled: false
  type: "Bearer"
  token: ""
```

这里没有深入 Authentication. 

因为本节访问的是 GitHub public resource. 

### Step 2: 扩展 API Client Headers

文件: 

`modules/api_client.py`

关键调整是让 _build_headers() 同时读取 default_headers. 

```python
from typing import Any

import requests
from requests import Response

from modules import loader
from modules.logger import logger


config = loader.load_yaml("configs/api.yaml")

DEFAULT_TIMEOUT: int = config["timeout"]
VERIFY_SSL: bool = config["verify_ssl"]
BASE_URL: str = config["base_url"]
DEFAULT_HEADERS: dict[str, str] = config.get("default_headers", {})

AUTH_ENABLED: bool = config["authentication"]["enabled"]
AUTH_TYPE: str = config["authentication"]["type"]
AUTH_TOKEN: str = config["authentication"]["token"]

session = requests.Session()


def _build_headers() -> dict[str, str]:
    """
    Build HTTP request headers from configuration.
    """
    headers = DEFAULT_HEADERS.copy()

    if AUTH_ENABLED and AUTH_TYPE == "Bearer":
        headers["Authorization"] = f"Bearer {AUTH_TOKEN}"

    return headers
```

注意这里仍然保持 Chapter 10 的边界: 

```
API Client 负责 Headers. 
Workflow 不知道 Headers. 
Service 不管理 Authentication. 
```

### Step 3: 新增 GitHub Endpoint

文件: 

`modules/endpoint.py`

增加: 

```python
GITHUB_USER_REPOSITORIES = "/users/{username}/repos"
```

这里使用 {username} 是因为它是 Path Parameter. 

Service Layer 会负责把业务输入映射到 Endpoint. 

### Step 4: 建立 Repository Service

文件: 

`modules/repository_service.py`

```python
from typing import Any

from modules import api_client
from modules import endpoint


RepositorySummary = dict[str, Any]


def _map_repository_payload(payload: dict[str, Any]) -> RepositorySummary:
    """
    Convert GitHub repository payload into internal business object.
    """
    owner = payload.get("owner", {})

    return {
        "name": payload.get("name"),
        "full_name": payload.get("full_name"),
        "owner": owner.get("login"),
        "url": payload.get("html_url"),
        "description": payload.get("description"),
        "language": payload.get("language"),
        "stars": payload.get("stargazers_count", 0),
        "forks": payload.get("forks_count", 0),
        "visibility": payload.get("visibility"),
    }


def collect_user_repositories(
    username: str,
    per_page: int = 10,
) -> list[RepositorySummary] | None:
    """
    Collect public repository summaries for a GitHub user.
    """
    if per_page < 1 or per_page > 100:
        raise ValueError("per_page must be between 1 and 100.")

    repository_endpoint = endpoint.GITHUB_USER_REPOSITORIES.format(
        username=username
    )

    response = api_client.get(
        repository_endpoint,
        params={
            "per_page": per_page,
            "sort": "updated",
            "direction": "desc",
        },
    )

    if response is None:
        return None

    repositories = []

    for item in response.json():
        repositories.append(
            _map_repository_payload(item)
        )

    return repositories
```

### Step 5: 建立 Workflow Script

文件: 

`scripts/collect_repositories.py`

```python
from modules import repository_service


def main() -> None:
    """
    Run the repository inventory collection workflow.
    """
    repositories = repository_service.collect_user_repositories(
        username="octocat",
        per_page=5,
    )

    if repositories is None:
        print("Repository collection failed.")
        return

    for repository in repositories:
        print(
            f"{repository['full_name']} | "
            f"stars={repository['stars']} | "
            f"language={repository['language']}"
        )


if __name__ == "__main__":
    main()
```

运行方式继续保持 Workbook 规范: 

```bash
python3 -m scripts.collect_repositories
```

## Engineering Analysis

这一节新增了一个 Service, 但没有破坏原来的 Framework. 

现在结构是: 

```
scripts/collect_repositories.py
    ↓
modules/repository_service.py
    ↓
modules/endpoint.py
modules/api_client.py
    ↓
GitHub REST API
```

请注意: 

```
repository_service.py 知道 GitHub Repository. 
api_client.py 不知道 GitHub Repository. 
Workflow 不知道 Endpoint. 
```

这正是 Chapter 10 建立的边界. 

Engineering Best Practice

真实 API 集成时, 应保持: 

- Path Parameter 由 Service 映射. 

- Query Parameters 由 Service 决定. 

- Headers 由 API Client 构造. 

- Base URL 来自 Configuration. 

- Response Payload 由 Service 转换为 Business Object. 

- Workflow 只调用业务接口. 

## Engineering Insight

本节真正完成的是: 

```
External API Model
    ↓
Service Mapping
    ↓
Internal Business Object
```
GitHub 返回的是 GitHub 的数据模型. 

Workbook 需要的是 Automation Platform 的业务对象. 

Service Layer 的价值就在于隔离这两者. 

## Engineering Checklist

完成本节后, 应能够回答: 

- 为什么不在 Workflow 中调用 GitHub Endpoint? 

- 为什么 Path Parameter 应由 Service 处理? 

- 为什么 Headers 不属于 Service? 

- 为什么 Response Payload 需要映射成 Business Object? 

- 为什么 api_client.py 不应该知道 Repository? 

- 这个设计如何延续 Chapter 10 的 Layered Architecture? 

## Summary

本节完成了第一个真实 REST API Service Extension. 
我们没有重新设计项目结构, 而是在现有 Framework 中增加 repository_service.py, 并通过 GitHub REST API 获取真实 Repository 数据. 