import os

import pandas as pd
import threading

import Path
import get_post_html

df=pd.read_csv('data.csv')

#去重
data=df['name'].value_counts().loc[df['name'].value_counts()>1]
names=data.keys()#前置前N行，加上key是表示只取值，取出A列的那个数据，不加key（）就是输出A列数据+重复次数
for j in range(len(data)):
    index=df.loc[df['name']==names[j],['name','url']].index
    for i in range(data[j]):
        if '(' in names[j]:
            df.loc[index[i], 'name']=names[j].split('(')[0]+'['+str(i+1)+']'+'('+names[j].split('(')[1]
        else:
            df.loc[index[i], 'name']=names[j]+'['+str(i+1)+']'


names=list(df['name'])
urls=list(df['url'])
path='D:\\1\\国内Cos\\'

def img_size(response):
    if 'Transfer-Encoding' in response.headers:
        return int(response.headers['Transfer-Encoding'])

    elif 'Content-Length' in response.headers:
        return int(response.headers['Content-Length'])

def wait(main,urls,l,names):
    threads = []
    for j in range(0,len(urls),l):
        for i in range(l):
            if i+j==len(urls):
                print('线程已完成任务！')
            else:
                t = threading.Thread(target=main, args=(names[i+j],urls[i+j]))
                threads.append(t)
                t.start()
        for t in threads:
            t.join()

def down(name,url):
    while 1:
        response=get_post_html.get_html(url)
        size=img_size(response)
        content = response.content
        Path.make_path(path+name.split('(')[0])
        img_path=path+name.split('(')[0]+'\\'+name+url[-4:]
        with open(img_path,'wb')as f:
            f.write(content)
            print(name)
        statinfo= os.stat(img_path).st_size
        if size==statinfo:
            return
        else:
            print('图片大小发生错误：',name)
            pass
#names=names[1950:]
#urls=urls[1950:]
wait(down,urls,100,names)