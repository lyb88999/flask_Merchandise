# from flask import Flask, render_template, json, request, redirect, session, abort, flash, url_for
# from flask.ext.mysql import MySQL

from flask import render_template, url_for, session, flash, abort
from flask import Flask, request, redirect
import cx_Oracle
cx_Oracle.init_oracle_client(lib_dir="/Users/lh/Downloads/instantclient_19_8")

connect = cx_Oracle.connect('w2019210771/lyb8889999@222.27.161.245:1521/orcl')

app = Flask(__name__)
cursor = connect.cursor()
app.secret_key = '101'

app.config['USERNAME'] = 'test'
app.config['PASSWORD'] = 'test'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/show_entries_1/')
def show_entries_1():
    sql = 'select gid, gclass, gname, gsize , gpro from Good order by gid desc'
    cursor.execute(sql)
    connect.commit()
    data = cursor.fetchall()
    entries = [dict(id=row[0], gclass=row[1], gname=row[2], gsize=row[3], gpro=row[4]) for row in data]
    return render_template('show_entries.html', entries=entries)

@app.route('/show_entries_2/')
def show_entries_2():
    sql = 'select gid, gpdata, gpnum, gpp from GoodPurchase order by gpdata desc,gid desc'
    cursor.execute(sql)
    connect.commit()
    data = cursor.fetchall()
    entries = [dict(id=row[0], gpdata=row[1], gpnum=row[2], gpp=row[3]) for row in data]
    return render_template('show_entries_2.html', entries=entries)

@app.route('/show_entries_3/')
def show_entries_3():
    sql = 'select gid, gcd, ginum, flag from GoodInventory order by gcd desc,gid desc'
    cursor.execute(sql)
    connect.commit()
    data = cursor.fetchall()
    entries = [dict(id=row[0], gcd=row[1], ginum=row[2], flag=row[3]) for row in data]
    return render_template('show_entries_3.html', entries=entries)

@app.route('/show_entries_4')
def show_entries_4():
    sql = 'select gid, sellid, selldate, snum, sp from GoodSell order by selldate desc,gid desc'
    cursor.execute(sql)
    connect.commit()
    data = cursor.fetchall()
    entries = [dict(id=row[0], sellid=row[1], selldate=row[2], snum=row[3], sp=row[4]) for row in data]
    return render_template('show_entries_4.html', entries=entries)

@app.route('/show_entry/<int:id>')
def show_entry(id):
    id = str(id)
    sql = 'select * from entries WHERE id=' + id
    cursor.execute(sql)
    connect.commit()
    data = cursor.fetchall()
    entries = [dict(id=row[0], title=row[1], post=row[2]) for row in data]
    return render_template('show_entries.html', entries=entries)
    connect.close()


@app.route('/edit_entry/<int:id>')
def edit_entry(id):
    if not session.get('logged_in'):
        abort(401)
    id = str(id)
    sql = 'select * from Good WHERE gid=' + id
    cursor.execute(sql)
    connect.commit()
    data = cursor.fetchall()
    entries = [dict(id=row[0], gclass=row[1], gname=row[2], gsize=row[3], gpro=row[4]) for row in data]
    # entries = [{"title": row[0], "text": row[1], "id": row[2]} for row in data]
    return render_template('edit_entry.html', entries=entries)
    connect.close()

@app.route('/edit_entry_2/<int:id>/<string:gpdata>')
def edit_entry_2(id,gpdata):
    if not session.get('logged_in'):
        abort(401)
    id = str(id)
    sql2 = 'select * from  GoodPurchase WHERE gid=' + id +' and gpdata='+"'{}'"
    sql=sql2.format(gpdata)
    cursor.execute(sql)
    connect.commit()
    data = cursor.fetchall()
    entries = [dict(id=row[0], gpdata=row[1], gpnum=row[2], gpp=row[3]) for row in data]
    # entries = [{"title": row[0], "text": row[1], "id": row[2]} for row in data]
    return render_template('edit_entry_2.html', entries=entries)
    connect.close()

