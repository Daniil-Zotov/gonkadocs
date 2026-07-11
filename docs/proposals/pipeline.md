<style>
.pipeline-wrap {
  max-width: 880px;
  margin: 0 auto;
  padding: 2rem 1.5rem 4rem;
  font-family: var(--md-text-font-family, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif);
  color: var(--md-default-fg-color, #24292f);
}

.pipeline-intro {
  font-size: 1.05rem;
  line-height: 1.65;
  color: var(--md-default-fg-color--light, #57606a);
  margin-bottom: 3rem;
  max-width: 640px;
}

.pipeline-timeline {
  position: relative;
  padding-left: 48px;
}

.pipeline-timeline::before {
  content: "";
  position: absolute;
  left: 14px;
  top: 8px;
  bottom: 8px;
  width: 2px;
  background: var(--md-default-fg-color--lightest, #d1d9e0);
  border-radius: 2px;
}

.pipeline-stage {
  position: relative;
  margin-bottom: 3.5rem;
}

.pipeline-stage:last-child {
  margin-bottom: 0;
}

.pipeline-node {
  position: absolute;
  left: -48px;
  top: 4px;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #fff;
  border: 3px solid var(--md-accent-fg-color, #0969da);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
  box-shadow: 0 0 0 4px var(--md-default-bg-color, #fff);
}

.pipeline-node::after {
  content: "";
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--md-accent-fg-color, #0969da);
}

.pipeline-card {
  background: var(--md-code-bg-color, #f6f8fa);
  border: 1px solid var(--md-default-fg-color--lightest, #d1d9e0);
  border-radius: 12px;
  padding: 1.5rem 1.75rem;
  transition: box-shadow 0.2s ease, transform 0.2s ease;
}

.pipeline-card:hover {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  transform: translateY(-2px);
}

.pipeline-title {
  font-size: 1.15rem;
  font-weight: 700;
  margin: 0 0 1rem;
  letter-spacing: -0.02em;
  color: var(--md-default-fg-color, #24292f);
}

.pipeline-list {
  margin: 0;
  padding: 0;
  list-style: none;
}

.pipeline-list li {
  position: relative;
  padding-left: 1.25rem;
  margin-bottom: 0.6rem;
  font-size: 0.92rem;
  line-height: 1.55;
  color: var(--md-default-fg-color, #24292f);
}

.pipeline-list li:last-child {
  margin-bottom: 0;
}

.pipeline-list li::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0.55rem;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--md-accent-fg-color, #0969da);
  opacity: 0.6;
}

@media (max-width: 600px) {
  .pipeline-timeline {
    padding-left: 36px;
  }
  .pipeline-node {
    left: -36px;
    width: 22px;
    height: 22px;
    border-width: 2px;
  }
  .pipeline-node::after {
    width: 8px;
    height: 8px;
  }
  .pipeline-card {
    padding: 1.25rem;
  }
}
</style>

<div class="pipeline-wrap">

<div class="pipeline-intro">
Полный цикл жизни предложения от идеи до отчётности. Каждый этап прозрачен, проверяем сообществом и задокументирован.
</div>

<div class="pipeline-timeline">

  <div class="pipeline-stage">
    <div class="pipeline-node"></div>
    <div class="pipeline-card">
      <h3 class="pipeline-title">Подготовка</h3>
      <ul class="pipeline-list">
        <li>Изучение роадмапа</li>
        <li>Изучение прошедших пропозалов (или списка бестпрактис)</li>
        <li>Изучение текущих пропозалов ончейн / превот</li>
        <li>Изучение GitHub / Issues / Proposals</li>
        <li>Изучение рекомендаций комитетов</li>
        <li>Заполнение анкеты Google запустит процесс обсуждения — создаст препропозал на gonka.vote / gonkadocs.com, создаст Telegram-чат</li>
      </ul>
    </div>
  </div>

  <div class="pipeline-stage">
    <div class="pipeline-node"></div>
    <div class="pipeline-card">
      <h3 class="pipeline-title">Обсуждение</h3>
      <ul class="pipeline-list">
        <li>Презентация пропозала и команды</li>
        <li>Живое обсуждение на vote-портале и в Telegram-чате с представителями комитетов, хостами и активными членами сообщества</li>
        <li>Проведение AMA-сессии</li>
        <li>Итогом обсуждения станет заключение профильных комитетов, рекомендации по доработке пропозала (суммы, сроки, формат пропозала и прочее)</li>
      </ul>
    </div>
  </div>

  <div class="pipeline-stage">
    <div class="pipeline-node"></div>
    <div class="pipeline-card">
      <h3 class="pipeline-title">Голосование</h3>
      <ul class="pipeline-list">
        <li>Комитет окажет помощь в технической части подготовки пропозала</li>
        <li>Разместит все необходимые документы, заключения, записи встреч в едином пространстве для ознакомления хостами</li>
        <li>В случае появления пропозала без предварительного обсуждения (заполнения анкеты) анкета будет создана членами сообщества для прохождения полной процедуры</li>
      </ul>
    </div>
  </div>

  <div class="pipeline-stage">
    <div class="pipeline-node"></div>
    <div class="pipeline-card">
      <h3 class="pipeline-title">Отчётность</h3>
      <ul class="pipeline-list">
        <li>В случае прохождения пропозала будет составлен график предоставления отчёта о проделанной работе, достижения KPI, прохождении мейлстоунов</li>
        <li>Комитеты будут контролировать сроки и оценивать содержание отчётов — будет вынесена резолюция (в случае отрывных пропозалов, скам, репутационных рисков и прочего)</li>
      </ul>
    </div>
  </div>

</div>

</div>
