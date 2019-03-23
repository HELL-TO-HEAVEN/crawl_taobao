# crawl_taobao
用selenium+pyquery爬取淘宝自定义商品的信息，同时保存到MongoDB，后续进行数据分析<br>
-------

考虑分为`单进程爬取（CRAWL.py）`与`多进程爬取（这个还在考虑中：如何构造淘宝的请求url）`

************

## 补充：
    1、强推多进程爬取；
    2、在代码里能看到有很多cookies，这些都是为了对付淘宝的登录操作，而淘宝的cookies有很多个，于是通过一个很好的插件 <font color=red>EditThisCookie</font> 把所有的cookies都按照序号导出来，这里有个问题就是导出的cookies字典有些地方不是字符串形式，所以我再通过两行代码把不是字符串的地方（e.g. false和true）变成字符串；

    3、由于一些大型网站都具有较强反扒的能力，淘宝网站就能通过某些机制判断是否是selenium控制浏览器，比如<font color=red>参数 window.navigator.webdriver，若为true则证明有selenium，undefined就没有
    `解决方案：` 
    A（推荐）、给Chrome()加上option参数（实验性参数），执行js代码屏蔽window.navigator.webdriver；
    B、往网站里注入代码屏蔽它
    
    
**********
##PS:
淘宝有时候需要登录验证，有时候又不需要（貌似记得是先手动开浏览器登录一次，再通过selenium控制登录，而这个肯定是不成功的（即使此时手动在被控制的browser上登录也会失败），此时不关闭这个browser，过一段时间后，再次在该browser上登录，成功）

***************

## 更新：
        通过分析源码，network请求等等，发现了请求的网页url的构造方法（打开后很惊讶的发现是jsonp类型的，很好爬取，直接用json的方法，最多结合一下正则表达式就获得了商品信息，不过让人怀疑是不是淘宝是不是用来误导爬虫的）
        
        结果：
        
