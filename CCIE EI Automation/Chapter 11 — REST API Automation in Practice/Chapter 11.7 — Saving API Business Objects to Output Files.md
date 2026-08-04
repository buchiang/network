前一节已经完成 API Data Validation. 

当前数据流如下: 

```
API Response
    ↓
Payload Validation
    ↓
Response Mapping
    ↓
Business Object
```

但是 Business Object 目前只存在于程序内存中. 

企业自动化通常还需要将执行结果保存为文件, 用于: 

- 后续数据分析

- 自动化任务交接

- 故障排查

- 审计留存

- 其他 Workflow 再次使用

本节将把经过验证和映射的 Repository Business Object 保存到现有项目的 output/ 目录. 

## Theory

API Response 与 Output File 并不是同一种数据. 

API Response 是外部系统返回的原始 Payload: `GitHub API Payload`

Output File 应该保存自动化项目认可的 Business Object: 
`Validated Repository Business Object`

因此完整数据流应该是: 

```
Endpoint
    ↓
API Client
    ↓
Raw API Payload
    ↓
Service Layer
    ↓
Validation
    ↓
Response Mapping
    ↓
Business Object
    ↓
Output Utility
    ↓
JSON Output File
```

不能直接将原始 API Response 保存到文件. 

例如下面的设计虽然可以工作: 

```python
response = api_client.get(endpoint_name)
output.save_json("output/repositories.json", response.json())
```

但它跳过了: 

- Data Validation

- Response Mapping

- Business Object Boundary

- Service Layer Interface

这会让外部 API Schema 直接进入项目输出. 

只要 GitHub 修改字段结构, Output File 的结构也会跟着变化. 

## Engineering Discussion

Output 应该由哪一层负责

当前项目已经存在: `modules/output.py`

这个 Module 在 Chapter 8 中负责保存生成的配置文件. 

现在可以继续扩展它, 让它支持 JSON Data. 

职责划分如下: 

`repository_service.py`

负责: 

- 调用 API Client

- 验证 Payload

- 映射 Business Object

- 返回 Repository Collection

`output.py`

负责: 

- 创建 Output Directory

- 将数据序列化为 JSON

- 写入 Output File

- 返回文件路径

`collect_repositories.py`

负责: 

- 启动 Workflow

- 调用 Repository Service

- 判断 Workflow Result

- 调用 Output Utility

因此依赖关系仍然是: 

```
Workflow
    ↓
Business Service
    ↓
API Client
```

当 Business Service 返回结果后: 

```
Workflow
    ↓
Output Utility
```

Service Layer 不应该直接调用 `output.py`. 

否则 Service 同时承担: 

- API Business Logic

- Data Persistence

这会违反 Single Responsibility Principle. 

## Hands-on Lab

### Step 1: 确认 Project Structure

继续沿用 Chapter 8 至 Chapter 10 的目录: 

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
│   └── collect_repositories.py
│
├── output/
│
└── logs/
```

本节不建立新的 API 目录, 也不重新设计 Project Structure. 

### Step 2: 扩展 Output Utility

打开: 
`modules/output.py`

保留现有的 `save_configuration()`, 然后增加以下 imports: 

```python
import json
from pathlib import Path
from typing import Any
```

新增 JSON Output Function: 

```python
def save_json(
    file_path: str,
    data: list[dict[str, Any]],
) -> Path:
    """
    Save a collection of Business Objects to a JSON file.

    Args:
        file_path: Destination path for the JSON output file.
        data: Business Object collection to serialize.

    Returns:
        Path to the generated JSON file.

    Raises:
        OSError: If the output directory or file cannot be created.
        TypeError: If the supplied data cannot be serialized to JSON.
    """
    output_path = Path(file_path)

    try:
        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with output_path.open(
            mode="w",
            encoding="utf-8",
        ) as output_file:
            json.dump(
                data,
                output_file,
                indent=4,
                ensure_ascii=False,
            )

        return output_path

    except (OSError, TypeError) as error:
        print(f"Failed to save JSON output: {error}")
        raise
```

这里的 save_json() 是 Utility Interface. 

它不理解 Repository, 也不理解 GitHub. 

它只理解: 

`JSON Data ➡ Output File`

因此以后其他 Workflow 也可以复用它. 

### Step 3: 更新 Workflow

更新: 

`scripts/collect_repositories.py`

```python
from modules import output
from modules import repository_service


OUTPUT_FILE = "output/github_repositories.json"


def main() -> None:
    """
    Collect GitHub repositories and save validated Business Objects.

    The Workflow coordinates the Repository Service and Output Utility
    without directly handling HTTP communication or raw API Payloads.
    """
    repositories = (
        repository_service.collect_all_user_repositories(
            username="octocat",
            repository_type="owner",
            sort="updated",
            direction="desc",
            per_page=30,
            max_pages=5,
        )
    )

    if repositories is None:
        print("Repository collection failed.")
        return

    output_path = output.save_json(
        file_path=OUTPUT_FILE,
        data=repositories,
    )

    print(
        f"Saved {len(repositories)} repositories "
        f"to {output_path}."
    )


