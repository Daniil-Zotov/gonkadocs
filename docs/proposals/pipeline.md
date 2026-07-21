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
}

.pipeline-timeline::before {
  content: "";
  position: absolute;
  left: 13px;
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

.stage-node {
  justify-self: center;
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

.item-text a {
  color: #0969da;
  text-decoration: underline;
  text-underline-offset: 2px;
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
    <div class="pipeline-item"><div class="item-dot"></div><div class="item-text">Ознакомиться с актуальным <a href="/community/roadmap/">роадмапом</a> Gonka, понять приоритеты сообщества и утверждённые направления развития сети — это поможет сформулировать идею, которая соответствует текущим целям экосистемы и имеет наибольшие шансы на поддержку.</div></div>
    <div class="pipeline-item"><div class="item-dot"></div><div class="item-text">Изучить <a href="/proposals/proposals/">прошедшие пропозалы</a> и собранные best practices, чтобы понять формат, требования и типичные ошибки. Обратите внимание на структуру: описание, бюджет, сроки, KPI и механизм отчетности — все успешные пропозалы следуют схожему шаблону.</div></div>
    <div class="pipeline-item"><div class="item-dot"></div><div class="item-text">Проанализировать текущие <a href="/proposals/proposals/">ончейн-пропозалы</a> и активные <a href="/proposals/preproposals/">препропозалы</a>, чтобы избежать дублирования и найти синергию. Возможно, ваша идея уже частично реализуется или может быть объединена с другой инициативой.</div></div>
    <div class="pipeline-item"><div class="item-dot"></div><div class="item-text">Просмотреть <a href="/community/discussion/">GitHub Discussions</a>, <a href="/community/issues/">Issues</a> и закрытые пропозалы — часто там уже есть частичные решения, обсуждения похожих идей или ценный фидбек от сообщества, который можно учесть заранее.</div></div>
    <div class="pipeline-item"><div class="item-dot"></div><div class="item-text">Ознакомиться с рекомендациями профильных комитетов: <a href="/community/governance%20support%20committee/">GSC</a> (процесс управления), <a href="/community/gonka%20restitution%20committee/">GRC</a> (реституция и компенсации), <a href="/community/go-to-market%20committee/">GTM</a> (маркетинг и рост). Учёт их требований на раннем этапе ускоряет прохождение следующих стадий.</div></div>
    <div class="pipeline-item"><div class="item-dot"></div><div class="item-text">Заполнить анкету в Google Forms (ссылка — в описании Telegram-канала сообщества) — это запустит формальный процесс обсуждения: будет создан препропозал на <a href="https://gonka.vote">gonka.vote</a>, а также выделен Telegram-чат для живого диалога с сообществом и комитетами. Без анкеты пропозал не попадает в официальный пайплайн. Все активные препропозалы публикуются на странице <a href="/proposals/preproposals/">Pre-Proposals</a>.</div></div>
  </div>

  <div class="pipeline-stage">
    <div class="stage-header">
      <div class="stage-node"></div>
      <div class="stage-title">Обсуждение</div>
    </div>
    <div class="pipeline-item"><div class="item-dot"></div><div class="item-text">Подготовить и провести презентацию пропозала и команды для сообщества — чётко обозначить цели, бюджет, сроки и ожидаемый результат. Хорошая презентация — основа доверия; примеры можно найти среди <a href="/proposals/preproposals/">прошедших препропозалов</a>.</div></div>
    <div class="pipeline-item"><div class="item-dot"></div><div class="item-text">Вести живое обсуждение на vote-портале <a href="https://gonka.vote">gonka.vote</a> и в выделенном Telegram-чате совместно с представителями <a href="/community/governance%20support%20committee/">комитетов</a>, хостами и активными участниками сообщества. Все вопросы и ответы публичны и остаются в истории для последующих пропозалов.</div></div>
    <div class="pipeline-item"><div class="item-dot"></div><div class="item-text">Организовать и провести AMA-сессию (Ask Me Anything), где любой член сообщества может задать вопросы команде и получить прямые ответы. Это обязательный этап для крупных или спорных пропозалов, помогающий снять неопределённость до голосования.</div></div>
    <div class="pipeline-item"><div class="item-dot"></div><div class="item-text">По итогам обсуждения профильные комитеты выносят заключение и дают рекомендации по доработке: корректировка суммы, сроков, формата подачи и других параметров пропозала. Заключения публикуются в репозитории и на <a href="https://gonka.vote">gonka.vote</a>.</div></div>
  </div>

  <div class="pipeline-stage">
    <div class="stage-header">
      <div class="stage-node"></div>
      <div class="stage-title">Голосование</div>
    </div>
    <div class="pipeline-item"><div class="item-dot"></div><div class="item-text">Комитет оказывает техническую помощь в подготовке финальной версии пропозала — помогает выверить параметры, форматирование, перевод на английский и соответствие стандартам ончейн-голосования. Цель — минимизировать ошибки, которые могут привести к отклонению или техническим проблемам при исполнении.</div></div>
    <div class="pipeline-item"><div class="item-dot"></div><div class="item-text">Все необходимые документы, заключения комитетов, записи AMA-встреч и презентации публикуются в едином пространстве для ознакомления хостами перед голосованием. Хосты — ключевые стейкхолдеры — голосуют своими токенами, поэтому прозрачность на этом этапе критична. Примеры опубликованных пропозалов — в <a href="/proposals/proposals/">архиве</a>.</div></div>
    <div class="pipeline-item"><div class="item-dot"></div><div class="item-text">Если пропозал появился на голосовании без предварительного обсуждения (без заполнения анкеты), члены сообщества самостоятельно создают анкету retroactively. Такой пропозал может быть отклонён или отправлен на доработку, если комитеты не успевают провести полный анализ.</div></div>
  </div>

  <div class="pipeline-stage">
    <div class="stage-header">
      <div class="stage-node"></div>
      <div class="stage-title">Отчётность</div>
    </div>
    <div class="pipeline-item"><div class="item-dot"></div><div class="item-text">В случае прохождения пропозала команда совместно с комитетами составляет детальный график отчётности: дедлайны, KPI, мейлстоуны и формат предоставления результатов. График публикуется вместе с финальной версией пропозала и доступен всем участникам сети. Примеры отчётов можно найти на странице <a href="/proposals/community%20pool/">Community Pool</a> (раздел Bounty Distribution).</div></div>
    <div class="pipeline-item"><div class="item-dot"></div><div class="item-text">Комитеты регулярно контролируют сроки, оценивают качество и содержание отчётов, и при необходимости выносят резолюцию — особенно в случаях отзывных пропозалов (когда средства выделяются частями и каждая следующая транша требует подтверждения), подозрений на скам или репутационных рисков для сети. Комитет <a href="/community/gonka%20restitution%20committee/">GRC</a> отвечает за компенсационные механизмы, <a href="/community/governance%20support%20committee/">GSC</a> — за соблюдение процедур.</div></div>
  </div>

</div>

</div>
