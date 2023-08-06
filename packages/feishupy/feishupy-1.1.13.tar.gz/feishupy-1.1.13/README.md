[![PyPI](https://img.shields.io/pypi/v/feishupy.svg)](https://pypi.org/project/wechatpy)

```
 _______  _______ _________  _______                          _______          
(  ____ \(  ____ \\__   __/ (  ____ \|\     /||\     /|      (  ____ )|\     /|
| (    \/| (    \/   ) (    | (    \/| )   ( || )   ( |      | (    )|( \   / )
| (__    | (__       | |    | (_____ | (___) || |   | |      | (____)| \ (_) / 
|  __)   |  __)      | |    (_____  )|  ___  || |   | |      |  _____)  \   /  
| (      | (         | |          ) || (   ) || |   | |      | (         ) (   
| )      | (____/\___) (___ /\____) || )   ( || (___) |      | )         | |   
|/       (_______/\_______/ \_______)|/     \|(_______)      |/          \_/   
                                                                       
```


FeiShuPY (FeiShu SDK for Python)
==


> A package for FeiShu, Implement API.(已实现部分接口,欢迎扩展)



### 功能特性

- 调用时支持切换Token

- 自定义Storage

  

### 安装

```
pip install feishupy
```



### 使用示例

```
from feishupy import FeiShuClient, TOKEN_TYPE_APP_ACCESS_TOKEN_INTERNAL

if __name__ == '__main__':
    fs_client = FeiShuClient(
        app_id=os.environ.get('APP_ID') or 'INPUT_APP_ID_HERE',
        app_secret=os.environ.get('APP_SECRET') or 'INPUT_APP_SECRET_HERE',
    )
    # 获取 access_token
    access_token = fs_client.access_token(token_type=TOKEN_TYPE_APP_ACCESS_TOKEN_INTERNAL)

    # code2session
    result = fs_client.mina.code2session(code='5b56a2993845f07e')

    # 获取通讯录授权范围
    result = fs_client.contact.scope_get()

    # 获取角色列表
    result = fs_client.contact.role_list()

```





### Token类型

- app_access_token ：访问App资源相关接口。
- app_access_token_internal ：访问App资源相关接口(自建应用)。
- tenant_access_token ：访问企业资源相关接口。
- tenant_access_token_internal ：访问企业资源相关接口(自建应用)。
- user_access_token ：访问用户资源相关接口。





### 问题反馈

使用 [GitHub Issues](https://github.com/WUWUTech/feishupy/issues) 进行问题追踪和反馈。


###  References
- [官方文档](https://open.feishu.cn/)

### 感谢

- [jxtech/wechatpy](https://github.com/jxtech/wechatpy)




### License 
---
This work is released under the MIT license. A copy of the license is provided in the LICENSE file.


