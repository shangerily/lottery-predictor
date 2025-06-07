#!/bin/bash
# 大乐透预测系统 - 一键构建脚本

echo "🎯 大乐透预测系统 - 开始构建APK"
echo "=================================="

# 检查文件
echo "📋 检查必要文件..."
files=("main.py" "lottery_mobile.py" "buildozer.spec" "requirements_mobile.txt")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ 缺少文件: $file"
        exit 1
    fi
done

# 安装依赖
echo "📦 安装构建依赖..."
pip install buildozer cython kivy pandas numpy

# 构建APK
echo "🔨 开始构建APK..."
buildozer android debug

# 检查结果
if [ -f bin/*.apk ]; then
    echo "🎉 构建成功！"
    echo "📱 APK文件位置: bin/"
    ls -la bin/*.apk
else
    echo "❌ 构建失败，请检查错误信息"
    exit 1
fi