@app.route('/edit_entry_3/<int:id>/<string:gcd>')
def edit_entry_3(id,gcd):
    if not session.get('logged_in'):
        abort(401)
    id = str(id)
    sql2 = 'select * from  GoodInventory WHERE gid=' + id + ' and gcd=' + "'{}'"
    sql = sql2.format(gcd)
    cursor.execute(sql)
    connect.commit()
    data = cursor.fetchall()
    entries = [dict(id=row[0], gcd=row[1], ginum=row[2], flag=row[3]) for row in data]
    # entries = [{"title": row[0], "text": row[1], "id": row[2]} for row in data]
    return render_template('edit_entry_3.html', entries=entries)
    connect.close()

@app.route('/edit_entry_4/<int:id>/<int:sellid>/<string:selldate>')
def edit_entry_4(id,sellid,selldate):
    if not session.get('logged_in'):
        abort(401)
    id = str(id)
    sql2 = 'select * from  GoodSell WHERE gid=' + id + ' and sellid=' + '{}'+' and selldate='+"'{}'"
    sql = sql2.format(sellid, selldate)
    cursor.execute(sql)
    connect.commit()
    data = cursor.fetchall()
    entries = [dict(id=row[0], sellid=row[1], selldate=row[2], snum=row[3], sp=row[4]) for row in data]
    # entries = [{"title": row[0], "text": row[1], "id": row[2]} for row in data]
    return render_template('edit_entry_4.html', entries=entries)
    connect.close()


@app.route('/update_entry_1/<int:id>', methods=['GET', 'POST'])
def update_entry_1(id):
    try:
        id = str(id)
        id_2=request.form['id']
        gclass = request.form['gclass']
        gname = request.form['gname']
        gsize = request.form['gsize']
        gpro =request.form['gpro']
        sql2= "UPDATE GOOD SET gid ='{}',gclass='{}', gname ='{}',gsize = '{}',gpro = '{}'  WHERE gid=" + id
        sql=sql2.format(id_2, gclass, gname, gsize, gpro)
        cursor.execute(sql)
        connect.commit()
        # connect.close()
        flash('已修改一条记录')
    except cx_Oracle.IntegrityError:
        abort(403)
    except cx_Oracle.DatabaseError:
        abort(403)
    return redirect(url_for('show_entries_1'))

@app.route('/update_entry_2/<int:id>', methods=['GET', 'POST'])
def update_entry_2(id):
    try:
        id = str(id)
        gpdata = request.form['gpdata']
        gpnum = request.form['gpnum']
        gpp = request.form['gpp']
        sql2 = "UPDATE GoodPurchase SET gpdata ='{}',gpnum ='{}',gpp = '{}'  WHERE gid=" + id +' and gpdata='+"'{}'"
        sql = sql2.format(gpdata, gpnum, gpp, gpdata)
        cursor.execute(sql)
        connect.commit()
        # connect.close()
        flash('已修改一条记录')
    except cx_Oracle.IntegrityError:
        abort(403)
    except cx_Oracle.DatabaseError:
        abort(403)
    return redirect(url_for('show_entries_2'))

@app.route('/update_entry_3/<int:id>', methods=['GET', 'POST'])
def update_entry_3(id):
    try:
        id = str(id)
        gcd = request.form['gcd']
        ginum = request.form['ginum']
        flag = request.form['flag']
        sql2 = "UPDATE GoodInventory SET gcd ='{}',ginum ='{}',flag = '{}'  WHERE gid=" + id +' and gcd=' + "'{}'"
        sql = sql2.format(gcd, ginum, flag, gcd)
        cursor.execute(sql)
        connect.commit()
        # connect.close()
        flash('已修改一条记录')
    except cx_Oracle.IntegrityError:
        abort(403)
    except cx_Oracle.DatabaseError:
        abort(403)
    return redirect(url_for('show_entries_3'))

@app.route('/update_entry_4/<int:id>', methods=['GET', 'POST'])
def update_entry_4(id):
    try:
        id = str(id)
        sellid = request.form['sellid']
        selldate = request.form['selldate']
        snum = request.form['snum']
        sp = request.form['sp']
        sql2= "UPDATE GoodSell SET sellid ='{}',selldate ='{}',snum = '{}',sp = '{}'  WHERE gid=" + id + ' and sellid=' + '{}'+' and selldate='+"'{}'"
        sql=sql2.format(sellid, selldate, snum, sp, sellid, selldate)
        cursor.execute(sql)
        connect.commit()
        # connect.close()
        flash('已修改一条记录')
    except cx_Oracle.IntegrityError:
        abort(403)
    except cx_Oracle.DatabaseError:
        abort(403)
    return redirect(url_for('show_entries_4'))


