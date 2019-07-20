// $(document).ready(function(){ // Стандартная обёртка Джиквери, которая говорит, что код должен выполняться, когда загрузится весь файл
//     var form = $('#form_buying_product'); // Выбираем форму. Знак $ означает, что к этой странице нужно обращаться, как к элементу Джиквери. И выбираем форму по Id
//     console.log(form); // Чтобы увидеть, как эта форма сраюотала выведем её в консоль
    
//     function basketUpdating(product_id, nmb, is_delete) { // Необходимо передавать product_id, nmb и какое-то дефолтное значение is_delete
//         var data = {};
//         data.product_id = product_id;// Добавляем в данные ай ди товара
//         data.nmb = nmb;// Добавляем в данные количество
//          var csrf_token = $('#form_buying_product [name="csrfmiddlewaretoken"]').val(); // Эти две строчки могут добавлять csrf токен, который нужен Джанго для того чтобы делать ПОСТ запрос.
//          data["csrfmiddlewaretoken"] = csrf_token;
        
//         if (is_delete) {
//             data["is_delete"] = true;
//         }

//         var url = form.attr("action"); // адрес, на который необходимо отправлять ПОСТ запрос.
        
//        console.log(data)
//         $.ajax({ // функция аджакс. Когда она будет успешно отрабатываться, то мы будем добавлять товар в корзину. Когда пользователь обновит страницу, изначально данные будут переадресовываться из базы данных
//             url: url,
//             type: 'POST', // Тип запроса
//             data: data, // равна нашей переменной с данными var data = {}; в которую мы будем добавлять какие-то данные
//             cache: true, // Киширование
//             success: function(data) { // Функция, которая вызывается, если успешно получин ответ с сервера
//                 console.log("OK");
//                 console.log(data.products_total_nmb);
//                 if (data.products_total_nmb || data.products_total_nmb == 0) { //если такое значение есть, то только тогда вписываем на страницу данный текст
//                     $('#basket_total_nmb').text("("+data.products_total_nmb+")"); // Изменяется количество нового товара в корзине
//                     console.log(data.products);
//                     $('.basket-items ul').html(""); // Очищаем все товары, которые уже есть в корзине. Т.е когда аджакс возвращается, он сперва удаляет то, что есть, а потом адресовывает заново. Но, так как это происходит быстро, то незаметно.
//                     $.each(data.products, function(k, v){ // Проходимся циклом по data.products и добавляем в корзину через указанную функцию. В Цикле у кажного элемента есть его индекс и сам объект. Следовательно можно указать k, v , кде k - порядковый номер(или индекс), v - непосредственно сам объект
//                         $('.basket-items ul').append('<li>'+v.name+', '+ v.nmb + ' шт. ' + ' по '+ v.price_per_item + 'грн ' +
//            '.....<a class="delete-item" href="" data-product_id="'+v.id+'">x</a>'+ // Чтобы появлялось подчёркивание, это должен быть энкор. Также, чтобы появлялся курсор, необходимо прописать href=""(хоть и пустой) 
//         '</li>'); // Когда мы отправляем форму, мы выбираем basket-items ul(т.е где-то на уровень ниже есть этот элемент). append('<li></li>') - функция, которая добавляет внутрь какой-то элемент. В данном случае <li></li>.  
//                     });
//                 }
                
//             },
//             error: function(){ // Если неуспешно получен ответ с сервера
//                 console.log("error")
//             }
// })
//     }

//     form.on('submit', function(e){ // Мы должны присоеденить к форме событие. По событию submit мы хотим присоеденить функцию, в которой будем писать код. Нужно что-то сделать, чтобы страница не обновлялась, когда мы отправляем форму. Это можно сделать с помощью такой конструкции, как поместить в скобки переменную "e". Есть стандартное поведение и мы можем его предупредить с помощью данной конструкции. 
//         e.preventDefault(); // К аргументу "e" применяем эту функцию, которая должна отменить отправку формы, так как мы сперва должны поместить товар в корзину.
//         console.log('123'); // Выводим в консоли 123, чтобы проверить как работает
//         var nmb = $('#number').val(); // мы хотим увидеть, какое количество покупается. Вызываем Id = number из инпута в шаблоне. val() - чтобы получить значение этого элемента.
//         console.log(nmb); // Проверяем через консоль какое количество мы отправляем.
//         var submit_btn = $('#submit_btn'); // id="submit-btn" - через него затем выводим id продукта и имя
//         var product_id =  submit_btn.data("product_id"); // Вписываем Id продукта, который мы хотим отправить в корзину
//         var name = submit_btn.data("name"); // Вписываем название продукта, который мы хотим отправить в корзину
//         var price = submit_btn.data("price");
//         console.log(product_id ); // выводим в консоди id
//         console.log(name); // выводим в консоли имя
        
//         basketUpdating(product_id, nmb, is_delete=false) // Вызываем функцию
 


       
//     }); 
    
//      function shovingBasket() {
//          $('.basket-items').removeClass('hidden'); // При наведении на этот класс запускается данный метод(т.е должен убраться данный класс)
//      };   

