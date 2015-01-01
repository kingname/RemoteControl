##代码目的

这是Gmail的海外转发程序，通过亚马逊AWS实现Gmail到邮件的转发，从而突破封锁。

##使用说明

请参看这篇文章，讲述了亚马逊EC2主机上Gmail API环境的搭建。
[使用AWS亚马逊云搭建Gmail转发服务（一）](http://kingname.info/2014/12/30/%E4%BD%BF%E7%94%A8AWS%E4%BA%9A%E9%A9%AC%E9%80%8A%E4%BA%91%E6%90%AD%E5%BB%BAGmail%E8%BD%AC%E5%8F%91%E6%9C%8D%E5%8A%A1/)

这篇文章讲解了本程序的使用说明。
[使用AWS亚马逊云搭建Gmail转发服务（二）](http://kingname.info/2014/12/31/%E4%BD%BF%E7%94%A8%E4%BA%9A%E9%A9%AC%E9%80%8A%E4%BA%91AWS%E6%90%AD%E5%BB%BAGmail%E9%82%AE%E4%BB%B6%E8%BD%AC%E5%8F%91%E6%9C%8D%E5%8A%A1%E4%BA%8C/)

要是退出session后，程序仍然能够在后台运行，需要使用Linux的screen命令。使用说明请看这篇日志：
[断电不断网——Linux的screen](http://kingname.info/2015/01/01/Linux%E7%9A%84screen/)