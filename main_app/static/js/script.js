$(document).ready(function(){
    $('.sidenav').sidenav();

    $('.carousel').carousel();

    setInterval(function(){
      $('.carousel').carousel('next');
    }, 4000)
  
    let showBtn = $('#showUpdate');
    let updateBtn = $('#update');
    let statusDropdown = updateBtn.siblings()[1];

    /* When Task Detail page loads show only UPDATE button */
    showBtn[0].style.display="inline-block"
    statusDropdown.style.display = "none";
    updateBtn[0].style.display = "none";

    /* When UPDATE STATUS button is selected, hide UPDATE STATUS button & show 
       Status dropdown and UPDATE button. 
       Once user clicks UPDATE page will refresh and dropdown and UPDATE button
       will once again be hidden */
    showBtn.click(function() {
      statusDropdown.style.display = "block";
      updateBtn[0].style.display = "inline-block";
      showBtn[0].style.display="none";
    })

  });


