fileName = input("请输入文件名：")
inf=open(fileName,'r')

flask = open('flask.txt','w',encoding='utf-8')
http = open('http.txt','w',encoding='utf-8')
mysql = open('mysql.txt','w',encoding='utf-8')
mysql_func = open('mysql_func.txt','w',encoding='utf-8')

tableName=[]
shape=[]
attrs=[]

#读取文件并存储在列表中
flag = 'tableName'
attr=[]
for line in inf.readlines():
    if line=='\n':
        flag='tableName'
        attrs.append(attr)
        continue

    if flag=='tableName':
        attr=[]
        flag='shape'
        tableName.append(line[:-1])
        continue
    
    if flag=='shape':
        flag='attribute'
        shape.append(line[:-1])
        continue
    
    if flag=='attribute':
        attr.append(line.split())
        continue

output=''
#生成flask.py文件
for i in range(len(tableName)):
    #生成第一行URL映射
    output += '@app.route(\'/mysql/seismological_bureau/add_'
    output += tableName[i] + '/\', methods = [\'POST\'])\n'

    #生成第二行函数名
    output += 'def add_'+ tableName[i] + '():\n'

    #生成函数内部代码
    output += '\tdata = json.loads(request.get_data())\n'
    output += '\tsid = data["sid"]\n'
    if shape[i] != "table":
        output += '\t'+ shape[i] + 's = data[\"' + shape[i] + 's\"]\n'
    for attribute in attrs[i]:
        output += '\t'+ attribute[1] + 's = data[\"' + attribute[1] +'s\"]\n'
    
    #生成调用mysql_api_seismological_bureau函数的代码
    output +='\tres = mysql_api_seismological_bureau.add_'+tableName[i]+'(sid'
    if shape[i] != "table":
        output+=', '+shape[i]+'s'
    for attribute in attrs[i]:
        output += ', '+attribute[1]+'s'
    output += ')\n' + '\treturn json.dumps(res, ensure_ascii=False)\n\n'

flask.write(output)

output=''
#生成http_seismological_bureau_api.py文件
for i in range(len(tableName)):
    #生成函数名
    output += "def api_add_" + tableName[i] + "(url, sid"
    if shape[i] != "table":
        output += ", " +shape[i]+'s'
    for attribute in attrs[i]:
        output += ', '+attribute[1]+'s'
    output += "):\n"
    output += "\tdata = {'sid':sid"
    if shape[i] != "table":
        output += ", \'" +shape[i]+'s\':'+shape[i]+'s'
    for attribute in attrs[i]:
        output += ', \''+attribute[1]+'s\':'+attribute[1]+'s'
    output += "}\n\treturn(common_fun(url, data))\n\n"

http.write(output)

output=''
#生成EsTEMySQLAPI.h文件的代码
for name in tableName:
    output += "bool EXPORTTEMYSQLAPI EsAdd"+name+"ToNetDB(const int nSId, const vector<_"+name.upper()+">& vec_"+name+");\n"
output+='\n'

#生成EsTEMySQLAPI.cpp的url和func声明
for name in tableName:
    output += "const char* func_add_"+name+"t = \"api_add_"+name+"\";\n"
output+='\n'
for name in tableName:
    output += "const char* url_add_"+name+" = \"http://localhost:5000/mysql/seismological_bureau/add_"+name+"/\";\n"

mysql.write(output)

