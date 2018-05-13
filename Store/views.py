from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.views import generic
from django.contrib import messages

from .models import Order

import json
import requests


WAREHOUSE_URL = "http://HOST/warehouse/api/"
STORE_ID = 1

"""
Main Index View for listing Orders
"""
class IndexView(generic.ListView):
	model = Order
	template_name = 'Store/index.html'
	ordering = ['-purchase_date']

"""
Display Order Details
"""
class DetailView(generic.DetailView):
	model = Order
	template_name = 'Store/detail.html'

"""
Cancel an Order
"""
def cancel(request,id):
	try:
		order = Order.objects.get(id=id)
	except:
		messages.info( request, "Could No longer find Order" )
		return redirect('store:index')

	order.status = 'C'

	## Check with Warehouse we're allowed to make this change
	result = makecall(order)

	## Check for any errors
	if ( result[0] == 1 ):
		messages.info( request, "There was an error cancelling this order: " + result[1] )
	else:
		messages.info( request, "Order Cancelled" )
		order.save()

	return redirect('store:detail', pk=id )


"""
Update an order and attempt to send to the Warehouse
"""
def update(request,id):
	try:
		order = Order.objects.get(id=id)
	except:
		messages.info( request, "Could No longer find Order" )
		return redirect('store:index')

	customer = request.POST['new_customer']

	## Confirm all Order Details received
	if not customer:
		messages.error( request, "You must supply a customer name for any order." )
		return redirect('store:detail', pk=id)


	## Assign for now, but don't save
	order.customer = customer

	## Check with Warehouse we're allowed to make this change
	result = makecall(order)

	## Check for any errors
	if ( result[0] == 1 ):
		messages.info( request, "There was an error submitting the order to the warehouse: " + result[1] )
	else:
		messages.info( request, "Order Updated" )
		order.status = 'A'
		order.save()

	return redirect('store:detail', pk=id )


"""
Create a New Order
"""
def create(request):
	customer = request.POST['customer']

	## Confirm all Order Details received
	if not customer:
		messages.error( request, "You must supply a customer name." )
		return redirect('store:index')

	## Save new order to local DB
	neworder = Order( customer=customer, purchase_date=timezone.now(),status='P')
	neworder.save()

	auto_fail = request.POST.get('fail', False)
	if ( auto_fail ):
		messages.info( request, "The API call mysteriously failed! Please review order." );
		return redirect('store:index')


	## Contact Warehouse with New Order
	result = makecall(neworder)

	## Check for any errors
	if ( result[0] == 1 ):
		messages.info( request, "There was an error submitting the order to the warehouse: " + result[1] )
	else:
		## Update the Order Status and return to User
		neworder.status = 'A'
		neworder.save()
		messages.info( request, "Created!!" )

	return redirect('store:index')



"""
Call the Warehouse API
"""
def makecall(order):
	data = {
	   'store_id': STORE_ID,
	   'customer': order.customer,
	   'id': order.id,
	   'status': order.status,
	   'purchase_date': order.purchase_date.isoformat(),
	}

	payload = json.dumps( data )
	r = requests.get(url = WAREHOUSE_URL, data=payload)

	# return r.text
	try:
		data = r.json()
	except:
		return 1, 'General Error'

	if 'OK' in data:
		return [ 0 ]
	elif 'error' in data:
		return 1, data['error']
	else:
		return 1, 'General Error'



"""
Receive Incoming Messages from the Warehouse
"""
def api(request):

	try:
		body = str( request.body, 'utf-8' )
	except:
		return api_error("Invalid HTTP message")

	try:
		data = json.loads(body)
	except:
		return api_error("Could not parse JSON:" + body )

	try:
		thisid = int( data['id'] )
		status = data['status']
	except:
		return api_error("Did not receive all Order information.")

	try:
		order = Order.objects.get(id=thisid)
	except:
		return api_error("Could not locate Order:" + str(thisid))

	order.status = status
	order.save()

	## Return Acknowledgment
	return HttpResponse( json.dumps( {'OK': thisid } ) )


"""
Generate and Format a JSON Error used with the API
"""
def api_error(msg):
	return HttpResponse( json.dumps( {'error': msg } ) )



