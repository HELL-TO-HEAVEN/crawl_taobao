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
        通过分析源码，network请求等等，发现了多进程请求的网页url的构造方法（打开后很惊讶的发现是jsonp类型的，很好爬取，直接用json的方法，最多结合一下正则表达式就获得了商品信息，不过让人怀疑是不是淘宝是不是用来误导爬虫的）,注意构造时有个jsonp参数，把他删去即可得到json类型，因此我构造的url是没有jsonp参数的
 ![url在这里](https://github.com/HELL-TO-HEAVEN/crawl_taobao/blob/master/%E5%AF%BB%E6%89%BEurl.png)
 <br>
 可以看到左边的search?data-key=xxxx&data-value=xxxx，（为了可观性，方便找到url，可选择右键Name，domain），能看到44、88、 132的数字，证明一次页面就改变44， 另外还有参数bcoffset、 ntoffset，通过等差数列构造。
 <br>
 特别是有个_ksTS参数，那个明显就是时间戳，只不过记忆里时间戳要不是13位的，要不就是16位的，这个参数却是 13位_4位类型的。好奇心驱使试了一下打印time.time, 发现的确是17位浮点数，那就好办咯～
 <br>
《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《
 
 结果：
-------------
单进程花了16分钟，原因分析应该是因为用的是selenium，页面要渲染，同时也加了几个time.sleep;<br>
        ![如图](https://github.com/HELL-TO-HEAVEN/crawl_taobao/blob/master/single_result.png)
        
 <br>
 *******************
 <br>
多进程花了20秒，因为直接用requests请求url（通过规律找出），而这个url页面打开后发现是 jsonp 类型，毫无渲染<br>
        ![如图](https://github.com/HELL-TO-HEAVEN/crawl_taobao/blob/master/url%E9%A1%B5%E9%9D%A2.png)
        ![如图](https://github.com/HELL-TO-HEAVEN/crawl_taobao/blob/master/multi_result.png)
        
<br>
接下来进行数据分析
        
