$(document).ready(function () {
   account = document.getElementById('account')
   pass = document.getElementById('pass')
   passwd = document.getElementById('passwd')

    accounterr = document.getElementById('accounterr')
    checkerr = document.getElementById('checkerr')
    passerr = document.getElementById('passerr')
    passwderr = document.getElementById('passwderr')


    account.addEventListener('focus',function () {
        accounterr.style.display = 'none'
        checkerr.style.display = 'none'
    },false)

    account.addEventListener('blur',function () {
        var inputStr = this.value
        if (inputStr.length != 8){
            accounterr.style.display = 'block'
        }else {
        //    验证账号是否被注册
            console.log("******************")
            $.ajax({
                url:"/checkuserid/",
                type:"post",
                typedata:"json",
                data:{"checkid":account.value},
                success:function (data){
                    console.log(data)
                    if ( data.status == "error"){
                        checkerr.style.display = 'block'
                    }
                }
            })
            // console.log(account.value)
        }
    },false)

    pass.addEventListener('focus',function () {
        passerr.style.display = 'none'

    },false)
    pass.addEventListener('blur',function () {
        var inputstr = this.value
        if (inputstr.length < 6 || inputstr.length >16){
            passerr.style.display = 'block'
        }
    },false)

})