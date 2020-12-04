from flask import Flask, redirect, render_template, flash, request, url_for
import xmlrpc.client
import json
import requests
import shopify
import forms
app = Flask(__name__)
app.config['SECRET_KEY'] = "Secret key here"
app.config['SHOPIFY_API_KEY'] = "f4d3179bd388e45e631e0f147a2c6027"
app.config['SHOPIFY_PASSWORD'] = "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"
app.config['SHOPIFY_STORE_DOMAIN'] = "test-store-4325.myshopify.com"

@app.route('/', methods=('GET', 'POST'))
def home():
    info = xmlrpc.client.ServerProxy('https://demo.odoo.com/start').start()
    url, db, username, password = \
        info['host'], info['database'], info['user'], info['password']

    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    ids = models.execute_kw(db, uid, password,
                            'product.product', 'search',
                            [[]])
    print(str(ids))
    form = forms.OdooProductForm()
    if form.validate_on_submit():
        return redirect('/get-and-push-product-into-odoo/' + form.product_id.data)
    return render_template('home.html', odoo_product_ids=ids, form=form)

@app.route('/get-and-push-product-into-odoo/<product_id>')
def get_odoo_and_push(product_id):
    #get proxy server
    info = xmlrpc.client.ServerProxy('https://demo.odoo.com/start').start()
    url, db, username, password = \
        info['host'], info['database'], info['user'], info['password']
    #make proxy server?
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    #login
    uid = common.authenticate(db, username, password, {})
    #get models
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    #parse first record
    print(product_id)
    models.execute_kw(db, uid, password,
                            'product.product', 'search',
                            [[]])
    product_id = int(product_id)
    [record] = models.execute_kw(db, uid, password,
                                 'product.product', 'read', [[product_id]])
    session = shopify.Session(app.config['SHOPIFY_STORE_DOMAIN'], "2020-10", app.config['SHOPIFY_PASSWORD'])
    shopify.ShopifyResource.activate_session(session)
    product = shopify.Product()
    product.title = record['name']
    product.price = record['price']
    product.weight = record['weight'],
    product.weight_unit = record['weight_uom_name']
    product.save()
    return redirect('/')

if __name__ == '__main__':
    #collect_and_save_shopify_data()
    #collect_and_save_amazon_data()
    app.run(threaded=True)
