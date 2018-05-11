from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.views import generic

from Warehouse.models import Order

import json
import requests


STORE_URL = "http://py.cpcoding.com/store/api/"


class IndexView(generic.ListView):
	model = Order
	template_name = 'Warehouse/index.html'
	ordering = ['-purchased_date']


	# filter_status = request.GET.get('status', 'I')
	# order_list = Order.objects.filter(status=filter_status).order_by('-purchased_date')

class DetailView(generic.DetailView):
	model = Order
	template_name = 'Warehouse/detail.html'



def update(request,id):
	order = Order.objects.get(id=id)
	new_status = request.GET.get('s', 'I' )

	if new_status not in [ 'S', 'C' ]:
		return redirect('warehouse:detail',pk=id)

	## Update the status
	order.status = new_status
	order.updated_date=timezone.now()
	order.save()

	result = makecall(order)

	## Check for errors, if so, flag error for human intervention
	if ( result[0] == 1 ):
		order.status = 'E'
		order.error_message = "Error contacting store: " + str(result[1])
		order.save()

	return redirect('warehouse:detail',pk=id)



def makecall(order):
	data = {
	   'id': order.store_order_id,
	   'status': order.status,
	}

	payload = json.dumps( data )
	r = requests.get(url = STORE_URL, data=payload)

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
		store_id = int( data['store_id'] )
		local_id = int( data['id'] )
		customer = data['customer']
		purchase_date = data['purchase_date']
		status = data['status']
	except:
		return api_error("Did not receive all Order information.")

	## Is this a new or existing order?

	try:
		existing = Order.objects.get(store_id=store_id, store_order_id=local_id )
	except:
		existing = False

	if ( existing ):
		if ( existing.status == 'I' ):
			if ( status == 'C' ):
				existing.status = 'C'
			else:
				existing.customer = customer
				existing.updated_date=timezone.now()
			existing.save()
		else:
			return api_error("Cannot modify order already shipped/canceled")
	else:
		if ( status != 'C' ):
			neworder = Order( store_id=store_id, store_order_id=local_id, customer=customer, purchased_date=purchase_date, updated_date=timezone.now(), status='I' )
			neworder.save()

	## Return Acknowledgment
	return HttpResponse( json.dumps( {'OK': local_id } ) )




def api_error(msg):
	return HttpResponse( json.dumps( {'error': msg } ) )
	
