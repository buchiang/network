## Theory

在企业自动化项目中, API Documentation 不只是“怎么调用接口”的说明书, 而是外部系统和自动化框架之间的工程契约. 

一个真实 Endpoint 至少要被拆解为：

| API 文档信息 | 工程含义 |
|---|---|
| HTTP Method | 这个 Endpoint 的操作类型 |
| URI Path | Resource 的位置 |
| Path Parameter | 必须由业务输入提供的资源标识 |
| Query Parameter | Filtering、Sorting、Pagination 控制项 |
| Headers | Communication Layer 的协议约束 |
| Request Payload | 写操作的数据契约 |
| Response Payload | Response Mapping 的输入 |
| Status Code | Service Layer 的错误处理依据 |

本节不重新讲 REST API 基础. Chapter 10 已经完成 API Client 和 Service Layer 的基础能力. Chapter 11 的重点是：把真实 API Documentation 转换成现有自动化框架中的 Business Interface、Business Object 和 Service Extension. 

## Engineering Discussion

以 GitHub REST API 的 List repositories for a user 为例：

Endpoint：`GET /users/{username}/repos`

它不是一个“URL 字符串”, 而是一个 Resource Collection：

`User -> Repositories`
从业务角度看, Workflow 并不关心：

```python
requests.get("https://api.github.com/users/octocat/repos")
```

Workflow 真正需要的是：

`Collect public repository inventory for a GitHub user`

因此, Workflow 不应该直接操作 Endpoint、Header、Session 或 JSON 结构. 

正确的 Layered Architecture 应该是：

```
Workflow
  -> Repository Inventory Service
    -> GitHub Repository API Client
      -> Existing API Client / Session / Communication Layer
        -> GitHub REST API Endpoint
```

这样设计的原因是：
- Endpoint 变化时, 只影响 API Client. 

- Payload 字段变化时, 只影响 Response Mapping. 

- Business Logic 变化时, 只影响 Service Layer. 

- Workflow 保持稳定, 只面向业务动作. 

## Hands-on Lab

Lab 11.1 的目标不是马上写请求代码, 而是完成真实 API 文档到工程设计的转换. 

业务需求：

>生成某个 GitHub 用户的公开 Repository Inventory. 

API Documentation 提取结果：
| 项目 | 设计结果 |
|---|---|
| Public API | GitHub REST API |
| Resource | Repository |
| Resource Collection | User repositories |
| Endpoint | `GET /users/{username}/repos` |
| Path Parameter | `username` |
| Query Parameters | `type`、`sort`、`direction`、`per_page`、`page` |
| Authentication | Public resource 可不使用 token；企业项目应支持 token 配置 |
| Response Type | JSON array |
| Nested JSON | `owner.login`、`owner.html_url` |
| Business Object | `RepositorySummary` |
| Service Interface | `collect_public_repository_inventory(username)` |

建议继续沿用目录：

```
automation_project/
  config/
  modules/
    api/
    github/
  scripts/
  logs/
  inventory/
  output/
```

本节应新增的设计意图是：

```
modules/github/
  repository_objects.py
  repository_service.py
  github_repository_client.py
```

其中：

`github_repository_client.py` 只处理 GitHub Endpoint. 

`repository_objects.py` 定义 Business Object. 

`repository_service.py` 提供 Business Interface. 

`scripts/` 下的 Workflow 只调用 Service Layer. 

## Engineering Analysis

真实 API 的 Response Payload 往往比业务需要的数据大得多. GitHub repository response 中包含 repository URL、owner 信息、权限字段、语言、时间戳、topics、security analysis 等大量字段. 企业自动化不应该把完整 Payload 直接传给 Workflow. 

错误做法：

`Workflow reads raw JSON directly.`

正确做法：

```
API Client receives raw Payload.
Response Mapper converts Payload into Business Object.
Service Layer returns Business Object to Workflow.
```

原因很直接：raw JSON 属于外部系统格式, Business Object 属于本项目业务模型. 两者不能混在一起. 

## Engineering Best Practice

本章后续实现 GitHub API 集成时, 必须遵守以下规则：

- 不在 scripts/ 中直接写 requests.get(). 

- 不在 Workflow 中拼接 Endpoint. 

- 不在 Workflow 中解析 nested JSON. 

- 不把完整 API Payload 当作 Business Object. 

- Header、base URL、timeout、token 都进入 Configuration. 

- API Client 只表达通信细节. 

- Service Layer 只表达业务能力. 

- Output 只保存经过业务筛选和验证的数据. 

## Engineering Insight

阅读 API Documentation 的真正目标, 不是找到一个能跑通的 cURL 命令, 而是回答三个工程问题：

- 这个 API 暴露了什么 Resource？

- 这个 Resource 如何映射到我的 Business Object？

- 我的 Workflow 应该看到什么 Business Interface？

如果这三个问题没有回答清楚, 代码即使可以运行, 也只是脚本, 不是企业自动化框架. 

## Engineering Checklist

进入下一节前, 确认：

- 已选择真实 Public REST API. 

- 已识别 Resource Collection. 

- 已识别 Endpoint、Path Parameter、Query Parameter. 

- 已区分 Payload 与 Business Object. 

- 已确认 Workflow 不直接依赖 API 文档细节. 

- 已确认继续复用 Chapter 8-10 的 Project Structure.

- 已确认本节没有进入后续章节知识边界. 

## Summary

本节完成了 Chapter 11 的起点：从真实 API Documentation 出发, 建立 API Resource Model, 并把它转换为企业自动化项目中的 Service Interface 设计. 