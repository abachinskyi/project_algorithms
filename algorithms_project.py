from flask import Flask
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash,send_from_directory

from werkzeug import secure_filename, SharedDataMiddleware

from products_shops import Products_shops
from algorithm import main_func

import numpy as np
import jinja2
import os

app = Flask(__name__)

@app.route('/calculate',methods=['GET','POST'])
def calculate():
    if request.method =='POST':
        print(request.form.getlist('hello'))
        products = request.form.getlist('hello')
        c_type = request.form['case']
        x_coord = request.form['coord_x']
        y_coord = request.form['coord_y']
        print x_coord
        print y_coord
        print c_type
        #make processing
        totals, path, what_and_where = main_func(c_type, products, x_coord, y_coord)
        total_price = totals[0]
        total_path = totals[1]
        opt_path = 'Home -> '
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
    '''
    total_price = 22.27
    total_path = 256.03196454
    path = [3, 7, 8, 2, 1, 4, 5]
    what_and_where = {1: ['apple'], 2: ['chicken'], 3: ['pasta'], 4: ['sausage', 'salt'], 5: ['vodka', 'rice', 'bread'],
                      7: ['juice'], 8: ['ketchup']}
    coords = {0: (86, 12), 1: (33, 36), 2: (57, 11), 3: (87, 68), 4: (8, 68), 5: (45, 64), 6: (4, 3), 7: (72, 2),
              8: (59, 13), 9: (34, 31)}
    '''
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
    app.run()
