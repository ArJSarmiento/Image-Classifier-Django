document.addEventListener('DOMContentLoaded', () => {
    fileInput = document.querySelector("#file");
    submit = document.querySelector("#submit");

    submit.disabled = true

    fileInput.addEventListener('change', () => { 
        if (fileInput.files.length == 0 )
        {
            submit.disabled = true
        }
        else{
            submit.disabled = false
        }
    });

    $(document).scroll(function() {
      navbarScroll();
    });
    
    function navbarScroll() {
      var y = window.scrollY;
      if (y > 10) {
        $('.header').addClass('small');
      } else if (y < 10) {
        $('.header').removeClass('small');
      }
    }    
}); 