from django.conf.urls import url
from . import views
from Django_MKarry import settings
from django.views.static import serve

urlpatterns = [
    # 首页
    url(r'^main/$',views.main,name='main'),
    # 闪送超市
    url(r'^market/$',views.market,name='market'),
    # 我的
    url(r'^mine/$',views.mine,name='mine'),
    url(r'^register/$',views.register,name='register'),
    url(r'^checkuserid/$',views.checkuserid,name='checkuserid'),
    url(r'^login/$',views.login,name='login'),
    url(r'^checkuserlogin/$',views.checkuserlogin,name="checkuserlogin"),
    #退出登陆
    url(r'^quit/$',views.quit,name='quit'),
    # 图片上传的路径
    url(r'^static/(.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    #购物车
    url(r'^cart/$',views.cart,name='cart'),
    url(r'^changecart/(\d+)/$',views.changecart)


]