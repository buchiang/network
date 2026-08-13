## Theory

Resource Collection 与 Resource Instance

REST API 通常包含两类读取操作. 

Resource Collection: 
`GET /users/octocat/repos`

返回: 

```json
[
    {
        "name": "Hello-World"
    },
    {
        "name": "Spoon-Knife"
    }
]
```

Resource Instance: 
`GET /repos/octocat/Hello-World`

返回: 

```json
{
    "name": "Hello-World",
    "full_name": "octocat/Hello-World"
}
```

两者的业务语义不同: 

```
Collection Interface
    ↓
Find or collect multiple resources
```

```
Detail Interface
    ↓
Inspect one identified resource
```

因此 Service Interface 也应该明确区分: 
`collect_user_repositories()`

与: 


`get_repository_detail()`

Workflow 不应该通过返回类型猜测当前操作是 Collection 还是 Detail. 

## Engineering Discussion

为什么不能让 Workflow 构建 URI

错误设计: 

```python
repository_endpoint = (
    f"/repos/{owner}/{repository_name}"
)

response = api_client.get(repository_endpoint)
```

这会让 Workflow 依赖: 

- GitHub URI Design

- Path Parameter Name

- API Client

- HTTP Response

- External Payload

正确设计: 

```python
repository = repository_service.get_repository_detail(
    owner=owner,
    repository_name=repository_name,
)
```

Workflow 只表达 Business Intent: 

>Get Repository Detail

### Summary 与 Detail 应该使用相同 Mapper 吗

Collection Payload 和 Detail Payload 包含很多相同字段: 

- `name`

- `full_name`

- `owner`

- `description`

- `language`

- `stargazers_count`

- `forks_count`

- `visibility`

- `default_branch`

如果 Detail Mapper 重新映射所有字段, 就会产生重复代码. 

正确策略是: 

```
Summary Mapper
    ↓
Common Business Fields
    ↓
Detail Mapper adds Detail Fields
```

这符合 DRY, 同时保持两个 Business Interface 的语义区别. 

## Hands-on Lab

### Step 1: 扩展 Endpoint Configuration

打开: `modules/endpoint.py`

增加: 

```python
GITHUB_REPOSITORY_DETAIL = (
    "/repos/{owner}/{repository_name}"
)
```

现在 Endpoint Module 同时管理: 

```python
GITHUB_USER_REPOSITORIES = "/users/{username}/repos"

GITHUB_REPOSITORY_DETAIL = (
    "/repos/{owner}/{repository_name}"
)
```

Endpoint Module 只负责 URI Template, 它不发送 Request, 也不处理 Payload. 

### Step 2: 定义 Detail Business Object

在: `modules/repository_service.py`

保留已有类型: 

```python
from typing import Any


RepositorySummary = dict[str, Any]
```

增加: 

```python
RepositoryDetail = dict[str, Any]
```

当前使用两个名称表达不同业务语义, 虽然底层结构都是 Dictionary, 但调用者可以清楚地区分: 

```
RepositorySummary
RepositoryDetail
```

### Step 3: 验证 Path Parameter

新增: 

```python
def _normalize_resource_identifier(
    value: str,
    field_name: str,
) -> str:
    """
    Validate and normalize one URI resource identifier.

    Args:
        value: Resource identifier supplied by the caller.
        field_name: Business field name used in error messages.

    Returns:
        Normalized resource identifier.

    Raises:
        ValueError: If the identifier is empty or contains a slash.
    """
    normalized_value = value.strip()

    if not normalized_value:
        raise ValueError(
            f"{field_name} must not be empty."
        )

    if "/" in normalized_value:
        raise ValueError(
            f"{field_name} must not contain '/'."
        )

    return normalized_value
```

这里没有让 Workflow 自己验证 URI. 

因为 `owner` 和 `repository_name` 是 Service Interface 的输入, 输入边界应该由 Service Layer 保护. 

同时拒绝 `/`, 防止一个 Path Parameter 意外改变 URI Structure. 

### Step 4: 验证 Detail Payload

增加 Detail Resource 的必需字段: 

```python
REQUIRED_REPOSITORY_DETAIL_FIELDS = {
    "id",
    "private",
    "fork",
    "archived",
    "disabled",
    "topics",
    "clone_url",
    "ssh_url",
}
```

新增验证函数: 

```python
def _validate_repository_detail_payload(
    payload: dict[str, Any],
) -> bool:
    """
    Validate fields required by a Repository Detail Resource.

    Args:
        payload: Raw Repository Detail Payload.

    Returns:
        True when the Detail Payload satisfies its Contract.
    """
    missing_fields = (
        REQUIRED_REPOSITORY_DETAIL_FIELDS - payload.keys()
    )

    if missing_fields:
        return False

    if not isinstance(payload["id"], int):
        return False

    boolean_fields = (
        "private",
        "fork",
        "archived",
        "disabled",
    )

    for field_name in boolean_fields:
        if not isinstance(payload[field_name], bool):
            return False

    if not isinstance(payload["topics"], list):
        return False

    if not isinstance(payload["clone_url"], str):
        return False

    if not isinstance(payload["ssh_url"], str):
        return False

    return True
```

