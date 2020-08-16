$("#modal_form_order_step2 button[type='submit']").on('click', function(event){
    event.preventDefault();
    var productType = $('#modal_form_order_step2 #product_type').find(":selected").val();
    var metadata = ""
    var tires = $('#modal_form_order_step2 input[name="tires"]').val();
    var price = $("#modal_form_order_step2 .price").text();
    var card_name = $("#modal_form_order_step2 input[name='cardname']").val()
    var card_number = $("#modal_form_order_step2 input[name='cardnumber']").val()
    var cvv = $("#modal_form_order_step2 input[name='cvv']").val()
    var expiry_date = $("#modal_form_order_step2 input[name='expiry_date']").val()
    $("#modal_form_order_step2 button[type='submit']").attr('disabled', 'disabled');
    $("#modal_form_order_step2 button[type='submit'] .loader").css('display', 'block');
    $.ajax({
        url: '/payout/',
        method: 'POST',
        data: {
            productType: productType,
            metadata:metadata,
            tires:tires,
            price:price,
            card_name:card_name,
            card_number:card_number,
            cvv:cvv,
            expiry_date:expiry_date,
            csrfmiddlewaretoken:$('#modal_form_order_step2 input[name=csrfmiddlewaretoken]').val(),
        },
        success:function(response){
            if(response.success){
              $("#modal_form_order_step2 button[type='submit']").removeAttr('disabled');
              $('#modal_form_order_step2').modal('hide');
              $('#modal_form_order_complete').modal('show');
              $("#modal_form_order_step2 button[type='submit'] .loader").css('display', 'none');
              var price = response.data.price / 100;
              $("#modal_form_order_complete .price").text('$' + price);
            }
            else{
              //set active pay button
              $("#modal_form_order_step2 button[type='submit']").removeAttr('disabled');
              $('#modal_form_order_step2 #msg-btn').html(response.message + '&times');
              $('#modal_form_order_step2 #alert-div').addClass('active');
              //hide progress view
              $("#modal_form_order_step2 button[type='submit'] .loader").css('display', 'none');
            }
            //reset all input field of order modal
            // $("#modal_form_order_step2 .modal-body input").val('');
            // $('#modal_form_order_step2 .currency-unit').removeClass('active');
            // $('#modal_form_order_step2 .price').text('');
            // $('#modal_form_order_step2 .totalPrice').text('');
        },
    });

});

$('#modal_form_order_step2 #msg-btn').on('click', function(event){
    $('#modal_form_order_step2 #alert-div').removeClass('active');
});