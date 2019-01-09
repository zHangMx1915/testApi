# coding=utf-8

# 定义变量参数
class GlobalVar:

    Id = 0
    name = 1
    url = 2
    run = 3
    request_way = 4
    header = 5
    case_depend = 6
    data_depend = 7
    field_depend = 8
    data = 9
    expect = 10
    result = 11


# 获取id
def get_id():
    return GlobalVar.Id


# 获取url
def get_url():
    return GlobalVar.url


# 是否运行
def get_run():
    return GlobalVar.run


# 获取请求类型
def get_request_way():
    return GlobalVar.request_way


# 获取header
def get_header():
    return GlobalVar.header


# 依赖id
def get_case_depend():
    return GlobalVar.case_depend


# 依赖数据
def get_data_depend():
    return GlobalVar.data_depend


# 依赖数据所属字段
def get_field_depend():
    return GlobalVar.field_depend


# 请求数据
def get_data():
    return GlobalVar.data


# 预期结果
def get_expect():
    return GlobalVar.expect


# 实际结果
def get_result():
    return GlobalVar.result

# 获取header的value,测试值，header获取方法待定
def get_header_value():
    header = {
        'header': '123',
        'cookie': 'None'
    }
    return header