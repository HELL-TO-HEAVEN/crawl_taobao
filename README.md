# crawl_taobao
用selenium+pyquery爬取淘宝自定义商品的信息，同时保存到MongoDB<br>
-------
分为<font color=red>单进程爬取（CRAWL.py）`与`多进程爬取`</font>


## 补充：
    1、在代码里能看到有很多cookies，这些都是为了对付淘宝的登录操作，而淘宝的cookies有很多个，于是通过一个很好的插件 <font color=red>EditThisCookie</font> 把所有的cookies都按照序号导出来，这里有个问题就是导出的cookies字典有些地方不是字符串形式，所以我再通过两行代码把不是字符串的地方（e.g. false和true）变成字符串；

    2、由于一些大型网站都具有较强反扒的能力，淘宝网站就能通过某些机制判断是否是selenium控制浏览器，比如<font color=red>参数 window.navigator.webdriver，若为true则证明有selenium，undefined就没有
    `解决方案：` 
    A（推荐）、给Chrome()加上option参数（实验性参数），执行js代码屏蔽window.navigator.webdriver；
    B、往网站里注入代码屏蔽它
    
    

