import httpx
from pytools.pytools import pickledump, pickleread
from markdown import markdown
from pytools.pytools import jmail
import os

s=httpx.Client()
logindata=os.getenv('logindata')

idlist=pickleread('idlist.txt',[])
freshtasks=[]
md=''
on=os.getenv('on')

resp=s.post('https://c.29592.net/api/EarnUser/BangBangTuanV2',data=logindata,headers={'content-type':'application/json; charset=utf-8'}).json()
tasklist=resp['tasklist']
for i in tasklist:
  id=i['earnid']
  name=i['prizename']
  count=i['remaincount']
  if (not id in idlist) or on!='schedule':
    if on=='schedule':
      idlist.append(id)
    freshtasks.append({'name':name,'count':count})

for count, i in enumerate(sorted(freshtasks,key=lambda d: d['count'])):
  md+='%s* %s (剩%s名额)'%('\n' if count>0 else '',i['name'],i['count'])
mailhtml=markdown(md)
print(md)
print(mailhtml)

if len(freshtasks)>0:
  jmail('ZRBBBT','帮帮团上了%s个新任务'%len(freshtasks),mailhtml,html=True)
pickledump(idlist,'idlist.txt')
