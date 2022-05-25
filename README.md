# Python-中国大学MOOC(慕课)课程信息爬取
参考文章：https://www.ijly.top/2018/12/03/python-%e7%88%ac%e5%8f%96%e4%b8%ad%e5%9b%bd%e5%a4%a7%e5%ad%a6%e6%85%95%e8%af%bemooc%e8%af%be%e7%a8%8b/<br>
爬取中国大学慕课网全站课程，包括课程的课程名、开课时间、老师、评论以及每门课程下的评论等信息<br>
课程信息包括：类别	课程名	课程ID	开课次数	参加人数	老师	课程概述	爬取时间<br>
课程评论信息包括：课程名	课程ID	评分	评论总数	用户名	用户主页	用户评分	用户评论	评论时间	点赞数
## 原理
利用Python3+Chrome+Selenium WebDrive
## 安装爬取环境
安装Chrome<br>
安装Selenium<br>
安装Chrome driver<br>
## 爬取步骤
依次根据课程种类，如：法学、工学、计算机、教育教学、经济管理等，依次爬取每类课程下的课程信息
## 爬取文件目录结构
mooc<br>
│  mooc163.py<br>
├mooc<br>
│   │   <br>
│   ├法学<br>
│   │   │<br>
│   │   mooc.csv(课程信息)<br>
│   │   mooc_海商法_DLMU-1001983016_evaluate.csv(评论信息)<br>
│   │   mooc_合同法基础_SWU-1003432002_evaluate.csv<br>
│   │   ...<br>
│   ├工学<br>
│   │   │<br>
│   │   mooc.csv(课程信息)<br>
│   │   mooc_3D打印技术及应用_NWPU-1001911003_evaluate.csv(评论信息)<br>
│   │   ...<br>
│   ├...
## mooc.csv(课程信息)
类别	课程名	课程ID	开课次数	参加人数	老师	课程概述	爬取时间
## mooc_XXXX_XXXX.csv(评论信息)
课程名	课程ID	评分	评论总数	用户名	用户主页	用户评分	用户评论	评论时间	点赞数
