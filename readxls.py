import os
import xlrd3

#path="D:/微信文件/WeChat Files/wxid_0ky67l09jqcy21/FileStorage/File/2020-07/schema(1)/schema"
path=input("请输入文件夹地址:")

outpath=input("请输入文件夹地址，默认为输入目录下:") or  path
filedir=os.listdir(path)

prop=''

for t in filedir:
    updir=os.path.join(path,t)
    if os.path.isfile(updir):
        continue
    l=os.listdir(updir)
    File=t+'_proprity.txt'
    fc=open(os.path.join(outpath,File),"w",encoding='utf-8')
    for index in l:
        print(index)
        strforwrite=''
        if(index[-5]=='线'):
            prop='line'
        elif(index[-5]=='面'):
            prop='face'
        elif(index[-5]=='点'):
            prop='point'
        else:#无几何属性的表
            prop='table'
        tempxls=xlrd3.open_workbook(os.path.join(updir,index))
        worksheet=tempxls.sheet_by_index(0)
        table=worksheet.name
        if(len(prop)):
            strforwrite+=table+'\n'+prop+'\n'
        else:
            strforwrite+=table+'\n'
        lname=worksheet.row_values(0)#字段名列表
        ltype=worksheet.row_values(2)#字段类型列表

        for i in range(len(ltype)):
            if ltype[i][0:6]=='String':
                ltype[i]='wstring'
            elif ltype[i][0:1]=='I':
                ltype[i]='int'
            elif ltype[i][0:6]=='Double':
                ltype[i]='double'
            elif ltype[i][0:5]=='Small':
                ltype[i]='int'
            elif ltype[i][:4]=='Date':
                ltype[i]='wstring'
            elif ltype[i]=='TitleLine':  
                ltype=ltype[:i]
                lname=lname[:i]
                break

        for i  in range(min(len(lname),len(ltype))):
            strforwrite+=ltype[i]+' '+lname[i]+'\n'
        strforwrite+='\n'#当前表结束，多一个换行
        fc.write(strforwrite)

    fc.close()

