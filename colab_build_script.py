"""
大乐透预测系统 - Google Colab APK构建脚本
在Colab中运行此脚本来构建APK
"""

# 安装系统依赖
!apt update
!apt install -y openjdk-8-jdk

# 设置JAVA_HOME
import os
os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-8-openjdk-amd64'

# 安装Python依赖
!pip install buildozer cython
!pip install kivy pandas numpy

# 上传项目文件
from google.colab import files
print("请上传以下文件:")
print("- main.py")
print("- lottery_mobile.py") 
print("- buildozer.spec")

# 构建APK
!buildozer android debug

# 下载APK
print("\n构建完成！正在准备下载...")
import glob
apk_files = glob.glob("bin/*.apk")
if apk_files:
    for apk in apk_files:
        files.download(apk)
        print(f"✅ APK文件已准备下载: {apk}")
else:
    print("❌ 未找到APK文件，请检查构建日志")