@app.route('/delete_entry_1/<int:id>')
def delete_entry_1(id):
    if not session.get('logged_in'):
        abort(401)
    id = str(id)
    sql = 'delete from Good WHERE gid=' + id
    cursor.execute(sql)
    connect.commit()
    sql = 'select gid , gclass, gname, gsize, gpro from Good order by gid desc'
    cursor.execute(sql)
    connect.commit()
    data = cursor.fetchall()
    entries = [dict(id=row[0], gclass=row[1], gname=row[2], gsize=row[3], gpro=row[4]) for row in data]
    # entries = [{"title": row[0], "text": row[1], "id": row[2]} for row in data]
    return render_template('show_entries.html', entries=entries)
    connect.close()

@app.route('/delete_entry_2/<int:id>/<string:gpdata>')
def delete_entry_2(id,gpdata):
    if not session.get('logged_in'):
        abort(401)
    id = str(id)
    sql = 'delete from GoodPurchase WHERE gid=' + id +' and gpdata='+"'{}'".format(gpdata)
    cursor.execute(sql)
    connect.commit()
    sql = 'select gid , gpdata, gpnum, gpp from GoodPurchase order by gid desc'
    cursor.execute(sql)
    connect.commit()
    data = cursor.fetchall()
    entries = [dict(id=row[0], gpdata=row[1], gpnum=row[2], gpp=row[3]) for row in data]
    # entries = [{"title": row[0], "text": row[1], "id": row[2]} for row in data]
    return render_template('show_entries_2.html', entries=entries)
    connect.close()
@app.route('/delete_entry_3/<int:id>/<string:gcd>')
def delete_entry_3(id,gcd):
    if not session.get('logged_in'):
        abort(401)
    id = str(id)
    sql = 'delete from GoodInventory WHERE gid=' + id +' and gcd=' + "'{}'".format(gcd)
    cursor.execute(sql)
    connect.commit()
    sql = 'select gid , gcd, ginum, flag from GoodInventory order by gid desc'
    cursor.execute(sql)
    connect.commit()
    data = cursor.fetchall()
    entries = [dict(id=row[0], gcd=row[1], ginum=row[2], flag=row[3]) for row in data]
    # entries = [{"title": row[0], "text": row[1], "id": row[2]} for row in data]
    return render_template('show_entries_3.html', entries=entries)
    connect.close()

@app.route('/delete_entry_4/<int:id>/<string:sellid>/<string:selldate>')
def delete_entry_4(id,sellid,selldate):
    if not session.get('logged_in'):
        abort(401)
    id = str(id)
    sql = 'delete from GoodSell WHERE gid=' + id + ' and sellid=' + '{}'.format(sellid)+' and selldate='+"'{}'".format(selldate)
    cursor.execute(sql)
    connect.commit()
    sql = 'select gid , sellid, selldate, snum, sp from GoodSell order by gid desc'
    cursor.execute(sql)
    connect.commit()
    data = cursor.fetchall()
    entries = [dict(id=row[0], sellid=row[1], selldate=row[2], snum=row[3], sp=row[4]) for row in data]
    # entries = [{"title": row[0], "text": row[1], "id": row[2]} for row in data]
    return render_template('show_entries_4.html', entries=entries)
    connect.close()


@app.route('/add_1', methods=['POST'])
def add_entry_1():
    if not session.get('logged_in'):
        abort(401)
    try:
        sql2 = "insert into Good (gid, gclass, gname, gsize, gpro) values ('{}','{}','{}','{}','{}')"
        sql = sql2.format(request.form['id'], request.form['gclass'], request.form['gname'],request.form['gsize'], request.form['gpro'])
        cursor.execute(sql)
        connect.commit()
        # connect.close()
        flash('已新增一条记录')
    except cx_Oracle.IntegrityError:
        abort(403)
    return redirect(url_for('show_entries_1'))

