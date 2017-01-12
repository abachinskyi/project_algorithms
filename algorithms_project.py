from flask import Flask
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash,send_from_directory

from werkzeug import secure_filename, SharedDataMiddleware

from products_shops import Products_shops
from algorithm import main_func

import numpy as np
import jinja2
import os

app = Flask(__name__, static_url_path='/static')
prods=['apple','banana','carrot','garlic','lemon','mushroom','orange','pea','peanut','pepper',
          'pineapple', 'strawberry', 'potato', 'tomato', 'watermelon','juice','bacon','beans',
          'beer', 'bread', 'cheese', 'chicken', 'coffee','corn','eggs', 'fish','ham','honey',
          'ketchup', 'milk', 'pasta','wine', 'vodka','yogurt','cream', 'onion','salmon','tea',
          'cabbage','rice','butter','sausage','beef','strawberry','cucumber', 'water','sugar',
          'salt','flour','pork']
@app.route('/calculate',methods=['GET','POST'])
def calculate():
    if request.method =='POST':
        print(request.form.getlist('input'))
        products = request.form.getlist('input')
        res_prod = []
        for i in products:
            tmp = i.split('val')[1]
            res_prod.append(prods[int(tmp) - 1])
        c_type = request.form['case']
        x_coord = request.form['coord_x']
        y_coord = request.form['coord_y']
        print x_coord
        print y_coord
        print c_type
        print res_prod
        #make processing
        totals, path, what_and_where = main_func(res_prod, c_type, x_coord, y_coord)
        total_price = totals[0]
        total_path = totals[1]
        opt_path = 'Home -> '
        path=path[1:-1]
        for i in range(len(path)):
            opt_path += str(path[i])
            opt_path += ' -> '
        opt_path += 'Home'
        shops = []
        for i in what_and_where.keys():
            shops.append(Products_shops(str(i), what_and_where[i]))
        return render_template('result_page.html', price=total_price, dist=total_path, opt_path=opt_path, shops=shops)
    return render_template('main_page.html')


@app.route('/test_shop')
def test_shop():
    total_price = 22.27
    total_path = 256.03196454
    path = [3, 7, 8, 2, 1, 4, 5]
    what_and_where = {1: ['apple'], 2: ['chicken'], 3: ['pasta'], 4: ['sausage', 'salt'], 5: ['vodka', 'rice', 'bread'],
                      7: ['juice'], 8: ['ketchup']}
    coords = {0: (86, 12), 1: (33, 36), 2: (57, 11), 3: (87, 68), 4: (8, 68), 5: (45, 64), 6: (4, 3), 7: (72, 2),
              8: (59, 13), 9: (34, 31)}

    opt_path = 'Home -> '
    for i in range(len(path)):
        opt_path += str(path[i])
        opt_path += ' -> '
    opt_path += 'Home'
    shops = []
    for i in what_and_where.keys():
        shops.append(Products_shops(str(i), what_and_where[i]))
    return render_template('result_page.html',price=total_price, dist=total_path, opt_path=opt_path, shops=shops)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)
