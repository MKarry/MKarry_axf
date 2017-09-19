from django.shortcuts import  render,redirect
import os
import time
import random
from django.contrib.auth import logout
from django.conf import settings
from .models import Wheel,Nav,mustbuy,Shop,FoodTypes,Goods,MainShow,User,Cart
import uuid
from django.http import JsonResponse
# 主页
def main(request):
    # 获取轮播数据
    loopList = Wheel.objects.all()
    # 导航数据
    navList = Nav.objects.all()
    # 每日必选
    buyList = mustbuy.objects.all()
    imgList = Shop.objects.all()
    quicksend = imgList[0]
    hotsell = imgList[1]
    newgoods = imgList[2]
    imgList1 = imgList[4:7]
    imgList2 = imgList[7:]

    # 商品列表
    mainList = MainShow.objects.all()

    context = {
        'loopWheelList': loopList,
        'navList': navList,
        'buyList': buyList,
        'quicksend':quicksend,
        'hotsell':hotsell,
        'newgoods':newgoods,
        'imgList1':imgList1,
        'imgList2':imgList2,
        'mainList':mainList,
    }
    return render(request,'axf/main.html',context)

# 闪送超市
def market(request):
    # pageid    cid    sortid   是从网页访问的url中获取的
    #左侧数据
    leftList = FoodTypes.objects.all()
    pageid = request.GET.get('id')
    cid = request.GET.get('cid')
    sortid = request.GET.get('sortid')
    print(pageid,cid,sortid)

    # goodsList = Goods.objects.all()
    if pageid != '104749':
        pageid = request.GET.get('id')
        print(pageid)

    #右侧数据
    if cid == '0':
        goodsList = Goods.objects.filter(categoryid=pageid)
    else:
        goodsList = Goods.objects.filter(categoryid=pageid, childcid=cid)

    # 排序goodsList  sortid:表示前台界面排序的几种方式：按价格、按销量、、
    if sortid == '0':
        goodsList = goodsList.order_by('productid')
    elif sortid == '1':
        goodsList = goodsList.order_by('productnum')
    elif sortid == '2':
        goodsList = goodsList.order_by('price').reverse()
    elif sortid == '3':
        goodsList = goodsList.order_by('price')

    # 子类名称
    fllist = []
    foodtype = FoodTypes.objects.get(typeid=pageid)
    allcname = foodtype.childtypenames
    # #全部分类:0#酸奶乳酸菌:103537#牛奶豆浆:103538#面包蛋糕:103540
    idnames = allcname.split("#")
    for str in idnames:
        arr = str.split(':')
        fllist.append({'code':arr[1],'title':arr[0]})
        cid = arr[1]
    # print(fllist,'-------------------')

    titleList = [{'title':'综合排序','index':'0'},{'title':'销量排序','index':'1'},
                 {'title':'价格最低','index':'2'},{'title':'价格最高','index':'3'}]

    return render(request,'axf/market.html',{'title':'闪送超市','leftList':leftList, 'goodsList':goodsList,
                                             'titleList':titleList,'id':pageid,'fllist':fllist,'cid':cid,'sortid':sortid})

# 购物车
def cart(request):
    token = request.session.get('token')
    # print("*******************************")
    # print("token:",token)
    if token == None:
        return render(request,'axf/login.html')
    user = User.objects.get(userToken=token)
    userid = user.userAccount
    cartlist = Cart.objects.filter(userid=userid)
    print("*******************************")
    print(cartlist)
    context = {
        'username':user.userName,
        'userphone':user.userPhone,
        'useraddress':user.userAddress,
        'cartlist':cartlist
    }

    return render(request,'axf/cart.html',context)

