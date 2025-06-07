# 🎯 大乐透预测系统 - 快速构建APK指南

## 📦 已准备的文件
- ✅ `lottery_apk_source_20250607_1525.zip` - 完整项目源码包
- ✅ `.github/workflows/build-android.yml` - GitHub自动构建配置
- ✅ `colab_build_script.py` - Google Colab构建脚本

## 🚀 方法1: GitHub Actions自动构建 (推荐)

### 步骤1: 创建GitHub仓库
1. 访问 https://github.com
2. 点击 "New repository"
3. 仓库名称: `lottery-predictor`
4. 设置为 Public
5. 点击 "Create repository"

### 步骤2: 上传文件
1. 在新仓库页面点击 "uploading an existing file"
2. 拖拽以下文件到页面:
   - `main.py`
   - `lottery_mobile.py`
   - `buildozer.spec`
   - `requirements_mobile.txt`
3. 创建文件夹 `.github/workflows/`
4. 上传 `build-android.yml` 到该文件夹
5. 点击 "Commit changes"

### 步骤3: 启动构建
1. 在仓库页面点击 "Actions" 标签
2. 点击 "Build Android APK" 工作流
3. 点击 "Run workflow" 按钮
4. 等待构建完成 (约10-15分钟)

### 步骤4: 下载APK
1. 构建完成后，在Actions页面找到成功的构建
2. 点击构建记录
3. 在 "Artifacts" 部分下载 `lottery-predictor-apk`
4. 解压得到APK文件

## 🧪 方法2: Google Colab构建

### 步骤1: 打开Colab
1. 访问 https://colab.research.google.com
2. 点击 "新建笔记本"

### 步骤2: 运行构建脚本
1. 复制 `colab_build_script.py` 的内容
2. 粘贴到Colab单元格中
3. 运行单元格 (Ctrl+Enter)

### 步骤3: 上传文件
当脚本提示时，上传以下文件:
- `main.py`
- `lottery_mobile.py`
- `buildozer.spec`

### 步骤4: 等待构建
- 构建过程约15-20分钟
- 完成后自动下载APK文件

## 💻 方法3: Replit在线构建

### 步骤1: 创建项目
1. 访问 https://replit.com
2. 点击 "Create Repl"
3. 选择 "Python" 模板
4. 项目名称: `lottery-predictor`

### 步骤2: 上传文件
1. 在文件管理器中上传所有项目文件
2. 确保文件结构正确

### 步骤3: 安装依赖
在终端运行:
```bash
pip install buildozer cython
pip install kivy pandas numpy
```

### 步骤4: 构建APK
在终端运行:
```bash
buildozer android debug
```

### 步骤5: 下载APK
构建完成后，在 `bin/` 文件夹中找到APK文件

## 📱 预期结果

### APK信息
- **应用名称**: 大乐透预测系统
- **包名**: com.lottery.predictor  
- **版本**: 1.0
- **文件大小**: 15-25MB
- **支持系统**: Android 5.0+

### 功能特性
- ✅ 统计分析预测
- ✅ 历史数据管理
- ✅ 预测结果保存
- ✅ 移动端优化界面
- ✅ 离线使用

## 🔧 故障排除

### 构建失败
1. 检查所有文件是否上传完整
2. 确认 `buildozer.spec` 配置正确
3. 查看构建日志中的错误信息

### APK安装失败
1. 在手机设置中允许"未知来源"应用安装
2. 确认Android版本 >= 5.0
3. 检查存储空间是否充足

## 💡 推荐流程

**最简单的方式是使用GitHub Actions:**

1. 📁 解压 `lottery_apk_source_20250607_1525.zip`
2. 🌐 在GitHub创建新仓库
3. 📤 上传所有文件
4. ⚡ 在Actions中运行构建
5. 📱 下载生成的APK

**预计时间**: 5分钟设置 + 15分钟构建 = 20分钟总计

## 📞 需要帮助?

如果遇到问题，请提供:
1. 使用的构建方法
2. 错误信息截图
3. 构建日志

祝您构建成功！🎉 