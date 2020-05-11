# simptest框架httprunner版

# 一、项目简介：
通过django rest framework基于httprunner测试框架进行接口测试，简单的实现mvc模式的测试框架，由于是个人研究和开发，功能不完善，有待后期解决。

# 二、项目需求：
此次接口自动化测试框架采用的是以Python语言为脚本开发语言，httprunner接口测试框架，通过djangorestframework搭建mvc项目。目的是希望达成可配置测试用例，组合为测试套件，能自动运行脚本，自动生成测试报告，所以所有的接口测试用例使用页面统一管理，便于维护。

# 三、实现功能：
功能模块
![功能模块](https://github.com/zhujun6538/simptest-httprunner/blob/master/mytestproj/data/img/bz1.png)  

测试步骤  
可管理httprunner中的测试步骤中相关参数
![测试步骤](https://github.com/zhujun6538/simptest-httprunner/blob/master/mytestproj/data/img/bz1.png)  
![测试步骤](https://github.com/zhujun6538/simptest-httprunner/blob/master/mytestproj/data/img/bz2.png) 

测试用例管理
可管理httprunner中的测试用例中相关参数，点击运行将参数组合成json字典并运行httprunner
![测试用例管理](https://github.com/zhujun6538/simptest-httprunner/blob/master/mytestproj/data/img/yl1.png) 
![测试用例管理](https://github.com/zhujun6538/simptest-httprunner/blob/master/mytestproj/data/img/yl2.png) 

测试套件管理
可管理httprunner中的测试套件中相关参数，点击运行将参数组合成json字典并运行httprunner
![测试套件管理](https://github.com/zhujun6538/simptest-httprunner/blob/master/mytestproj/data/img/tj1.png) 
![测试套件管理](https://github.com/zhujun6538/simptest-httprunner/blob/master/mytestproj/data/img/tj2.png) 

测试报告管理
对测试结果进行统计，并实时查看测试报告
![测试报告管理](https://github.com/zhujun6538/simptest-httprunner/blob/master/mytestproj/data/img/csbg1.png) 
![测试报告管理](https://github.com/zhujun6538/simptest-httprunner/blob/master/mytestproj/data/img/csbg2.png) 

测试报告
httprunner生成的测试报告，内容比较基本
![测试报告](https://github.com/zhujun6538/simptest-httprunner/blob/master/mytestproj/data/img/csbg3.png) 







