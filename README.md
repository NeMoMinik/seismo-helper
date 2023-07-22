# seismo-helper
<p><a href="https://konkurs.sochisirius.ru" target="_blank">
  <img src="seismo_helper/media/Photos_for_Front/ЛОГО (ЗЕЛЕНЫЙ).png" alt="Большие вызовы", style="width: 30%; height: 30%;">
</a></p>

## Автоматический анализ сейсмической активности геологических сред
Наш партнёр: [Газпромнефть](https://www.gazprom-neft.ru/)

![ГРП](seismo_helper/media/Photos_for_Front/ГРП.gif)

Наша цель:
Создание сервиса для автоматического мониторинга сейсмической активности

#Основные задачи
* 1 Предобработать данные и задетектировать события
  + Используем полосовой фильтр и находим STA/LTA
* 2 Нейросеть-пикировщик
  + Обучили свёрточную нейронную сеть для определения точного времени прихода P- и S-волн
* 3 Определение координат гипоцентра
  + С помощью математического алгоритма определяем координаты гипоцентра сейсмического возмущения
* 4 Web-сервис
  + Написали backend и frontend с RestAPI, создали дизайн

![M1](seismo_helper/media/Photos_for_Front/M1.jpg)

<h2>Сборка docker-контейнера</h2>
В директории проекта прописать <code>docker-compose -f docker-compose.prod up -d --build</code><br>
Для просмотра логов <code>docker-compose -f docker-compose.prod logs</code><br>
При первом запуске вам потребуется выполнить следующие команды<br>
<code>docker-compose -f docker-compose.prod exec web python manage.py makemigrations</code><br>
<code>docker-compose -f docker-compose.prod exec web python manage.py migrate</code>
