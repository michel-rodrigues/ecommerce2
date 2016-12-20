function showFlashMessage(message){
 
  var firstHalfTemplate = `
    <div class='container container-alert-flash'>
      <div class='row'>
        <div class='col-md-3 col-md-offset-8'>
          <div class='alert alert-success alert-dismissible' role='aler'>
            <button type='button' class='close' data-dismiss='alert' aria-label='Close'>
              <span aria-hidden='true'>&times;</span>
            </button>`;
        
  var lastHalfTemplate = `
          </div>
        </div>
      </div>
    </div>`;

  var template = firstHalfTemplate + message + lastHalfTemplate;

  $('body').append(template);
  $('.container-alert-flash').fadeIn();
  setTimeout(function(){
    $(".container-alert-flash").fadeOut();
  },3000);
};
