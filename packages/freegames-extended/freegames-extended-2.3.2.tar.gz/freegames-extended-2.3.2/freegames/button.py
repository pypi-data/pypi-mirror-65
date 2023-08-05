"""使用turtle模块绘制按钮。
七分诚意制作   2019.4.24"""
import math,random
from turtle import *

class Button():
    "turtle绘制出的按钮类"
    def __init__(self,width=120,height=40,
                 color1=(0,0,0),color2=None,
                 text=None,font='Arial'):
        #定义类属性
        self.h=height
        self.w=width
        self.color1=color1
        self.color2=color2 or color1
        self.text=text
        self.font=font
        self.llx=self.lly=0#llx、lly:画布左上角x、y坐标
        self.urx=self.ury=0#urx、ury:画布右下角x、y坐标
        self.drew=False
        self.draw()
    def draw(self):
        if self.drew:return
        self.drew=True
        setheading(0)
        colormode(255)
        fillcolor(self.color1)
        begin_fill()
        self.llx=pos()[0]#记录画笔坐标
        self.lly=pos()[1]
        pencolor("black")
        
        pendown()#画出按钮上半部分
        forward(self.w)
        right(90)
        forward(self.h/2)
        right(90)
        penup()
        forward(self.w)
        right(90)
        pendown()
        forward(self.h/2)
        end_fill()
        
        fillcolor(self.color2)
        right(180) #画出按钮下半部分
        forward(self.h/2)
        begin_fill()
        forward(self.h/2)
        left(90)
        forward(self.w)
        self.urx=pos()[0]#再次记录画笔坐标
        self.ury=pos()[1]
        left(90)
        forward(self.h/2)
        end_fill()
        
        if self.text:#绘制文本
            penup()
            left(90)
            l=len(self.text)
            if type(self.font) is str:
                fontsize=int(self.font.split()[1])
            else:fontsize=int(self.font[1])
            forward(self.w/2 + l*fontsize/1.5)
            left(90)
            forward(fontsize/2)
            write(self.text,True,align="left",font=self.font)
        penup()
        goto(self.llx,self.ury)
        setheading(0)
    def inarea(self,x,y):
        "判断x,y这个坐标是否位于按钮内。"
        return x>self.llx and x<self.urx and y<self.lly and y>self.ury

def click(x, y):
    global a,b
    #判断用户单击的是哪个按钮
    if a.inarea(x,y):#如果是关于按钮
        try:
            showturtle()#显示画笔
            shape("triangle")#设置画笔形状为三角形
            delay(20)
            setheading(135)
            forward(320)
            for s in __doc__:
                write(s,True,align="left",font=("微软雅黑",20))#绘制文字
            hideturtle()#再次隐藏画笔
        except Terminator:pass
    elif b.inarea(x,y):#如果是退出按钮
        print("bye!")
        bye()

##def main():
##    global a,b
##    #初始化
##    delay(0)
##    penup()
##    setx(-50)
##    #hideturtle()#隐藏画笔
##
##    #绘制关于按钮
##    a=Button(100,50,"green2","green3",
##             text="关于",font="华文行楷 20")
##    setheading(-90)
##    forward(50)
##
##    #绘制退出按钮
##    b=Button(100,50,"green2","green3",
##             text="退出",font="华文行楷 20")
##    
##    onscreenclick(click)
##    done()
##
##if __name__=="__main__":main()