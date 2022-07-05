# KuznechikChat
<p>В данном проекте представлена реализация программного обеспечения для обмена сообщениями по открытому каналу связи с использованием алгоритма симметричного шифрования, утверждённого в ГОСТ 34.12-2018.</p>
<p>Проект разработан в качестве практической части моей выпускной квалификационной работы (ВКР или дипломной работы) в ВУЗе.</p>

# Содержание
1. [Разработка ПО](#dev)
2. [Сетевое подключение](#network)
3. [Общая информация о рассматриваемом шифре](#general_info)
4. [Основные преобразования алгоритма](#transformations)
5. [Сеть Фейстеля](#feistel)
6. [Алгоритм шифрования](#encryption)
7. [Алгоритм дешифрования](#decryption)

## Разработка ПО <a name="dev"></a>
Проект приложения содержит следующие модули:
<ul>
    <li>main.py – модуль инициализации и запуска проекта;</li>
    <li>consts.py – модуль с массивами констант, используемых в алгоритме шифрования;</li>
    <li>crypto.py – модуль с реализацией класса для шифрования/дешифрования при помощи ГОСТ 34.12-2018;</li>
    <li>utils.py – модуль с реализацией всех необходимых математических преобразований;</li>
    <li>chat_app.py – модуль с реализацией класса всего оконного приложения;</li>
    <li>connection_handler.py – модуль с реализацией класса обработчика соединения;</li>
    <li>chat_window.py – модуль с реализацией класса окна чата;</li>
    <li>connect_window.py – модуль с реализацией класса окна подключения;</li>
    <li>main_window.py – модуль с реализацией класса главного окна приложения;</li>
    <li>open_server_window.py – модуль с реализацией класса окна открытия сервера;</li>
    <li>request_dialog.py – модуль с реализацией класса диалогового окна запроса на подключение.</li>
</ul>
<p>Разработанное ПО имеет название «KuznechikChat» и используется для обмена сообщениями по открытому каналу с использованием алгоритма шифрования «Кузнечик» в режиме простой замены, описанного в ГОСТ 34.12-2018.</p>

## Сетевое подключение <a name="network"></a>
<p>Подключение между двумя пользователями осуществляется при помощи сокетов.</p>
<p>Реализовано "point-to-point" соединение по локальной сети.</p>
<p>Обмен сообщениями осуществляется между двумя пользователями по модели «сервер-клиент». Это означает, что в представленной реализации соединение и обмен сообщениями происходит без третьей стороны.</p>
<p>Для установки соединения между двумя пользователями, один из пользователей должен создать экземпляр сокета, сделать его серверным («слушающим»), привязать его к порту операционной системы, и ожидать входящего подключения от другого пользователя.</p>
<p>Пользователь-клиент должен создать экземпляр сокета, сделать его клиентским, привязать его к порту операционной системы, и послать запрос на подключение пользователю-серверу, указав пару «IP-адрес, порт» собеседника.</p>
<p>Обмен ключом шифрования происходит по протоколу Диффи-Хеллмана.</p>

## Общая информация о рассматриваемом шифре <a name="general_info"></a>
<p>Для реализации алгоритма шифрования сообщений в разрабатываемом программном обеспечении был выбран алгоритм блочного шифрования «Кузнечик» (в режиме простой замены).</p>
<p>«Кузнечик» – симметричный алгоритм блочного шифрования с размером блока 128 бит и длиной ключа 256 бит. Ключ используется для генерации раундовых ключей сети Фейстеля.</p>
<p>Шифр «Кузнечик» (наряду с блочным шифром «Магма») утверждён в качестве стандарта в ГОСТ Р 34.12-2015 «Информационная технология. Криптографическая защита информации. Блочные шифры» приказом от 19 июня 2015 года № 749-ст. Стандарт вступил в действие с 1 января 2016 года.
Протоколом № 54 от 29 ноября 2018 года, на основе ГОСТ Р 34.12-2015, Межгосударственным советом по метрологии, стандартизации и сертификации был принят межгосударственный стандарт ГОСТ 34.12-2018 «Информационная технология. Криптографическая защита информации. Блочные шифры». Приказом Федерального агентства по техническому регулированию и метрологии от 4 декабря 2018 года № 1061-ст стандарт ГОСТ 34.12-2018 введен в действие в качестве национального стандарта Российской Федерации с 1 июня 2019 года.</p>
<p>Шифр разработан Центром защиты информации и специальной связи ФСБ России с участием АО «Информационные технологии и коммуникационные системы» (АО «ИнфоТеКС»). Внесён Техническим комитетом по стандартизации ТК 26 «Криптографическая защита информации».</p>

## Основные преобразования алгоритма <a name="transformations"></a>
<p>В алгоритме используются следующие преобразования:</p>
<ul>
    <li>
        сложение по модулю 2 (XOR), применяемое к блокам данных;
    </li>
    <li>
        нелинейное биективное преобразование;
    </li>
    <li>
        линейное преобразование.
    </li>
</ul>
<p>В качестве нелинейного биективного преобразования выступает подстановка по значениям массива (см. рисунок 1): за индекс массива берётся a_i – 8 бит блока данных, где i=15…0.</p>
<img src="https://user-images.githubusercontent.com/73097290/177288164-4e8eb14f-793e-4d31-897d-e524588f2a1c.png" alt="Массив констант">
<i>Рисунок 1 – Массив констант для нелинейного биективного преобразования</i>
<p>Линейное преобразование задается отображением L(a) = R^16(a), которое определяется следующим образом:</p>
<img src="https://user-images.githubusercontent.com/73097290/177290165-aae6a83b-1fb7-4147-b634-90da69938b9e.png" alt="Линейное отображение">
<p>где a_i – 8 бит блока данных, i = 15…0.</p>
<p>Преобразование V_8^16 → V_8 определяется следующим образом:</p>
<img src="https://user-images.githubusercontent.com/73097290/177290696-b7bec68b-e758-4e7e-a412-7e80323274e4.png" alt="Линейное преобразование">
<p>где	lin_j – линейная константа (см. рисунок 2), j = 0…15.</p>
<img src="https://user-images.githubusercontent.com/73097290/177291109-0f96492b-cbf9-4244-a001-298b4a3014f8.png" alt="Линейныее константы">
<i>Рисунок 2 – Массив констант для линейного биективного преобразования</i>
<p>Стоит отметить следующее:</p>
<ul>
    <li>для a_i: i = 15 является старшим разрядом, а i = 0 является младшим разрядом;</li>
    <li>в функции линейного преобразования операции сложения и умножения осуществляются в поле Галуа GF(2^8).</li>
</ul>
<p>В арифметике полей Галуа операция сложения является простым побитовым сложением по модулю 2 (ХОR).</p>
<p>Для умножения в поле Галуа необходимо выполнить ряд действий:</p>
<ol>
    <li>взять число x, обратившись к массиву констант поля Галуа по индексу, равному a_i;</li>
    <li>взять число y, обратившись к массиву констант поля Галуа по индексу, равному l_j;</li>
    <li>путём сложения получить число z = x + y;</li>
    <li>взять число r, обратившись к массиву констант поля Галуа по индексу, равному z;</li>
    <li>полученное число r идёт на вход операции сложения по модулю 2 (XOR).</li>
</ol>
<p>В полях Галуа существует понятие примитивного члена – элемент поля, чьи степени содержат все ненулевые элементы поля.</p>
<p>Сложение на шаге 3 объясняется следующим образом: для поля GF(2^8), которое мы используем, в качестве примитивного члена всегда выбирают 2.</p>
<p>Учитывая это свойство, любой элемент поля можно выразить через степень примитивного члена.</p>
<p>Например:</p>
<ul>
    <li>обращаясь к таблице по индексу 7, мы получаем число 2^7 = 128;</li>
    <li>обращаясь к таблице по индексу 8, мы получаем число 2^8 = 195;</li>
    <li>и т.д.</li>
</ul>
<p>Таким образом, чтобы вычислить выражение 2^7 * 2^8, мы можем воспользоваться свойством перемножения чисел с одинаковым основанием и разными степенями:</p>	
<p>a^m * a^n = a^(m + n).</p>
<p>Получаем, что 2^7 * 2^8 = 2^(7 + 8) = 2^15.</p>
<p>В данном случае, на шаге 4 мы будем использовать число z = 15.</p>

## Сеть Фейстеля <a name="feistel"></a>
<p>В рассматриваемом алгоритме сеть Фейстеля используется для формирования раундовых (или итерационных) ключей.</p>
<p>Раундовые ключи используются в процессах шифрования и дешифрования, которые будут рассмотрены в работе ниже.</p>
<p>Раундовые ключи получаются путём преобразований на основе мастер-ключа K. Формирование самого мастер-ключа рассмотрено в главе о сетевом подключении.</p>
<p>Используемая сеть Фейстеля использует следующую последовательность функций:</p>
<ol>
    <li>побитовое сложение по модулю 2 (XOR);</li>
    <li>нелинейное биективное преобразование;</li>
    <li>линейное преобразование;</li>
    <li>побитовое сложение по модулю 2 (XOR).</li>
</ol>
<p>Сеть Фейстеля состоит из нескольких раундов, называемых ячейками Фейстеля.</p>
<p>Перед первой итерацией отработки ячейки Фейстеля, мастер-ключ K (длиной 256 бит) разбивается пополам: на ветви сети Фейстеля K_1 и K_2 (см. рисунок 3). Данные значения являются первым и вторым итерационным ключом соответственно.</p>
<img src="https://user-images.githubusercontent.com/73097290/177296009-985b43a6-d5a3-4eb4-a2df-52fbefc98857.png" alt="Первый раунд сети Фейстеля">
<i>Рисунок 3 – Первый раунд используемой сети Фейстеля</i>
<p>В свою очередь, ячейка Фейстеля представляет собой следующую последовательность действий:</p>
<ol>
    <li>на вход ячейки подаётся две ветви сети Фейстеля; обозначим их как блоки L и R соответственно;</li>
    <li>после чего блок L побитово складывается по модулю 2 (подаётся на вход функции XOR) с итерационной константой C_i, где i = 0…31; процесс формирование констант будет описан ниже;</li>
    <li>полученное на предыдущем шаге значение подаётся на вход функции нелинейного биективного преобразования;</li>
    <li>полученное на предыдущем шаге значение подаётся на вход функции линейного преобразования;</li>
    <li>полученное на предыдущем шаге значение побитово складывается по модулю 2 (подаётся на вход функции XOR) с блоком R;</li>
    <li>в правую ветвь сети записывается значение блока L, в левую ветвь записывается значение, полученное в результате выполнения шагов 2-5;</li>
    <li>новые значения блоков подаются на вход следующей ячейки Фейстеля.</li>
</ol>
<p>Расчёт по ячейке Фейстеля повторяется 32 раунда. Через каждые 8 раундов мы получаем пару раундовых ключей (K_(2i-1), K_2i), где i = 2…5.</p>
<p>Учитывая, что значения K_1 и K_2 мы получили путём разбиение мастер-ключа надвое, после 32 раундов ячейки Фейстеля, мы получаем необходимые нам 10 раундовых ключей ключей.</p>
<p><b>Итерационные константы</b> получаются с помощью линейного преобразования, где на вход функции подаётся массив array(i), где i = 0…31. Т.е. значения номеров итераций преобразуются при помощи функции в итерационные константы.</p>
<p>В целях уменьшения времени шифрования/дешифрования данных, в ходе разработки программного обеспечения было решено не вычислять итерационные константы непосредственно в процессе обмена сообщениями, а реализовать их как статичный массив констант.</p>

## Алгоритм шифрования <a name="encryption"></a>
<p>Как уже говорилось ранее, шифр на основе SP-сети получает на вход блок и ключ и совершает несколько чередующихся раундов, состоящих из чередующихся стадий подстановки и стадий перестановки. В алгоритме «Кузнечик» выполняется девять полных раундов и один неполный.</p>
<p>Первые девять раундов представляют собой следующую последовательность действий:</p>
<ol>
    <li>выполняется побитовое сложение по модулю 2 (XOR) входного блока данных a и раундового ключа K_(i+1), где i = 0…8 – номер (индекс) раунда;</li>
    <li>полученное на предыдущем шаге значение подаётся на вход функции нелинейного биективного преобразования;</li>
    <li>полученное на предыдущем шаге значение подаётся на вход функции линейного преобразования.</li>
</ol>
<p>Последний десятый раунд является операцией побитового сложения по модулю 2 (XOR) результирующего блока данных r (полученного после 9 раунда SP-сети) и раундового ключа K_10.</p>
<p>На рисунке 4 представлена схема первых девяти раундов шифрования.</p>
<img src="https://user-images.githubusercontent.com/73097290/177297345-da3e11d4-19b2-4fde-a5f7-1bada62c89d2.png" alt="Первые девять раундов алгоритма шифрования">
<i>Рисунок 4 – Первые девять раундов алгоритма шифрования</i>

## Алгоритм дешифрования <a name="decryption"></a>
Для дешифрования шифротекста используются те же операции, что и в алгоритме шифрования, но в обратной последовательности (см. рисунок 5).
<img src="https://user-images.githubusercontent.com/73097290/177298488-2603b796-f8b6-4ed0-9abf-ddc37ea5889b.png" alt="Первые девять раундов алгоритма дешифрования">
<i>Рисунок 5 – Первые девять раундов алгоритма дешифрования</i>
<p>Первые девять раундов представляют собой следующую последовательность действий:</p>
<ol>
    <li>выполняется побитовое сложение по модулю 2 (XOR) входного блока данных a и раундового ключа K_(10-i), где i = 0…8 – номер (индекс) раунда;</li>
    <li>полученное на предыдущем шаге значение подаётся на вход функции линейного преобразования;</li>
    <li>полученное на предыдущем шаге значение подаётся на вход функции нелинейного биективного преобразования; константы для обратного нелинейного преобразования отличаются от первоначальных.</li>
</ol>
<p>Последний десятый раунд является операцией побитового сложения по модулю 2 (XOR) результирующего блока данных r (полученного после 9 раунда SP-сети) и раундового ключа K_1.</p>
