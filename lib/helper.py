# coding=utf-8

import math


def helper_pager(current_page, total, limit, params):

    total_page = int(math.ceil(float(total) / float(limit)))

    query_params = ''
    for key in params:
        if params[key]:
            query_params += "&{key}={val}".format(key=key, val=params[key])

    # previous
    if current_page > 1:
        previous = '<li class="waves-effect"><a href="/customers?current_page=' + \
            str(current_page - 1) + query_params + \
            '"><i class="material-icons">chevron_left</i></a></li>'
    else:
        previous = '<li class="disabled"><a href="javascript:;"><i class="material-icons">chevron_left</i></a></li>'

    # 頁數
    page = ''
    page_conut = 1
    while page_conut <= total_page:
        if page_conut == current_page:
            page += '<li class="active"><a href="/customers?current_page=' + \
                str(page_conut) + query_params + '">' + \
                str(page_conut) + '</a></li>\n'
        else:
            page += '<li class="waves-effect"><a href="/customers?current_page=' + \
                str(page_conut) + query_params + '">' + \
                str(page_conut) + '</a></li>\n'

        page_conut += 1
        pass

    # next
    if current_page >= total_page:
        next = '<li class="disabled"><a href="javascript:;"><i class="material-icons">chevron_right</i></a></li>'
    else:
        next = '<li class="waves-effect"><a href="/customers?current_page=' + \
            str(current_page + 1) + query_params + \
            '"><i class="material-icons">chevron_right</i></a></li>'

    pager = '''
            <ul class="pagination">
                ''' + previous + page + next + '''
            </ul>
        '''

    return pager
