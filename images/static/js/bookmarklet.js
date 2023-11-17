(function(){
    var jquery_version = '3.3.1';
    var site_url = 'https://14b1-212-58-120-42.ngrok-free.app/';
    var static_url = site_url + 'static/';
    var min_width = 100;
    var min_height = 100;

    function bookmarklet(msg) {
        // Загрузка CSS-стилей
        // загружаем стили bookmarklet.css, добавляя случайное число для предот-
        // вращения кеширования стилей браузером;
        var css = jQuery('<link>');
        css.attr({
            rel: 'stylesheet',
            type: 'text/css',
            href: static_url + 'css/bookmarklet.css?r=' + Math.floor(Math.random()*99999999999999999999)
        });
        jQuery('head').append(css);

        // добавляем HTML-элемент в <body> текущего сайта. Этот элемент содер-
        // жит <div> с изображениями, найденными на сайте;
        box_html = '<div id="bookmarklet"><a href="#" id="close">&times;</a> + <h1>Select an image to bookmark:</h1><div class="images"></div></div>';
        jQuery('body').append(box_html);

        // Добавление скрытия букмарклета при нажатии на крестик.
        // да пользователь кликает на кнопку закрытия блока. Используем селек-
        // тор #bookmarklet#close, чтобы найти элемент с ID close, у которого есть
        // родительский элемент с ID bookmarklet. Селекторы jQuery позволяют нам
        // находить HTML-элементы. Они возвращают все подходящие объекты.
        // Более подробную информацию о селекторах jQuery можно найти на
        // странице https://api.jquery.com/category/selectors/.
        jQuery('#bookmarklet #close').click(function (){
            jQuery('#bookmarklet').remove();
        });

        // Находим картинки на текущем сайте и вставляем их в окно букмарклета
        // Здесь используется селектор img[src$="jpg"], чтобы найти все <img>-элементы,
        // у которых значение атрибута src заканчивается на jpg. Так мы найдем все JPEG-
        // изображения на текущем сайте. Для итерации по ним обращаемся к методу jQueryeach().
        // Все изображения, большие по ширине и высоте, чем заданные
        // min_width и min_height, добавляем в наш контейнер <div class="images">.
        jQuery.each(jQuery('img[src$="jpg"]'), function (index, image) {
            if (jQuery(image).width() >=min_width && jQuery(image).height() >= min_height)
            {
                image_url = jQuery(image).attr('src');
                jQuery('#bookmarklet .images').append(
                    '<a href="#"><img src="'+ image_url +'" /></a>');
            }
        });

        // Когда изображение выбрано, добавляем его в список сохранённых картинок на нашем сайте.
        // привязывает обработчик события click на ссылку изображения;
        //когда пользователь кликает на изображение, сохраняет адрес картинки в переменную selected_image;
        jQuery('#bookmarklet .images a').click(function(e){
            selected_image = jQuery(this).children('img').attr('src');
            // Скрываем букмарклет.
            jQuery('#bookmarklet').hide();
            // Открываем новое окно с формой изображения.
            // скрывает букмарклет и открывает новую вкладку браузера с GET-параметрами
            // (передает заголовок страницы и URL картинки).
            window.open(site_url +'images/create/?url='
                + encodeURIComponent(selected_image)
                + '&title='
                + encodeURIComponent(jQuery('title').text()),
                '_blank');
        });

    };
    // Проверяем, подключена ли jQuery.
    if (typeof window.jQuery != 'undefined') {
        bookmarklet();
    } else {
        // Проверяем что атрибут $ окна не занят другим обьектом.
        var conflict = typeof window.$ != 'undefined';
        // Создание тега <script> с загрузкой jQuery.
        var script = document.createElement('script');
        script.src = '//ajax.googleapis.com/ajax/libs/jquery/' +
            jquery_version + '/jquery.min.js';
        // Добавление тега в блок <heal> документа.
        document.head.appendChild(script);

        // Добавление возможности использовать несколько попыток для загрузки jQuery.
        var attempts = 15;
        (function(){
            // Проверка, подключена ли jQuery
            if(typeof window.jQuery == 'undefined')  {
                if(--attempts > 0) {
                    // Если не подключена, пытаемся снова загрузить
                    window.setTimeout(arguments.callee, 250)
                }
                else {
                    // Превыщено число попыток загрузки jQuery, выводим сообщение.
                    alert('An error occurred while loading jQuery')
                }
            } else {
                bookmarklet();
            }
        })();
    }
})()