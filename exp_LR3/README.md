# Лабораторная работа 3: Основы работы с n8n

## Цель работы

Создание pipeline для парсинга статей на habr.com, обработки их с помощью ИИ, а
также отправки результата на почту.

Создать полностью автоматический workflow в n8n, который:

1. Принимает HTTP-запрос с датой
2. Парсит статьи с Habr за указанную дату
3. Обрабатывает их с помощью GigaChat для создания дайджеста
4. Отправляет результат на email

## Задачи работы

1. Установить и настроить self-hosted n8n с Python/JavaScript раннерами
2. Создать workflow для парсинга Habr с фильтрацией по дате
3. Настроить интеграцию с GigaChat API (получение токена, отправка запросов)
4. Реализовать 6 типов промптов для LLM
5. Настроить отправку дайджеста на email

---

## Выполненные шаги

### Установка и настройка n8n

<img width="1798" height="933" alt="image" src="https://github.com/user-attachments/assets/2416ffa7-6512-4585-b534-bdb01784ed4a" />


<img width="1193" height="150" alt="image" src="https://github.com/user-attachments/assets/a97621aa-546e-4589-b050-0c105e7d750b" />


### Создание и настройка основного Workflow

<img width="415" height="293" alt="image" src="https://github.com/user-attachments/assets/bdacbce8-4e33-4d81-a0d1-3b228f169a57" />

### Формирование промптов к GigaChat 

```
if (promptType === "role") {
    userPrompt = "Ты профессиональный аналитик новостей по искусственному интеллекту. Сделай дайджест статей за " + (filterDate || "сегодня") + ":\n\n" + JSON.stringify(articles, null, 2) + "\n\nФормат: Markdown. Для каждой статьи напиши заголовок, автора и краткую суть.";
}
else if (promptType === "zero-shot") {
    userPrompt = "Сделай краткий дайджест этих статей: " + JSON.stringify(articles);
}
else if (promptType === "one-shot") {
    userPrompt = "Пример дайджеста:\n---\n**Новая нейросеть** (автор: AI_News) → Суть: вышла новая версия ChatGPT\n---\nТеперь сделай дайджест для:\n" + JSON.stringify(articles, null, 2);
}
else if (promptType === "few-shot") {
    userPrompt = "Пример 1:\n**ИИ в медицине** (автор: MedNews) → Идея: диагностика рака\n\nПример 2:\n**Роботы-курьеры** (автор: RoboNews) → Идея: доставка за 15 минут\n\nПример 3:\n**Нейросеть рисует** (автор: ArtNews) → Идея: генерация изображений\n\nТеперь сделай дайджест по этому же шаблону:\n" + JSON.stringify(articles, null, 2);
}
else if (promptType === "chain-of-thought") {
    userPrompt = "Пошагово:\nШаг 1: Определи главную тему каждой статьи.\nШаг 2: Напиши одно предложение с сутью.\nШаг 3: Объедини всё в связный текст.\n\nСтатьи:\n" + JSON.stringify(articles, null, 2);
}
else if (promptType === "negative") {
    userPrompt = "Сделай дайджест. Запрещено использовать слова: 'данный', 'вышеупомянутый', 'в статье рассказывается'. Не пиши вводных фраз. Статьи:\n" + JSON.stringify(articles, null, 2);
}
else {
```

### Отправка на email

Не получилось реализовать из-за недоступности и недопонимания сервесов, были испробованы такие сервисы: VK WorkSpace и Mailtrap 

В первом не получилось такие пароль и user для подключения. А для второго нужен впн на устройстве, где запущен контейнер (впн не работает)

---

### Итоговый результат

<img width="1743" height="781" alt="image" src="https://github.com/user-attachments/assets/b3173526-aaac-4e2d-aa97-a2b1f4c20097" />
