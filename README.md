兔窝保卫战
==========
游戏是参考一篇网络文章和其中的代码制作出来的，原文名称和地址如下：[《青少年如何使用Python开始游戏开发》](http://www.oschina.net/translate/beginning-game-programming-for-teens-with-python)。
个人觉得原文中有些代码有问题，因此对其进行了修改，若您觉得代码有问题，欢迎指正。源代码在bunny.py中可以查看，修改后的代码可以在dawei_bunny.py中查看。下面列出有问题的地方和具体问题：

- 第五步：射击吧，兔子！改进代码
    - 问题1：代码#6.2中有个嵌套for循环，内部for循环可以拿到外面和外部for循环有同等缩进级别，否则每更改一个子弹位置都需要重新绘制一遍所有子弹，效率太低。
    - 问题2：代码#6.2中有个index变量，用于记录当前子弹编号，但是无法实现此效果，因为每次循环都会把其置为0，因此每次删除的都是子弹列表中的第一个子弹。
    - 问题3：代码#6.2中在正在遍历的列表中删除该列表中的元素，会导致无法预料的错误，尽管当前程序不会出错。

