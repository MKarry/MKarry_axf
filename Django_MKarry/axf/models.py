from django.db import models

# Create your models here.
class Wheel(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    trackid = models.CharField(max_length=10)

class Nav(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    trackid = models.CharField(max_length=10)

class mustbuy (models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    trackid = models.CharField(max_length=10)

class Shop(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    pd = models.CharField(max_length=100)


class FoodTypes(models.Model):
    typeid = models.CharField(max_length=10)
    typename = models.CharField(max_length=20)
    childtypenames = models.CharField(max_length=150)
    typesort = models.IntegerField()


class Goods(models.Model):
    # 商品id
    productid = models.CharField(max_length=10)
    productimg = models.CharField(max_length=150)
    productname = models.CharField(max_length=50)
    productlongname = models.CharField(max_length=100)
    isxf = models.NullBooleanField(default=False)
    pmdesc = models.CharField(max_length=10)
    specifics = models.CharField(max_length=20)
    price = models.CharField(max_length=10)
    marketprice = models.CharField(max_length=10)
    categoryid = models.CharField(max_length=10)
    childcid = models.CharField(max_length=10)
    childcidname = models.CharField(max_length=10)
    dealerid = models.CharField(max_length=10)
    # 库存
    storenums = models.IntegerField()
    # 销量
    productnum = models.IntegerField()

class MainShow(models.Model):
    trackid = models.CharField(max_length=10)
    name = models.CharField(max_length=20)
    img = models.CharField(max_length=100)
    categoryid = models.CharField(max_length=10)
    brandname = models.CharField(max_length=20)

    img1 = models.CharField(max_length=100)
    childcid1 = models.CharField(max_length=10)
    productid1 = models.CharField(max_length=10)
    longname1 = models.CharField(max_length=50)
    price1 = models.CharField(max_length=10)
    marketprice1 = models.CharField(max_length=10)

    img2 = models.CharField(max_length=100)
    childcid2 = models.CharField(max_length=10)
    productid2 = models.CharField(max_length=10)
    longname2 = models.CharField(max_length=50)
    price2 = models.CharField(max_length=10)
    marketprice2 = models.CharField(max_length=10)

    img3 = models.CharField(max_length=100)
    childcid3 = models.CharField(max_length=10)
    productid3 = models.CharField(max_length=10)
    longname3 = models.CharField(max_length=50)
    price3 = models.CharField(max_length=10)
    marketprice3 = models.CharField(max_length=10)

class User(models.Model):
    userAccount = models.CharField(max_length=20,unique=True)
    userPasswd = models.CharField(max_length=20)
    userName = models.CharField(max_length=20)
    userPhone = models.CharField(max_length=20)
    userAddress = models.CharField(max_length=100)
    userImg = models.CharField(max_length=150)
    userRank = models.IntegerField()

    # token 值验证，每次登陆都会更新
    userToken = models.CharField(max_length=50)
    @classmethod
    def createuser(cls,account,passwd,name,phone,address,img,rank,token):
        user = cls(userAccount=account,userPasswd=passwd,userName=name,userPhone=phone,userAddress=address,userImg=img,userRank=rank,userToken=token)
        return user


class Cart(models.Model):
    userid = models.CharField(max_length=10)
    productid = models.CharField(max_length=10)
    productnum = models.IntegerField()
    productprice = models.FloatField()
    productlongname = models.CharField(max_length=100)
    productimg = models.CharField(max_length=150)
    ischose = models.BooleanField()
    isdelete = models.BooleanField()

    @classmethod
    def createcart(cls,userid,productid,productnum,productprice,productlongname,productimg,ischose,isdelete,):
        cart = cls(userid=userid, productid=productid, productnum=productnum, productprice=productprice, productlongname=productlongname,
                   productimg=productimg, ischose=ischose, isdelete=isdelete)
        return cart









