从本章开始, 整个项目文件更加规范化, 如以下

```file
automation/

├── inventory/
├── logs/
├── backups/
├── config/
├── modules/
├── main.py
```

## Terminology Consistency Check

统一术语如下。

| Preferred Term           | 不再使用                          |
| ------------------------ | ----------------------------- |
| Device Inventory         | Device List                   |
| Network Device           | Router List                   |
| Automation Project       | Python Script Project         |
| Module                   | Utility File                  |
| Function                 | Method（避免混用）                  |
| Configuration Deployment | Config Push                   |
| Verification             | Validation（统一使用 Verification） |
