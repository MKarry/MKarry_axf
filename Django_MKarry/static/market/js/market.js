$(document).ready(function () {
    var alltypebtn = document.getElementById('alltypebtn')
    var showsortbtn = document.getElementById('showsortbtn')

    var typediv = document.getElementById('typediv')
    var sortdiv = document.getElementById('sortdiv')

    typediv.style.display = 'none'
    sortdiv.style.display = 'none'

    alltypebtn.addEventListener('click', function () {
        typediv.style.display = 'block'
        sortdiv.style.display = 'none'

    }, false)
    showsortbtn.addEventListener('click', function () {
        typediv.style.display = 'none'
        sortdiv.style.display = 'block'

    }, false)

    typediv.addEventListener('click', function () {
        this.style.display = 'none'
    }, false)

    sortdiv.addEventListener('click', function () {
        this.style.display = 'none'
    }, false)






//    添加购物车
    var addShoppings = document.getElementsByClassName('addShopping')
    var subShoppings = document.getElementsByClassName('subShopping')


    for (var i = 0; i < subShoppings.length; i++) {
        addShoppings[i].addEventListener('click', function () {
            gid = this.getAttribute('ga')
            // console.log(gid)
            $.post("/changecart/0/", {'productid': this.getAttribute('ga')}, function (data) {
                if (data.status == 'success') {
                        document.getElementById(gid).innerHTML = data.data
                        console.log("数量：", data.data)
                } else {
                    if (data.data == '0') {
                            //说明没有登录
                            window.location.href = "http://127.0.0.1:8000/login/"
                    }
                }
            })

        }, false)

        subShoppings[i].addEventListener('click', function () {
            gid = this.getAttribute('ga')
            // console.log(subShoppings.length)
            $.post("/changecart/1/", {'productid': this.getAttribute('ga')}, function (data) {
                if (data.status == 'success') {
                    document.getElementById(gid).innerHTML = data.data
                    console.log("数量：", data.data)
                } else {
                    if (data.data == '0') {
                        //说明没有登录
                        window.location.href = "http://127.0.0.1:8000/login/"
                    }
                }
            })
        }, false)


    }
})