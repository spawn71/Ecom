

const monthName = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul','Aug', 'Sep','Oct', 'Nov', 'Dec'];

$('#commentForm').submit(function(e){
    e.preventDefault();

    let dt = new Date();
    let time = dt.getDay() + " " + monthName[dt.getUTCMonth] + ", " + dt.getFullYear();

    $.ajax({
        data: $(this).serialize(),

        method: $(this).attr("method"),

        url: $(this).attr("action"),

        dataType: "json",

        success: function(response){
            console.log("comment posted");

            if(response.bool == true){
                $('#reviews-resp').html("Reviews Added Successfully");
                $(".hide-comment-form").hide();
                $(".add-review").hide();

                let _html = '<div class="single-comment justify-content-between d-flex mb-30">'
                _html +='<div class="user justify-content-between d-flex">'
                _html +='<div class="thumb text-center">'
                _html +='<img src="https://www.pngarts.com/files/10/Default-Profile-Picture-PNG-Download-Image.png" alt="">'
                _html +='<a href="#" class="font-heading text-brand">'+ response.context.user +'</a>'
                _html +='</div>'

                _html +='<div class="desc">'
                _html +='<div class="d-flex justify-content-between mb-10">'
                _html +='<div class="d-flex align-items-center">'
                _html +='<span class="font-xs text-muted">'+ time +'</span>'
                _html +='</div>'

                for(let i=1; i <= response.context.rating; i++) {
                    _html +='<i class="fas fa-star text-warning"></i>'
                }
                _html +='</div>'
                _html +='<p class="mb-10">'+ response.context.review +'</p>'

                _html +='</div>'
                _html +='</div>'
                _html +='</div>'

                $('.comment-list').prepend(_html);

            }
        }
    });
});


$(document).ready(function() {
    $('.filter-checkbox, #filter-by-price').on("click", function(){

        let filter_object = {}

        let min_price = $('#max_price').attr('min')
        let max_price = $('#max_price').val()

        filter_object.min_price = min_price;
        filter_object.max_price = max_price;

        $('.filter-checkbox').each(function(){
            let filter_value = $(this).val()
            let filter_key = $(this).data('filter')

            // console.log('filter Value: ' + filter_value);
            // console.log('filter Key: ' + filter_key);

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter='+ filter_key+']:checked')).map(function(element) {
                return element.value

            })
        })
        console.log("filter object is", filter_object);
        $.ajax({
            url: '/filter-products',
            data: filter_object,
            dataType: 'json',
            beforeSend: function(){
                console.log('sending data...');
            },
            success: function(response){
                console.log(response);
                console.log("data fired successfully");
                $("#filtered-products").html(response.data);
            }
        })
    })


    $("#max_price").on("blur",function(){
        let min_price = $(this).attr("min")
        let max_price = $(this).attr("max")
        let current_price = $(this).val()

        console.log("current", current_price);
        console.log("min Price", min_price);
        console.log("Max Price", max_price);
        if(current_price < parseInt(min_price) || current_price > parseInt(max_price)){

            min_price = Math.round(min_price* 100) /100
            max_price = Math.round(max_price* 100) /100

            alert("Price must be between" +min_price + " and" +max_price )
            $(this).val(min_price)
            $('#range').val(min_price)
            $(this).focus()

            return false

        }

    })
    // Add to cart
    $('.add-to-cart-btn').on('click', function(){

        let this_val = $(this)
        let index = this_val.attr("data-index")

        let quantity = $('.product-quantity-' + index).val()
        let product_title = $('.product-title-' + index).val()
        let product_id = $('.product-id-' + index).val()
        let product_price = $('.current-product-price-' + index).text()
        let product_pid = $('.product-pid-' + index).val()
        let product_image = $('.product-image-' + index).val()

        console.log('Quantity: ' + quantity);
        console.log('title: ' + product_title);
        console.log('ID: ' + product_id);
        console.log('PID: ' + product_pid);
        console.log('Image: ' + product_image);
        console.log('Price: ' + product_price);
        console.log('Index: ' + index);
        console.log('current Element: ' ,this_val);

        $.ajax({
            url:'/add-to-cart',
            data:{
                'id': product_id,
                'pid':product_pid,
                'image':product_image,
                'qty':quantity,
                'title':product_title,
                'price':product_price,
            },
            dataType: 'json',
            beforeSend: function(){
                this_val.html("Adding to cart");

            },
            success:function(response){
                this_val.html("✓")
                console.log("Added to cart");
                $(".cart-items-count").text(response.totalcartitems)
                
            }
        })
    })

    $(".delete-product").on("click", function(){
        let product_id = $(this).attr("data-product")
        let this_val = $(this)

        console.log("Product Id: ",product_id);

        $.ajax({
            url:"/delete-from-cart",
            data:{
                "id": product_id
            },
            dataType:"json",
            beforeSend: function(){
                this_val.hide()
            },
            success: function(response){
                this_val.show()
                $(".cart-items-count").text(response.totalcartitems)
                $("#cart-list").html(response.data)
            }

        })
    })


    // Update Cart Product List

    $(".update-product").on("click", function(){
        let product_id = $(this).attr("data-product")
        let this_val = $(this)
        let product_quantity = $(".product-qty-"+product_id).val()

        console.log("Product Id: ",product_id);
        console.log("Product qty: ",product_quantity);

        $.ajax({
            url:"/update-cart",
            data:{
                "id": product_id,
                "qty":product_quantity,
            },
            dataType:"json",
            beforeSend: function(){
                this_val.hide()
            },
            success: function(response){
                this_val.show()
                $(".cart-items-count").text(response.totalcartitems)
                $("#cart-list").html(response.data)
            }

        })
    })
})












// $('#add-to-cart-btn').on('click', function(){
//     let quantity = $('#product-quantity').val()
//     let product_title = $('.product-title').val()
//     let product_id = $('.product-id').val()
//     let product_price = $('#current-product-price').text()
//     let this_val = $(this)

//     console.log('Quantity: ' + quantity);
//     console.log('title' + product_title);
//     console.log('ID: ' + product_id);
//     console.log('Price: ' + product_price);
//     console.log('current Element: ' +this_val);

//     $.ajax({
//         url:'/add-to-cart',
//         data:{
//             'id': product_id,
//             'qty':quantity,
//             'title':product_title,
//             'price':product_price,
//         },
//         dataType: 'json',
//         beforeSend: function(){
//             this_val.html("Adding to cart");

//         },
//         success:function(response){
//             this_val.html("Item Added Success")
//             console.log("Added to cart");
//             $(".cart-items-count").text(response.totalcartitems)
            
//         }
//     })
// })