Summary Validation 与 Detail Validation 各自保护自己的 Contract: 

```
Summary Required Fields
    +
Detail Required Fields
```

Step 5: 处理 Nullable License Object

Repository Payload 中的 license 可能是 Nested Object, 也可能是 null. 

新增: 

```python
def _map_license_name(
    payload: dict[str, Any],
) -> str | None:
    """
    Extract the license name from a Repository Payload.

    Args:
        payload: Raw Repository Payload.

    Returns:
        License name when available, otherwise None.
    """
    license_payload = payload.get("license")

    if not isinstance(license_payload, dict):
        return None

    license_name = license_payload.get("name")

    if not isinstance(license_name, str):
        return None

    return license_name
```

不要直接执行: 

```python
payload["license"]["name"]
```

因为下面的 Payload 是合法的: 

```json
{
    "license": null
}
```

Service Layer 必须吸收这种 External Schema 复杂度. 

Workflow 最终只看到: 

```python
"license": None
```

或: 

```python
"license": "MIT License"
```

### Step 6: 建立 Detail Mapper

新增: 

```python
def _map_repository_detail_payload(
    payload: dict[str, Any],
) -> RepositoryDetail | None:
    """
    Map a raw Repository Detail Payload to a Business Object.

    Args:
        payload: Raw Repository Detail Payload.

    Returns:
        Repository Detail Business Object when valid,
        otherwise None.
    """
    repository_summary = _map_repository_payload(payload)

    if repository_summary is None:
        return None

    if not _validate_repository_detail_payload(payload):
        return None

    topics = [
        topic
        for topic in payload["topics"]
        if isinstance(topic, str)
    ]

    return {
        **repository_summary,
        "repository_id": payload["id"],
        "is_private": payload["private"],
        "is_fork": payload["fork"],
        "archived": payload["archived"],
        "disabled": payload["disabled"],
        "topics": topics,
        "license": _map_license_name(payload),
        "clone_url": payload["clone_url"],
        "ssh_url": payload["ssh_url"],
        "pushed_at": payload.get("pushed_at"),
    }
```

这里使用: 

```python
**repository_summary
```

复用已有 Summary Mapping. 

Detail Mapper 只增加 Detail Resource 特有字段. 

完整关系为: 

```
Raw Detail Payload
    ↓
Summary Validation and Mapping
    ↓
Detail Validation
    ↓
Detail Field Mapping
    ↓
Repository Detail Business Object
```

### Step 7: 建立 Business Service Interface

在 repository_service.py 中增加: 

```python
def get_repository_detail(
    owner: str,
    repository_name: str,
) -> RepositoryDetail | None:
    """
    Retrieve one Repository Detail Business Object.

    Args:
        owner: Repository owner account.
        repository_name: Repository name without the .git suffix.

    Returns:
        Repository Detail Business Object when successful,
        otherwise None.

    Raises:
        ValueError: If a resource identifier is invalid.
    """
    normalized_owner = _normalize_resource_identifier(
        value=owner,
        field_name="owner",
    )

    normalized_repository_name = (
        _normalize_resource_identifier(
            value=repository_name,
            field_name="repository_name",
        )
    )

    repository_endpoint = (
        endpoint.GITHUB_REPOSITORY_DETAIL.format(
            owner=normalized_owner,
            repository_name=normalized_repository_name,
        )
    )

    response = api_client.get(repository_endpoint)

    if response is None:
        return None

    payload = response.json()

    if not isinstance(payload, dict):
        return None

    return _map_repository_detail_payload(payload)
```

Service Interface 没有暴露: 

- HTTP Method

- URI Template

- Response Object

- Nested JSON

- External Field Names

调用者只需要理解: 

```
Owner + Repository Name
    ↓
Repository Detail Business Object
```

### Step 8: 扩展 JSON Output Type

上一节的 save_json() 只接受 Collection: 

```python
list[dict[str, Any]]
```

现在需要保存单个 Detail Object. 
在 `modules/output.py` 中定义: 

```python
JsonDocument = (
    dict[str, Any]
    | list[dict[str, Any]]
)
```

将函数签名更新为: 

```python
def save_json(
    file_path: str,
    data: JsonDocument,
) -> Path:
    """
    Save a Business Object or Collection to a JSON file.

    Args:
        file_path: Destination path for the JSON file.
        data: Business Object or Business Object Collection.

    Returns:
        Path to the generated JSON file.

    Raises:
        OSError: If the file cannot be created.
        TypeError: If the data cannot be serialized.
    """
```

函数内部的 `json.dump()` 不需要改变. 

这是向后兼容的 Utility Extension: 

```
Before:
Collection only

After:
Single Business Object or Collection
```

### Step 9: 建立 Detail Workflow

新增: `scripts/get_repository_detail.py`

