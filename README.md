# AutoLark - 飞书多维表格API库

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

AutoLark 是一个专门用于飞书（Lark/Feishu）多维表格API操作的Python库，提供了完整的多维表格管理功能。

## ✨ 主要功能

### 🔐 认证管理
- **应用认证**: 获取应用访问令牌（App Access Token）
- **用户认证**: 获取用户访问令牌（User Access Token）
- **租户认证**: 获取租户访问令牌（Tenant Access Token）
- **令牌刷新**: 自动刷新用户访问令牌

### 📊 多维表格操作
- **表格管理**: 创建、查询、更新多维表格
- **字段管理**: 创建、删除、更新表格字段
- **记录管理**: 增删改查表格记录
- **视图管理**: 获取和管理表格视图

### 🔧 实用工具
- **URL解析**: 从飞书URL提取表格信息
- **批量操作**: 支持CSV文件批量导入数据
- **字段检查**: 自动检查和创建缺失字段
- **数据转换**: 字段格式转换工具

## 📁 项目结构

```
AutoLark/
├── __init__.py                     # 包初始化文件
├── AutoLark.py                    # 主API类
├── setup.py                       # 安装配置
├── test.py                        # 示例测试文件
│
├── 认证相关/
│   ├── GET_APP_ACCESS_TOKEN.py    # 获取应用访问令牌
│   ├── GET_USER_ACCESS_TOKEN.py   # 获取用户访问令牌
│   ├── GET_TENANT_ACCESS_TOKEN.py # 获取租户访问令牌
│   ├── REFRESH_USER_ACCESS_TOKEN.py # 刷新用户令牌
│   └── GET_LOGIN_CODE.py          # 获取登录授权码
│
├── 表格管理/
│   ├── LIST_TABLES.py             # 列出所有表格
│   ├── CREATE_TABLE.py            # 创建新表格
│   ├── CREATE_TABLE_QUICK.py      # 快速创建表格
│   └── GET_TABLE_ID.py            # 获取表格ID
│
├── 字段管理/
│   ├── LIST_FIELDS.py             # 列出字段
│   ├── CREATE_FIELD.py            # 创建字段
│   ├── UPDATE_FIELD.py            # 更新字段
│   ├── DELETE_FIELDS.py           # 删除字段
│   ├── BUILD_FIELD.py             # 构建字段
│   └── CHECK_FIELD_EXIST.py       # 检查字段存在
│
├── 记录管理/
│   ├── LIST_RECORDS.py            # 列出记录
│   ├── GET_RECORD.py              # 获取单条记录
│   ├── UPDATE_RECORD.py           # 更新记录
│   ├── DELETE_RECORD.py           # 删除记录
│   └── ADD_RECORDS_FROM_CSV.py    # 从CSV批量添加
│
├── 视图管理/
│   ├── LIST_VIEWS.py              # 列出视图
│   └── GET_VIEW_ID.py             # 获取视图ID
│
└── 工具函数/
    ├── GET_INFO_FROM_URL.py       # 从URL提取信息
    ├── CONVERSION_FIELDS.py       # 字段转换工具
    └── WRITE_*.py                 # 各种写入工具
```

## 🚀 快速开始

### 安装

```bash
pip install git+https://github.com/Brain2nd/AutoLark.git
```

### 基本使用

```python
from AutoLark import AutoLark

# 创建API实例
api = AutoLark()

# 从URL获取表格信息
url = "https://your-feishu-url"
app_token = api.GET_APPTOKEN_FROM_URL(url)
table_id = api.GET_TABLEID_FROM_URL(url)

# 获取表格字段列表
fields = api.LIST_FIELDS(app_token=app_token, table_id=table_id)
print("表格字段:", fields)

# 获取表格记录
records = api.LIST_RECORDS(app_token=app_token, table_id=table_id)
print("表格记录:", records)
```

### 批量操作示例

```python
# 从CSV文件批量添加记录
result = api.ADD_RECORDS_FROM_CSV(
    app_token="your_app_token",
    table_id="your_table_id",
    csv_file="data.csv"
)
```

### 认证配置

```python
# 获取应用访问令牌
app_token = api.GET_APP_ACCESS_TOKEN(
    app_id="your_app_id",
    app_secret="your_app_secret"
)

# 获取用户访问令牌
user_token = api.GET_USER_ACCESS_TOKEN(
    app_access_token=app_token,
    code="authorization_code"
)
```

## ⚙️ 配置

建议创建配置文件来管理敏感信息：

```ini
[TOKEN]
app_id = YOUR_APP_ID_HERE
app_secret = YOUR_APP_SECRET_HERE
app_token = YOUR_APP_TOKEN_HERE
user_access_token = YOUR_USER_TOKEN_HERE
tenant_access_token = YOUR_TENANT_TOKEN_HERE

[DEFAULT]
page_size = 100
```

## 📖 API文档

### 主要方法

| 方法 | 描述 | 参数 |
|------|------|------|
| `GET_APPTOKEN_FROM_URL(url)` | 从URL提取应用令牌 | url: 飞书表格URL |
| `LIST_TABLES(app_token, ...)` | 获取应用下所有表格 | app_token, user_access_token等 |
| `CREATE_TABLE(name, ...)` | 创建新的多维表格 | name: 表格名称 |
| `LIST_FIELDS(app_token, table_id, ...)` | 获取表格字段列表 | app_token, table_id等 |
| `CREATE_FIELD(field_name, field_type, ...)` | 创建新字段 | field_name, field_type等 |
| `LIST_RECORDS(app_token, table_id, ...)` | 获取表格记录 | app_token, table_id等 |
| `ADD_RECORDS_FROM_CSV(...)` | 批量导入CSV数据 | csv_file路径等 |

### 字段类型

- `1`: 多行文本
- `2`: 数字
- `3`: 单选
- `4`: 多选
- `5`: 日期
- `7`: 复选框
- `11`: 人员
- `13`: 电话号码
- `15`: 超链接
- `17`: 附件
- `18`: 单向关联
- `20`: 公式
- `21`: 双向关联

## 🤝 贡献

欢迎提交Issue和Pull Request来帮助改进项目！

## 📄 许可证

本项目基于 MIT 许可证开源 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

- 项目地址: https://github.com/Brain2nd/AutoLark
- 问题反馈: https://github.com/Brain2nd/AutoLark/issues

## 📝 更新日志

### v3.3.4
- 修复已知问题
- 优化API调用性能
- 增加更多实用工具函数

---

🌟 如果这个项目对你有帮助，请给它一个星标！ 