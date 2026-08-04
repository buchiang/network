到这里, 我们已经完成了:

- GitHub Repository Service

- Nested JSON Processing

- Filtering

- Sorting

- Pagination

接下来需要处理真实 API 自动化中非常容易被忽略的问题:

>Data Validation

GitHub Repository API 的 response schema 中包含大量字段, 例如 `name`, `full_name`, `owner`, `html_url`, `language`, `forks_count`, `stargazers_count`, `visibility`, `created_at`, `updated_at` 等. 文档也说明部分字段可能是 null, 例如示例中的 language. 

## Theory

很多初学者认为:

```python
response.json()
```

成功以后, 数据就可以直接使用. 在企业自动化中, 这不够. 因为真实 API 数据可能存在以下情况:

- 字段不存在

- 字段值为 None

- 字段类型不符合预期

- 字段名称发生变化

- 返回空列表

- 返回的数据不是业务需要的数据

因此, 在把 API Payload 转换成 Business Object 之前, Service Layer 应该验证数据是否满足最低业务要求. 

## Engineering Discussion

例如 GitHub Repository Payload 中:

```python
payload["owner"]["login"]
```

看起来很自然, 但是如果 owner 不存在, 程序会失败. 

如果 owner 是 None, 程序也会失败. 

如果 owner 存在但没有 login, Workflow 拿到的 Business Object 就是不完整的. 

所以真实 API 自动化不能只做 Mapping, 还要做 Validation. 

数据流应该变成:

```
Response Payload
    ↓
Data Validation
    ↓
Response Mapping
    ↓
Business Object
    ↓
Workflow
```

## Hands-on Lab

继续修改:

`modules/repository_service.py`

先定义 Repository Summary 需要的最低字段. 

```python
REQUIRED_REPOSITORY_FIELDS = [
    "name",
    "full_name",
    "owner",
    "html_url",
]
```

新增验证函数:

```python
def _validate_repository_payload(payload: dict[str, Any]) -> bool:
    """
    Validate the minimum required GitHub repository payload fields.
    """
    for field in REQUIRED_REPOSITORY_FIELDS:
        if field not in payload:
            return False

    owner = payload.get("owner")

    if not isinstance(owner, dict):
        return False

    if "login" not in owner:
        return False

    return True
```

然后在 Mapping 前使用它:

```python
def _map_repository_payload(payload: dict[str, Any]) -> RepositorySummary | None:
    """
    Convert GitHub repository payload into an internal repository summary.
    """
    if not _validate_repository_payload(payload):
        return None

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
```

最后在分页函数中跳过无效数据:

```python
for item in payload:
    repository = _map_repository_payload(item)

    if repository is None:
        continue

    repositories.append(repository)
```

完整片段:

```python
repositories = []

for item in payload:
    repository = _map_repository_payload(item)

    if repository is None:
        continue

    repositories.append(repository)

return repositories
```

为什么不是直接 raise Error?

这里有一个工程取舍. 如果一个 repository payload 不完整, 有两种处理方式:

```
Fail Fast
Skip Invalid Item
```

Fail Fast:

>发现一条数据异常, 整个 Workflow 停止. 

Skip Invalid Item:

>跳过异常数据, 继续处理其他数据. 

在本节中, 我们使用 Skip Invalid Item. 

原因是当前业务目标是:

>Collect Repository Inventory

如果某一条数据不符合最低要求, 不应该影响其他 repository 的收集. 

但是在更高风险场景中, 例如:

- Create Device

- Update Policy

- Deploy Configuration

则应优先考虑 Fail Fast. 

### Validation 应该放在哪一层?

不要放在 Workflow. 

错误设计:

```python
for repository in repositories:
    if repository["owner"] is None:
        continue
```

这表示 Workflow 开始理解数据质量规则. 

正确设计:

```
Service Layer
    ↓
Validate Payload
    ↓
Map Business Object
    ↓
Return Clean Data
```

Workflow 应该拿到已经整理过的数据. 

## Engineering Analysis

Data Validation 与 Response Mapping 是两个不同职责. 

Validation 回答:

这条数据是否可以使用?

Mapping 回答:

如何把外部字段转换成内部字段?

虽然它们都在 Service Layer 中完成, 但是最好拆成两个函数:

```python
_validate_repository_payload()
_map_repository_payload()
```

这符合 Single Responsibility Principle. 

每个函数只做一件事. 

## Engineering Best Practice

企业项目中处理真实 API 数据时, 建议:

- 不假设 API Payload 一定完整. 

- 不假设 nested JSON 一定存在. 

- 在 Mapping 前进行最低字段验证. 

- Validation 和 Mapping 拆成独立函数. 

- Workflow 只接收已经验证和整理过的 Business Object. 

- 根据业务风险选择 Fail Fast 或 Skip Invalid Item. 

- 对写操作、变更操作、合规判断优先 Fail Fast. 

- 对 Inventory Collection、Report Collection 可考虑 Skip Invalid Item. 

## Engineering Insight

真实 API 自动化的核心难点, 不是 HTTP Request, 而是数据质量. 

企业自动化程序通常不是因为不会发送请求而失败, 而是因为:

- 假设字段永远存在

- 假设类型永远正确

- 假设返回永远符合文档

- 假设所有数据都能直接用于业务

Validation 的目的不是让代码更复杂, 而是保护 Workflow 不被外部数据污染. 

这也是 Business 与 Infrastructure 解耦的一部分:

- 外部 API 可以复杂. 

- Service Layer 负责吸收复杂性. 

- Workflow 只处理可信业务对象. 

## Engineering Checklist

完成本节后, 应能够回答:

- 为什么真实 API 数据需要 Validation?

- Validation 与 Mapping 有什么区别?

- 为什么不应在 Workflow 中做 Payload Validation?

- 什么情况下适合 Fail Fast?

- 什么情况下可以 Skip Invalid Item?

- 为什么 nested JSON 需要额外验证?

- Data Validation 如何保护 Business Object 的稳定性?

## Summary

本节完成了真实 API 数据使用前的 Validation 设计. 

我们在 `repository_service.py` 中增加 `_validate_repository_payload()`, 并在 Mapping 前检查最低字段要求, 避免 Workflow 接触不完整或不可信的外部 Payload. 