//     $('.basket-container').on('click', function(e){
//         e.preventDefault(); // Прокинем также ивент
//         shovingBasket();
//     });   //Когда мы наводим на этот контейнер(перечисляем какие ивенты: click или hover) выполняется функция
    
//     $('.basket-container').mouseover(function(){
//         shovingBasket();
//     });   //Когда мы наводим на этот контейнер(перечисляем какие ивенты: click или hover) выполняется функция
    
//     $('button').on('click', function(){
//         shovingBasket();
//     });
    

//     $(document).on('click', '.delete-item', function(e){ // Обязательно пишем $(document), так как каждый раз, когда мы добавляем товар в корзину, скрипт об этом не знает. Т.е каждый раз он должен сканировать весь документ.  Если будете нажимать на delete-item(т.е по событию on('click',), тогда выполняется функция
//         e.preventDefault(); //На всякий случай, чтобы ничего не происходило при нажатии на эту ссылку
//         product_id = $(this).data("product_id");// Считываем Дата атрибут на этой кнопке и добавляем его выше.
//         nmb = 0;
//         basketUpdating(product_id, nmb, is_delete=true); // Когда удаляем эту функцию, пишем is_delete=true
    
// });  

$(document).ready(function(){
    var form = $('#form_buying_product');
    console.log(form);


    function basketUpdating(product_id, nmb, is_delete){
        var data = {};
        data.product_id = product_id;
        data.nmb = nmb;
         var csrf_token = $('#form_buying_product [name="csrfmiddlewaretoken"]').val();
         data["csrfmiddlewaretoken"] = csrf_token;

        if (is_delete){
            data["is_delete"] = true;
        }

         var url = form.attr("action");

        console.log(data)
         $.ajax({
             url: url,
             type: 'POST',
             data: data,
             cache: true,
             success: function (data) {
                 console.log("OK");
                 console.log(data.products_total_nmb);
                 if (data.products_total_nmb || data.products_total_nmb == 0){
                    $('#basket_total_nmb').text("("+data.products_total_nmb+")");
                     console.log(data.products);
                     $('.basket-items ul').html("");
                     $.each(data.products, function(k, v){
                        $('.basket-items ul').append('<li>'+ v.name+', ' + v.nmb + 'шт. ' + 'по ' + v.price_per_item + 'грн  ' +
                            '<a class="delete-item" href="" data-product_id="'+v.id+'">x</a>'+
                            '</li>');
                     });
                 }

             },
             error: function(){
                 console.log("error")
             }
         })

    }

    form.on('submit', function(e){
        e.preventDefault();
        console.log('123');
        var nmb = $('#number').val();
        console.log(nmb);
        var submit_btn = $('#submit_btn');
        var product_id =  submit_btn.data("product_id");
        var name = submit_btn.data("name");
        var price = submit_btn.data("price");
        console.log(product_id );
        console.log(name);

        basketUpdating(product_id, nmb, is_delete=false)

    });

    function showingBasket(){
        $('.basket-items').removeClass('hidden');
    };

    //$('.basket-container').on('click', function(e){
    //    e.preventDefault();
    //    showingBasket();
    //});

     $('.basket-container').mouseover(function(){
         showingBasket();
     });

     //$('.basket-container').mouseout(function(){
     //    showingBasket();
     //});

     $(document).on('click', '.delete-item', function(e){
         e.preventDefault();
         product_id = $(this).data("product_id")
         nmb = 0;
         basketUpdating(product_id, nmb, is_delete=true)
     });

    function calculatingBasketAmount(){ // Общая сумма всех товаров в корзине
        var total_order_amount = 0;
        $('.total-product-in-basket-amount').each(function() {
            total_order_amount = total_order_amount + parseFloat($(this).text());
        });
        console.log(total_order_amount);
        $('#total_order_amount').text(total_order_amount.toFixed(2));
    };

    $(document).on('change', ".product-in-basket-nmb", function(){ // Функция, считывающая текущее количество
        var current_nmb = $(this).val(); // Считали текущее количество с Инпута
        console.log(current_nmb);

        var current_tr = $(this).closest('tr'); // Для того, чтобы найти текущую стоимость, необходимо сперва найти текущий ряд(ячейку), в кот изменяется количество
        var current_price = parseFloat(current_tr.find('.product-price').text()).toFixed(2); // Берём текущую стоимость товара. Находим спен с классом product-price. Из него будем брать текст и переводить его в число. Для этого потребуется функция parseFloat.
        console.log(current_price);
        var total_amount = parseFloat(current_nmb*current_price).toFixed(2); // Находим общую сумму. toFixed(2) - означает два числа после запятой
        console.log(total_amount);
        current_tr.find('.total-product-in-basket-amount').text(total_amount); // После того, как мы нашли общую сумму, находим текущий ряд, в нём находим ячейку с классом total-product-in-basket-amount и в этот класс будем текстом записывать total_amount

        calculatingBasketAmount(); // Вызываем эту функцию, чтобы пересчитать общее количество
    });

    calculatingBasketAmount();

    
});
  




