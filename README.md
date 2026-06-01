<div align="center">

# 🧠 DocuMind AI

**AI-Powered Document Conversion & Knowledge Extraction**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/PyPI-Coming%20Soon-orange.svg)](https://pypi.org/)

[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文)

</div>

---

<a name="english"></a>
## 🇺🇸 English

### 🎉 Introduction

DocuMind AI is an intelligent document processing tool that goes beyond simple format conversion. While inspired by tools like `markitdown`, DocuMind AI differentiates itself by leveraging **Large Language Models (LLMs)** to deeply understand document content, extract meaningful insights, and build knowledge graphs.

**Key Differentiators:**
- 🧠 **AI-Powered Analysis**: Not just conversion—understand your documents
- 🔗 **Knowledge Graph Extraction**: Visualize relationships between entities
- 🤖 **Multi-Model Support**: Works with OpenAI, Azure OpenAI, and compatible APIs
- 📊 **Smart Summarization**: Automatic key points and topic extraction
- 🌐 **15+ Format Support**: PDF, DOCX, XLSX, PPTX, HTML, and more

### ✨ Core Features

| Feature | Description | Status |
|---------|-------------|--------|
| 📄 **Document Conversion** | Convert 15+ formats to clean Markdown | ✅ Ready |
| 🧠 **AI Analysis** | Summarize, extract entities, analyze sentiment | ✅ Ready |
| 🔗 **Knowledge Graphs** | Extract entities and relationships | ✅ Ready |
| ❓ **Q&A Generation** | Auto-generate questions from content | ✅ Ready |
| ✅ **Action Items** | Extract tasks and todos | ✅ Ready |
| 🎨 **Rich CLI** | Beautiful terminal interface with progress bars | ✅ Ready |
| 📦 **Multiple Exports** | JSON, Cypher (Neo4j), RDF formats | ✅ Ready |

### 🚀 Quick Start

#### Installation

```bash
# Clone the repository
git clone https://github.com/gitstq/documind-ai-pro.git
cd documind-ai-pro

# Install dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

#### Environment Setup

```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Optional: Set custom API base for Azure or other providers
export OPENAI_API_BASE="https://api.openai.com/v1"
```

#### Basic Usage

```bash
# Convert a single document
documind convert document.pdf

# Convert with AI analysis
documind convert document.pdf --extract-kg --questions

# Convert directory of documents
documind convert ./documents/ -o ./output/

# Analyze document only
documind analyze document.pdf

# Extract knowledge graph
documind extract-kg document.pdf --format cypher
```

### 📖 Detailed Usage

#### Command: `convert`

Convert documents to Markdown with optional AI analysis.

```bash
documind convert [OPTIONS] INPUT_PATH

Options:
  -o, --output PATH       Output directory
  --no-ai                 Disable AI analysis
  --model TEXT            AI model to use [default: gpt-4o-mini]
  --api-key TEXT          OpenAI API key
  --extract-kg            Extract knowledge graph
  --questions             Generate questions
  --actions               Extract action items
  --max-pages INTEGER     Maximum pages to process
```

**Examples:**

```bash
# Basic conversion
documind convert report.pdf

# Full analysis with knowledge extraction
documind convert report.pdf --extract-kg --questions --actions

# Use specific model
documind convert report.pdf --model gpt-4o

# Batch processing
documind convert ./input/ -o ./output/ --extract-kg
```

#### Command: `analyze`

Analyze document content with AI.

```bash
documind analyze [OPTIONS] INPUT_PATH

Options:
  --model TEXT    AI model to use
  --api-key TEXT  OpenAI API key
```

**Output includes:**
- 📋 Executive summary
- 📝 Key points (top 10)
- 🏷️ Topics and themes
- 💭 Sentiment analysis
- 👥 Named entities

#### Command: `extract-kg`

Extract knowledge graph from document.

```bash
documind extract-kg [OPTIONS] INPUT_PATH

Options:
  -o, --output PATH       Output file path
  --format [json|cypher|rdf]  Output format [default: json]
```

**Export Formats:**
- **JSON**: Standard graph format with nodes and edges
- **Cypher**: Neo4j query language for graph databases
- **RDF**: Resource Description Framework for semantic web

### 💡 Design Philosophy

DocuMind AI was built with three core principles:

1. **Intelligence over Conversion**: We don't just convert formats—we understand content
2. **Developer Experience**: Rich CLI, comprehensive APIs, and extensive documentation
3. **Extensibility**: Modular architecture for easy customization

### 📦 Supported Formats

| Format | Extension | Conversion | AI Analysis |
|--------|-----------|------------|-------------|
| PDF | .pdf | ✅ | ✅ |
| Word | .docx, .doc | ✅ | ✅ |
| Excel | .xlsx, .xls | ✅ | ✅ |
| PowerPoint | .pptx, .ppt | ✅ | ✅ |
| HTML | .html, .htm | ✅ | ✅ |
| Markdown | .md | ✅ | ✅ |
| Text | .txt | ✅ | ✅ |
| CSV | .csv | ✅ | ✅ |
| JSON | .json | ✅ | ✅ |
| XML | .xml | ✅ | ✅ |
| RTF | .rtf | ✅ | ✅ |
| OpenDocument | .odt, .ods, .odp | ✅ | ✅ |

### 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<a name="简体中文"></a>
## 🇨🇳 简体中文

### 🎉 项目介绍

DocuMind AI 是一款智能文档处理工具，它超越了简单的格式转换。虽然灵感来源于 `markitdown` 等工具，但 DocuMind AI 通过利用**大语言模型（LLM）**来深度理解文档内容、提取有意义的洞察，并构建知识图谱，从而实现差异化。

**核心差异化亮点：**
- 🧠 **AI 驱动分析**：不仅是转换，更是理解您的文档
- 🔗 **知识图谱提取**：可视化实体间的关系
- 🤖 **多模型支持**：兼容 OpenAI、Azure OpenAI 及兼容 API
- 📊 **智能摘要**：自动提取关键点和主题
- 🌐 **15+ 格式支持**：PDF、DOCX、XLSX、PPTX、HTML 等

### ✨ 核心特性

| 特性 | 描述 | 状态 |
|------|------|------|
| 📄 **文档转换** | 将 15+ 格式转换为干净的 Markdown | ✅ 就绪 |
| 🧠 **AI 分析** | 摘要、实体提取、情感分析 | ✅ 就绪 |
| 🔗 **知识图谱** | 提取实体和关系 | ✅ 就绪 |
| ❓ **问答生成** | 从内容自动生成问题 | ✅ 就绪 |
| ✅ **行动项提取** | 提取任务和待办事项 | ✅ 就绪 |
| 🎨 **精美 CLI** | 带进度条的优雅终端界面 | ✅ 就绪 |
| 📦 **多格式导出** | JSON、Cypher (Neo4j)、RDF 格式 | ✅ 就绪 |

### 🚀 快速开始

#### 安装

```bash
# 克隆仓库
git clone https://github.com/gitstq/documind-ai-pro.git
cd documind-ai-pro

# 安装依赖
pip install -r requirements.txt

# 或以开发模式安装
pip install -e .
```

#### 环境配置

```bash
# 设置 OpenAI API 密钥
export OPENAI_API_KEY="your-api-key-here"

# 可选：为 Azure 或其他提供商设置自定义 API 基础地址
export OPENAI_API_BASE="https://api.openai.com/v1"
```

#### 基本用法

```bash
# 转换单个文档
documind convert document.pdf

# 带 AI 分析的转换
documind convert document.pdf --extract-kg --questions

# 批量转换目录
documind convert ./documents/ -o ./output/

# 仅分析文档
documind analyze document.pdf

# 提取知识图谱
documind extract-kg document.pdf --format cypher
```

### 📖 详细使用指南

#### 命令：`convert`

将文档转换为 Markdown，可选 AI 分析。

```bash
documind convert [选项] 输入路径

选项：
  -o, --output 路径       输出目录
  --no-ai                 禁用 AI 分析
  --model 文本            使用的 AI 模型 [默认: gpt-4o-mini]
  --api-key 文本          OpenAI API 密钥
  --extract-kg            提取知识图谱
  --questions             生成问题
  --actions               提取行动项
  --max-pages 整数        最大处理页数
```

**示例：**

```bash
# 基础转换
documind convert report.pdf

# 完整分析并提取知识
documind convert report.pdf --extract-kg --questions --actions

# 使用特定模型
documind convert report.pdf --model gpt-4o

# 批量处理
documind convert ./input/ -o ./output/ --extract-kg
```

#### 命令：`analyze`

使用 AI 分析文档内容。

```bash
documind analyze [选项] 输入路径

选项：
  --model 文本    使用的 AI 模型
  --api-key 文本  OpenAI API 密钥
```

**输出包括：**
- 📋 执行摘要
- 📝 关键点（前 10 个）
- 🏷️ 主题和标签
- 💭 情感分析
- 👥 命名实体

#### 命令：`extract-kg`

从文档提取知识图谱。

```bash
documind extract-kg [选项] 输入路径

选项：
  -o, --output 路径       输出文件路径
  --format [json|cypher|rdf]  输出格式 [默认: json]
```

**导出格式：**
- **JSON**：标准图谱格式，包含节点和边
- **Cypher**：Neo4j 图数据库查询语言
- **RDF**：语义网资源描述框架

### 💡 设计理念

DocuMind AI 基于三个核心原则构建：

1. **智能优于转换**：我们不只是转换格式，更是理解内容
2. **开发者体验**：丰富的 CLI、全面的 API 和详尽的文档
3. **可扩展性**：模块化架构，易于定制

### 📦 支持的格式

| 格式 | 扩展名 | 转换 | AI 分析 |
|------|--------|------|---------|
| PDF | .pdf | ✅ | ✅ |
| Word | .docx, .doc | ✅ | ✅ |
| Excel | .xlsx, .xls | ✅ | ✅ |
| PowerPoint | .pptx, .ppt | ✅ | ✅ |
| HTML | .html, .htm | ✅ | ✅ |
| Markdown | .md | ✅ | ✅ |
| 文本 | .txt | ✅ | ✅ |
| CSV | .csv | ✅ | ✅ |
| JSON | .json | ✅ | ✅ |
| XML | .xml | ✅ | ✅ |
| RTF | .rtf | ✅ | ✅ |
| OpenDocument | .odt, .ods, .odp | ✅ | ✅ |

### 🤝 贡献指南

我们欢迎贡献！详情请参阅我们的[贡献指南](CONTRIBUTING.md)。

1. Fork 本仓库
2. 创建您的功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

### 📄 开源协议

本项目采用 MIT 协议开源 - 详见 [LICENSE](LICENSE) 文件。

---

<a name="繁體中文"></a>
## 🇹🇼 繁體中文

### 🎉 專案介紹

DocuMind AI 是一款智慧文件處理工具，它超越了簡單的格式轉換。雖然靈感來源於 `markitdown` 等工具，但 DocuMind AI 透過利用**大型語言模型（LLM）**來深度理解文件內容、提取有意義的洞察，並建構知識圖譜，從而實現差異化。

**核心差異化亮點：**
- 🧠 **AI 驅動分析**：不僅是轉換，更是理解您的文件
- 🔗 **知識圖譜提取**：可視化實體間的關係
- 🤖 **多模型支援**：相容 OpenAI、Azure OpenAI 及相容 API
- 📊 **智慧摘要**：自動提取關鍵點和主題
- 🌐 **15+ 格式支援**：PDF、DOCX、XLSX、PPTX、HTML 等

### ✨ 核心特性

| 特性 | 描述 | 狀態 |
|------|------|------|
| 📄 **文件轉換** | 將 15+ 格式轉換為乾淨的 Markdown | ✅ 就緒 |
| 🧠 **AI 分析** | 摘要、實體提取、情感分析 | ✅ 就緒 |
| 🔗 **知識圖譜** | 提取實體和關係 | ✅ 就緒 |
| ❓ **問答生成** | 從內容自動生成問題 | ✅ 就緒 |
| ✅ **行動項提取** | 提取任務和待辦事項 | ✅ 就緒 |
| 🎨 **精美 CLI** | 帶進度條的優雅終端介面 | ✅ 就緒 |
| 📦 **多格式匯出** | JSON、Cypher (Neo4j)、RDF 格式 | ✅ 就緒 |

### 🚀 快速開始

#### 安裝

```bash
# 克隆倉庫
git clone https://github.com/gitstq/documind-ai-pro.git
cd documind-ai-pro

# 安裝依賴
pip install -r requirements.txt

# 或以開發模式安裝
pip install -e .
```

#### 環境配置

```bash
# 設定 OpenAI API 金鑰
export OPENAI_API_KEY="your-api-key-here"

# 可選：為 Azure 或其他提供商設定自定義 API 基礎地址
export OPENAI_API_BASE="https://api.openai.com/v1"
```

#### 基本用法

```bash
# 轉換單個文件
documind convert document.pdf

# 帶 AI 分析的轉換
documind convert document.pdf --extract-kg --questions

# 批量轉換目錄
documind convert ./documents/ -o ./output/

# 僅分析文件
documind analyze document.pdf

# 提取知識圖譜
documind extract-kg document.pdf --format cypher
```

### 📖 詳細使用指南

#### 命令：`convert`

將文件轉換為 Markdown，可選 AI 分析。

```bash
documind convert [選項] 輸入路徑

選項：
  -o, --output 路徑       輸出目錄
  --no-ai                 禁用 AI 分析
  --model 文字            使用的 AI 模型 [預設: gpt-4o-mini]
  --api-key 文字          OpenAI API 金鑰
  --extract-kg            提取知識圖譜
  --questions             生成問題
  --actions               提取行動項
  --max-pages 整數        最大處理頁數
```

**範例：**

```bash
# 基礎轉換
documind convert report.pdf

# 完整分析並提取知識
documind convert report.pdf --extract-kg --questions --actions

# 使用特定模型
documind convert report.pdf --model gpt-4o

# 批量處理
documind convert ./input/ -o ./output/ --extract-kg
```

#### 命令：`analyze`

使用 AI 分析文件內容。

```bash
documind analyze [選項] 輸入路徑

選項：
  --model 文字    使用的 AI 模型
  --api-key 文字  OpenAI API 金鑰
```

**輸出包括：**
- 📋 執行摘要
- 📝 關鍵點（前 10 個）
- 🏷️ 主題和標籤
- 💭 情感分析
- 👥 命名實體

#### 命令：`extract-kg`

從文件提取知識圖譜。

```bash
documind extract-kg [選項] 輸入路徑

選項：
  -o, --output 路徑       輸出檔案路徑
  --format [json|cypher|rdf]  輸出格式 [預設: json]
```

**匯出格式：**
- **JSON**：標準圖譜格式，包含節點和邊
- **Cypher**：Neo4j 圖資料庫查詢語言
- **RDF**：語義網資源描述框架

### 💡 設計理念

DocuMind AI 基於三個核心原則構建：

1. **智慧優於轉換**：我們不只是轉換格式，更是理解內容
2. **開發者體驗**：豐富的 CLI、全面的 API 和詳盡的文件
3. **可擴展性**：模組化架構，易於定製

### 📦 支援的格式

| 格式 | 副檔名 | 轉換 | AI 分析 |
|------|--------|------|---------|
| PDF | .pdf | ✅ | ✅ |
| Word | .docx, .doc | ✅ | ✅ |
| Excel | .xlsx, .xls | ✅ | ✅ |
| PowerPoint | .pptx, .ppt | ✅ | ✅ |
| HTML | .html, .htm | ✅ | ✅ |
| Markdown | .md | ✅ | ✅ |
| 文字 | .txt | ✅ | ✅ |
| CSV | .csv | ✅ | ✅ |
| JSON | .json | ✅ | ✅ |
| XML | .xml | ✅ | ✅ |
| RTF | .rtf | ✅ | ✅ |
| OpenDocument | .odt, .ods, .odp | ✅ | ✅ |

### 🤝 貢獻指南

我們歡迎貢獻！詳情請參閱我們的[貢獻指南](CONTRIBUTING.md)。

1. Fork 本倉庫
2. 建立您的功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 開啟 Pull Request

### 📄 開源協議

本專案採用 MIT 協議開源 - 詳見 [LICENSE](LICENSE) 檔案。

---

<div align="center">

**Made with ❤️ by the DocuMind AI Team**

[⭐ Star us on GitHub](https://github.com/gitstq/documind-ai-pro) | [🐛 Report Issues](https://github.com/gitstq/documind-ai-pro/issues) | [💡 Request Features](https://github.com/gitstq/documind-ai-pro/discussions)

</div>
