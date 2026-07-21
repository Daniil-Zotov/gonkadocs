---
title: "Улучшаем инфиренс Kimi"
template: proposals-main.html
---

# Улучшаем инфиренс Kimi

<div class="preproposal-header" markdown="1">

<div class="preproposal-status">🔴 Expired</div>

**Author:** Mitch
**Created:** 2026-07-14 01:37 UTC
**Closes:** 2026-07-21 01:37 UTC
**Language:** RU
**Votes:** 6
**Avg. Bid:** 0.00 GNK

</div>

Kimi в Gonka перегружен и сыпет ошибками. Разбираем, почему так вышло, и что можно исправить прямо сейчас через Governance и настройки нод.

---

## Full Proposal

Факты:

* \~20% веса сети приходится на Kimi  
* Запросов на инфиренс идет столько, что ноды с Kimi часто перегружены, и ответ падает с ошибкой  
* Недели 2 назад Kimi можно было нормально пользоваться  
* Сейчас Kimi часто дает ошибку, стало больше запросов  
* Сама по себе цена не будет расти и при 100% загрузке нод с Kimi (динамического прайсинга нету в девшардах, и в след релизе не появится)  
* Майнеры часто запускают Kimi на 8xH-200, чтобы не терять 5% за делегацию. Хотя по весу, там было бы выгоднее запустить MiniMax. Эта карта слабовата для Kimi, работает плохо, по сути ее запускают для галочки, такие ноды получают инфиренсы и плохо с ними справляются, ухудшают качество. Если отменить штраф \- на них перестанут запускать Kimi и качество улучшится, но тут надо прояснить от чего нас защищает этот штраф?  
* На 8xB-300 выгодность для Minimax и Kimi одинакова. И там все запускают Minimax, потому что без нагрузки жить проще, ниже риск падения ноды, и это базовая модель которая не может “выпасть из сети”, как было с Kimi недавно.  
* На 8xB-200 Kimi выгоднее чем Minimax на 20%. Пока загадка почему там тоже часто запущен Minimax. Если вы такой майнер \- скажете мне в личку плиз.

У разработчиков большие планы, как много чего улучшить, и от майнеров тут не особо что то зависит, ток советы можем давать.  
Но вот что мы реально можем, так это менять настройки через Governance, и это сработает прямо сейчас.

# Что можно сделать если у вас 8xB-200

* Перейдите на Kimi прямо сейчас\!   
* Оптимизированные ML образы тут: [https://registry.kaitaku.ai/](https://registry.kaitaku.ai/)  
* Станете зарабатывать на 20% больше.  
* И пользователям инфиренса будет приятно.

# Что можно сделать через Governance

* Убрать штраф за не-делегацию модели.   
  * Результат: на H-200 перестанут запускать Kimi, тк это потеряет экономический смысл. Качество инференция улучшится, ошибок станет меньше.  
* Повысить коэфициент для Kimi, процентов на 10  
  * Результат: майнеры с B-300 начнут запускать Kimi вместо MiniMax  
* Поднять цену на инфиренс Kimi.  
  * Результат: меньше станут гонять тестовых запросов, снизится нагрузка. По сути такая защита от спама.  
  * На сколько поднимать:  
    * Для начала в 10 раз, посмотреть, повлияет ли это вообще на количество запросов. Может быть там тестовых мало, а все что есть это реальные клиенты. Если так то продолжить еще поднимать.  
    * Даже если поднять в 100 раз, то все равно у нас будет дешевле в 10 раз чем на OpenRouter

# Последовательность изменений

* Все изменения делать отдельными пропозалами. Поменяли, посмотрели 3-4 дня хотя бы что поменялось, сделали выводы, потом менять что то другое.  
* Первым делом я бы убрал штраф за не-делегацию. Но тут стоит прояснить \- от чего он нас вообще должен был защищать? Я что то забыл, напомните плиз.  
* Потом повысить коэфициент для Kimi, процентов на 10\. На H-200 минимакс все равно останется выгоднее. А на H-100 вообще Kimi нельзя запустить, так что Minimax не вымрет.  
* Потом поднять цену инфиренса на Kimi. И делать это постепенно, новыми пропозалами, такое динамическое ценообразование “врнучную”, пока не станет заметно что цена влияет на нагрузу.

---

## Comments (2)

### 💬 Viktor
*2026-07-14 03:04* · 👍 0 · 👎 0

Thanks for the detail research and clarity!

For me it seems better to
1. Start with increasing the coefficient for Kimi by 10%. Expect that situation will improve and measure, how much
2. Increase the coefficient for Kimi again, depending on the results of step 1. Iterate.

---

Regarding idea with removing non-delegation penalty:
 - it's looks as a good idea to play with it, it really can decrease number of not quality attempts to handle Kimi requests
 - arguments, why it was implemented should be considered deeper
 - as I remember, in May-June, when network worked well, such penalty already existed - we should consider deeper, what changed

---

Regarding to idea with Kimi price changes - here it's better to investigate, why the implemented denamic price mechanism doesn't work - and try to fix it while we have an opportunity to test it on small volumes.

To change price manually - it's a dangerous zone that even more decreases the sence of brokers and clients stability. Problems with Kimi were even before it was fully loaded.

---
My experience regarding to such a question: modeling Yandex Market auction, optimizing bids for goods providers

---

### 💬 Slava MyGonka
*2026-07-14 07:20* · 👍 0 · 👎 0

Жалко что здесь нельзя прикладывать скрины.
Ты обращаешься к двум людям фактически, т.к. в сети всего четыре адреса с такими GPU.

Прилагаю ссылкой: https://prnt.sc/9gCAQ26WvSeA

Два крупных, два не крупных.

Хорошо бы лично обратиться, если бы знать, кто это ))

Но, я думаю, они боятся мисрейтов.

Тут бы мог помочь сильный  яRestitution Comity, но они открещиваются от таких задач и сейчас вообще непонятно, есть ли этот комитет.

Инфу я брал отсюда: https://ranking.gonkadb.com/

Кроме того я не видел еще запущенных Kimi на 8*В200. Одна нода (есть на скрине), но это нода КорТим и у нее какие-то особые правила работы. Смотреть на нее не нужно.

---


---

<div class="preproposal-link" markdown="1">

[View on gonka.vote](https://gonka.vote/proposal/d185d9eb-243f-4228-b4ac-e2c7a50a5325)

</div>
