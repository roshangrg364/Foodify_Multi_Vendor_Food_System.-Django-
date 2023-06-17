
$(document).on("click","#btn-cash-on-delivery",function(e){
e.preventDefault()
savePayment("CashOnDelivery","")
})



function savePayment(paymentMethod,transaction_id){
    const order_no = $('#order-number').val()
    const csrf_token = getCookie('csrftoken');
    const data ={
        "order_number":order_no,
        "csrfmiddlewaretoken":csrf_token,
        "payment_method":paymentMethod,
        "transaction_id":transaction_id  
    }
 $.ajax({
    type:"post",
    url:"/orders/order-payment/",
    data:data,
    success:function(response){
        console.log(response)
        shownotification("success",response.message)
        setTimeout(function(){
            window.location.href =`/orders/order-confirmation?order_id=${response.order_id}&transaction_id=${response.transaction_id}`
        },1000)
    },
    error:function(error){
        shownotification("error","something went wrong")
    }


 })
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
