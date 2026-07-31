到这里, 我们已经完成了: 

GitHub Repository Service

Nested JSON Processing

Filtering

Sorting

Query Parameters Validation

接下来进入真实 API 中非常重要的一部分: 
Pagination

GitHub REST API 对大量结果会进行分页. GitHub 文档说明, 当 REST API Response 包含很多结果时, GitHub 会返回一部分结果, 并通过 link response header 提供后续页面信息；如果 Endpoint 支持 per_page, 可以控制每页返回数量. List repositories for a user 也支持 per_page 和 page 参数. 

## Theory

Chapter 10 已经介绍过 Pagination 的基本思想: 

```
一个业务操作
    ↓
可能对应多个 HTTP Request
```

例如 Workflow 希望: 

```python
repositories = repository_service.collect_user_repositories(
    username="octocat"
)
```

但是真实 API 可能不会一次返回所有 repositories. 

实际通信可能是: 

```
GET /users/octocat/repos?page=1&per_page=30
GET /users/octocat/repos?page=2&per_page=30
GET /users/octocat/repos?page=3&per_page=30
```

Workflow 不应该知道这些 page number. 
分页属于 Service Layer 的职责. 

## Engineering Discussion

为什么 Pagination 不放在 Workflow?

错误设计: 

```python
page = 1

while True: 
    repositories = repository_service.collect_user_repositories(
        username="octocat",
        page=page
    )

    if not repositories: 
        break

    page += 1
```

这段代码的问题是: 

>Workflow 开始知道 API 分页规则. 

正确设计应该是: 

```python
repositories = repository_service.collect_all_user_repositories(
    username="octocat"
)
```

Workflow 只表达业务目标: 

>Collect all repositories.

至于需要请求几页, 由 Service Layer 处理. 

## Hands-on Lab

继续修改: 

`modules/repository_service.py`

先保留前面已经完成的 Mapping 和 Validation. 

新增一个内部函数: 

```python
def _build_repository_query(
    repository_type:  str,
    sort:  str,
    direction:  str,
    per_page:  int,
    page:  int,
) -> dict[str, object]: 
    """
    Build GitHub repository query parameters.
    """
    return {
        "type":  repository_type,
        "sort":  sort,
        "direction":  direction,
        "per_page":  per_page,
        "page":  page,
    }
```

然后新增完整分页 Service: 

```python
def collect_all_user_repositories(
    username:  str,
    repository_type:  str = "owner",
    sort:  str = "updated",
    direction:  str = "desc",
    per_page:  int = 30,
    max_pages:  int = 5,
) -> list[RepositorySummary] | None: 
    """
    Collect repository summaries from multiple GitHub result pages.
    """
    _validate_repository_query(
        repository_type=repository_type,
        sort=sort,
        direction=direction,
        per_page=per_page,
    )

    if max_pages < 1: 
        raise ValueError("max_pages must be greater than 0.")

    repository_endpoint = endpoint.GITHUB_USER_REPOSITORIES.format(
        username=username
    )

    repositories = []

    for page in range(1, max_pages + 1): 
        params = _build_repository_query(
            repository_type=repository_type,
            sort=sort,
            direction=direction,
            per_page=per_page,
            page=page,
        )

        response = api_client.get(
            repository_endpoint,
            params=params,
        )

        if response is None: 
            return None

        payload = response.json()

        if not payload: 
            break

        for item in payload: 
            repositories.append(
                _map_repository_payload(item)
            )

        if len(payload) < per_page: 
            break

    return repositories
```

Workflow 变成:

```python
from modules import repository_service


repositories = repository_service.collect_all_user_repositories(
    username="octocat",
    repository_type="owner",
    sort="updated",
    direction="desc",
    per_page=30,
    max_pages=3,
)

if repositories is None: 
    print("Repository collection failed.")

else: 
    for repository in repositories: 
        print(repository["full_name"])
```

为什么增加 max_pages?

很多人会问:

为什么不一直请求到没有数据?

在真实企业 API 中, 自动化程序必须有边界.

例如:

```python
per_page=100
max_pages=10
```

- 表示最多收集 1000 条记录.

- 这样可以避免:

- API 返回异常导致无限循环

- 大量请求触发 Rate Limit

- Workflow 运行时间不可控

- 输出文件过大

- 调试困难

企业自动化不是“尽可能多地请求”.

而是:

>在明确边界内获取业务需要的数据.

### Page Parameter 与 Link Header

GitHub 支持 page 和 per_page 参数.

同时, GitHub 也会在分页 Response 中使用 link header 指向 next, prev, first, last 页面.

在本 Workbook 当前阶段, 我们先使用:

```python
params={
    "page":  page,
    "per_page":  per_page
}
```

原因是它与 Chapter 10 已建立的 `api_client.get(endpoint, params=params)` 完全一致.

Link Header 是真实 API 中非常重要的机制, 但它涉及 Response Header 解析和通用 Pagination Helper. 为了不破坏当前章节知识边界, 本节先不扩展为通用 Link Header Pagination Engine.

## Engineering Analysis

本节代码中, API Client 仍然只负责一次 HTTP Request:

```python
api_client.get(endpoint, params=params)
```

Service Layer 负责决定:

```
请求第几页
每页多少条
什么时候停止
如何合并结果
如何转换 Business Object
```

Workflow 完全不知道:

```
page
per_page
HTTP Request 次数
Response Payload 合并过程
```

这正是 Chapter 10 的原则:

```
API Client 负责通信. 
Service 负责业务语义和数据适配. 
Workflow 只负责编排业务流程. 
```

## Engineering Best Practice

- 处理真实 API Pagination 时, 建议:

- 不在 Workflow 中处理 page number.

- 不在 Workflow 中合并多页结果.

- 不让 API Client 自动决定是否翻页.

- 在 Service Layer 中设置 max_pages 这样的执行边界.

- 每一页 Response 都转换为相同 Business Object.

- 对空 Payload 或不足一页的数据进行停止判断.

- 对真实生产 API, 后续可根据 Link Header 建立通用 Pagination Utility.

## Engineering Insight

Pagination 再次说明:

HTTP Request 不等于 Business Action.

一个业务动作:

Collect all repositories.

可能对应:

```
HTTP Request 1
HTTP Request 2
HTTP Request 3
```

但是 Workflow 不应该因此变复杂. 

Service Layer 的价值, 就是把多个通信动作包装成一个稳定业务能力. 

这也是企业 API Automation Framework 与普通脚本的区别. 

普通脚本关心: 

下一页怎么请求?

企业框架关心: 

```
业务接口是否稳定?
分页复杂性是否被隔离?
Workflow 是否仍然清晰?
```

## Engineering Checklist

完成本节后, 应能够回答: 

- 为什么真实 API 通常需要 Pagination?

- 为什么 Pagination 不应放在 Workflow?

- 为什么 API Client 不应自动获取所有页面?

- page 与 per_page 分别控制什么?

- 为什么企业代码需要 max_pages?

- 多页 Response 应该在哪一层合并?

- Pagination 如何体现一个 Business Action 对应多个 HTTP Request?

## Summary

本节完成了真实 API Resource 的 Pagination 设计. 

我们在 `repository_service.py` 中新增 `collect_all_user_repositories()`，让 Service Layer 负责 page 参数、请求循环、停止条件、结果合并和 Response Mapping. 

Workflow 仍然只调用一个业务接口, 不接触任何分页细节. 