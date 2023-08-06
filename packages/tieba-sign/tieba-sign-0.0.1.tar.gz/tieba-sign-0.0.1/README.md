## 百度贴吧自动签到

### 安装
```
pip install --user tieba-sign
```

### 使用
```
tieba-sign [--cookie YOUR_BAIDU_COOKIE] [-f cookie_file]
```

###  
```
from tieba import Tieba

tieba=Tieba("Your Cookie")
tieba.get_bars()
tieba.batch_sign(1)
```