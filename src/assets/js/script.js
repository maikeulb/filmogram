// for ui kit
$(document).ready(function() {
  $(".uk-navbar-nav a").on("click", function(){
     $(".uk-navbar-nav").find(".uk-active").removeClass("uk-active");
     $(this).parent('li').addClass("uk-active");
   });
});

// for img preview
$(document).ready(function () {
   function readURL(input) {
     if (input.files && input.files[0]) {
       var reader = new FileReader();
       reader.onload = function (e) {
         $('#target')
           .attr('src', e.target.result);
       };
       reader.readAsDataURL(input.files[0]);
     }
   }
  $(".imgInp").change(function(){
    readURL(this);
  });
});

// for list.js   
$(document).ready(function () {
  var options = {
    valueNames: [ 'name' ],
    page: 5,
    pagination: true
  };
  var userList = new List('users', options);
});

$(document).ready(function () {
  var options = {
    valueNames: [ 'name' ],
    page: 5,
    pagination: true
  };
  var userList = new List('followers', options);
});

$(document).ready(function () {
  var options = {
    valueNames: [ 'name' ],
    page: 5,
    pagination: true
  };
  var userList = new List('followings', options);
});


import '../css/styles.scss';
