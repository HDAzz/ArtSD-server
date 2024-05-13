

'''
40000 BadRequest
'''
def success(data,msg='ok'):
    return {'code':0,'msg':msg,'data':data}
def error(errcode,msg):
    return {'code':errcode,'msg':msg}