inp = input("请输入文件名：")
infile=open(inp,'r')
inp = inp[:-1] + "txt"
outfile=open(inp,"w",encoding='utf-8')

tableName=''
output=''
flag=True

for line in infile.readlines():
    if flag and line[:6]=='struct':
        tableName = line[8:]
        output += tableName

        if tableName[3]=='P':
            output+='point\n'
        elif tableName[3]=='L':
            output+='line\n'
        elif tableName[3]=='A':
            output+='face\n'
        
        output += 'wstring ID\n'#在所有变量之前加ID变量
        flag = False
        continue

    if not flag and line[1:4]=='int':
        output += 'int '+line[6:-2]+'\n'
        continue

    if not flag and line[1:7]=='double':
        output += 'double '+line[9:-2]+'\n'
        continue

    if not flag and line[1:8]=='wstring':
        output += 'wstring '+line[10:-2]+'\n'
        continue

    if line[:2] == '};':
        flag = True
        output +='wstring CommentInfo\n\n'#在所有变量之后加CommentInfo变量
        continue

outfile.write(output)