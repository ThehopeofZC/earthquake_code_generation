import os


path = input("请输入文件名：")
outpath=input("请输入文件夹地址，默认为输入目录下:") or path
infile=open(path,'r')
File=outpath+'\\'+path[-15:-2]+'upload.txt'
fc=open(File,"w",encoding='utf-8')
#F:\MasterStudy\wgtd\地震局活动断裂三维建模公共平台\code\SB_FGDB_API\EsSBData_A2_Geography1_2000.h
for line in infile.readlines():
    strforwrite=''
    if line[:6]=='struct':
        tbname= line[8:-1]
        strforwrite='bool CSB_GDB_UPLOAD_TOOLDlg::EsUpload'
        strforwrite+=tbname+'()\n{\n\tEsGDBReader obReader;\n\t((CEdit*)GetDlgItem(IDC_EDIT_PROCESS_INFO))->ReplaceSel("正在获取'+tbname
        strforwrite+='...\\r\\n");\n\tvector<_'+tbname+'> vec_'+tbname+';\n\tif(!obReader.EsGet'+tbname+'(vec_'+tbname+'))\n\t{\n\t\t'
        strforwrite+='((CEdit*)GetDlgItem(IDC_EDIT_PROCESS_INFO))->ReplaceSel("'+tbname+'获取失败！\\r\\n");\n\t\t'
        strforwrite+='((CEdit*)GetDlgItem(IDC_EDIT_PROCESS_INFO))->ReplaceSel(obReader.EsGetError());\n\t\t'
        strforwrite+='((CEdit*)GetDlgItem(IDC_EDIT_PROCESS_INFO))->ReplaceSel("\\r\\n");\n\t\treturn false;\n\t}\n\t'
        strforwrite+='((CEdit*)GetDlgItem(IDC_EDIT_PROCESS_INFO))->ReplaceSel("'+tbname+'获取成功！\\r\\n");\n\t'
        strforwrite+='((CEdit*)GetDlgItem(IDC_EDIT_PROCESS_INFO))->ReplaceSel("正在上传'
        strforwrite+=tbname+'...\\r\\n");\n\tif(!EsAdd'+tbname+'ToNetDB(m_nSId, vec_'+tbname+'))\n\t{\n\t\t((CEdit*)GetDlgItem(IDC_EDIT_PROCESS_INFO))->ReplaceSel("'
        strforwrite+=tbname+'上传失败！");\n\t\t((CEdit*)GetDlgItem(IDC_EDIT_PROCESS_INFO))->ReplaceSel(obReader.EsGetError());\n\t\t'
        strforwrite+='((CEdit*)GetDlgItem(IDC_EDIT_PROCESS_INFO))->ReplaceSel("\\r\\n");\n\t\treturn false\n\t}\n\t'
        strforwrite+='((CEdit*)GetDlgItem(IDC_EDIT_PROCESS_INFO))->ReplaceSel("'+tbname+'上传成功！\\r\\n");\n\treturn true;\n}\n'

    fc.write(strforwrite)
fc.close()

