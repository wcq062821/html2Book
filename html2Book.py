# -*- coding: utf-8 -*-
# @Author: wcq
# @Date:   2019-04-24 19:30:13
# @Last Modified by:   skfwe
# @Last Modified time: 2019-04-26 20:25:14
import os
import sys
import re
from time import sleep
import datetime
import json
import random
import hashlib
from PIL import Image, ImageDraw, ImageFont

def Usage():
    print('python3 %s <bookName> <mobi | pdfk | pdfpc | all> [SUMMARY.md | skip | ss]'%(os.sys.argv[0]))
    print('SUMMARY.md                   --use current SUMMARY.md')
    print('skip                         --does\'t regenerate markdown files')
    print('ss                           --both SUMMARY.md and skip')
    exit(0)

class generateCover():
    coverColor = ({'name':'cover0', 'backgroundColor':(78,9,41), 'fontColor':(123, 31, 231)},
        {'name':'cover1', 'backgroundColor':(98,111,27), 'fontColor':(188, 125, 70)},
        {'name':'cover2', 'backgroundColor':(247,74,200), 'fontColor':(55, 249, 158)},
        {'name':'cover3', 'backgroundColor':(122,118,79), 'fontColor':(17, 53, 12)},
        {'name':'cover4', 'backgroundColor':(151,55,45), 'fontColor':(85, 228, 60)},
        {'name':'cover5', 'backgroundColor':(100,0,182), 'fontColor':(43, 249, 170)},
        {'name':'cover6', 'backgroundColor':(211,112,169), 'fontColor':(114, 21, 74)},
        {'name':'cover7', 'backgroundColor':(92,187,139), 'fontColor':(51, 30, 248)},
        {'name':'cover8', 'backgroundColor':(203,138,54), 'fontColor':(140, 201, 38)},
        {'name':'cover9', 'backgroundColor':(123,137,189), 'fontColor':(177, 183, 162)},
        {'name':'cover10', 'backgroundColor':(238,220,102), 'fontColor':(146, 7, 239)},
        {'name':'cover11', 'backgroundColor':(102,12,59), 'fontColor':(250, 30, 159)},
        {'name':'cover12', 'backgroundColor':(57,12,22), 'fontColor':(49, 172, 27)},
        {'name':'cover13', 'backgroundColor':(97,102,122), 'fontColor':(163, 159, 21)},
        {'name':'cover14', 'backgroundColor':(8,99,32), 'fontColor':(208, 144, 192)},
        {'name':'cover15', 'backgroundColor':(73,220,192), 'fontColor':(249, 222, 120)},
        )
    coverDir = 'mycovers'
    deWidth = 758
    deHeight = 1024
    deFontSize = 48
    deTitleName = '我人有的和主产不为这工要在地一上是asdfvgbhnjmk要在地一上是gbhnjmk要在地一上是bhnjmk'
    def __init__(self):
        self.deTitleName = self.deTitleName.upper()
        if not os.path.exists(self.coverDir):
            os.mkdir(self.coverDir)
            for c in self.coverColor:
                self.generateCover(self.deTitleName, self.deWidth, self.deHeight, self.deFontSize, c)
        else:
            self.generateCover(self.deTitleName, self.deWidth, self.deHeight, self.deFontSize, self.coverColor[4])


    def generateCover(self, titleName, width, height, fontSize, coverName=None):
        if isinstance(coverName, dict):
            cover = coverName
            jpgName = os.path.join(self.coverDir, cover['name']+'.jpg')
        else:
            jpgName = 'cover.jpg'
            if coverName is None:
                # use cover according to titleName
                coverIndex = int(hashlib.sha256(titleName.encode('utf-8')).hexdigest(), 16)%len(self.coverColor)
                print('use %s'%(self.coverColor[coverIndex]['name']))
                cover = self.coverColor[coverIndex]
            else:
                for c in self.coverColor:
                    if c['name'] == coverName:
                        cover = c
                        break
                else:
                    print('%s not found!'%(os.path.join(self.coverDir, coverName)))
                    exit(0)

        bgcolor = cover['backgroundColor']
        #print('bgcolor : ', bgcolor)
        #创建画面对象
        im = Image.new('RGB', (width, height), bgcolor)
        #创建画笔对象
        draw = ImageDraw.Draw(im)
        #调用画笔的point()函数绘制噪点
        for i in range(0, 200):
            x = random.randrange(0, width)
            y = random.randrange(0, height)
            fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
            draw.point((x, y), fill=fill)
            draw.point((x-1, y-1), fill=fill)
            draw.point((x+1, y-1), fill=fill)
            draw.point((x-1, y+1), fill=fill)
            draw.point((x+1, y+1), fill=fill)

        #构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
        import platform
        if platform.system() == 'Windows':
            font = ImageFont.truetype('static/STXIHEI.TTF', fontSize)
        elif platform.system() == 'Darwin':
            font = ImageFont.truetype('static/Songti.ttc', fontSize)
        else:
            print('have no %s font file '%platform.system())

        #font = ImageFont.load_default().font
        #构造字体颜色
        titleLen = fontSize*len(titleName)
        tmpWidth = width
        spaceCnt = 2
        while True:
            titleStartX = (tmpWidth - titleLen)//spaceCnt
            if titleStartX >= fontSize:
                break
            else:
                tmpWidth += width
                spaceCnt += 2

        titleStartY = random.randint(fontSize, height//2)
        lineLen = len(titleName)//(tmpWidth//width)
        lineLenPixel = lineLen*fontSize

        # import textwrap
        # lines = textwrap.wrap(titleName, width=lineLen)
        # for line in lines:
        #     print('line : ', line)
        # exit(0)

        fontcolor = cover['fontColor']
        # print('titleStartX : %d, titleStartY : %d'%(titleStartX, titleStartY))
        pos = 0
        for i in range((tmpWidth//width) + 1):
            if pos >= len(titleName):
                break
            text = titleName[pos:pos+lineLen]
            for j in range(0, fontSize):
                realLineLenPixel = draw.textsize(text, font=font)[0]
                if realLineLenPixel < lineLenPixel:
                    text = titleName[pos:pos+lineLen+j]
                elif realLineLenPixel > lineLenPixel:
                    text = titleName[pos:pos+lineLen+j-2]
                    pos = pos+lineLen+j-2
                    break
                else:
                    text = titleName[pos:pos+lineLen+j-1]
                    pos = pos+lineLen+j-1
                    break
                if pos+lineLen+j >= len(titleName):
                    pos = pos+lineLen+j
                    break

            if i == 0:
                lineLenPixel = draw.textsize(text, font=font)[0]
            print('text : ', text)
            print('size : ', draw.textsize(text, font=font)[0])
            print('pos : ', pos, 'len : ', len(titleName))
            print('lineLenPixel : ', lineLenPixel)
            draw.text((titleStartX, titleStartY+(i*fontSize)), text, font=font, fill=fontcolor, spacing=0, align='left')
        #释放画笔
        del draw
        # im.save(jpgName, 'jpg')
        im.save(jpgName, 'png')

class Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        '''根据系统平台选择合适的函数'''
        try:
            self.impl = GetchWindows()
        except ImportError:
            self.impl = GetchUnix()
    def __call__(self): return self.impl()


class GetchUnix:
    '''linux 平台的非阻塞获得输入'''
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        sys.stdout.flush()
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno(), termios.TCSANOW)
            ch = sys.stdin.read(1)
            sys.stdout.write(ch)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class GetchWindows:
    '''windows 平台的非阻塞获得输入'''
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch().decode('ascii')

class Html2Book():
    getchar = Getch()
    mathPositionLog = 'mathPosition.log'
    removeRubbishMsgCompiler = re.compile(r'{.katex-mathml[\S\s]*?{.katex}')
    extractMathExpressionCompiler = re.compile(r'\[\[\$([\S\s]*?)\$\]')
    rangeBracketCompiler = re.compile(r'\\\[([\s\S][\d|,]*?)\\\]')
    bookConfigFile = 'book.json'
    defaultBookJson = '''
    {
        "title": "example a book",
        "author": "Unknow",
        "description": null,
        "extension": null,
        "generator": "site",
        "isbn": "",
        "links": {
            "sharing": {
                "all": null,
                "facebook": null,
                "google": null,
                "twitter": null,
                "weibo": null
            },
            "sidebar": {}
        },
        "output": null,
        "pdf": {
            "fontSize": 12,
            "footerTemplate": null,
            "headerTemplate": null,
            "margin": {
                "bottom": 36,
                "left": 62,
                "right": 62,
                "top": 36
            },
            "pageNumbers": false,
            "paperSize": "a4"
        },
        "plugins": [
            "katex"
        ],
        "variables": {}
    }
    '''
    useCurSUMMARY = False
    reGenMDFileFlag = True
    doAll = False
    bookFormatList = ('mobi', 'pdfk', 'pdfpc')
    indexMdBak = 'index.md.bak'
    DEBUG = False
    kindleWidth = 758
    kindleHeight = 1024
    titleFontSize = 48

    """docstring for Html2Book"""
    def __init__(self):
        if len(os.sys.argv) != 3 and len(os.sys.argv) != 4:
            Usage()
        if len(os.sys.argv) == 4 and os.sys.argv[3].upper() == 'SUMMARY':
            self.useCurSUMMARY = True
        elif len(os.sys.argv) == 4 and os.sys.argv[3].upper() == 'SKIP':
            self.reGenMDFileFlag = False
        elif len(os.sys.argv) == 4 and os.sys.argv[3].upper() == 'SS':
            self.reGenMDFileFlag = False
            self.useCurSUMMARY = True

        self.bookFormat = os.sys.argv[2].lower()
        if self.bookFormat in self.bookFormatList:
            self.registerGenFunction()
        elif self.bookFormat == 'all':
            self.doAll = True
        else:
            Usage()

        self.bookName = os.sys.argv[1]
        # 使用相对路径 防止绝对路径中有空格
        curPath = '.'
        self.rootIndexHtmlFile = os.path.join(curPath, 'index.html')
        self.allHtmlFileList = self.listAllHtmlFile(curPath)
        # print('allHtmlFileList : ', self.allHtmlFileList)

    def listAllHtmlFile(self, file_dir):
        htmlList = []
        for root, dirs, files in os.walk(file_dir):
            # print ("-----------")
            # print (root)   #os.walk()所在目录
            # print (dirs)   #os.walk()所在目录的所有目录名
            # print (files)   #os.walk()所在目录的所有非目录文件名
            # print ("-----------")
            #filtrate _book dir
            if not root.startswith(os.path.join(file_dir, '_book')):
                for f in files:
                    if f.endswith('.html'):
                        htmlList.append(os.path.join(root, f))
        return htmlList

    def handleMathKatex(self, infile):
        tmpfile = 'tmp.md'
        foundMathTex = False
        with open(infile, 'r', encoding='utf-8') as fpr, open(tmpfile, 'w', encoding='utf-8') as fpw:
            rBuf = fpr.read()
            if self.removeRubbishMsgCompiler.findall(rBuf):
                wBuf = self.removeRubbishMsgCompiler.sub('', rBuf)
                wBuf = self.extractMathExpressionCompiler.sub(r'$$\1$$', wBuf)
                wBuf = self.rangeBracketCompiler.sub(r'[\1]', wBuf)
                fpw.write(wBuf)
                foundMathTex = True
        if foundMathTex:
            os.remove(infile)
            os.rename(tmpfile, infile)
        else:
            os.remove(tmpfile)

    def initBookJson(self, book_name, isKindle):
        if os.path.exists(self.bookConfigFile):
            self.defaultBookJson = json.load(open(self.bookConfigFile, 'r'))
        else:
            self.defaultBookJson = json.loads(self.defaultBookJson)
        self.defaultBookJson['title'] = book_name
        if isKindle:
            self.defaultBookJson['pdf']['paperSize'] = "a5"
        else:
            self.defaultBookJson['pdf']['paperSize'] = "a4"
        json.dump(self.defaultBookJson, open(self.bookConfigFile, 'w'), indent=4)

    def html2Markdown(self, h, rootIndexHtml):
        for f in h:
            if os.system('pandoc -f html -t markdown -o %s.md %s.html'%(f[:-5], f[:-5])):
                print('html2Markdown error file : %s'%f)
                exit(0)
            print('html2Markdown file %s'%f)
            #remove rubbish msg
            dstFile = f[:-5] + '.md'
            bakFile = dstFile + '.bak'
            if os.path.exists(bakFile):
                os.remove(bakFile)
            os.rename(dstFile, bakFile)
            self.handleMathKatex(bakFile)
            wFlag = False
            with open(bakFile, 'r', encoding='utf-8') as fpr, open(dstFile, 'w', encoding='utf-8') as fpw:
                lines = fpr.readlines()
                for line in lines:
                    # print('line : %s sectionCnt : %d normalCnt : %d'%(line, line.count('section'), line.count('section')))
                    if line.count('section') == 2 and line.count('normal') == 1:
                        # print('match ok %s'%line)
                        wFlag = True
                    elif (line.startswith(':::') or line.startswith('</div')) and wFlag:
                        break
                    elif wFlag:
                        fpw.write(line)
            if f != rootIndexHtml:
                pass
                if self.DEBUG is False:
                    #remove mid file
                    os.remove(bakFile)
            else:
                self.indexMdBak = bakFile
            # os.system('pause')
            # sleep(5)

    def logMathPosition(self, h):
        hadMath = False
        with open(self.mathPositionLog, 'w', encoding='utf-8') as fpw:
            fpw.write('Math formula position log file\n')
            for f in h:
                mdFile = f[:-5]+'.md'
                with open(mdFile, 'r', encoding='utf-8') as fpr:
                    lines = fpr.readlines()
                    lineNum = 0
                    for line in lines:
                        lineNum += 1
                        mathPos = line.find('$$')
                        if mathPos != -1:
                            fpw.write('%s line : %d column : %d\n'%(mdFile, lineNum, mathPos))
                            hadMath = True
        if hadMath is False:
            os.remove(self.mathPositionLog)

    def generateSummaryFromIndex(self):
        if os.path.exists('SUMMARY.md'):
            #backup
            os.rename('SUMMARY.md', 'SUMMARY' + '_' + datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S") + '.md')
        with open(self.indexMdBak, 'r', encoding='utf-8') as fpr, open('SUMMARY.md', 'w', encoding='utf-8') as fpw:
            lines = fpr.readlines()
            startFlag = False
            mergeFlag = False
            tmpLine = ''
            for line in lines:
                if line.startswith('-'):
                    startFlag = True
                elif (not line.replace(' ', '').startswith('-')) and startFlag:
                    if mergeFlag:
                        line = re.sub('^\s*', ' ', line)
                        line = tmpLine[:-1] + line
                    else:
                        break

                if re.findall('\[.*\]\(.*\)$', line) or line.find('gitbook-link}') != -1:
                    mergeFlag = False
                    tmpLine = ''
                else:
                    mergeFlag = True
                    tmpLine = line
                    continue

                if startFlag:
                    line = line.replace('.html)', '.md)')
                    #某些目录如果没有索引 赋值为README.md 防止后面build出错
                    if line.find('.md)') ==  -1 and ( line.find('gitbook-link}') == -1):
                        preLine = line
                        line = re.sub('\(.*\)', '(./README.md)', line)
                        print('summary %s invalid replace => %s'%(preLine[:-1], line))
                    fpw.write(line)

    def gitbookInstallPlugins(self):
        #install plugins
        if os.system('gitbook install'):
            print('gitbook install error')
            exit(0)

    def gitbookBuild(self):
        if os.system('gitbook build'):
            print('gitbook build error')
            exit(0)

    def createPDF_ForKindle(self):
        print('generate book %s'%(self.bookName+'_forKindle'))
        self.initBookJson(self.bookName+'_forKindle', True)
        if os.system('gitbook pdf . %s.pdf'%(self.bookName+'_forKindle')):
            print('gitbook mobi error')
            exit(0)

    def createPDF_ForPC(self):
        print('generate book %s'%(self.bookName+'_forPC'))
        self.initBookJson(self.bookName+'_forPC', False)
        if os.system('gitbook pdf . %s.pdf'%(self.bookName+'_forPC')):
            print('gitbook mobi error')
            exit(0)

    def createMobi_ForKindle(self):
        print('generate book %s.mobi'%self.bookName)
        self.initBookJson(self.bookName, True)
        if os.system('gitbook mobi . %s.mobi'%self.bookName):
            print('gitbook mobi error')
            exit(0)

    def generateBook(self):
        if self.reGenMDFileFlag and os.path.exists(self.mathPositionLog):
            print('             This project maybe contain math formula you can modify the markdown file which in the %s \n \
                and then run gitbook build to build the book and run gitbook mobi to generator mobi book\n \
                Do you want to regenerate markdown file(Y/n)?'%(self.mathPositionLog))
            while True:
                ch = self.getchar()
                if ch.upper() == 'Y':
                    break
                elif ch.upper() == 'N':
                    allMdFileList = []
                    with open(self.mathPositionLog, 'r', encoding='utf-8') as fpr:
                        lines = fpr.readlines()
                        for line in lines[1:]:
                            mdfile = line.split(' ')[0]
                            if mdfile not in allMdFileList:
                                allMdFileList.append(mdfile)
                    print('len(allMdFileList) : ', len(allMdFileList))
                    allMdFileList.append(self.mathPositionLog)
                    allMdFileList = ' '.join(allMdFileList)
                    print('allMdFileList : ', allMdFileList)
                    #open a sublime text new window and open the allMdFileList file
                    try:
                        os.system('subl -n %s'%allMdFileList)
                    except:
                        print('using sublime to open the allMathMdFiles error')
                    self.reGenMDFileFlag = False
                    break
        if self.reGenMDFileFlag:
            self.html2Markdown(self.allHtmlFileList, self.rootIndexHtmlFile)
            self.logMathPosition(self.allHtmlFileList)

        if not self.useCurSUMMARY:
            self.generateSummaryFromIndex()

        if not os.path.exists('README.md'):
            with open('README.md', 'w', encoding='utf-8') as fpw:
                fpw.write('README')

        self.initBookJson(self.bookName, True)
        self.gitbookInstallPlugins()
        self.gitbookBuild()
        if self.doAll:
            self.createMobi_ForKindle()
            self.createPDF_ForKindle()
            self.createPDF_ForPC()
        else:
            self.genFuncList[self.bookFormat]()

    def registerGenFunction(self):
        self.genFuncList = {'mobi':self.createMobi_ForKindle, 'pdfk':self.createPDF_ForKindle, 'pdfpc':self.createPDF_ForPC}

if __name__ == '__main__':
    if sys.version_info.major != 3:
        print('This project only support python3!')
        exit(0)

    cgc = generateCover()
    exit(0)
    chtml2book = Html2Book()
    chtml2book.generateBook()




