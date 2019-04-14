from django.shortcuts import render

# Create your views here.
# -*-# -*- coding:utf-8 -*-
import pymysql
from django.shortcuts import render, redirect


def classes(request):
    # 创建连接
    conn = pymysql.connect(host='106.13.123.51', port=3306, user='root', passwd='root', db='stu', charset='utf8')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select * from class_list"
    # 执行SQL，并返回收影响行数
    cursor.execute(sql)

    class_list = cursor.fetchall()
    # 执行SQL，并返回受影响行数
    # effect_row = cursor.execute("update hosts set host = '1.1.1.2' where nid > %s", (1,))

    # 执行SQL，并返回受影响行数
    # effect_row = cursor.executemany("insert into hosts(host,color_id)values(%s,%s)", [("1.1.1.11",1),("1.1.1.11",2)])

    # 提交，不然无法保存新建或者修改的数据
    # conn.commit()

    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    return render(request, 'classes.html', {'class_list': class_list})


def add_class(request):
    conn = pymysql.connect(host='106.13.123.51', port=3306, user='root', passwd='root', db='stu', charset='utf8')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    id = request.GET.get('id')
    print(id)
    if request.method == 'GET':
        if id:
            sql = "select * from class_list where id = (%s)"
            cursor.execute(sql, (id,))
            item = cursor.fetchone()
            return render(request, 'add-class.html', {'item': item})
        else:
            return render(request, 'add-class.html')
    elif request.method == 'POST':
        class_name = request.POST.get('class_name')
        if id is None:
            sql = "insert into class_list(class_name) values (%s)"
            effect_row = cursor.execute(sql, (class_name,))
            print('insert', effect_row, "条记录")
        else:
            sql = "update class_list set class_name = (%s) where id = (%s)"
            effect_row = cursor.execute(sql, (class_name, id))
            print('update', effect_row, "条记录")
        # 执行SQL，并返回收影响行数
        conn.commit()
        # 关闭游标
        cursor.close()
        # 关闭连接
        conn.close()
        return redirect('/classes/')


def rm_class(request):
    id = request.GET.get('id')
    conn = pymysql.connect(host='106.13.123.51', port=3306, user='root', passwd='root', db='stu', charset='utf8')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "delete from class_list where id=(%s)"
    # 执行SQL，并返回收影响行数
    effect_row = cursor.execute(sql, (id,))
    print('删除了', effect_row, '行')
    conn.commit()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    return redirect('/classes/')