if __name__ == "__main__":
    main()
```

Workflow 中没有出现: 
`requests.get()`

也没有出现: 
`response.json()`

更没有访问: 
`repository["owner"]["login"]`

因为这些细节已经分别属于: 

- Communication Layer

- Service Layer

- Payload Mapping

Workflow 始终只面向 Business Interface. 

## Step 4: 检查 Output File

运行 Workflow 后, 项目应该生成: 
`output/github_repositories.json`

文件内容类似: 

```json
[
    {
        "name": "Hello-World",
        "full_name": "octocat/Hello-World",
        "owner": "octocat",
        "owner_url": "https://github.com/octocat",
        "url": "https://github.com/octocat/Hello-World",
        "description": "My first repository on GitHub!",
        "language": null,
        "stars": 2500,
        "forks": 2200,
        "visibility": "public",
        "default_branch": "master",
        "created_at": "2011-01-26T19:01:12Z",
        "updated_at": "2026-01-01T10:00:00Z"
    }
]
```

这里保存的不是完整 GitHub Payload, 而是项目定义的 Repository Business Object. 

## Engineering Analysis

为什么不能保存 Raw Payload

GitHub Repository Payload 可能包含大量当前 Workflow 不需要的字段. 

直接保存原始 Payload 会产生以下问题: 

- Output File 体积增大

- 外部 Schema 泄漏到项目内部

- 下游程序依赖不稳定字段

- 不容易判断哪些字段属于正式业务接口

- API 修改可能导致 Output Contract 改变

Response Mapping 实际上建立了一个边界: 

```
External API Schema
    ↓
Internal Business Object Schema
```

Output File 应该位于边界内部. 

None 和空 Collection 不相同

Workflow 使用: 

```python
if repositories is None:
```

而不是: 

```python
if not repositories:
```

因为两种状态具有不同含义: 
`None` 表示 API Request, Response Processing 或 Service Operation 失败. 

`[]` 表示 API Operation 成功, 但是没有找到符合条件的 Resource. 

空 Collection 仍然是合法业务结果, 因此可以保存为: 

`[]`

混淆这两种状态, 会让 Workflow 无法区分“没有数据”和“执行失败”. 

### Output 与 Log 不相同

`output/` 保存业务执行结果: 
`github_repositories.json`

logs/ 保存程序执行过程: 

```
Request started
Response status: 200
Page 2 collected
Output file generated
```

它们不能混合. 

```
Output = Business Result
Log = Execution Evidence
```

## Engineering Best Practice

企业 API Automation 中建议遵循以下规则: 

- 只保存经过验证和映射的 Business Object. 

- 不在 API Client 中写 Output File. 

- 不在 Service Layer 中决定文件路径. 

- 由 Workflow 决定何时保存结果. 

- 由 Output Utility 负责文件写入细节. 

- 使用 UTF-8 明确文件编码. 

- 自动创建不存在的 Output Directory. 

- 保留 None 与空 Collection 的语义区别. 

- Output File 使用稳定且具有业务含义的名称. 

- 不将日志内容和业务数据保存在同一个文件中. 

## Engineering Insight

Output File 不只是一个程序生成的文件. 

它实际上是自动化系统向下游提供的数据接口. 

今天下游可能是 Network Engineer. 

明天可能是: 

- 另一个 Python Workflow

- Compliance Module

- Reporting Module

- Data Analysis Tool

因此 Output Schema 也应该被视为一种 Contract. 

这就是为什么企业工程不会简单地执行: 

```python
json.dump(response.json(), output_file)
```

而是建立: 

```
API Payload
    ↓
Validation
    ↓
Business Object
    ↓
Stable Output Contract
```

外部 API 可以变化, 但内部 Business Object 和 Output Contract 应尽可能保持稳定. 

## Engineering Checklist

完成本节后, 应能够回答以下问题: 

- 为什么不能直接保存 Raw API Payload? 

- Service Layer 是否应该直接写 Output File? 

- output.py 属于 Business Module 还是 Utility Module? 

- Workflow 在输出过程中负责什么? 

- 为什么 None 和空 Collection 必须区分? 

- Output 与 Log 的职责有什么区别? 

- 为什么 Output Schema 应被视为一种 Contract? 

- 为什么 Output Utility 不应该理解 GitHub Repository? 

- 如何保证 Output Module 具有 High Cohesion 和 Low Coupling? 

## Summary

本节完成了真实 REST API Workflow 的结果持久化: 

```
GitHub Endpoint
    ↓
API Client
    ↓
Repository Service
    ↓
Payload Validation
    ↓
Response Mapping
    ↓
Repository Business Objects
    ↓
Output Utility
    ↓
output/github_repositories.json
```

整个设计继续保持: 

- Layered Architecture

- Separation of Concerns

- Single Responsibility Principle

- High Cohesion

- Low Coupling

- Business 与 Infrastructure 解耦

- Workflow 只面向 Business Interface