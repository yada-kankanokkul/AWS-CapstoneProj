from django.shortcuts import render                            
from django.http import HttpResponse                           
from .models import Product, Order, Order_Item
from django.template import loader                     

import json
import pprint                                     
from django.core import serializers

def index(request):
    print('\n***LOG: in "index" function')
    product_items = Product.objects.all()

    #The 4 lines below used during VIEW TESTING 
    jsondata = serializers.serialize('json', product_items)  
    json_to_runserver = json.loads(jsondata)
    pprint.pprint(json_to_runserver)
    # return HttpResponse('/ page loaded. Check the runserver console for test result.')
    context = {'product_items': product_items}    
    return render(request, "test_form.html", context)


def all_orders(request):
    print('\n***LOG: in "all_orders" function')
    orders = Order.objects.all() 

    #The 4 lines below used during VIEW TESTING 
    jsondata = serializers.serialize('json', orders)  
    json_to_runserver = json.loads(jsondata)
    pprint.pprint(json_to_runserver)
    return HttpResponse('/order_history page loaded. Check the runserver console for test result.') 

    #The 2 lines below are uncommented in the next lab
    #context = {'orders': orders}
    #return render(request, "order_history.html", context)

def lookup_order(request, order_id):
    print('\n***LOG: in "lookup_order" function')
    order = Order.objects.filter(id=order_id)

    #The 4 lines below used during VIEW TESTING 
    jsondata = serializers.serialize('json', order)  
    json_to_runserver = json.loads(jsondata)
    pprint.pprint(json_to_runserver)
    return HttpResponse('/lookup_order page loaded. Check the runserver console for test result.')
    
    #The 3 lines below are uncommented in the next lab
    #items = Order_Item.objects.filter(order_number=order_id).values() 
    #context = {'order_details': items, 'order': order}
    #return render(request, "order_result.html", context)


def process_order(request):
    print('\n***LOG: in "process_order" function')
    if request.method == "POST":
        print('LOG: in "process_order" function - POST received')
        #save POST data and convert from Djanjo QueryDict to Python Dict
        received_data = dict(request.POST)

        # parse into Python "lists"
        product_name = received_data['product_name']
        print('product_name = ' + str(product_name))
        product_id = received_data['product_id']
        print('product_id = ' + str(product_id))
        item_price = received_data['amount']
        print('item_price = ' + str(item_price))
        quantity = received_data['quantity']
        print('quantity = ' + str(quantity))
        
        #ITERATE THROUGH SUBMITTED DATA
        i = 0
        items = []
        total_order_amount = float(0)
        for i in range(len(quantity)):
            if int(quantity[i]) != int(0):
                print('ITEM WANTED: ' + product_name[i] + ' - quantity: ' + quantity[i])
                total_order_amount += float(quantity[i])*float(item_price[i])   
                # calculate amount for single product
                single_prod_total_amt = float(quantity[i]) * float(item_price[i])
                print('single_prod_total_amt: ' + str(single_prod_total_amt))

                # gather order item data and append it to a list
                order_item_data = {
                    "product_id": product_id[i],
                    "quantity": quantity[i],
                    "amount": single_prod_total_amt
                }
                print('order_item_data =' + str(order_item_data))
                items.append(order_item_data)
            #print("No " + product_name[i] + " requested.")
            i += int(1)

        print('total order amount: ' + str(total_order_amount))

        # gather order data
        order = Order(amount=total_order_amount)
        
        #more logic goes here
        # add new entries in the database for both order and order items
        try:
            order.full_clean()
            print("order is valid")
            # write order to the database
            order.save()
            print("order",order.id, "saved")
            # iterate over order items
            for item in items:
                item["order_number"] = order.id
                order_item = Order_Item(
                    order_number=order,
                    product_id=item["product_id"],
                    quantity=item["quantity"],
                    amount=item["amount"],
                )
                order_item.full_clean()
                order_item.save()
                # display sucessful order confirmation page
                order_data = {
                "id": order.id,
                "order_date_time": order.order_date_time,
                "amount": total_order_amount,
            }
            context = {"order_details": items, "order": order_data}
            #return render(request, "order_result.html", context)
        except ValidationError as e:
            # should never get here
            print("ERROR: object not valid", e)    
        #return a response
        return HttpResponse('/order_result page loaded. Check the runserver console for test result.')

    else:
        #should never get here
        return HttpResponse('process_order must receive a POST action.')

