from sqlalchemy import desc

class ToolsError(RuntimeError):
    pass

def _get_records(db = None, Table = None, Attr = None, Value = None, pageNum = 1, pageSize = 10, reverse=False):
    '''

    This method's get the Database and information, return the records.

    params: db        SQL DB.
    params: Table     Table object you defined in models.py.
    params: Attr      Table object's attr you want to select from.
    params: Value     The Attr value you expect.
    params: pageNum   The number of pages you want to get. Default is the first page.
    params: pageSize  The size of each page you want to set. Default each page have 10 data segments.
    params: reverse   Reverse the records. Default is False.

    return: a python dict obejct, include
            pageNow:  [int]  the page you except.
            pageMax:  [int]  the records provide the max pages number.
            hasNext:  [bool] if have next page, set it True.
            rowsNum:  [int]  the conditional records count number.
            dataList: [list] the list of records.

    Please make sure you give the ```db```　argument, otherwise we will raise ToolsError.

    '''
    if db is None:
        raise ToolsError()
    if Attr is None:
        rows = db.session.query(Table).count()
    else:
        rows = db.session.query(Table).filter(Attr == Value).count()
    pageMax = type(1)(rows/pageSize)
    if rows % pageSize:
        pageMax += 1
    hasNext = True
    if pageNum >= pageMax:
        hasNext = False
    if Attr is not None:
        if reverse:
            dataList = db.session.query(Table).filter(Attr ==Value).order_by("id desc").limit(pageSize).offset((pageNum-1)*pageSize)
        else:
            dataList = db.session.query(Table).filter(Attr == Value).limit(pageSize).offset((pageNum-1)*pageSize)
    else:
        if reverse:
            dataList = db.session.query(Table).order_by("id desc").limit(pageSize).offset((pageNum-1)*pageSize)
        else:
            dataList = db.session.query(Table).limit(pageSize).offset((pageNum-1)*pageSize)
    return {
        'pageNum': pageNum,
        'pageMax': pageMax,
        'hasNext': hasNext,
        'rowsNum': rows,
        'dataList': dataList,
    }
