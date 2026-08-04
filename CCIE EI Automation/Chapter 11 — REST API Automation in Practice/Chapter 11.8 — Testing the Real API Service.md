## Theory

API Testing 不能只测试 HTTP Status Code. 

例如: 

`HTTP Status Code: 200`

只能证明服务器接受请求并返回了成功响应. 

它不能证明: 

- 返回的是 Collection

- Payload Schema 正确

- Nested JSON Mapping 正确

- Filtering 生效

- Business Object 字段完整

- Output File 数据正确

因此需要区分三个测试层次: 

```
Communication Test
    ↓
Service Contract Test
    ↓
Workflow Output Test
```

Communication Test

验证: API Client ➡ Endpoint ➡ HTTP Response

Service Contract Test

验证: Service Layer ➡ Business Object

Workflow Output Test

验证: Business Object ➡ Output Utility ➡ JSON File

企业测试关注的是每一层的 Contract, 而不只是程序有没有抛出 Exception. 

## Engineering Discussion

Live API Test 与稳定测试

本章使用真实 GitHub REST API, 因此测试会受到外部环境影响: 

- Internet Connection

- GitHub API Availability

- API Rate Limit

- Public Repository Data Changes

- API Version Changes

GitHub 的 `GET /users/{username}/repos` Endpoint 成功时返回 200 和 Repository Collection, 并支持 `type`、`sort`、`direction`、`per_page` 与 page 等 Query Parameters. 

因此 Live API Test 属于 Integration Test. 

它不能完全替代稳定的 Business Logic Test. 

### 什么数据可以 Assert

可以验证稳定 Contract: 

```
Result is not None
Result is a list
Collection size does not exceed per_page
Repository contains required fields
owner is a string
language may be string or None
```

不应该固定动态业务数据: 

```python
assert repository["stars"] == 2500
```

Stars 随时可能变化. 

下面也不稳定: 

```python
assert len(repositories) == 8
```

用户可以随时创建或删除 Repository. 

测试应该验证 Contract, 不应该依赖经常变化的业务值. 

## Hands-on Lab

### Step 1: 建立测试入口

在现有 `scripts/` 中新增: 

`scripts/test_repository_service.py`

它仍然是一个 Entry Point, 不是公共业务模块. 

项目结构保持: 

```
automation_project/

├── configs/
│   └── api.yaml
│
├── modules/
│   ├── api_client.py
│   ├── endpoint.py
│   ├── repository_service.py
│   ├── output.py
│   ├── loader.py
│   └── logger.py
│
├── scripts/
│   ├── collect_repositories.py
│   └── test_repository_service.py
│
├── output/
└── logs/
```

### Step 2: 实现 Business Object Validation

```python
import json
from typing import Any

from modules import output
from modules import repository_service


TEST_USERNAME = "octocat"
TEST_OUTPUT_FILE = "output/test_github_repositories.json"

RepositorySummary = dict[str, Any]

REQUIRED_BUSINESS_FIELDS: set[str] = {
    "name",
    "full_name",
    "owner",
    "owner_url",
    "url",
    "description",
    "language",
    "stars",
    "forks",
    "visibility",
    "default_branch",
    "created_at",
    "updated_at",
}


def validate_repository_object(
    repository: RepositorySummary,
) -> None:
    """
    Validate the Contract of one Repository Business Object.

    Args:
        repository: Mapped Repository Business Object.

    Raises:
        AssertionError: If the Business Object violates its Contract.
    """
    missing_fields = (
        REQUIRED_BUSINESS_FIELDS - repository.keys()
    )

    assert not missing_fields, (
        "Repository Business Object is missing fields: "
        f"{sorted(missing_fields)}"
    )

    assert isinstance(repository["name"], str)
    assert isinstance(repository["full_name"], str)
    assert isinstance(repository["owner"], str)
    assert isinstance(repository["url"], str)
    assert isinstance(repository["stars"], int)
    assert isinstance(repository["forks"], int)

    language = repository["language"]

    assert language is None or isinstance(language, str), (
        "Repository language must be a string or None."
    )
```

这里测试的是内部 Business Object, 而不是 GitHub Raw Payload. 

因此不会验证: 

```
owner.login
stargazers_count
forks_count
html_url
```

这些属于 External API Schema. 

