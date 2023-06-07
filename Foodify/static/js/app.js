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