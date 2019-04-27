# html2Book

#### 介绍
把通过gitbook编译后的html目标文件反向生成markdown文件进而生成用于kindle的mobi格式电子书  
以及适合kindle的pdf文件  
及适合PC的pdf文件
自动生成book.json 支持自定义封面 不自定义则根据书名生成封面(书名不变样式不变)
#### 软件架构
软件架构说明


#### 安装教程

##### Windows
1. 安装pandoc  
   https://github.com/jgm/pandoc/releases  下载.msi安装包安装
2. 安装gitbook
```
npm install gitbook-cli -g
```

##### MAC
1. 安装pandoc  
```
brew install pandoc
```
2. 安装gitbook
```
npm install gitbook-cli -g
```

#### 使用说明
将html2MobiBook.py 拷贝到最顶层的目录索引文件index.html所在目录  
只生成mobi格式电子书
```
python3 html2Book.py bookName mobi
```

只生成适合kindle的pdf格式电子书
```
python3 html2Book.py bookName pdfk
```

只生成适合PC的pdf格式电子书
```
python3 html2Book.py bookName pdfpc
```

同时生成三种格式电子书
```
python3 html2Book.py bookName all
```

当根据索引生成的目录SUMMARY.md不如人意时可手动更改SUMMARY.md然后执行命令时加上 SUMMARY.md 选项即可使用当前SUMMARY.md生成书籍 否则SUMMARY.md会根据index.html生成
```
python3 html2Book.py bookName all SUMMARY.md
```

当html中含有数学公式时pandoc对html转markdown做得还不是很好这时gitbook build会出错 我们可以根据出错信息把对应的md文件改对之后执行命令时加上skip选项即可在不重新生成md文件的条件下生成书籍
```
python3 html2Book.py bookName all skip
```

若想即不重新生成SUMMARY.md 又不重新生成markdown文件则加上ss选项
```
python3 html2Book.py bookName all ss
```


### 注意
在windows下可能会出现 Error with command "svgexport"错误
解决办法: npm install svgexport -g

在html有数学公式的情况下如果build出错 则根据错误信息改对应的markdown文件再手动跑命令  
gitbook build
再根据错误信息改markdown文件再build 改一处build一次因为大部分数学公式还是没问题的 也许改一两处就好了  
修改数学公式可以在线编辑: https://www.codecogs.com/latex/eqneditor.php  

支持封面  
默认生成的book.json中variables属性是:  

```
    "variables": {
        "cover": "null"
    }
``` 

表示根据书名生成封面(书名不变 封面样式不变)

```
        "cover": "cur"
```

根据根目录下的cover.jpg生成封面

```
        "cover": "coverN"
```

生成与./mycovers/coverN.jpg样式一样的封面