def changecart(request,flag):
    print(flag,"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    #判断是否登录
    token = request.session.get('token')
    # print("-----------------token:",token)
    # token==None   没有登录
    if token == None:
        return JsonResponse({'data':"0","status":'error'})

    #用户登录后
    # 通过token获取用户的信息userToken
    user = User.objects.get(userToken=token)
    #用户id
    userid = user.userAccount
    #商品id
    # 从前台ajax传来的参数中获取（ajax传参一般是post、get两种方式，此处是post传回的）
    productid = request.POST.get("productid")
    #善品信息
    product = Goods.objects.get(productid=productid)
    #从购物车里获取数据展示在界面上
    carts = Cart.objects.filter(userid=userid,productid=productid)
   #没有商品数据   就将获取的数据传入数据库
    if carts.count() == 0:
        onecart = Cart.createcart(userid,productid,1,product.price,product.productlongname,product.productimg,True,False)
        onecart.save()
        return JsonResponse({'data':onecart.productnum,"status":"success"})
    else:
        c = carts[0]
        if flag == '0':
            print('执行到此处2--------')
            #增加
            if product.storenums != 0:
                c.productnum = c.productnum + 1
                print(c.productnum)
                product.storenums -= 1
                newprice = float(product.price)*c.productnum
                newprice = "%.2f"%newprice
                c.save()
                product.save()

        elif flag == '1':
            #减少
            c.productnum = c.productnum - 1
            product.storenums += 1
            product.save()
            if c.productnum == 0:
                c.delete()
                return JsonResponse({"data":0,"status":"success"})
            else:
                newprice = float(product.price) * c.productnum
                newprice = "%.2f"%newprice
                c.save()
        elif flag == "2":
            c.ischose = not c.ischose
            c.save()
            if c.ischose:
                str = '√'
            else:
                str=''
            return JsonResponse({'data':str,'status':'success'})
        elif flag == "3":
            if c.ischose:
                str = "√"
            return JsonResponse({"data":0,"status":'success'})

        return JsonResponse({'data':c.productnum,'status':'success'})



# 我的
def mine(request):
    token = request.session.get('token')
    print(token, "--------------------------")
    if token == None:
        # username = request.session.get('userName','未登陆')
        # return render(request,'axf/mine.html',{"username":username})
        return redirect("/login/")

    un = User.objects.get(userToken=token)
    un = un.userName
    username = un
    # print(username,'~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    return render(request,'axf/mine.html',{"username":username})

# 注册界面
def register(request):
    if request.method == 'GET':
        return render(request,'axf/register.html')
    if request.method == 'POST':
        userAccount = request.POST.get('userAccount')
        userPass = request.POST.get('userPass')
        userPasswd = request.POST.get('userPasswd')
        userName = request.POST.get('userName')
        # print('#################userName:',userName)
        userPhone = request.POST.get('userPhone')
        userAdderss = request.POST.get('userAdderss')
        f = request.FILES.get('picture')
        # print('------------------f:',f)
        # http://img01.bqstatic.com/upload/goods/000/001/1538/0000011538_41480.jpg@200w_200h_90Q
        # fname = str(uuid.uuid4())+'.jpg'
        fname = str(userAccount)+'.jpg'
        dname = 'static\\media\\' + fname
        imgpath = os.path.join(settings.BASE_DIR,dname)

        print(imgpath)
        with open(imgpath,'wb') as img:
            # chunks:块   调用这个函数自动将img分成几块   循环遍历将图片写入到img路径中
            for data in f.chunks():
                img.write(data)
        print(img)
        # 密码、用户编号 不被每次访问时被中间截获 利用
        token = time.time() + random.randint(1,10000)
        token = '%f'%token

        user = User.createuser(userAccount,userPass,userName,userPhone,userAdderss,imgpath,0,token)
        user.save()
        # 保存一下昵称，token  为了用户下次登录时的验证
        request.session['userName'] = userName
        # print("-----------------------username:",userName)
        request.session['token'] = token

    return redirect('/login/')
    # return  render(request,'axf/login.html')


# 验证用户的id是否可用
def checkuserid(request):
    userid = request.POST.get('checkid')
    try:
        use = User.objects.get(userAccount=userid)
    except User.DoesNotExist as e:
         # 该用户是新人
        return JsonResponse({'data':0,'status':'success'})
    #该用户已存在
    return JsonResponse({'data':1,'status':'error'})
#退出登陆
def quit(request):
    logout(request)
    return redirect('/main/')
def login(request):
    return render(request,'axf/login.html',{"title":"登陆"})
def checkuserlogin(request):
    username = request.POST.get('ua',None)
    userpasswd = request.POST.get('up')

    try:
        user = User.objects.get(userAccount=username)
    except User.DoesNotExist as e:
        return JsonResponse({'data':0,"status":"error"})

    if userpasswd != user.userPasswd:
        return JsonResponse({"data":1,"status":"error"})

    request.session['username'] = user.userName
    request.session['token'] = user.userToken
    return JsonResponse({"data":0,"status":"success"})

