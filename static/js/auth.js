

$('#login-form #msg-btn').on('click', function(event){
    $('#login-form #alert-div').removeClass('active');
});

$('#signup-form #msg-btn').on('click', function(event){
    $('#signup-form #alert-div').removeClass('active');
});

//this method validates login
function validate_login(e)
{
    e.preventDefault();
    if($('#email').val()===''){
        // e.preventDefault();
        $('#login-form #msg-btn').html('<i class="fa fa-warning (alias)"></i> Email is required! &times');
        $('#login-form #alert-div').addClass('active');
        return;       
    } 

    if($('#password').val()===''){
        // e.preventDefault();
        $('#login-form #msg-btn').html('<i class="fa fa-warning (alias)"></i> Password is required! &times');
        $('#login-form #alert-div').addClass('active');
        return;       
    }

    if($('#email').val()==='' || $('#password').val()===''){
        // e.preventDefault();
        $('#login-form #msg-btn').html('<i class="fa fa-warning (alias)"></i> Please all field are required&times');
        $('#login-form #alert-div').addClass('active');
        return;    
    }
}

//this method validates login
function validate_register(e)
{
    if($('#name').val()===''){
        e.preventDefault();
        $('#signup-form #msg-btn').html('<i class="fa fa-warning (alias)"></i>Name is required! &times');
        $('#signup-form #alert-div').addClass('active');
        return;       
    }

    if($('#email').val()===''){
        e.preventDefault();
        $('#signup-form #msg-btn').html('<i class="fa fa-warning (alias)"></i> Email is required! &times');
        $('#signup-form #alert-div').addClass('active');
        return;       
    } 

    if($('#password').val()===''){
        e.preventDefault();
        $('#signup-form #msg-btn').html('<i class="fa fa-warning (alias)"></i> Password is required! &times');
        $('#signup-form #alert-div').addClass('active');
        return;       
    }

    if($('#cfm_password').val()===''){
        e.preventDefault();
        $('#signup-form #msg-btn').html('<i class="fa fa-warning (alias)"></i> Confirm Password is required! &times');
        $('#signup-form #alert-div').addClass('active');
        return;       
    }

    if($('#cfm_password').val()!=='' && $('#password').val() !==''){
        if($('#cfm_password').val() !== $('#password').val()){
            e.preventDefault();
            $('#signup-form #msg-btn').html('<i class="fa fa-warning (alias)"></i> Confirm Password is incorrect!&times');
            $('#signup-form #alert-div').addClass('active');
            return;
        }
    }
}



$('#msg-btn').on('click', function(event){
    $('#alert-div').removeClass('active');
});

$("#login-form button[type='submit']").on('click', function(event){
    event.preventDefault();
    validate_login(event);
    var email = $("#login-form input[name='email']").val();
    var password = $("#login-form input[name='password']").val();
    $.ajax({
        
        url: '/ajax_login/',
        method: 'POST',
        data: {
            email: email/*'admin'*/,
            password: password/*'!@#$qwer'*/,
            csrfmiddlewaretoken:$('#login-form input[name=csrfmiddlewaretoken]').val(),
        },
        success:function(response){
            if(response.success == true){
                if(response.order == true){
                    window.location.href = "/ownguestmapp/"
                }
                else{
                    window.location.href = "/planprices/"
                }
            }
            else{
                $('#msg-btn').html(response.message + '&times');
                $('#alert-div').addClass('active');
                
            }
        },
        
    });
});


$("#modal_form_signup button[type='submit']").on('click', function(event){
    event.preventDefault();
    $.ajax({
        url: '/ajax_register/',
        method: 'POST',
        data: {
            username: 'conda9',
            email: 'conda959@outlook.com',
            password: '!@#$qwer',
            csrfmiddlewaretoken:$('#modal_form_signup input[name=csrfmiddlewaretoken]').val(),
        },

        success:function(response){
            if(response.success == true){
                window.location.href = "/planprices/";
            }
        }
    });
});
