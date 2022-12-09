from flask import Flask, render_template, session, redirect, url_for, request, Blueprint
import models
from datetime import date

#create a Blueprint variable named admin_page.
admin_page = Blueprint('admin_page', __name__, template_folder='templates/admin')

def logged_in():
    if 'username' not in session or 'admin' not in session['userroles']:
        return False
    else:
        return True
@admin_page.route("/admin/")
def admin():
    if not logged_in():
        return redirect(url_for('login', next='/admin/'))

    # username in session and user has admin role, continue
    return render_template('index.html')

@admin_page.route("/admin/products/")
def products():
    if not logged_in():
        return redirect(url_for('login', next='/admin/products/'))

    # username in session, continue
    # get our registered products from the database
    products = models.Product.query.all()

    # check whether when products route was called using redirect, information was passed.
    # If not passed, use a default message, 'Here you can administer products'
    information = request.args.get('information')

    # check whether when products route was called using redirect, css was passed.
    # If not passed, use default css 'normal'
    css = request.args.get('css', 'normal')

    return render_template('products.html', css=css, products=products)

@admin_page.route("/admin/products/process-product-add/", methods=['POST','GET'])
def process_product_add():
    if not logged_in():
        return redirect(url_for('login', next='/admin/products/'))
    # username in session and admin role, continue

    if request.method != 'POST':
        # return to products.html page containing add form. Only POST method is allowed
        error = 'Please use the form to add new products'
        return render_template('products.html', title="ADMINISTER PRODUCTS", information=error, css="error")

    # No problem so far, get the request object and the parameters sent from the form.
    type = request.form['type']
    name = request.form['name']
    description = request.form['description']
    weight = request.form['weight']
    price_per_unit = request.form['price_per_unit']
    quantity = request.form['quantity']
    product_inception_date = request.form['product_inception_date']

    # let's write to the database
    try:
        product = models.Product(type=type, name=name, description=description, weight=weight, price_per_unit=price_per_unit, quantity=quantity, product_inception_date=product_inception_date)
        models.db.session.add(product)
        models.db.session.commit()
    except Exception as e:
        error = 'Could not submit. The error message is {}'.format(e.__cause__)
        return render_template('products.html', title="ADMINISTER PRODUCTS", information=error, css="error")

        # no error, continue
    return redirect(url_for('admin_page.products', information="Add successful", css="success"))

@admin_page.route("/admin/products/edit/<int:id>/", methods=['POST','GET'])
def product_edit(id):
    # check database for the product to edit
    product = models.Product.query.filter_by(id=id).first()
    # send to the edit form
    return render_template('product-edit.html', product=product)

@admin_page.route("/admin/products/process-product-edit/<int:id>/", methods=['POST', 'GET'])
def process_product_edit(id):
    if not logged_in():
        return redirect(url_for('login', next='/admin/products/'))
    # username in session and admin in role, continue

    if request.method != 'POST':
        # redirect to signup form. Only POST method is allowed
        error = 'Please use the form to edit products'
        return render_template('products.html', title="ADMINISTER PRODUCTS", information=error, css="error")

    # No problem so far, get the request object and the parameters sent.
    type = request.form['type']
    name = request.form['name']
    description = request.form['description']
    weight = request.form['weight']
    price_per_unit = request.form['price_per_unit']
    quantity = request.form['quantity']
    product_inception_date = request.form['product_inception_date']

    # let's update the database
    try:
        # Get the existing data from database as object
        product = models.Product.query.filter_by(id=id).first()
        # Update the fields
        product.type = type
        product.name = name
        product.description = description
        product.weight = weight
        product.price_per_unit = price_per_unit
        product.quantity = quantity
        product.product_inception_date = product_inception_date
        # commit
        models.db.session.commit()

    except Exception as e:
        error = 'Could not update product. The error message is {}'.format(e.__cause__)
        return redirect(url_for('admin_page.products', information="Update not successful", css="error"))

    return redirect(url_for('admin_page.products', information="Update successful", css="success"))

@admin_page.route("/admin/products/delete/<int:id>/", methods=['POST', 'GET'])
def product_delete(id):
    if not logged_in():
        return redirect(url_for('login', next='/admin/products/'))

    # username in session and admin role, continue

    # No problem so far
    # let's update the database
    try:
        # Get the existing data from database as object
        product = models.Product.query.filter_by(id=id).first()
        # Delete the record
        models.db.session.delete(product)
        # commit
        models.db.session.commit()
    except Exception as e:
        error = 'Could not delete product. The error message is {}'.format(e.__cause__)
        return redirect(url_for('admin_page.products', information="Delete not successful", css="error"))

    return redirect(url_for('admin_page.products', information="Delete successful", css="success"))

@admin_page.route("/admin/customer/")
def customer():
    if not logged_in():
        return redirect(url_for('login', next='/admin/customer/'))

    # username in session, continue
    # get our registered customer from the database
    Customer = models.Customer.query.all()

    information = request.args.get('information')

    css = request.args.get('css', 'normal')

    return render_template('customer.html', css=css, customer=Customer)

@admin_page.route("/admin/customer/process-customer-add/", methods=['POST','GET'])
def process_customer_add():
    if not logged_in():
        return redirect(url_for('login', next='/admin/customer/'))
    # username in session and admin role, continue

    if request.method != 'POST':
        # return to customer.html page containing add form. Only POST method is allowed
        error = 'Please use the form to add a new customer'
        return render_template('customer.html', title="ADD CUSTOMER INFO", information=error, css="error")

    # No problem so far, get the request object and the parameters sent from the form.
    name = request.form['name']
    email = request.form['email']
    Phone_number = request.form['Phone_number']
    address = request.form['address']

    # let's write to the database
    try:
        Customer = models.Customer(name=name, email=email, Phone_number=Phone_number, address=address)
        models.db.session.add(Customer)
        models.db.session.commit()
    except Exception as e:
        error = 'Could not submit. The error message is {}'.format(e.__cause__)
        return render_template('customer.html', title="ADMINISTER PRODUCTS", information=error, css="error")

        # no error, continue
    return redirect(url_for('admin_page.customer', information="Add successful", css="success"))
