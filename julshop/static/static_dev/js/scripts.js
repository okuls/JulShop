$(document).ready(function(){
    var form = $('#form_buying_product');
    console.log(form);

    function cartUpdating(product_id, number, is_delete){
        var data = {};                            // переменные которые отправляются (id, number  товара)
        data.product_id = product_id
        data.number = number
        var csrf_token = $('#form_buying_product [name="csrfmiddlewaretoken"]').val(); // постзапрос для Django
        data["csrfmiddlewaretoken"] = csrf_token;

        if (is_delete){
            data["is_delete"] = true;
        }

        var url = form.attr("action");            // адрес на который необходимо отправлять постзапрос

        console.log(data)
            $.ajax({
                url: url,
                type: 'POST',                         // тип запроса
                data: data,
                cache: true,                          // кэширование
                // функция вызывается если успешно получен ответ с сервера
                success: function(data){
                    console.log("OK");
                    console.log(data.products_total_number);
                    if (data.products_total_number || data.products_total_number == 0){
                        $('#cart_total_number').text("("+data.products_total_number+")");
                        console.log(data.products);
                        $('.cart-items ul').html("");
                        // Добавление нового элемента в корзину (Визуальное отображение)
                        $.each(data.products, function(k, v){
                            $('.cart-items ul').append('<li>' + v.name + ': ' + v.number + 'шт. ' + 'по ' + v.price_per_item + 'руб. ' +
                                '<a class="delete-item" href="" data-product_id="'+v.id+'">x</a>' + '</li>');
                        }) ;
                    }
                },
                error: function(){
                    console.log('error')
                }
            })

    }

    form.on('submit', function(e){
        e.preventDefault();
        console.log('123');
        var number = $('#number').val();
        console.log(number);
        var submit_btn = $ ('#submit_btn');
        var product_id = submit_btn.data("id");
        var product_name = submit_btn.data("name");
        var product_price = submit_btn.data("price");
        console.log(product_id);
        console.log(product_name);

        cartUpdating(product_id, number, is_delete=false)
    });

//    function showingCart(){
//        $('.cart-items').removeClass('hidden');
//    };
//
////    $('.cart-container').on('click', function(e){
////        e.preventDefault();
////        showingCart();
////    });

    $('.cart-container').mouseover(function(){
        $('.cart-items').removeClass('hidden');
    });

    $('.cart-container').mouseout(function(){
        $('.cart-items').addClass('hidden');
    });

    //Функция добавления удаления товаров из корзины
    $(document).on('click', '.delete-item', function(e){
        e.preventDefault();
        product_id = $(this).data("product_id");
        number = 0;
        cartUpdating(product_id, number, is_delete=true)
     });

    function calculatingCartAmount(){
        var total_order_amount = 0
            $('.total-product-in-cart-amount').each(function(){
                total_order_amount = total_order_amount + parseFloat($(this).text()).toFixed(2);
            });
            console.log(total_order_amount);
            $('#total_order_amount').text(parseFloat(total_order_amount)).toFixed(2);
    };

    $(document).on('change', ".product-in-cart-quantity", function(){
        var current_quantity = $(this).val();
        console.log(current_quantity);

        var current_tr = $(this).closest('tr');
        var current_price = parseFloat(current_tr.find('.product-price').text()).toFixed(2);
        var total_amount = parseFloat(current_quantity * current_price).toFixed(2);
        current_tr.find('.total-product-in-cart-amount').text(total_amount);
        console.log(current_price);
        calculatingCartAmount();
    });

    calculatingCartAmount();
});

