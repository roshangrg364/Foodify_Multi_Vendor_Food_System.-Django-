$(document).ready(function(){
    $(".increase_qty").on("click",function(e){
        e.preventDefault();
        const elm = $(this)
        const id = elm.attr("data-id")
        $.ajax({
            type: "get",
            url: "/marketplace/add_to_cart/"+id,
            success: function(response){
              if(response.status =="unauthenticated")
              {
                Swal.fire({
                  title: 'UnAuthenticated!',
                  text: "Please Login To Continue",
                  icon: 'warning',
                  showCancelButton: true,
                  confirmButtonColor: '#3085d6',
                  cancelButtonColor: '#d33',
                  confirmButtonText: 'Continue'
                }).then((result) => {
                  if (result.isConfirmed) {
                    window.location ="/accounts/login/"
                  }
                })
              }
             if(response.status =="success")
             {
              $(`#item-quantity-${id}`).html(response.quantity)
              $("#cart-counter").html(response.cart_counter.cart_count)
              populateCartAmount(response.cart_amount.subtotal,response.cart_amount.tax,response.cart_amount.total)
             }
            },
            error:function(errResponse){
              shownotification("error","error","something went wrong. please contact to administrator")
            }
          });
    })


    $(".decrease_qty").on("click",function(e){
      e.preventDefault();
      const elm = $(this)
      const id = elm.attr("data-id")
      $.ajax({
          type: "get",
          url: "/marketplace/remove_from_cart/"+id,
          success: function(response){

            if(response.status =="unauthenticated")
            {
              Swal.fire({
                title: 'UnAuthenticated!',
                text: "Please Login To Continue",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Continue'
              }).then((result) => {
                if (result.isConfirmed) {
                  window.location ="/accounts/login/"
                }
              })
            }
           if(response.status =="success")
           {
            $(`#item-quantity-${id}`).html(response.quantity)
            $("#cart-counter").html(response.cart_counter.cart_count)
            populateCartAmount(response.cart_amount.subtotal,response.cart_amount.tax,response.cart_amount.total)
            if(response.quantity <=0)
            {
              shownotification("error","no item left to remove","Item Empty")
              elm.closest(".cart-item-single").remove()
              checkcartcounter(response.cart_counter.cart_count)
            }
            
           }
          },
          error:function(errResponse){
             shownotification("error","error","something went wrong. please contact to administrator")
          }
        });
  })


  
  $(".delete_cart_item").on("click",function(e){
    e.preventDefault();
    const elm = $(this)
    const id = elm.attr("data-id")
    $.ajax({
        type: "get",
        url: "/marketplace/delete_cart_item/"+id,
        success: function(response){

          if(response.status =="unauthenticated")
          {
            Swal.fire({
              title: 'UnAuthenticated!',
              text: "Please Login To Continue",
              icon: 'warning',
              showCancelButton: true,
              confirmButtonColor: '#3085d6',
              cancelButtonColor: '#d33',
              confirmButtonText: 'Continue'
            }).then((result) => {
              if (result.isConfirmed) {
                window.location ="/accounts/login/"
              }
            })
          }
         if(response.status =="success")
         {
          $("#cart-counter").html(response.cart_counter.cart_count)
          elm.closest(".cart-item-single").remove()
          checkcartcounter(response.cart_counter.cart_count)
          populateCartAmount(response.cart_amount.subtotal,response.cart_amount.tax,response.cart_amount.total)
          shownotification("success","Success","Deleted Succesfully")
         }
        },
        error:function(errResponse){
           shownotification("error","error","something went wrong. please contact to administrator")
        }
      });
})

    //populate qty on load
    $(".item-qty").each(function(){
      const id = $(this).attr("id")
      const qty = $(this).attr("data-qty")
      $(`#${id}`).html(qty)
    })

    function checkcartcounter(cart_counter){

      if(cart_counter<=0){
        $("#cart-list-main").append(`<div class="text-center p-5">
        <h3> Cart is empty</h3>
    </div> `)
      }
    }

    function populateCartAmount(subtotal,tax,total){
      $("#sub-total").html(subtotal)
      $("#cart-tax").html(tax)
      $("#cart-total").html(total)
    }
})