```python
from modules import output
from modules import repository_service


REPOSITORY_OWNER = "octocat"
REPOSITORY_NAME = "Hello-World"
OUTPUT_FILE = "output/github_repository_detail.json"


def main() -> None:
    """
    Collect and save one Repository Detail Business Object.
    """
    repository = repository_service.get_repository_detail(
        owner=REPOSITORY_OWNER,
        repository_name=REPOSITORY_NAME,
    )

    if repository is None:
        print("Repository detail collection failed.")
        return

    output_path = output.save_json(
        file_path=OUTPUT_FILE,
        data=repository,
    )

    print(
        f"Repository detail saved to {output_path}."
    )


if __name__ == "__main__":
    main()
```

运行: `python scripts/get_repository_detail.py`

生成: `output/github_repository_detail.json`

## Engineering Analysis

Collection 和 Detail 为什么不能共用一个 Service Function

下面的设计语义不清晰: 

```python
get_repositories(
    username=None,
    repository_name=None,
)
```

调用者无法快速判断: 

- 返回 Collection 还是 Dictionary

- 哪些参数组合有效

- None 表示什么

- 当前调用的是哪个 Endpoint

更清晰的 Interface 是: 

```python
collect_user_repositories()
```

以及: 

```python
get_repository_detail()
```

一个 Service Function 应该表达一个明确 Use Case. 

### 为什么 Detail Mapper 要复用 Summary Mapper

如果两个 Mapper 分别实现: 

- name Mapping

- owner Mapping

- stars Mapping

- forks Mapping

- visibility Mapping

字段更名时需要修改两个位置. 

复用 Summary Mapper 后: 

```
Common Mapping: one location
Detail Mapping: detail fields only
```

这同时实现: 

- DRY

- High Cohesion

- Lower Maintenance Cost

- Consistent Business Object Naming

### 为什么不把所有 Payload 字段都返回

GitHub Detail Payload 包含大量 URL, 权限和平台内部字段. 

企业 Service 不应该因为字段存在就全部暴露. 

本节只选择当前业务需要的字段: 

- Resource Identity

- Repository State

- Repository Classification

- Clone Information

- Lifecycle Timestamp

Business Object 不是 External Payload 的副本. 

它是项目定义的内部数据模型. 

当前错误接口的限制

GitHub 的 Detail Endpoint 可能返回 403 或 404 等状态. 

当前 API Client 将非成功 Response 统一转换为: 

```python
None
```

因此 Service 暂时不能区分: 

```
Repository Not Found
Permission Denied
Communication Failure
```

这是当前 Error Contract 的已知限制. 

本节不重新设计 Chapter 10 的 API Client, 但企业项目后续通常会引入更明确的 Error Object 或 Exception Hierarchy. 

## Engineering Best Practice

- 企业 Service Extension 建议遵循: 

- Collection 与 Detail 使用独立 Business Interface. 

- URI Template 统一保存在 Endpoint Module. 

- Workflow 不构建 Endpoint. 

- Path Parameter 在 Service Boundary 验证. 

- Detail Mapper 复用已有 Summary Mapper. 

- Nullable Nested Object 必须显式处理. 

- Business Object 只保留业务需要的字段. 

- External API Field Name 不泄漏到 Workflow. 

- Output Utility 支持 Object 和 Collection, 但不理解 Repository. 

- 新功能应扩展现有 Layer, 而不是绕过现有 Layer. 

- Service Extension 不应破坏已有 Collection Workflow. 

## Engineering Insight

Service Extension 的关键不是增加一个新的 GET Request. 

真正的工程问题是: 

```
新 Resource 如何进入现有 Architecture
```

良好的扩展路径应该是: 

```
Add Endpoint
    ↓
Add Payload Validation
    ↓
Reuse Existing Mapping
    ↓
Add Detail Mapping
    ↓
Add Business Interface
    ↓
Add Workflow
```

整个过程中: 

- API Client 不需要理解 Repository

- Output Utility 不需要理解 GitHub

- Collection Workflow 不需要修改

- Detail Workflow 不需要理解 HTTP

这说明 Layered Architecture 不只是组织代码, 它还控制系统如何安全扩展. 

## Engineering Checklist

完成本节后, 应能够回答: 

- Resource Collection 与 Resource Instance 有什么区别? 

- 为什么 Collection 和 Detail 应使用不同 Service Interface? 

- Workflow 为什么不能构建 URI? 

- Path Parameter 应该在哪一层验证? 

- Detail Mapper 为什么应该复用 Summary Mapper? 

- license 为什么不能直接访问 ["name"]? 

- Business Object 为什么不应该包含全部 API 字段? 

- Output Utility 如何向后兼容单个 Business Object? 

- 当前 None Error Contract 有什么限制? 

- Service Extension 如何保持 High Cohesion 和 Low Coupling? 

## Summary

本节将单个 Repository Resource 集成到现有 API Framework: 

```
Workflow
    ↓
get_repository_detail()
    ↓
Repository Service
    ↓
Endpoint Template
    ↓
API Client
    ↓
Detail Payload Validation
    ↓
Summary Mapping Reuse
    ↓
Detail Mapping
    ↓
Repository Detail Business Object
    ↓
JSON Output
```

整个扩展继续保持: 

- Layered Architecture

- DRY

- Single Responsibility Principle

- Separation of Concerns

- Stable Business Interface

- Business 与 Infrastructure 解耦

- Workflow 只面向 Business Interface