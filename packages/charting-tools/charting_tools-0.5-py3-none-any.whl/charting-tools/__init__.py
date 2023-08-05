from PIL import Image,ImageDraw,ImageFont
def 绘制横向虚线(PILImageDraw,起始位置,长度,每段长度,间隔,颜色):
    a=0
    点坐标列表=[]
    for i in range(起始位置[0],起始位置[0]+长度+1):
        a+=1
        if a==每段长度+间隔+1:
            a=1
        if not(a>每段长度):
            点坐标列表+=[(i,起始位置[1])]
    PILImageDraw.point(点坐标列表,fill=颜色)
    return PILImageDraw
class 你不需要用它:
    def 取整(a,b) -> '你不需要用它':
        if (c:=round(a,b))>a:
            return c,0.1**b
        else:
            return c+0.1**b,0.1**b
    def 获取文字占用位置(a) -> '你不需要用它':
        global font
        if round(a,5)==int(round(a,5)):
            ab=int(round(a,5))
        else:
            ab=round(a,5)
        return font.getsize(str(a))
    def 获取因素文字占用位置(a) -> '你不需要用它':
        global font
        return font.getsize(a)
def bar_chart(RGB_list,
              factor_string_list,
              *subscriptable:'(project name, factor[0] corresponding value, factor[1] corresponding value ...)'
              ,numerical_unit='') -> Image.Image:
    global font
    颜色列表=[(0,0,0)]+RGB_list
    content_text=[['']+factor_string_list]+list(subscriptable)
    a=0
    for row in range(1,len(content_text[0])):
        for col in range(1,len(content_text)):
            if (数值:=(float(content_text[col][row]) if content_text[col][row].replace(".", "").isdigit()else 0))>a:
                a=数值
    if a>1:
        c=你不需要用它.取整(a,-len(str(int(a)))+1)
    elif a!=0:
        a=0
        for row in range(1,len(content_text[0])):
            for col in range(1,len(content_text)):
                if (float(content_text[col][row]) if content_text[col][row].replace(".", "").isdigit()else 0)<a:
                    a=(float(content_text[col][row]) if content_text[col][row].replace(".", "").isdigit()else 0)
        c=你不需要用它.取整(a,len(str(a).split('.')[1]))
    else:
        c=(1,0.1)
    if round(c[0],5)==int(round(c[0],5)):
        ab=int(round(c[0],5))
    else:
        ab=round(c[0],5)
    font = ImageFont.truetype('simhei.ttf', 24)#字体大小
    数值列表=[]
    b=-1
    for i in range(1040,50,int(990/(-(c[0]/c[1])))):
        b+=1
        数值列表+=[c[1]*b]
    a=max(数值列表,key=你不需要用它.获取文字占用位置)
    数值列表=[]
    for col in range(1,len(content_text)):
        数值列表+=[content_text[col][0]]
    for col in range(1,len(content_text)):
        加入数值列表的东东=''
        for row in range(1,len(content_text[0])):
            加入数值列表的东东+=content_text[col][0]+numerical_unit
        数值列表+=[加入数值列表的东东]
    因素占用位置=max(len(content_text[0])*50*(len(content_text[0])-1),len(content_text[0])*(font.getsize(max(数值列表,key=你不需要用它.获取因素文字占用位置))[0]+10))
    if round(a,5)==int(round(a,5)):
        ab=int(round(a,5))
    else:
        ab=round(a,5)
    文字占用位置=font.getsize(str(ab))[0]+10
    x坐标=10
    for 项目 in range(1,len(content_text)):
        x坐标+=70+font.getsize(content_text[项目][0])[0]
    im= Image.new('RGB',(max(文字占用位置+50+(1+(len(content_text[0])-1)*因素占用位置)+10+文字占用位置+50,x坐标),105+1040+font.getsize(str(ab))[1]+50) , 'white')
    draw = ImageDraw.Draw(im)
    x坐标=10
    颜色列表[1]=颜色列表[1]
    for 项目 in range(1,len(content_text)):
        颜色=颜色列表[项目]
        draw.ellipse((x坐标,1100 , x坐标+25, 1125), fill=(int(颜色[0]*256),int(颜色[1]*256),int(颜色[2]*256)))
        draw.text((x坐标+30,1100),content_text[项目][0],'GREY',font=font)
        x坐标+=70+font.getsize(content_text[项目][0])[0]
    draw.line(((文字占用位置,50),(文字占用位置,1040+font.getsize(str(ab))[1])),'grey',5)
    draw.line(((文字占用位置,1040),(50+(len(content_text[0])-1)*因素占用位置+10+文字占用位置,1040)),'grey',5)
    b=-1
    for i in range(1040,49,int(990/(-(c[0]/c[1])))):
        b+=1
        if round(c[1]*b,5)==int(round(c[1]*b,5)):
            ab=int(round(c[1]*b,5))
        else:
            ab=round(c[1]*b,5)
        draw.text((0,i),str(ab),'grey',font=font)
        draw=绘制横向虚线(draw,(0+文字占用位置,i),50+(len(content_text[0])-1)*因素占用位置+10,5,5,'grey')
    for i in range(1,len(content_text[0])):
        draw.text((int(因素占用位置*(i-1)+因素占用位置/len(content_text)*1.5+因素占用位置/len(content_text)*(len(content_text)-1)/2-font.getsize(content_text[0][i])[0]/2),1050),content_text[0][i],'grey',font=font)
    a=文字占用位置
    for 因素 in range(1,len(content_text[0])):
        a+=int(因素占用位置/len(content_text))
        for 项目 in range(1,len(content_text)):
            颜色=颜色列表[项目]
            draw.text((a+int(因素占用位置/len(content_text))/2-font.getsize(content_text[项目][因素]+numerical_unit)[0]/2,1040-int((float(content_text[项目][因素])/c[0])*990)-10-font.getsize(content_text[项目][因素]+numerical_unit)[1]),content_text[项目][因素]+numerical_unit,'black',font=font)
            draw.rectangle([a,1040,a+int(因素占用位置/len(content_text)),1040-int((float(content_text[项目][因素])/c[0])*990)],(int(颜色[0]*256),int(颜色[1]*256),int(颜色[2]*256),),'black',1)
            a+=int(因素占用位置/len(content_text))
    return im
    
