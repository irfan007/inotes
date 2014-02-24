


def parse_string(value,msg,require,override):
    if require and not value:
        if override:
            raise i_invalidFieldException('',msg,True)
        else:
            raise i_invalidFieldException('',msg+" can not be empty !",True)
    else:
        return str(value)

def parse_num(value,msg,require,override):
    if require and not value:
        raise i_invalidFieldException('',msg+" can not be empty !",True)
    elif not require and not value:
        return None
    else:
        try:
            return int(value)
        except ValueError:
            raise i_invalidFieldException(value,msg,override)


def parse_bool(value,msg,require,override):
    if require and value=='':
        raise i_invalidFieldException('',msg+" can not be empty !",True)
    elif not require and not value:
        return None
    else:
        try:
            return bool(value)
        except ValueError:
            raise i_invalidFieldException(value,msg,override)

def parse_email(value,msg,require,override):
    if require and not value:
        raise i_invalidFieldException('',msg+" can not be empty !",True)
    elif not require and not value:
        return value
    else:
        if '@' not in value:
            raise i_invalidFieldException(value,msg,override)
        else:
            return value


def parse_xldate(value,msg,require,override):
    
    if require and not value:
        raise i_invalidFieldException('',msg+" can not be empty !",True)
    elif not require and not value:
        return None
    else:
        try:
            import datetime
            import xlrd
            tpl=xlrd.xldate_as_tuple(value[0],value[1])
            return datetime.datetime(tpl[0],tpl[1],tpl[2])
            #return tpl
        except ValueError:
            raise i_invalidFieldException(value,msg,override)


class i_invalidFieldException(Exception):
    def __init__(self,value,msg,override):
        self.value=value
        self.msg=msg
        self.overirde=override
    def error_msg(self):
        if self.overirde and self.msg:
            return self.msg
        else:
            return "Invalid value found '"+str(self.value)+"' for "+self.msg+" !"
            


def i_validateField(value,mark,msg,override=False,require=True,options={}):
    
    '''
    NOTE :
    when parsing xld ,value must be touple like (value,workbook.datemode) where workbook=xlrd.open_workbook('file.xls') return 0/1 (0 for 1900-based /1 for 1904-based). 
    calling this method has to be safe by catching i_invalidFieldException
    
    override used to customize default error message bydefault is false 
    override =false means normal message 
    override =true means override whole message
    
    mark has values for different data type
    string          's'
    integer/number  'n'
    boolean         'b'
    excel date      'xld' (excel store date as float type,so 'value' must be float) 

    '''
    
    d={'s':parse_string,'n':parse_num,'e':parse_email,'xld':parse_xldate,'b':parse_bool}
    
    try:
        return d[mark](value,msg,require,override)
    except KeyError:
        raise i_invalidFieldException('',"Undefined 'Mark' argument '"+mark+"' in validation for value '"+str(value)+"' !",True)