@app.route('/add_2', methods=['POST'])
def add_entry_2():
    if not session.get('logged_in'):
        abort(401)
    try:
        sql2 = "insert into GoodPurchase (gid, gpdata, gpnum, gpp) values ('{}','{}','{}','{}')"
        sql = sql2.format(request.form['id'], request.form['gpdata'], request.form['gpnum'],request.form['gpp'])
        cursor.execute(sql)
        connect.commit()
        sql="select gcd from GoodInventory"
        cursor.execute(sql)
        connect.commit()
        res=cursor.fetchall()
        if(res):
            b=res[-1][0]
            c = int("".join(list(filter(str.isdigit, b))))
            e=request.form['gpdata']
            d = int("".join(list(filter(str.isdigit, e))))
            '''
            if d > c:
                sql="update GoodInventory set flag = 0 "
                cursor.execute(sql)
                connect.commit()
            '''
            sql3="select * from GoodInventory where gid='{}'".format(request.form['id'])
            cursor.execute(sql3)
            res=cursor.fetchall()
            if(res):
                sql4="update GoodInventory t set t.gcd = '{}',t.ginum=t.ginum+'{}',flag=1 where gid='{}'".format(request.form['gpdata'],request.form['gpnum'],request.form['id'])
                cursor.execute(sql4)
            else:
                sql5="insert into GoodInventory(gid,gcd,ginum,flag) values('{}','{}','{}','{}')".format(request.form['id'],request.form['gpdata'],request.form['gpnum'],1)
                cursor.execute(sql5)
            if d > c:
                sql = "update GoodInventory set flag = 0 where gcd!='{}' ".format(e)
                cursor.execute(sql)
                connect.commit()
        # connect.close()
            flash('已新增一条记录')
        else:
            sql5 = "insert into GoodInventory(gid,gcd,ginum,flag) values('{}','{}','{}','{}')".format(request.form['id'],request.form['gpdata'],request.form['gpnum'], 1)
            cursor.execute(sql5)
    except cx_Oracle.IntegrityError:
        abort(403)
    return redirect(url_for('show_entries_2'))

@app.route('/add_3', methods=['POST'])
def add_entry_3():
    if not session.get('logged_in'):
        abort(401)
    try:
        sql2 = "insert into goodinventory (gid, gcd, ginum, flag) values ('{}','{}','{}','{}')"
        sql = sql2.format(request.form['id'], request.form['gcd'], request.form['ginum'], request.form['flag'])
        cursor.execute(sql)
        connect.commit()
        # connect.close()
        flash('已新增一条记录')
    except cx_Oracle.IntegrityError:
        abort(403)
    return redirect(url_for('show_entries_3'))

@app.route('/add_4', methods=['POST'])
def add_entry_4():
    if not session.get('logged_in'):
        abort(401)
    try:
        sql="select ginum from GoodInventory where gid='{}'".format(request.form['id'])
        cursor.execute(sql)
        connect.commit()
        res=cursor.fetchall()
        if(res):
            a=int(request.form['snum'])
            if(a<=(res[0])[0]):
                sql2 = "insert into goodsell (gid, sellid, selldate, snum, sp) values ('{}','{}','{}','{}','{}')"
                sql = sql2.format(request.form['id'], request.form['sellid'], request.form['selldate'], request.form['snum'], request.form['sp'])
                cursor.execute(sql)
                connect.commit()
                # connect.close()
                flash('已新增一条记录')
                sql="update GoodInventory set ginum=ginum-'{}' where gid='{}'".format(request.form['snum'],request.form['id'])
                cursor.execute(sql)
                connect.commit()
            else:
                abort(404)
        else:
            abort(403)
    except cx_Oracle.IntegrityError:
        abort(403)
    return redirect(url_for('show_entries_4'))


@app.route('/select_1', methods=['POST'])
def select_entry_1():
    if not session.get('logged_in'):
        abort(401)
    sql=''
    entries = dict(gid=request.form['id'], gclass=request.form['gclass'], gname=request.form['gname'], gsize=request.form['gsize'], gpro=request.form['gpro'])
    #entries_len=len(entries)
    for k, v in entries.items():
        if v:
            sql+="{}='{}' and ".format(k,v)
    res = 'select gid, gclass, gname, gsize, gpro from Good where {}'.format(sql)
    res=res.strip()
    res=res.strip('and')
    cursor.execute(res)
    connect.commit()
    data = cursor.fetchall()
    entries = [dict(id=row[0], gclass=row[1], gname=row[2], gsize=row[3], gpro=row[4]) for row in data]
    # entries = [{"title": row[0], "text": row[1], "id": row[2]} for row in data]
    res='select count(*) from Good where {}'.format(sql)
    res=res.strip()
    res=res.strip('and')
    cursor.execute(res)
    res=cursor.fetchall()
    num1=(res[0])[0]
    res = 'select count(distinct gclass) from Good where {}'.format(sql)
    res = res.strip()
    res = res.strip('and')
    cursor.execute(res)
    res = cursor.fetchall()
    num2 = (res[0])[0]
    res = 'select count(distinct gsize) from Good where {}'.format(sql)
    res = res.strip()
    res = res.strip('and')
    cursor.execute(res)
    res = cursor.fetchall()
    num3 = (res[0])[0]
    res = 'select count(distinct gpro) from Good where {}'.format(sql)
    res = res.strip()
    res = res.strip('and')
    cursor.execute(res)
    res = cursor.fetchall()
    num4 = (res[0])[0]
    flash("共查询到{}条记录,其中有{}种型号，有{}种规格，有{}个生产厂家，具体结果如下".format(num1,num2,num3,num4))
    return render_template('show_entries.html', entries=entries)
    # connect.close()

