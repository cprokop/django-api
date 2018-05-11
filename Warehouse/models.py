from django.db import models


class Order(models.Model):
	STATUS_LIST = (
	   ('I', 'Incoming'),
	   ('S', 'Shipped'),
	   ('C', 'Canceled'),
	   ('E', 'Error'),
	)
	id = models.AutoField(primary_key=True)
	store_id = models.IntegerField(default=0)
	store_order_id = models.IntegerField(default=0)
	customer = models.CharField(max_length=100)
	purchased_date = models.DateTimeField()
	updated_date = models.DateTimeField()
	status = models.CharField(max_length=1, choices=STATUS_LIST)
	error_message = models.CharField(max_length=100,default='')

	def __str__(self):
		return '%d' % ( self.id )
