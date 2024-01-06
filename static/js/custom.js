let autocomplete;

function initAutoComplete() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('id_address'),
        {
            types: ['geocode', 'establishment'],
            //default in this app is "IN" - add your country code
            // componentRestrictions: {'country': ['in']},
        })
    // function to specify what should happen when the prediction is clicked
    autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged() {
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry) {
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else {
        // console.log('place name=>', place.name)
    }

    // get the address components and assign them to the fields
    // console.log(place);
    var geocoder = new google.maps.Geocoder()
    var address = document.getElementById('id_address').value

    geocoder.geocode({ 'address': address }, function (results, status) {
        // console.log('results=>', results)
        // console.log('status=>', status)
        if (status == google.maps.GeocoderStatus.OK) {
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();

            // console.log('lat=>', latitude);
            // console.log('long=>', longitude);
            $('#id_latitude').val(latitude);
            $('#id_longitude').val(longitude);

            $('#id_address').val(address);
        }
    });

    // loop through the address components and assign other address data
    console.log(place.address_components);
    for (var i = 0; i < place.address_components.length; i++) {
        for (var j = 0; j < place.address_components[i].types.length; j++) {
            // get country
            if (place.address_components[i].types[j] == 'country') {
                $('#id_country').val(place.address_components[i].long_name);
            }
            // get state
            if (place.address_components[i].types[j] == 'administrative_area_level_1') {
                $('#id_state').val(place.address_components[i].long_name);
            }
            // get city
            if (place.address_components[i].types[j] == 'locality') {
                $('#id_city').val(place.address_components[i].long_name);
            }
            // get pincode
            // if(place.address_components[i].types[j] == 'postal_code'){
            //     $('#id_pin_code').val(place.address_components[i].long_name);
            // }else{
            //     $('#id_pin_code').val("");
            // }
        }
    }

}



// $(document).ready(function(){
//     $('.increase').on('click', function(e){
//         e.preventDefault();
//         var qtyLabel = parseInt($('.qty').text())
//         if (qtyLabel < 30){
//         var newQtyLabel = qtyLabel + 1
//         $('.qty').text(newQtyLabel)
//     }
//     });

//     $('.decrease').on('click', function(e){
//         e.preventDefault()
//         let qtyLabel = parseInt($('.qty').text())
//         if (qtyLabel > 0){
//             let newQtyLabel = qtyLabel - 1
//             $('.qty').text(newQtyLabel)
//         }
//     });
// })
$(document).ready(function () {
    $('.decrease-qty').on('click', function (e) {
        e.preventDefault();
        var productId = $(this).data('product-id');

        var qtyLabel = $('.qty[data-product-id="' + productId + '"]');
        var currentVal = parseInt(qtyLabel.text());
        if (currentVal > 0) {
            qtyLabel.text(currentVal - 1);
        }
    });

    $('.increase-qty').on('click', function (e) {
        e.preventDefault();
        var productId = $(this).data('product-id');

        var qtyLabel = $('.qty[data-product-id="' + productId + '"]');
        var currentVal = parseInt(qtyLabel.text());
        if (currentVal < 30) {
            qtyLabel.text(currentVal + 1);
        }
    });
});



$(document).ready(function() {

    // Add To Cart

    $('.add-to-cart').on('click', function(event) {
        event.preventDefault();

        var foodId = $(this).data('food-id');
        var url = $(this).attr('data-url');

        // var csrfToken = $(this).data('csrf');
        var csrftoken = $('[name=csrfmiddlewaretoken]').val();
        

        // var quantity = parseInt($('.qty[data-product-id="' + foodId + '"]').text());
        let quantity = parseInt($('#qty-'+foodId).text())
        
        
        
        $.ajax({
            type: 'GET',
            url: url ,  // آدرس ویوی جنگویی که محصول را به سبد خرید اضافه می‌کند
            data: {
                // 'csrfmiddlewaretoken': csrftoken,
                'food_id': foodId,
                'quantity': quantity,
                // 'flag': flag
            },
            success: function(response) {
                // در اینجا می‌توانید بر اساس پاسخ دریافتی از سرور عملیاتی انجام دهید
                if (response.success) {
                    
                    $('#counter-item').html(response.cart_counter)
                    $('#qty-'+foodId).html(response.qty)
                    $('#total').html(response.cart_amount)
                    
                    setTotalItemPrice( foodId,response.food_price)

                    setTotalPrice(response.cart_amount)

                    // alert(response.message);
                } else {
                    alert('Failed to add product to cart');
                }
            },
            error: function(xhr, errmsg, err) {
                // در صورت بروز خطا
                alert('Error: ' + errmsg);
            }
        });
    
    });
    
    // Set Quantity for food
    $('.item_qty').each(function(){
        let theId = $(this).attr('id')
        let qtyFood = $(this).attr('data-qty')
        $('#'+theId).text(qtyFood)
    })

   
    // Decrease Item From Cart
    $('.decrease-qty').on('click', function(e){
        e.preventDefault();

        let foodId = $(this).data('food-id')
        let url = $(this).data('url')
        
        
        $.ajax({
            type: 'GET',
            url: url,
            data:{
                'food_id': foodId,

            },
            success: function(response){
                if(response.success){
                    $('#counter-item').html(response.cart_counter)
                    $('#qty-'+foodId).html(response.qty)
                    setTotalItemPrice( foodId,response.food_price)
                    setTotalPrice(response.cart_amount)

                        
                    
                    if(window.location.pathname == ''){
                        removeCartItem(response.qty, cart_id);
                        checkEmptyCart();
                    }
                }else{
                    swal('Failed', 'Food quantity must be greater than 0', "error")

                    // alert(response.message);
                }
            },
            
            error: function(xhr, errmsg, err){
                // alert('Error: ' + 'Food quantity must be greater than 0');
                // swal('Failed', 'Food quantity must be greater than 0', "error")
                }
        })
    })




    // Delete food from food
    $('.delete_cart').on('click', function(e){
        e.preventDefault();
        let itemId = $(this).data('id')
        let deleteUrl = $(this).data('url')
        let csrfToken = $(this).data('csrf')
        // alert(`${itemId} ${deleteUrl} ${csrfToken}`)
        console.log(`#cart-item-${itemId}`)
        $.ajax({
            type: 'POST',
            url : deleteUrl,
            data : {
                'item_id': itemId,
                'csrfmiddlewaretoken': csrfToken,
            },
            success: function(response){
                if (response.success){
                    swal(response.status, response.message, "success")
                    $('#counter-item').html(response.cart_counter)
                    setTotalPrice(response.cart_amount)
                    removeItem(0, itemId)
                    checkEmptyCart()
                } else{
                    alert('Something Wrong. Try later')
                }

            },
            error: function(xhr, errmsg, err){
                alert('Error: ' + errmsg)
            }
            
        })
    });
    

    function setTotalItemPrice(fid,itemTotal){
    
        document.getElementById('item-total-price-'+fid).innerText=itemTotal
    };

    function setTotalPrice(grandTotal){
        $('#total').html(grandTotal)
    };


    function removeItem(quantity,itemId){
        if(quantity <=0){
            document.getElementById('cart-item-'+itemId).remove()
        }
    };

    function checkEmptyCart(){
        let counterItem = document.getElementById('counter-item').innerHTML
        console.log(counterItem)
        if (counterItem == 0){
            document.getElementById('empty-cart').style.display = 'block';
        } 
    }

});