@app.route('/select_2', methods=['POST'])
def select_entry_2():
    if not session.get('logged_in'):
        abort(401)
    sql=''
    entries = dict(gid=request.form['id'], gpdata=request.form['gpdata'], gpnum=request.form['gpnum'], gpp=request.form['gpp'])
    #entries_len=len(entries)
    for k, v in entries.items():
        if v:
            sql+="{}='{}' and ".format(k,v)
    res = 'select gid, gpdata, gpnum, gpp from GoodPurchase where {}'.format(sql)
    res=res.strip()
    res=res.strip('and')
    cursor.execute(res)
    connect.commit()
    data = cursor.fetchall()
    entries = [dict(id=row[0], gpdata=row[1], gpnum=row[2], gpp=row[3]) for row in data]
    # entries = [{"title": row[0], "text": row[1], "id": row[2]} for row in data]
    res = 'select sum(gpnum) from GoodPurchase where {}'.format(sql)
    res = res.strip()
    res = res.strip('and')
    cursor.execute(res)
    res = cursor.fetchall()
    num = (res[0])[0]
    flash("该商品库存为{}".format(num))
    return render_template('show_entries_2.html', entries=entries)
    # connect.close()

@app.route('/select_4', methods=['POST'])
def select_entry_4():
    if not session.get('logged_in'):
        abort(401)
    sql=''
    entries = dict(gid=request.form['id'], sellid=request.form['sellid'], selldate=request.form['selldate'], snum=request.form['snum'], sp=request.form['sp'])
    #entries_len=len(entries)
    for k, v in entries.items():
        if v:
            sql+="{}='{}' and ".format(k,v)
    res = 'select gid, sellid, selldate, snum, sp from GoodSell where {}'.format(sql)
    res=res.strip()
    res=res.strip('and')
    cursor.execute(res)
    connect.commit()
    data = cursor.fetchall()
    entries = [dict(id=row[0], sellid=row[1], selldate=row[2], snum=row[3], sp=row[4]) for row in data]
    # entries = [{"title": row[0], "text": row[1], "id": row[2]} for row in data]
    res = 'select sum(snum) from GoodSell where {}'.format(sql)
    res = res.strip()
    res = res.strip('and')
    cursor.execute(res)
    res = cursor.fetchall()
    num1 = (res[0])[0]
    res = 'select sum(sp*snum) from GoodSell where {}'.format(sql)
    res = res.strip()
    res = res.strip('and')
    cursor.execute(res)
    res = cursor.fetchall()
    num2 = (res[0])[0]
    '''
    res = 'select gpp from GoodPurchase where {}
    res = res.strip()
    res = res.strip('and')
    cursor.execute(res)
    res = cursor.fetchall()
    num3 = (res[0])[0]
    '''
    flash("该商品符合条件的销售数量为{},销售总金额为{}".format(num1,num2))
    return render_template('show_entries_4.html', entries=entries)
    # connect.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You are now logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You are now logged out')
    return redirect(url_for('show_entries_1'))

@app.errorhandler(401)
def handle_404_error(error):
    return "您尚未登陆，请登陆后再操作！"

@app.errorhandler(403)
def handle_404_error(error):
    return "您的输入有误，请重新输入！"

@app.errorhandler(404)
def handle_404_error(error):
    return "库存不足！"

if __name__ == '__main__':
    app.run(
        debug=True,
        #host='127.0.0.1',
        host='0.0.0.0',
        port=9803
    )
    # app.debug = True