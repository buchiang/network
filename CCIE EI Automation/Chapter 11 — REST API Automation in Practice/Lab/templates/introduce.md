这是 Jinja2 的一个高级特性，叫 Template Inheritance（模板继承）。

不过我先说明一点：

按照我们 Workbook 的 Frozen Roadmap，目前（Chapter 8）我们不应该正式引入 extends 和 block。

因为 Chapter 7 我们只学习了：

Variables
Loops
Conditions
Macros
Include

没有学习 Template Inheritance。

所以这里我只做概念介绍，不把它加入 Workbook 内容。

为什么会有 extends？

假设你开发一个网站。

所有网页都有：

========================
Company Logo

Navigation Bar

------------------------

页面内容

------------------------

Copyright 2026
========================

如果有 100 个页面，

难道每个 HTML 都复制一次？

当然不好。

所以 Jinja2 发明了：

Inheritance（继承）

base.html

例如：

<html>

<head>
<title>Company</title>
</head>

<body>

<h1>Company Logo</h1>

{% block content %}
{% endblock %}

<hr>

Copyright

</body>

</html>

注意：

这里出现：

{% block content %}
{% endblock %}

它表示：

这里留一个"空位"。

以后别人可以填。

然后：

home.html
{% extends "base.html" %}

{% block content %}

Welcome to our website.

{% endblock %}

这里：

第一句：

{% extends "base.html" %}

意思就是：

继承 base.html

然后：

把：

{% block content %}

里面的内容：

替换掉父模板里的：

{% block content %}

最后 Render：

得到：

<html>

<head>
<title>Company</title>
</head>

<body>

<h1>Company Logo</h1>

Welcome to our website.

<hr>

Copyright

</body>

</html>

可以看到：

Logo

Copyright

都是：

base.html

提供的。

只有：

中间内容：

来自：

home.html。

block 是什么？

可以理解成：

一个可以被子模板覆盖（Override）的区域。

例如：

{% block menu %}
{% endblock %}

这里：

menu

只是：

Block 的名字。

以后：

子模板：

{% block menu %}

Network Automation

{% endblock %}

就会把：

父模板：

这个区域：

替换掉。

extends 做了什么？

一句话：

{% extends "base.html" %}

表示：

不要重新写整个模板，而是在 base.html 的基础上修改。

所以：

Inheritance：

像：

Python：

class Router(Device):

Router：

继承：

Device。

Jinja2：

router.j2

extends

base.j2

Router Template：

继承：

Base Template。

为什么 Web 开发喜欢用？

因为：

所有网页：

几乎都有：

Logo

↓

Navigation

↓

Footer

不同的：

只是：

中间正文。

所以：

Inheritance

非常适合。

为什么网络自动化很少用？

Cisco 配置：

通常不是：

固定框架

↓

正文

而是：

很多独立模块：

hostname

↓

interfaces

↓

OSPF

↓

BGP

↓

ACL

↓

SNMP

它们之间：

没有：

父模板

子模板

关系。

所以：

网络自动化：

几乎都是：

{% include "hostname.j2" %}

{% include "interface.j2" %}

{% include "ospf.j2" %}

而不是：

extends
一个简单对比
Include（我们 Workbook 使用）
main.j2
│
├── hostname.j2
├── interface.j2
└── ospf.j2

可以理解成：

把多个小模板拼接成一个大模板。

Extends（Web 常用）
base.html
        │
        ├── home.html
        ├── about.html
        └── contact.html

可以理解成：

多个页面共享同一个骨架，每个页面只修改自己的内容。

对我们的 Workbook 的建议

我建议保持目前的路线，不在 Chapter 8 引入 extends 和 block。

原因有三点：

网络自动化中 include 的使用频率远高于 extends，更符合 Cisco 配置模板的组织方式。
引入 extends 会增加新的 Jinja2 概念，但 Chapter 8 的目标是整合前面章节，而不是继续扩展模板语法。
如果以后在 Chapter 17 或 Chapter 18 讨论大型企业模板库（例如多厂商、多角色模板体系），再介绍 Template Inheritance 会更自然，也更能体现它的价值。

因此，当前 Workbook 保持以 include 为核心的模板设计是更合理的选择。