测试使用的是映射后的内部字段: 

```
owner
stars
forks
url
```

### Step 3: 测试非法 Query Input

```python
def test_invalid_query_is_rejected() -> None:
    """
    Verify that invalid query input is rejected before communication.

    Raises:
        AssertionError: If invalid input reaches the normal workflow.
    """
    try:
        repository_service.collect_user_repositories(
            username=TEST_USERNAME,
            per_page=101,
        )
    except ValueError:
        return

    raise AssertionError(
        "Service accepted per_page greater than 100."
    )
```

这个测试不需要访问 Internet. 

它验证的是 Service Layer 的 Business Rule: 

`per_page must be between 1 and 100`

非法输入应该在 Communication Layer 之前被拒绝: 

```
Invalid Input
    ↓
Service Validation
    ↓
STOP
```

而不是: 

```
Invalid Input
    ↓
API Request
    ↓
Remote API Error
```

### Step 4: 测试真实 Repository Service

```python
def test_repository_collection() -> list[RepositorySummary]:
    """
    Test the Repository Service against the real GitHub API.

    Returns:
        Validated Repository Business Objects.

    Raises:
        AssertionError: If the Service Contract is violated.
    """
    repositories = (
        repository_service.collect_user_repositories(
            username=TEST_USERNAME,
            repository_type="owner",
            sort="updated",
            direction="desc",
            per_page=5,
        )
    )

    assert repositories is not None, (
        "Repository Service returned a failure result."
    )

    assert isinstance(repositories, list), (
        "Repository Service must return a list."
    )

    assert len(repositories) <= 5, (
        "Repository collection exceeded per_page."
    )

    for repository in repositories:
        validate_repository_object(repository)

        assert repository["owner"] == TEST_USERNAME, (
            "Repository owner does not match the query."
        )

    return repositories
```

这个测试只发送一次真实 API Request. 

它同时验证: 

- Endpoint Integration

- Query Parameter Mapping

- Collection Processing

- Nested JSON Mapping

- Business Object Contract

- Nullable Field Processing

### Step 5: 测试 Output Data Integrity

```python
def test_repository_output(
    repositories: list[RepositorySummary],
) -> None:
    """
    Verify that Business Objects survive JSON serialization.

    Args:
        repositories: Validated Repository Business Objects.

    Raises:
        AssertionError: If the output file is missing or corrupted.
    """
    output_path = output.save_json(
        file_path=TEST_OUTPUT_FILE,
        data=repositories,
    )

    assert output_path.exists(), (
        "JSON output file was not created."
    )

    with output_path.open(
        mode="r",
        encoding="utf-8",
    ) as input_file:
        saved_repositories = json.load(input_file)

    assert saved_repositories == repositories, (
        "Saved JSON data does not match the Business Objects."
    )
```

这个过程称为 Round-trip Validation: 

```
Business Object
    ↓
JSON Serialization
    ↓
JSON File
    ↓
JSON Deserialization
    ↓
Compare with Original Object
```

它验证的不只是文件存在, 还验证数据内容没有在序列化过程中发生改变. 

### Step 6: 建立 Test Workflow

```python
def main() -> None:
    """
    Run the Repository Service integration test workflow.
    """
    print("Repository Service Test: START")

    try:
        test_invalid_query_is_rejected()

        repositories = test_repository_collection()

        test_repository_output(repositories)

    except AssertionError as error:
        print(f"Repository Service Test: FAIL - {error}")
        raise

    print("Repository Service Test: PASS")


if __name__ == "__main__":
    main()
```

完整执行顺序: 

```
Validate Invalid Input Handling
    ↓
Call Real GitHub API
    ↓
Validate Service Result
    ↓
Validate Business Objects
    ↓
Save JSON Output
    ↓
Reload JSON Output
    ↓
Compare Data
    ↓
PASS / FAIL
```

从项目根目录运行: 
`python scripts/test_repository_service.py`
预期结果: 

```
Repository Service Test: START
Repository Service Test: PASS
```
同时生成: 

`output/test_github_repositories.json`

## Postman as an Auxiliary Tool

Postman 可以帮助观察真实 HTTP Request. 

建立以下 Request: 

```
Method:
GET

URL:
https://api.github.com/users/octocat/repos
```

Query Parameters: 

