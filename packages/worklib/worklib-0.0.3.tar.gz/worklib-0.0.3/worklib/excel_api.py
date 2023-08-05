#-*- coding:utf-8 -*-
'''
实现Excel模块读写能力
xlsxwriter文档：https://www.bbsmax.com/A/LPdolMWjz3/

'''
import xlrd
import xlsxwriter

def readexcel(path,sheet_name,row=2,isRow=True):
    '''
    :param path: Excel路径
    :param sheet_name: 表名
    :param row: 默认从第几行读取
    :return:
    '''
    workbook = xlrd.open_workbook(path)
    table = workbook.sheet_by_name(sheet_name)
    row_table = table.nrows
    cols_table = table.ncols
    res = []
    header = []
    for i in range(row,row_table):
        one_row_table = {}
        one_row_table_list = []
        for k in range(0,cols_table):
            value = table.cell(i,k).value #获取excel中单元格的内容
            isType =  table.cell(i,k).ctype ##获取单元格内容的数据类型：ctype:1整型 2浮点型 3日期 4布尔
            if isType == 3:
                value = xlrd.xldate_as_datetime(value, 0)  # 将内容转为datetime格式
                value = value.strftime(("%Y/%m/%d"))  # 格式转换显示
            if isRow == True:
                one_row_table_list.append(value)
            else:
                if i == row:
                    header.append(value)
                else:
                    one_row_table[header[k]] = value
        if isRow == True:
            res.append(one_row_table_list)
        else:

            if i != row:
                res.append(one_row_table)
    print("read excel data response------>"+str(res))
    return res


def writeexcel(path,head,data,row=2):
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet("name")  # 创建一个sheet
    worksheet.write_row('A1', head)  # 将title写入excel
    #开始写入数据
    # data = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
    for i in range(row,len(data)+row):
        worksheet.write_row('A'+str(i), data[i-row])  # 将title写入excel
    workbook.close()  # 关闭excel

# if __name__ == '__main__':
#     read_path = "/Users/zhenghong/work/pythonCenter/github/worklib/worklib/test.xlsx"
#     readexcel("/Users/zhenghong/work/pythonCenter/github/worklib/worklib/test.xlsx", "项目管理") #读取数据
#     write_path = "/Users/zhenghong/work/pythonCenter/github/worklib/worklib/write.xlsx"
#     head = []
#     for i in range(10):
#         head.append(i)
#     print(head)
#     data = []
#     for i in range(len(head)):
#         data.append(head)
#     writeexcel(write_path,head,data)
