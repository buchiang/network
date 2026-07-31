## Theory

Chapter 10 已经讨论过: 

>Response Payload != Business Object

真实 API 会让这个问题更加明显. 

GitHub Repository Payload 中不仅有第一层字段: 

```
name
full_name
html_url
description
language
stargazers_count
forks_count
visibility
```

还有 nested JSON: 

```
owner.login
owner.html_url
owner.type
```

也就是说, API 返回的数据不是简单的一层 Dictionary, 而是多层结构. 

## Engineering Discussion

很多初学者会在 Workflow 中这样写: 

```python
print(repository["owner"]["login"])
```

这能够运行, 但是设计不正确, 因为 Workflow 开始知道 GitHub Payload 的内部结构. 

如果未来 GitHub 返回结构变化, 或者我们换成另一个 Git 平台 API, 所有 Workflow 都可能需要修改. 

正确边界仍然是: 

```
Workflow
    ↓
Business Object
    ↓
Service Layer
    ↓
Response Payload
```

Nested JSON 解析属于 Service Layer. 

## Hands-on Lab

继续使用上一节的文件: 

`modules/repository_service.py`

重点改进 _map_repository_payload(). 

```python
from typing import Any

from modules import api_client
from modules import endpoint


RepositorySummary = dict[str, Any]


def _map_repository_payload(payload: dict[str, Any]) -> RepositorySummary:
    """
    Convert GitHub repository payload into an internal repository summary.
    """
    owner = payload.get("owner") or {}

    return {
        "name": payload.get("name"),
        "full_name": payload.get("full_name"),
        "owner": owner.get("login"),
        "owner_url": owner.get("html_url"),
        "url": payload.get("html_url"),
        "description": payload.get("description"),
        "language": payload.get("language"),
        "stars": payload.get("stargazers_count", 0),
        "forks": payload.get("forks_count", 0),
        "visibility": payload.get("visibility"),
        "default_branch": payload.get("default_branch"),
        "created_at": payload.get("created_at"),
        "updated_at": payload.get("updated_at"),
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
            "type": "owner",
            "sort": "updated",
            "direction": "desc",
            "per_page": per_page,
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

Workflow 仍然不变: 

```python
from modules import repository_service


repositories = repository_service.collect_user_repositories(
    username="octocat",
    per_page=5,
)

for repository in repositories:
    print(repository["full_name"])
```

## Engineering Analysis

这里最重要的不是 `.get()`. 最重要的是字段所有权. 

GitHub Payload 字段属于外部系统: 

```
owner.login
html_url
stargazers_count
forks_count
```

Workbook 内部 Business Object 字段属于自动化平台: 

```
owner
owner_url
url
stars
forks
```

两者不必完全一样. 
Service Layer 的职责就是完成这种转换. 

## Engineering Best Practice

- 处理 nested JSON 时, 建议遵守: 

- 不在 Workflow 中访问 nested JSON. 

- 不直接假设 nested object 一定存在. 

- 使用 Service Layer 做 Response Mapping. 

- 将外部字段名转换成内部业务字段名. 

- Workflow 只使用稳定的 Business Object. 

- Mapping 函数保持单一职责, 只负责一个 Payload 到一个 Business Object 的转换. 

## Engineering Insight

Nested JSON 是真实 API 与教学 API 的重要区别. 

教学 API 通常结构简单. 

真实企业 API 通常结构复杂, 并且经常包含平台内部字段、权限字段、链接字段、状态字段和嵌套对象. 

如果 Workflow 直接解析这些结构, 整个项目会被外部 API 数据模型绑定. 

Service Layer 的价值就是: 

>隐藏外部复杂性, 提供内部稳定性. 

## Engineering Checklist

完成本节后, 应能够回答: 

- 什么是 nested JSON? 

- 为什么 Workflow 不应访问 owner.login? 

- 为什么 Service Layer 应负责 nested JSON 解析? 

- External API Model 与 Internal Business Object 有什么区别? 

- 为什么 Mapping 函数应保持单一职责? 

- GitHub Payload 字段变化时, 应该优先修改哪一层? 

## Summary

本节完成了真实 API Response 中 nested JSON 的工程处理. 

我们没有让 Workflow 依赖 GitHub Payload, 而是通过 repository_service.py 将复杂 Response Payload 转换成稳定的 Repository Business Object. 