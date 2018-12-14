$(document).ready(function(){
    var form = $('#form_buying_product');
    console.log(form);
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
        console.log(product_price);

            var data = {};                            // переменные которые отправляются (id, number  товара)
            data.product_id = product_id
            data.number = number
            var csrf_token = $('#form_buying_product [name="csrfmiddlewaretoken"]').val(); // постзапрос для Django
            data ["csrfmiddlewaretoken"] = csrf_token;

            var url = form.attr("action");            // адрес на который необходимо отправлять постзапрос

        console.log(data)
            $.ajax({
                url:url,
                type: 'POST',                         // тип запроса
                data: data,
                cache: true,                          // кэширование
                success: function(data){              // функция вызывается если успешно получен ответ с сервера
                    console.log("OK");
                    console.log(data.products_total_number);
                    if (data.products_total_number){
                        $('#cart_total_number').text("("+data.products_total_number+")");
                    }
                },
                error: function(){
                    console.log('error')
                }
            })

        // Добавление нового элемента в корзину (Визуальное отображение)
        $('.cart-items ul').append('<li>' + product_name + ': ' + number + 'шт. ' + 'по ' + product_price + 'руб. ' +
            '<a class="delete-item" href="">x</a>'+
        '</li>');

    })

    function showingCart(){
        $('.cart-items').toggleClass('hidden');     //Функция добавления удаления товаров из корзины
    };

    $('.cart-container').on('click', function(e){
        e.preventDefault();
        showingCart();
    });

    $('.cart-container').mouseover(function(){
        showingCart();
    });

    $('.cart-container').mouseout(function(){
        showingCart();
    });

     $(document).on('click', '.delete-item', function(e){
     e.preventDefault();
        $(this).closet('li').remove();
     });
});

