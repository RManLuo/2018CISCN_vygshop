题目说明:

得到/tmp/flag

Hint1: MarkDown

Hint2: 接口格式了解一下

Hint3: 手动触发

更新命令

--build-arg FLAAAAAG 

```
ARG FLAAAAAG
ENV FLAAAAAG ${FLAAAAAG:-CISCN{this_is_a_sample_flag}}
```





exp使用说明：

库依赖同deploy里requirement.pip。默认先检查漏洞2，失败后**再**检查漏洞1，如需同时检查，请将

```
        if sol2:
            print 'exp2:',sol2.group()
            return True
```

的`return True`注释。

检查漏洞1时涉及到暴力枚举，如影响效率请见谅。