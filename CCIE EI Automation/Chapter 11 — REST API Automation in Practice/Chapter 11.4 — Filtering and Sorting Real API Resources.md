到这里, 我们已经完成了: 

- 读取真实 API Documentation

- 建立 GitHub Repository Service

- 处理 nested JSON

- 将 GitHub Payload 转换为 Business Object

接下来进入真实 REST API 中非常常见的能力:

>Filtering 与 Sorting

GitHub `List repositories for a user` Endpoint 支持 `type`, `sort`, `direction`, `per_page`, `page` 等 Query Parameters. `type` 可用于限制 repository 类型，`sort` 可按照 `created`, `updated`, `pushed`, `full_name` 排序，`direction` 可使用 `asc` 或 `desc`. 

## Theory

Chapter 10 已经介绍过 Query Parameters, 但是 Chapter 10 使用的是教学 API. 

Chapter 11 面对的是真实 API.

真实 API 的 Query Parameters 通常有明确限制:

```
type      -> all / owner / member
sort      -> created / updated / pushed / full_name
direction -> asc / desc
per_page  -> max 100
page      -> page number
```

这意味着 Service Layer 不能随便把 Workflow 的输入直接传给 API. 

Service Layer 应该先做业务输入验证, 再构造 Query Parameters. 

## Engineering Discussion

错误设计: 

```python
repositories = repository_service.collect_user_repositories(
    username="octocat",
    sort="anything",
    direction="random"
)
```

如果 Service 不检查这些参数, 错误会一直传到 GitHub API. 

然后 Workflow 只看到 API 调用失败, 但是不知道失败原因来自业务输入. 

正确设计是: 

```
Workflow Input
    ↓
Service Validation
    ↓
Query Parameters
    ↓
API Client
    ↓
HTTP Request
```

也就是说, Filtering 和 Sorting 虽然最终表现为 Query Parameters, 但是它们首先是业务条件. 

## Hands-on Lab

继续修改: 
`modules/repository_service.py`

增加允许值: 

```python
VALID_REPOSITORY_TYPES = ["all", "owner", "member"]

VALID_SORT_FIELDS = ["created", "updated", "pushed", "full_name"]

VALID_DIRECTIONS = ["asc", "desc"]
```

完整 Service 设计: 

```python
from typing import Any

from modules import api_client
from modules import endpoint


RepositorySummary = dict[str, Any]

VALID_REPOSITORY_TYPES = ["all", "owner", "member"]
VALID_SORT_FIELDS = ["created", "updated", "pushed", "full_name"]
VALID_DIRECTIONS = ["asc", "desc"]


def _map_repository_payload(payload:  dict[str, Any]) -> RepositorySummary: 
    """
    Convert GitHub repository payload into an internal repository summary.
    """
    owner = payload.get("owner") or {}

    return {
        "name":  payload.get("name"),
        "full_name":  payload.get("full_name"),
        "owner":  owner.get("login"),
        "owner_url":  owner.get("html_url"),
        "url":  payload.get("html_url"),
        "description":  payload.get("description"),
        "language":  payload.get("language"),
        "stars":  payload.get("stargazers_count", 0),
        "forks":  payload.get("forks_count", 0),
        "visibility":  payload.get("visibility"),
        "default_branch":  payload.get("default_branch"),
        "created_at":  payload.get("created_at"),
        "updated_at":  payload.get("updated_at"),
    }


def _validate_repository_query(
    repository_type:  str,
    sort:  str,
    direction:  str,
    per_page:  int,
) -> None: 
    """
    Validate repository query options before sending the API request.
    """
    if repository_type not in VALID_REPOSITORY_TYPES: 
        raise ValueError("repository_type must be all, owner, or member.")

    if sort not in VALID_SORT_FIELDS: 
        raise ValueError("sort must be created, updated, pushed, or full_name.")

    if direction not in VALID_DIRECTIONS: 
        raise ValueError("direction must be asc or desc.")

    if per_page < 1 or per_page > 100: 
        raise ValueError("per_page must be between 1 and 100.")


def collect_user_repositories(
    username:  str,
    repository_type:  str = "owner",
    sort:  str = "updated",
    direction:  str = "desc",
    per_page:  int = 10,
) -> list[RepositorySummary] | None: 
    """
    Collect public repository summaries for a GitHub user.
    """
    _validate_repository_query(
        repository_type=repository_type,
        sort=sort,
        direction=direction,
        per_page=per_page,
    )

    repository_endpoint = endpoint.GITHUB_USER_REPOSITORIES.format(
        username=username
    )

    params = {
        "type":  repository_type,
        "sort":  sort,
        "direction":  direction,
        "per_page":  per_page,
    }

    response = api_client.get(
        repository_endpoint,
        params=params,
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

Workflow 可以这样调用: 

```python
from modules import repository_service


