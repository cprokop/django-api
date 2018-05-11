from django.db import models
from datetime import datetime

# Create your models here.

class Order(models.Model):
	STATUS_LIST = ( 
	   ('P', 'Pending'),
	   ('A', 'Awaiting Shipment'),
	   ('S', 'Shipped'),
	   ('C', 'Canceled'),
	)
	id = models.AutoField(primary_key=True)
	customer = models.CharField(max_length=100)
	purchase_date = models.DateTimeField(default=datetime.now)
	status = models.CharField(max_length=1, choices=STATUS_LIST, default='P')

	def __str__(self):
		return '%d' % ( self.id )
