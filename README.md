# 深圳工业大学校园网自动登录脚本

主要用于在远程连接校内设备时校园网登录挂掉的情况，特别是在 **2024 年**后，校园网基本 7 天需要重新登录一次。

## 使用
```
git clone https://github.com/kajimi16/auto_wifi.git
```

### 使用 uv 管理项目
```
pip install uv 
uv init 
uv add selenium
```
在完成后，即可使用`uv run main.py`，使用该脚本

