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

    # main page
    step = 3
    page = ''
    # 縮短顯示分頁
    if (total_page > step * 2):

        # 所顯示的頁數編號
        page_range = [1, total_page]
        for i in range(current_page - step, current_page + step + 1, 1):
            page_range.append(i)

        for page_conut in range(1, total_page + 1, 1):
            if page_conut in page_range:
                if page_conut == 1 and (current_page - step) > 1 and (current_page - step - 1) != 1:
                    page += '<li class="waves-effect"><a href="/customers?current_page=' + \
                        str(page_conut) + query_params + '">' + \
                        str(page_conut) + '</a></li>\n'
                    page += '<li class="disabled"><a href="javascript:;">...</a></li>\n'
                elif page_conut == current_page:
                    page += '<li class="active"><a href="/customers?current_page=' + \
                        str(page_conut) + query_params + '">' + \
                        str(page_conut) + '</a></li>\n'
                elif page_conut == total_page and (current_page + step) < total_page and (current_page + step + 1) != total_page:
                    page += '<li class="disabled"><a href="javascript:;">...</a></li>\n'
                    page += '<li class="waves-effect"><a href="/customers?current_page=' + \
                        str(page_conut) + query_params + '">' + \
                        str(page_conut) + '</a></li>\n'
                else:
                    page += '<li class="waves-effect"><a href="/customers?current_page=' + \
                        str(page_conut) + query_params + '">' + \
                        str(page_conut) + '</a></li>\n'
    else:
        for page_conut in range(1, total_page + 1, 1):
            if page_conut == current_page:
                page += '<li class="active"><a href="/customers?current_page=' + \
                    str(page_conut) + query_params + '">' + \
                    str(page_conut) + '</a></li>\n'
            else:
                page += '<li class="waves-effect"><a href="/customers?current_page=' + \
                    str(page_conut) + query_params + '">' + \
                    str(page_conut) + '</a></li>\n'

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
