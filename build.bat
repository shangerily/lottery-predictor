@echo off
chcp 65001 >nul
echo 🎯 大乐透预测系统 - 开始构建APK
echo ==================================

echo 📋 检查必要文件...
if not exist "main.py" (
    echo   ❌ 缺少文件: main.py
    pause
    exit /b 1
)
if not exist "lottery_mobile.py" (
    echo   ❌ 缺少文件: lottery_mobile.py
    pause
    exit /b 1
)
if not exist "buildozer.spec" (
    echo   ❌ 缺少文件: buildozer.spec
    pause
    exit /b 1
)
echo   ✅ 所有文件检查完成

echo 📦 安装构建依赖...
pip install buildozer cython kivy pandas numpy

echo 🔨 开始构建APK...
buildozer android debug

if exist "bin\*.apk" (
    echo 🎉 构建成功！
    echo 📱 APK文件位置: bin\
    dir bin\*.apk
) else (
    echo ❌ 构建失败，请检查错误信息
)

pause
