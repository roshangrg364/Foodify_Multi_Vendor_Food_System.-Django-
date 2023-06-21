function shownotification(status,title,message)
{
    Swal.fire({
        title: title,
        text: message,
        icon: status,
       showConfirmButton: false,
        timer: 1500
      });
}

$(document).on("click",".delete-opening-hour",function(e){
  e.preventDefault()
  Swal.fire({
    title: 'Do you want to remove this schedule?',
    showCancelButton: true,
    confirmButtonText: 'Yes',
  }).then((result) => {
    if (result.isConfirmed) {
      const elm = $(this)
  id = elm.attr("data-id")
  $.ajax({
    type:"get",
    url:"/accounts/vendor/openinghours/delete/"+id,
    success:function(response){
      if(response.status =="success"){
        shownotification("success","success",response.message)
        elm.closest("tr").remove()
      }
      else
      {
        shownotification("info","info",response.message)
      }
    },
    error:function(error){
      shownotification("error","error","something went wrong. please contact to administrator")
    }
  })
    } 
  })
  
})

$("#openinghours-form").on("submit",function(e){
  e.preventDefault();
  const day = $("#id_day").val()
  const fromHour = $("#id_from_hour").val()
  const toHour= $("#id_to_hour").val()
  const is_closed = $("#id_is_closed").is(":checked")
  const csrf_token = $('input[name=csrfmiddlewaretoken]').val()
  if(!day || !fromHour || !toHour)
  {
    if(is_closed ==false)
    {
    shownotification("error","Validation error","Day, From Hour, To Hour field are required")
    return false
    }
  }
  const data ={
    "day":day,
    "from_hour":fromHour,
    "to_hour":toHour,
    "is_closed":is_closed,
    "csrfmiddlewaretoken":csrf_token
  }

  $.ajax({
      type: "POST",
      url: "/accounts/vendor/openinghours/add/",
      data:data,
      success: function(response){
        console.log(response)
       if(response.status =="success")
       {
          const html = ` <tr>
          <td><b> ${response.day}</b></td>
         <td>
          ${response.is_closed =="false"?  response.from_hour +" - "+response.to_hour:"Closed"}
         </td>
         <td>
          <a href='#' data-id = "${response.id}" class="delete-opening-hour"> Remove</a>
         </td>
       </tr>`
      $("#opening_hour-list").append(html)
      shownotification("success","Added Successfully",response.message)
       }
       else
       {
        shownotification("info","Info",response.message)
       }
      },
      error:function(errResponse){
         shownotification("error","error","something went wrong. please contact to administrator")
      }
    });
})


function blockwindow()
{
  document.querySelector(".loading").classList.remove("hidden")
}

function unblockwindow()
{
  document.querySelector(".loading").classList.add("hidden")
}