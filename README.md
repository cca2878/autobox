# AutoBox

一款用于批量查询并导出公主连结简中服账号信息的工具。

## Features

- 支持自动和手动验证，在自动验证不可用时自动转为手动。

- 多线程执行支持（最高8线程~~照顾人类手速~~

- 一键导出相关信息到Excel文件，以支持更复杂的应用。

## How to use

你可以选择直接运行Python源代码或从Release中下载预先构建的可执行文件来运行。

请注意，程序会在其相同目录下存储cache（cache文件夹），因此请尽量在独立目录中运行。

- ### 直接运行

  推荐使用Python3.8，并安装`requirements.txt`中的依赖。

  拉取项目后，运行项目根目录内的`main.py`文件。

- ### 预构建可执行文件运行

  ~~不会有人运行这玩意还要教罢。~~

## Todo List

- [ ] 支持选取单个或多个角色导出。

- [ ] 支持选取单个或多个账户执行。

- [ ] 添加角色为行、账号为列的导出模式。

- [ ] 便利化账号管理交互方式。

## Open Source Information

本项目的部分代码来自以下开源项目，向他们表示致敬和感谢。

- 登录、验证、查询相关：[cc004/autopcr](https://github.com/cc004/autopcr)