def broken_line_statistic_chart(RGB_list,
              factor_string_list,
              *subscriptable:'(project name, factor[0] corresponding value, factor[1] corresponding value ...)'
              ,numerical_unit='') -> Image.Image:
    global font
    颜色列表=[(0,0,0)]+RGB_list
    content_text=[['']+factor_string_list]+list(subscriptable)
    a=0
    for row in range(1,len(content_text[0])):
        for col in range(1,len(content_text)):
            if (数值:=(float(content_text[col][row]) if content_text[col][row].replace(".", "").isdigit()else 0))>a:
                a=数值
    if a>1:
        c=你不需要用它.取整(a,-len(str(int(a)))+1)
    elif a!=0:
        a=0
        for row in range(1,len(content_text[0])):
            for col in range(1,len(content_text)):
                if (float(content_text[col][row]) if content_text[col][row].replace(".", "").isdigit()else 0)<a:
                    a=(float(content_text[row][col]) if content_text[col][row].replace(".", "").isdigit()else 0)
        c=你不需要用它.取整(a,len(str(a).split('.')[1]))
    else:
        c=(1,0.1)
    if round(c[0],5)==int(round(c[0],5)):
        ab=int(round(c[0],5))
    else:
        ab=round(c[0],5)
    font = ImageFont.truetype('simhei.ttf', 24)#字体大小
    数值列表=[]
    b=-1
    for i in range(1040,50,int(990/(-(c[0]/c[1])))):
        b+=1
        数值列表+=[c[1]*b]
    a=max(数值列表,key=你不需要用它.获取文字占用位置)
    数值列表=[]
    for col in range(1,len(content_text)):
        数值列表+=[content_text[col][0]]
    for col in range(1,len(content_text)):
        加入数值列表的东东=''
        for row in range(1,len(content_text[0])):
            加入数值列表的东东+=content_text[col][0]+numerical_unit
        数值列表+=[加入数值列表的东东]
    因素占用位置=max(50*(len(content_text[0])-1),(font.getsize(max(数值列表,key=你不需要用它.获取因素文字占用位置))[0]+10))
    if round(a,5)==int(round(a,5)):
        ab=int(round(a,5))
    else:
        ab=round(a,5)
    文字占用位置=font.getsize(str(ab))[0]+10
    x坐标=10
    for 项目 in range(1,len(content_text)):
        x坐标+=70+font.getsize(content_text[项目][0])[0]
    im= Image.new('RGB',(max(文字占用位置+50+(1+(len(content_text[0])-1)*因素占用位置)+10+文字占用位置+50,x坐标),105+1040+font.getsize(str(ab))[1]+50) , 'white')
    draw = ImageDraw.Draw(im)
    x坐标=10
    颜色列表[1]=颜色列表[1]
    for 项目 in range(1,len(content_text)):
        颜色=颜色列表[项目]
        draw.ellipse((x坐标,1100 , x坐标+25, 1125), fill=(int(颜色[0]*256),int(颜色[1]*256),int(颜色[2]*256)))
        draw.text((x坐标+30,1100),content_text[项目][0],'GREY',font=font)
        x坐标+=70+font.getsize(content_text[项目][0])[0]
    draw.line(((文字占用位置,50),(文字占用位置,1040+font.getsize(str(ab))[1])),'grey',5)
    draw.line(((文字占用位置,1040),(50+(len(content_text[0])-1)*因素占用位置+10+文字占用位置,1040)),'grey',5)
    b=-1
    for i in range(1040,49,int(990/(-(c[0]/c[1])))):
        b+=1
        if round(c[1]*b,5)==int(round(c[1]*b,5)):
            ab=int(round(c[1]*b,5))
        else:
            ab=round(c[1]*b,5)
        draw.text((0,i),str(ab),'grey',font=font)
        draw=绘制横向虚线(draw,(0+文字占用位置,i),50+(len(content_text[0])-1)*因素占用位置+10,5,5,'grey')
    for i in range(1,len(content_text[0])):
        draw.text((int(因素占用位置*(i-1)+因素占用位置/len(content_text)*1.5+因素占用位置/len(content_text)*(len(content_text)-1)/2-font.getsize(content_text[0][i])[0]/2),1050),content_text[0][i],'grey',font=font)
    for 项目 in range(1,len(content_text)):
        a=文字占用位置
        坐标列表=[]
        for 因素 in range(1,len(content_text[0])):
            颜色=颜色列表[项目]
            坐标=(a+int(因素占用位置)/2,1040-int((float(content_text[项目][因素])/c[0])*990))
            坐标列表+=[坐标]
            a+=int(因素占用位置)
        draw.line(坐标列表,tuple(int(i*256) for i in 颜色),5)
    for 项目 in range(1,len(content_text)):
        a=文字占用位置
        for 因素 in range(1,len(content_text[0])):
            颜色=颜色列表[项目]
            文字坐标=(a+int(因素占用位置)/2-font.getsize(content_text[项目][因素]+numerical_unit)[0]/2,1040-int((float(content_text[项目][因素])/c[0])*990)-23-font.getsize(content_text[项目][因素]+numerical_unit)[1])
            坐标=(a+int(因素占用位置)/2,1040-int((float(content_text[项目][因素])/c[0])*990))
            draw.text(文字坐标,content_text[项目][因素]+numerical_unit,'black',font=font)
            draw.ellipse((坐标[0]-12,坐标[1]-13 , 坐标[0]+13, 坐标[1]+12), 'white',(int(颜色[0]*256),int(颜色[1]*256),int(颜色[2]*256)),2)
            a+=int(因素占用位置)
    return im