output=''
#生成EsTEMySQLAPI.cpp的函数
for i in range(len(tableName)):
    #生成函数名
    output += "bool EsAdd"+tableName[i]+"ToNetDB(const int nSId, const vector<_"+tableName[i].upper()+">& vec_"+tableName[i]+")\n{\n"
    #生成从开始到生成元组之前的代码
    output += "if(vec_"+tableName[i]+".empty())\n{\n"
    output += "return false;\n}\n"
    output += "Py_Initialize();\nif (!Py_IsInitialized())\n{\nreturn false;\n}\n"
    output += "PyRun_SimpleString(\"import sys\");\nPyRun_SimpleString(\"sys.path.append(\'./\')\");\n"
    output += "PyObject* pModule = NULL;\nPyObject* pFunc = NULL;\npModule = PyImport_ImportModule(module_name);\n"
    output += "if (pModule == NULL)\n{\nreturn false;\n}\n"
    output += "int nRecordNum = int(vec_"+tableName[i]+".size());\n"
    output += "pFunc = PyObject_GetAttrString(pModule, func_add_"+tableName[i]+");\n"
    output += "if(pFunc == NULL)\n{\nreturn false;\n}\n"
    #定义各变量的元组
    count_var = len(attrs[i])+2 #统计变量个数
    if shape[i]!='table':
        count_var += 1
    output += "PyObject* args = PyTuple_New("+str(count_var)+");\n"
    output += "PyObject* pyTupleURL = PyTuple_New(1);\nPyObject* pyTupleSID = PyTuple_New(1);\n"
    if shape[i]=="point":
        output += "PyObject* pyTuplePoints = PyTuple_New(nRecordNum);\n"
    elif shape[i]=="line":
        output += "PyObject* pyTuplePolylines = PyTuple_New(nRecordNum);\n"
    elif shape[i]=="face":
        output += "PyObject* pyTuplePolygons = PyTuple_New(nRecordNum);\n"
    
    for attribute in attrs[i]:
        output += "PyObject* pyTuple"+attribute[1]+"s = PyTuple_New(nRecordNum);\n"
    #给各元组赋值
    output += "PyTuple_SetItem(pyTupleURL, 0, StringToPy(url_add_"+tableName[i]+"));\n"
    output += "PyTuple_SetItem(pyTupleSID, 0, Py_BuildValue(\"i\", nSId));\n"
    output += "for (int idx = 0; idx < nRecordNum; idx++)\n{\n"

    vec = "vec_"+tableName[i]
    if shape[i]=="point":
        output += "PyObject* pyTuplePoint = PyTuple_New(3);\n"
        output += "PyTuple_SetItem(pyTuplePoint, 0, PyFloat_FromDouble("+vec+"[idx]._baseinfo._point._x));\n"
        output += "PyTuple_SetItem(pyTuplePoint, 1, PyFloat_FromDouble("+vec+"[idx]._baseinfo._point._y));\n"
        output += "PyTuple_SetItem(pyTuplePoint, 2, PyFloat_FromDouble("+vec+"[idx]._baseinfo._point._z));\n"
        output += "PyTuple_SetItem(pyTuplePoints, idx, pyTuplePoint);\n"
    elif shape[i]=="line":
        output += "int nPolylineNum = int("+vec+"[idx]._baseinfo._polyline.size());\n"
        output += "int nPolylinePtNumTotal = 0;\nint nPolylineEleCount = 0;\nvector<int> vecPolylinePtNum;\nvecPolylinePtNum.resize(nPolylineNum);\n"
        output += "for(int idxLine=0; idxLine<nPolylineNum; idxLine++)\n{\n"
        output += "vecPolylinePtNum[idxLine] = int("+vec+"[idx]._baseinfo._polyline[idxLine].size());\n"
        output += "nPolylinePtNumTotal += vecPolylinePtNum[idxLine];\n}\nPyObject* pyTuplePolyline = PyTuple_New(1+nPolylineNum+3*nPolylinePtNumTotal);\n"
        output += "PyTuple_SetItem(pyTuplePolyline, nPolylineEleCount, Py_BuildValue(\"i\", nPolylineNum));\nnPolylineEleCount++;\n"
        output += "for(int idxLine=0; idxLine<nPolylineNum; idxLine++)\n{\nPyTuple_SetItem(pyTuplePolyline, nPolylineEleCount, Py_BuildValue(\"i\", vecPolylinePtNum[idxLine]));\n"
        output += "nPolylineEleCount++;\n}\nfor(int idxLine = 0; idxLine<nPolylineNum; idxLine++)\n{\n"
        output += "for(int idxPt = 0; idxPt<vecPolylinePtNum[idxLine]; idxPt++)\n{\n"
        output += "PyTuple_SetItem(pyTuplePolyline, nPolylineEleCount, PyFloat_FromDouble("+vec+"[idx]._baseinfo._polyline[idxLine][idxPt]._x));\nnPolylineEleCount++;\n"
        output += "PyTuple_SetItem(pyTuplePolyline, nPolylineEleCount, PyFloat_FromDouble("+vec+"[idx]._baseinfo._polyline[idxLine][idxPt]._y));\nnPolylineEleCount++;\n"
        output += "PyTuple_SetItem(pyTuplePolyline, nPolylineEleCount, PyFloat_FromDouble("+vec+"[idx]._baseinfo._polyline[idxLine][idxPt]._z));\nnPolylineEleCount++;\n"
        output += "}\n}\nPyTuple_SetItem(pyTuplePolylines, idx, pyTuplePolyline);\n"
    elif shape[i]=="face":
        output += "int nPolylineNum = int("+vec+"[idx]._baseinfo._polygon.size());\n"
        output += "int nPolylinePtNumTotal = 0;\nint nPolylineEleCount = 0;\nvector<int> vecPolylinePtNum;\nvecPolylinePtNum.resize(nPolylineNum);\n"
        output += "for(int idxLine=0; idxLine<nPolylineNum; idxLine++)\n{\n"
        output += "vecPolylinePtNum[idxLine] = int("+vec+"[idx]._baseinfo._polyline[idxLine].size());\n"
        output += "nPolylinePtNumTotal += vecPolylinePtNum[idxLine];\n}\nPyObject* pyTuplePolygon = PyTuple_New(1+nPolylineNum+3*nPolylinePtNumTotal);\n"
        output += "PyTuple_SetItem(pyTuplePolygon, nPolylineEleCount, Py_BuildValue(\"i\", nPolylineNum));\nnPolylineEleCount++;\n"
        output += "for(int idxLine=0; idxLine<nPolylineNum; idxLine++)\n{\nPyTuple_SetItem(pyTuplePolygon, nPolylineEleCount, Py_BuildValue(\"i\", vecPolylinePtNum[idxLine]));\n"
        output += "nPolylineEleCount++;\n}\nfor(int idxLine = 0; idxLine<nPolylineNum; idxLine++)\n{\n"
        output += "for(int idxPt = 0; idxPt<vecPolylinePtNum[idxLine]; idxPt++)\n{\n"
        output += "PyTuple_SetItem(pyTuplePolygon, nPolylineEleCount, PyFloat_FromDouble("+vec+"[idx]._baseinfo._polygon[idxLine][idxPt]._x));\nnPolylineEleCount++;\n"
        output += "PyTuple_SetItem(pyTuplePolygon, nPolylineEleCount, PyFloat_FromDouble("+vec+"[idx]._baseinfo._polygon[idxLine][idxPt]._y));\nnPolylineEleCount++;\n"
        output += "PyTuple_SetItem(pyTuplePolygon, nPolylineEleCount, PyFloat_FromDouble("+vec+"[idx]._baseinfo._polygon[idxLine][idxPt]._z));\nnPolylineEleCount++;\n"
        output += "}\n}\nPyTuple_SetItem(pyTuplePolygons, idx, pyTuplePolygon);\n"
    
    for attribute in attrs[i]:
        output += "PyTuple_SetItem(pyTuple"+attribute[1]+"s, idx, "
        if attribute[0]=='wstring':
            output += "StringToPy(WstringToString("+vec+"[idx]._baseinfo._"+attribute[1]+")));\n"
        elif attribute[0]=='double':
            output += "PyFloat_FromDouble("+vec+"[idx]._"+attribute[1]+"));\n"
        elif attribute[0]=='int':
            output += "Py_BuildValue(\"i\", "+vec+"[idx]._"+attribute[1]+"));\n"
    
    output += "}\nPyTuple_SetItem(args, 0, pyTupleURL);\nPyTuple_SetItem(args, 1, pyTupleSID);\n"
    count = 3
    if shape[i]=="point":
        output += "PyTuple_SetItem(args, 2, pyTuplePoints);\n"
    elif shape[i]=="line":
        output += "PyTuple_SetItem(args, 2, pyTuplePolylines);\n"
    elif shape[i]=="face":
        output += "PyTuple_SetItem(args, 2, pyTuplePolygons);\n"
    else:
        count -= 1
    
    for attribute in attrs[i]:
        output += "PyTuple_SetItem(args, "+str(count)+", pyTuple"+attribute[1]+"s);\n"
        count += 1
    
    output += "PyObject* pRet = PyEval_CallObject(pFunc, args);\n"
    output += "const char* szRet = pRet->ob_type->tp_name;\n"
    output += "if(*szRet == *err_URLError || *szRet == *err_HTTPError)\n"
    output += "return false;\n"
    output += "Py_Finalize();\nreturn true;\n}\n\n"
mysql_func.write(output)