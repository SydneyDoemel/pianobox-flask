from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from collections import Counter
from flask_cors import CORS, cross_origin
from ..apiauthhelper import token_required



#import login funcitonality
from flask_login import login_required, current_user


# import models
from app.models import IgShop, User, Carts, Songs
shop = Blueprint('shop', __name__, template_folder='shoptemplates')
from app.models import db


@shop.route('/shop')
def shopPage():
    x = IgShop.query.all()
    return render_template('shop.html', x=x)


@shop.route('/add/<string:title>')
@login_required
def addToCart(title):
    item = IgShop.query.filter_by(title=title).first()
    x = Carts(user_id=current_user.id, ig_shop_id=item.id)
    print(x)
    x.save()
    flash('Succesfully added to cart.', 'success')
    return redirect(url_for('shop.shopPage'))


 

@shop.route('/cart')
def cartPage():
    items =Carts.query.filter_by(user_id=current_user.id).all()
    items_lst = []
    qty = 0
    for each in items:
        item = IgShop.query.get(each.ig_shop_id)
        items_lst.append(item)
    grand_total = 0
    for each in items_lst:
        grand_total += int(each.price)
    print(items)
    return render_template('cart.html', items_lst = items_lst, grand_total = grand_total)

@shop.route('/cart/<string:title>')
@login_required
def seeItem(title):
    item = IgShop.query.filter_by(title=title).first()
    see =Carts.query.filter_by(user_id=current_user.id, ig_shop_id = item.id).first()
    return render_template('see.html', item = item)



@shop.route('/del/<string:title>')
@login_required
def removeFromCart(title):
    item = IgShop.query.filter_by(title=title).first()
    x =Carts.query.filter_by(user_id=current_user.id, ig_shop_id = item.id).first()
    x.delete()
    flash('Succesfully removed from cart.', 'danger')
    return redirect(url_for('shop.cartPage'))


@shop.route('/del')
@login_required
def removeAll():
    x = Carts.query.filter_by(user_id = current_user.id).all()
    for each in x:
        each.delete()
    flash('Succesfully removed from cart.', 'danger')
    return redirect(url_for('shop.cartPage'))



# ########## ########## #########
# API ROUTES
@shop.route('/api/shop')
def getShopAPI():
    # args = request.args
    # pin = args.get('pin')
    # print(pin, type(pin))
    # if pin == '1234':

        shop = IgShop.query.all()

        shop_items = [s.to_dict() for s in shop]
        return {'status': 'ok', 'total_results': len(shop), "items": shop_items}
    # else:
    #     return {
    #         'status': 'not ok',
    #         'code': 'Invalid Pin',
    #         'message': 'The pin number was incorrect, please try again.'
    #     }

@shop.route('/api/shop/<int:item_id>')
def getShopItemAPI(item_id):
    item = IgShop.query.filter_by(id=item_id).first()
    if item:
        return {
            'status': 'ok',
            'total_results': 1,
            "item": item.to_dict()
            }
    else:
        return {
            'status': 'not ok',
            'message': f"An item with the id : {item.id} does not exist."
        }





#####fix below?
@shop.route('/api/cart/add', methods=["POST"])
@cross_origin()
@token_required
def addToCartAPI(user):
    try:
        data = request.json
        title=data['title']
        item = IgShop.query.filter_by(title=title).first()
        print(item.id)
        print(user.id)
        x = Carts(user.id, item.id)
        print(x)
        x.save()
        
        return {
            'status': 'ok',
            'message': "Succesfully added to cart."
        }
    except:
        return {
            'status': 'not ok',
            'message': "Not succesful."
        }


@shop.route('/api/cart/del',  methods=['POST'])
@cross_origin()
@token_required
def removeFromCartAPI(user):
    data = request.json
    title=data['title']
    item = IgShop.query.filter_by(title=title).first()
    x =Carts.query.filter_by(user_id=user.id, ig_shop_id = item.id).first()
    x.delete()
    
    return {
        'status': 'ok',
        'message': "Item was successfully deleted."
    }



@shop.route('/api/del',  methods=['POST'])
@cross_origin()
@token_required
def removeAllAPI(user):
    
    x = Carts.query.filter_by(user_id = user.id).all()
    for each in x:
        each.delete()
  
    return {
        'status': 'ok',
        'message': "Cart was successfully cleared."
    }


@shop.route('/api/cart')
@token_required
def getCartAPI(user):
 
    cart = Carts.query.filter_by(user_id=user.id).all()
    print(cart)
    cart_items = [s.to_dict() for s in cart]
    items_lst = []
    qty = 0
    for each in cart:
        item = IgShop.query.get(each.ig_shop_id)
        items_lst.append(item)
    cart_items = [s.to_dict() for s in items_lst]
    if cart_items:
    
        return {'status': 'ok', 'total_results': len(cart), "items": cart_items}


@shop.route('/song/api',  methods=['POST'])
@cross_origin()
def postSong():
    blob = request.data
    new = Songs(blob)
    new.save()
    with open('file.wav', 'ab') as f:
        f.write(blob)
    return {'status': 'ok'}
    


    
@shop.route('/api/getsong', methods=['GET'])

def getSong():
 
    song = Songs.query.filter_by(id=1)
    print(song)
    
   
    
    return {'status': 'ok', 'song': song}
