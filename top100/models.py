from django.db import models

# Create your models here.

class Relations(models.Model):
    type = models.IntegerField(verbose_name="1:客服,2:销售")
    name = models.CharField(max_length=50,verbose_name="姓名")
    phone = models.CharField(max_length=50,verbose_name="电话")
    is_main = models.IntegerField(verbose_name="0:非主要,1:主要")

    class Meta:
        db_table = 'relations'



class Customer(models.Model):
    cust_code = models.CharField(max_length=50)
    customer_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=500)
    belong_zone = models.CharField(max_length=50)
    relations = models.ManyToManyField(Relations)
    # ip_pool = models.CharField(max_length=50)
    # product = models.CharField(max_length=50)
    # contract_bandwidth = models.CharField(max_length=50)
    # graphid = models.IntegerField()
    # bandwidth_usageRate = models.FloatField()
    # interface_usageRate = models.FloatField(default='99.99')

    class Meta:
        db_table = 'customer'


class Interface(models.Model):
    wl_device_name = models.CharField(max_length=500)
    port_desc = models.CharField(max_length=100)
    bandwidth = models.CharField(max_length=500,null=True)
    pact_code = models.CharField(max_length=200,verbose_name="合同1编号",null=True)
    pact_line = models.CharField(max_length=200,verbose_name="合同行号",null=True)
    ip_range = models.CharField(max_length=200,verbose_name="ip段",null=True)
    start_ip = models.IntegerField(null=True)
    end_ip = models.IntegerField(null=True)
    port_code_key = models.CharField(max_length=100)
    contractnum = models.CharField(max_length=500,null=True)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)

    class Meta:
        db_table = 'interface'


class Attack(models.Model):
    ip = models.CharField(max_length=500,null=True)
    ipint = models.IntegerField(null=True)
    info = models.CharField(max_length=1000,null=True)
    time = models.DateTimeField()
    detail = models.CharField(max_length=1000,null=True)
    rule_name = models.CharField(max_length=500,null=True)
    deal = models.IntegerField(default=0,null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        db_table = 'attack'



