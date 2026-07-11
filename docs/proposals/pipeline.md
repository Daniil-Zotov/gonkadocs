<style>
.pipeline-wrap {
  max-width: 640px;
  margin: 0 auto;
  padding: 1rem 0.5rem 3rem;
  font-size: 0.75rem;
  line-height: 1.45;
  color: #1f2328;
}

.pipeline-intro {
  font-size: 0.78rem;
  color: #57606a;
  margin-bottom: 1.5rem;
  line-height: 1.45;
}

.pipeline-timeline {
  position: relative;
  /* НЕТ padding-left — линия и точки в одной координатной системе */
}

/* вертикальная чёрная линия — строго по центру первой 28px-колонки */
.pipeline-timeline::before {
  content: "";
  position: absolute;
  left: 13px;              /* центр 28px-колонки = 14px; линия 2px → left = 14-1 = 13px */
  top: 10px;
  bottom: 10px;
  width: 2px;
  background: #24292f;
}

.pipeline-stage {
  margin-bottom: 2rem;
}
.pipeline-stage:last-child {
  margin-bottom: 0;
}

.stage-header {
  display: grid;
  grid-template-columns: 28px 1fr;
  gap: 10px;
  align-items: center;
  margin-bottom: 0.5rem;
}

/* пустой кружок — центр строго на 14px (центр 28px-колонки) */
.stage-node {
  justify-self: center;    /* центр первой колонки = 14px */
  width: 16px;
  height: 16px;
  box-sizing: border-box;
  border-radius: 50%;
  border: 2.5px solid #24292f;
  background: #fff;
  position: relative;
  z-index: 2;
}

.stage-title {
  font-size: 3.0rem;
  font-weight: 700;
  line-height: 1.2;
  color: #1f2328;
  letter-spacing: -0.02em;
}

.pipeline-item {
  display: grid;
  grid-template-columns: 28px 1fr;
  gap: 10px;
  margin-bottom: 0.4rem;
}
.pipeline-item:last-child {
  margin-bottom: 0;
}

/* чёрная точка — центр строго на 14px (центр 28px-колонки) */
.item-dot {
  justify-self: center;
  align-self: start;
  margin-top: 0.48em;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #24292f;
  position: relative;
  z-index: 2;
}

.item-text {
  font-size: 0.6rem;
  line-height: 1.4;
  color: #24292f;
}
</style>

<div class="pipeline-wrap">

<div class="pipeline-intro">
РАЗДЕЛ В ПРОЦЕССЕ РАЗРАБОТКИ
Полный цикл жизни предложения от идеи до отчётности. Каждый этап прозрачен, проверяем сообществом и задокументирован.
</div>

<div class="pipeline-timeline">

  <div class="pipeline-stage">
    <div class="stage-header">
      <div class="stage-node"></div>
      <div class="stage-title">Подготовка</div>
    </div>
    <div class="pipeline-item"><div class="item-dot"></div><div class="item-text">Ознакомиться с актуальным роадмапом Gonka, понять приоритеты сообщества и утверждённые направления развития сети</div></div>
    <div class="pipeline-item"><div class="item-dot"></div><div class="item-text">Изучить прошедшие пропозалы и собранные best practices, чтобы понять формат, требования и типичные ошибки</div></div>
    <div class="pipeline-item"><div class="item-dot"></div><div class="item-text">Проанализировать текущие ончейн-пропозалы и активные препропозалы, чтобы избежать дублирования и найти синергию</div></div>
    <div class="pipeline-item"><div class="item-dot"></div><div class="item-text">Просмотреть GitHub Discussions, Issues и закрытые пропозалы — часто там уже есть частичные решения или обсуждения похожих идей</div></div>
    <div class="pipeline-item"><div class="item-dot"></div><div class="item-text">Ознакомиться с рекомендациями профильных комитетов (GSC, GRC, GTM) и учесть их требования при формировании идеи</div></div>
    <div class="pipeline-item"><div class="item-dot"></div><div class="item-text">Заполнить анкету в Google Forms — это запустит формальный процесс обсуждения: будет создан препропозал на gonka.vote, а также выделен Telegram-чат для живого диалога</div></div>
  </div>

  <div class="pipeline-stage">
    <div class="stage-header">
      <div class="stage-node"></div>
      <div class="stage-title">Обсуждение</div>
    </div>
    <div class="pipeline-item"><div class="item-dot"></div><div class="item-text">Подготовить и провести презентацию пропозала и команды для сообщества — чётко обозначить цели, бюджет, сроки и ожидаемый результат</div></div>
    <div class="pipeline-item"><div class="item-dot"></div><div class="item-text">Вести живое обсуждение на vote-портале gonka.vote и в выделенном Telegram-чате совместно с представителями комитетов, хостами и активными участниками сообщества</div></div>
    <div class="pipeline-item"><div class="item-dot"></div><div class="item-text">Организовать и провести AMA-сессию (Ask Me Anything), где любой член сообщества может задать вопросы команде и получить прямые ответы</div></div>
    <div class="pipeline-item"><div class="item-dot"></div><div class="item-text">По итогам обсуждения профильные комитеты выносят заключение и дают рекомендации по доработке: корректировка суммы, сроков, формата подачи и других параметров пропозала</div></div>
  </div>

  <div class="pipeline-stage">
    <div class="stage-header">
      <div class="stage-node"></div>
      <div class="stage-title">Голосование</div>
    </div>
    <div class="pipeline-item"><div class="item-dot"></div><div class="item-text">Комитет оказывает техническую помощь в подготовке финальной версии пропозала — помогает выверить параметры, формулировки и соответствие стандартам</div></div>
    <div class="pipeline-item"><div class="item-dot"></div><div class="item-text">Все необходимые документы, заключения комитетов и записи встреч публикуются в едином пространстве для ознакомления хостами перед голосованием</div></div>
    <div class="pipeline-item"><div class="item-dot"></div><div class="item-text">Если пропозал появился без предварительного обсуждения (без заполнения анкеты), члены сообщества самостоятельно создают анкету retroactively</div></div>
  </div>

  <div class="pipeline-stage">
    <div class="stage-header">
      <div class="stage-node"></div>
      <div class="stage-title">Отчётность</div>
    </div>
    <div class="pipeline-item"><div class="item-dot"></div><div class="item-text">В случае прохождения пропозала команда совместно с комитетами составляет детальный график отчётности: дедлайны, KPI, мейлстоуны и формат предоставления результатов</div></div>
    <div class="pipeline-item"><div class="item-dot"></div><div class="item-text">Комитеты регулярно контролируют сроки, оценивают качество и содержание отчётов, и при необходимости выносят резолюцию — особенно в случаях отзывных пропозалов, подозрений на скам или репутационных рисков</div></div>
  </div>

</div>

</div>
