import os

path="D:/微信文件/WeChat Files/wxid_0ky67l09jqcy21/FileStorage/File/2020-07/schema(1)/schema"
#path=input("请输入文件夹地址:")

outpath=input("请输入文件夹地址，默认为输入目录下:") or  path
filedir=os.listdir(path)


for t in filedir:
    updir=os.path.join(path,t)
    if os.path.isfile(updir):
        continue
    l=os.listdir(updir)
    File=t+'uploadDialog.txt'
    fc=open(os.path.join(outpath,File),"w",encoding='utf-8')
    for index in l:
        strforwrite='bool CSB_GDB_UPLOAD_TOOLDlg::EsUpload'
        temp=index.split('-')
        tbname=''#表英文名
        if(len(temp[2])>5): #项目表
            tbname=temp[0][3:]
        else:
            tbname=temp[0]
        strforwrite+=tbname+'()\n{\n\tEsGDBReader obReader;\n\t((CEdit*)GetDlgItem(IDC_EDIT_PROCESS_INFO))->ReplaceSel("正在获取'+temp[1]
        strforwrite+='...\\r\\n");\n\tvector<_'+tbname.upper()+'> vec_'+tbname+';\n\tif(!obReader.EsGet'+tbname+'(vec_'+tbname+'))\n\t{\n\t\t'
        strforwrite+='((CEdit*)GetDlgItem(IDC_EDIT_PROCESS_INFO))->ReplaceSel("'+temp[1]+'获取失败！\\r\\n");\n\t\t'
        strforwrite+='((CEdit*)GetDlgItem(IDC_EDIT_PROCESS_INFO))->ReplaceSel(obReader.EsGetError());\n\t\t'
        strforwrite+='((CEdit*)GetDlgItem(IDC_EDIT_PROCESS_INFO))->ReplaceSel("\\r\\n");\n\t\treturn false;\n\t}\n\t'
        strforwrite+='((CEdit*)GetDlgItem(IDC_EDIT_PROCESS_INFO))->ReplaceSel("'+temp[1]+'获取成功！\\r\\n");\n\t'
        strforwrite+='((CEdit*)GetDlgItem(IDC_EDIT_PROCESS_INFO))->ReplaceSel("正在上传'
        strforwrite+=temp[1]+'...\\r\\n");\n\tif(!EsAdd'+tbname+'ToNetDB(m_nSId, vec_'+tbname+'))\n\t{\n\t\t((CEdit*)GetDlgItem(IDC_EDIT_PROCESS_INFO))->ReplaceSel("'
        strforwrite+=temp[1]+'上传失败!");\n\t\t((CEdit*)GetDlgItem(IDC_EDIT_PROCESS_INFO))->ReplaceSel(obReader.EsGetError());\n\t\t'
        strforwrite+='((CEdit*)GetDlgItem(IDC_EDIT_PROCESS_INFO))->ReplaceSel("\\r\\n");\n\t\treturn false;\n\t}\n\t'
        strforwrite+='((CEdit*)GetDlgItem(IDC_EDIT_PROCESS_INFO))->ReplaceSel("'+temp[1]+'上传成功！\\r\\n");\n\treturn true;\n}\n'
        fc.write(strforwrite)

    fc.close()