```
type=owner
sort=updated
direction=desc
per_page=5
page=1
```

Headers: 

```
Accept: application/vnd.github+json
X-GitHub-Api-Version: 2022-11-28
User-Agent: ccie-ei-automation-workbook
```

GitHub 要求 Request 包含有效的 User-Agent, 并建议明确发送 Accept 和 API Version Headers. 

在 Postman 中检查: 

- HTTP Status Code

- Response Headers

- JSON Collection

- Nested `owner` Object

- Nullable `language`

- Pagination Information

但是 Postman 不能替代 Service Test. 

Postman 看到的是: 

`External API Payload`

Python Test 验证的是: 

`Internal Business Contract`

## Engineering Analysis

为什么返回 200 仍然可能失败

以下情况都可能返回成功 HTTP Response, 但业务处理仍然错误: 

- Mapping 使用了错误字段

- owner.login 没有正确读取

- stargazers_count 被映射到错误名称

- Nullable Field 导致异常

- Filtering 参数没有传递

- Output File 丢失字段

因此: `HTTP Success ≠ Business Success`

为什么 Live API Test 不能太多

每个 Live API Test 都依赖: 

- Network

- External Service

- API Rate Limit

- External Data State

GitHub API 会执行 Rate Limiting, 因此测试不应该为了验证同一个 Contract 重复发送大量请求. 

本 Lab 复用一次查询结果完成后续 Output Test, 避免重复通信. 

为什么不测试 Private Function

测试脚本没有直接调用: 

```python
_validate_repository_payload()
_map_repository_payload()
_build_repository_query()
```

这些是 Service Layer 的内部实现. 

测试面向公开 Business Interface: 

`collect_user_repositories()`

内部实现以后可以重构, 只要 Business Contract 不变, 测试就不需要修改. 

这就是 Low Coupling 在 Testing 中的体现. 

## Engineering Best Practice

企业 API Testing 建议遵循: 

- 测试公开 Business Interface. 

- 不让测试依赖 Private Function. 

- 区分 Communication Success 与 Business Success. 

- 对动态 API Data 只验证稳定 Contract. 

- 不固定 Stars、Forks、时间或 Collection 总数. 

- 明确测试 Nullable Field. 

- 验证非法输入在通信前被拒绝. 

- 控制真实 API Request 数量. 

- 复用同一次请求结果完成后续验证. 

- 验证 Output 内容, 而不只检查文件是否存在. 

- Postman 用于观察和排查, 不替代自动化测试. 

- Test Script 不保存公共 Business Logic. 

## Engineering Insight

Layered Architecture 不仅提高可维护性, 也决定了系统是否容易测试. 

如果 Workflow 直接调用: 

`requests.get()`

测试必须同时面对: 

- HTTP

- Payload

- Mapping

- Filtering

- Output

- Error Handling

当这些职责被分层后, 每一层都有清晰 Contract: 

```
API Client Contract
Service Contract
Business Object Contract
Output Contract
```

因此 Testability 不是最后增加的功能. 
它是良好 Architecture 的直接结果. 

## Engineering Checklist

完成本节后, 应能够回答: 

- 为什么 HTTP 200 不等于 Business Success？

- Communication Test 与 Service Contract Test 有什么区别？

- Live API Test 为什么属于 Integration Test？

- 哪些字段适合 Assert？

- 为什么不应该固定 Stars 或 Repository 总数？

- 为什么需要测试 Nullable Field？

- 为什么非法 Query 应在发送 Request 前被拒绝？

- 为什么测试应该面向公开 Service Interface？

- Postman 在 API Testing 中承担什么角色？

- 什么是 JSON Round-trip Validation？

- 为什么真实 API Test 应控制 Request 数量？

## Summary

本节完成了真实 API Service 的第一版测试流程: 

```
Input Validation Test
    ↓
Real Endpoint Integration Test
    ↓
Service Contract Test
    ↓
Business Object Validation
    ↓
Output Serialization Test
    ↓
Round-trip Data Validation
```

整个测试设计继续保持: 

- Workflow 面向 Business Interface

- Service Layer 隔离 External API Schema

- API Client 管理 Communication

- Output Utility 管理文件写入

- Tests 验证稳定 Contract

- Business 与 Infrastructure 解耦