repositories = repository_service.collect_user_repositories(
    username="octocat",
    repository_type="owner",
    sort="updated",
    direction="desc",
    per_page=5,
)

for repository in repositories: 
    print(
        f"{repository['full_name']} "
        f"{repository['updated_at']}"
    )
```

Filtering 的位置

请注意 `repository_type="owner"` 是业务表达. 

而真正发送给 HTTP 的是: 

```python
params = {
    "type":  "owner"
}
```

因此: 

```
Workflow 表达业务条件
Service 转换为 Query Parameters
API Client 负责发送
```

Workflow 不应该自己写: 

```python
"?  type=owner&sort=updated&direction=desc"
```

Sorting 的位置

Sorting 也是一样. 

Workflow 可以表达: 

```python
sort="updated"
direction="desc"
```

但是 Workflow 不应该关心最终 URL 是否变成: 

`/users/octocat/repos?  sort=updated&direction=desc`

这是 HTTP 表达方式, 属于 API Client 和 requests 的职责. 

## Engineering Analysis

这一节看起来只是增加了几个参数. 

实际上它完成了一个重要变化: 

```
固定查询
    ↓
可配置业务查询
```

但是这种可配置不能失控. 

如果 Service 允许任意字符串进入 API, 那么 Service 就只是一个薄包装, 没有真正承担业务边界. 

成熟的 Service Layer 应该同时负责: 

- 暴露业务接口

- 验证业务输入

- 构造 Query Parameters

- 调用 API Client

- 映射 Response Payload

这就是 Service Layer 不只是“调用 API”的原因. 

## Engineering Best Practice

企业项目中处理 Filtering 和 Sorting 时, 建议: 

- 不在 Workflow 中拼接 Query String. 

- 不让 API Client 决定业务过滤条件. 

- 在 Service Layer 中验证允许值. 

- 使用 params 传递 Query Parameters. 

- 为 Service 参数设置安全默认值. 

- 只暴露业务需要的过滤和排序能力, 不盲目暴露 API 支持的所有参数. 

## Engineering Insight

真实 API 通常会提供很多 Query Parameters. 

但是企业自动化平台不应该把所有 API 参数原样暴露给 Workflow. 

因为那样 Workflow 仍然是在面向 Vendor API 编程. 

更好的设计是: 

```
Vendor Query Parameters
    ↓
Service Interface
    ↓
Business Options
```

也就是说, Service Layer 应该把外部 API 能力整理成内部业务能力. 

这也是 Chapter 11 与 Chapter 10 的区别: 

Chapter 10 建立 Framework. 

Chapter 11 开始使用 Framework 管理真实 API 的复杂性. 

## Engineering Checklist

完成本节后, 应能够回答: 

- Filtering 与 Query Parameters 有什么关系?  

- Sorting 为什么也属于 Service Layer 的设计范围?  

- 为什么 Service 需要验证 type, sort, direction?  

- 为什么不应把 GitHub 支持的所有参数直接暴露给 Workflow?  

- Workflow 为什么不应拼接 Query String?  

- Filtering 和 Sorting 如何体现 Business 与 Infrastructure 解耦?  

## Summary

本节完成了真实 API Resource 的 Filtering 与 Sorting 设计. 

我们将 GitHub 的 Query Parameters 转换成 repository_service.

collect_user_repositories() 的业务参数, 并在 Service Layer 中完成输入验证和参数映射. 