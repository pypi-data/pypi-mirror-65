# SpecCreator

> 顾名思义，俺是创建私有库模板的脚本
> 顺手还做个检查，打个静态库（.a 和.framework）包啥的

## 我能干啥

1. 创建标准私有库的模板
2. 帮你写一部分 podspec的语句，能够符合提供 **源码/.a/.framework** 三种方式的切换
3. 能帮你检查写的库能不能lint通过
4. 帮你打包 .framework 的静态库
5. 帮你打包 .a 的静态库


## 组件发布
相关文档：https://blog.csdn.net/liangjun_feng/article/details/80037315

1. 开发完毕后，先git commit
2. 如果要发布，修改setup.py 里的version字段，修改specCreator.py 里的__version__ 字段, 提交
3. 运行命令：`python setup.py sdist` 生成pip安装包
4. 运行命令：`twine upload ./dist/specCreator-1.0.17.tar.gz` 上传安装包。注意版本信息要改。

## 用法


1. 前提：
    - 你确实要从0开始创建一个私有库，不符合请用其他的功能
    - 如果已经有私有库了，如果不符合cocopods标准库模板，请慎用打包功能，目前还没有测试
    - 向张岩松申请一个git仓库地址，比如，我这里申请的是 `LJCache`

2. 如果前提都满足了，就可以用这个脚本了，首先安装环境，运行
    
    ``` ruby
    python specCreator env
    ```
    来安装必要的环境，这里因为每个人的电脑环境不同，可能检测结果不一样。最好多运行几遍，直到运行后没有反应位置，当然如果出现反应，请对照提示安装，或者找 我。我是谁？ 我是韩达~😓

3. 环境没问题了，就要创建私有库了。运行：

    ``` ruby
    python specCreator.py init
    ```
    
   例如：
   
   ``` ruby
     ~/Documents/specCreator  python specCreator.py init
请输入您的girrit用户名：
handa
请输入您要创建的工程目录：（tips:工程名要和girrit的工程名保持一致,请区分大小写,例如要创建LJCache的spec请输入：/Users/handa/Documents）
/Users/handa/Documents
请输入要创建的工程名，如：LJCache
LJCache

    ```
    
    之后会生成一个目录,如图：

4. 然后就可以在Example里敲代码了。（注意，如果新增一个文件，需要再example 里pod update下才能在工程里面引用header）
5. 帮你把PodSpec文件改为如下结构，可以区分源码和二进制。
    打包前先改下podspec tag号和commit地址，保证打的包是最新的。
6.改完podspec，需要检查写的是否正确，运行

 ``` ruby
 python specCreator.py check
 ```
 会帮你检测spec文件书写是否准确
 
7. 利用命令 `python specCreator.py package` 可以把subspec打包成 .framework 形式，并把静态库放到 特定位置，如：
   LJCache有两个subspec，一个是Foudation ，一个是UIKIt，生成的静态库会自动放到以下两个位置：
     LJCache/Framework/Foundation/LJCacheFoundation.framework
     LJCache/Framework/UIKit/LJCacheUIKit.framework
     
8. 利用命令：

    ``` ruby
    python specCreator.py packageA
    ```
    可以把subspec打包成 `.a` 文件分别放到：
    
    LJCache/Archive/Foundation/libLJCacheFoundation.a
    LJCache/Archive/UIKit/libLJCacheUIKit.a

9. 打完包后commit，并提到远程，
10. 发布，完成

