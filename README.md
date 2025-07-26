<h1 align="center">Phasalo Bot Template</h1>
<p align="center">
Полпути к идеальному боту. Красиво, как всегда
</p><p align="center">
<img src="https://img.shields.io/badge/made%20by-CSSSensei,%20MaxMavr-439900" >
<img src="https://img.shields.io/badge/Phasalopedia-84D300">
<img src="https://img.shields.io/badge/version-if%20n%20==%202-D1F24E">
</p>

<p align="center" style="background-color: red; color: white;">

</p>

Так много лет нас просили показать, как же мы пишем таких охуительных ботов. Вот встречайте — все наши знания в одном репозитории!
Это не просто шаблон, а выжимка из сотен часов продакшена, боли и любви к красивому коду.

# Быстрый старт
### Пошаговая инструкция для самых маленьких.

## Вариант 1. Если хотите работать через форк (рекомендуется)
### 1. Создайте форк репозитория
— Нажмите кнопку `Fork` в правом верхнем углу страницы репозитория

— Выберите свой аккаунт как место назначения

### 2. Клонируйте СВОй форк
```bash
git clone https://github.com/ВАШ_АККАУНТ/PhasaloBotTemplate.git my-project
cd my-project
```
— Замените `my-project` на имя директории, куда хотите всё сохранить.

### 3. Настройте связь с оригиналом (опционально)
Чтобы получать обновления из исходного шаблона:
```bash
git remote add upstream https://github.com/CSSSensei/PhasaloBotTemplate.git
```

### 4. Проверьте репозитории
```bash
git remote -v
```
**Должно показать:**

`origin` - ваш форк (на чтение/запись)

`upstream` - оригинал (только для чтения)


## Вариант 2. Независимый проект

### 1. Клонируем репозиторий
```bash
git clone https://github.com/CSSSensei/PhasaloBotTemplate.git my-project
```
— Замените `my-project` на имя директории, куда хотите всё сохранить.

### 2. Переходим в проект и удаляем *origin*
```bash
cd my-project
git remote remove origin
```

### 3. Проверяем, что удалённые ссылки исчезли
```bash
git remote -v
```
— Должно быть пусто — значит, всё получилось.

## Как обновляться из оригинала (для форка)
### Если вы выбрали Вариант 1 и хотите получить свежие изменения:
```bash
git fetch upstream
git merge upstream/main
# ИЛИ для перезаписи всех изменений:
git reset --hard upstream/main
```

### Пользуйтесь!
Теперь вы можете:

- Свободно изменять код в своем форке (`git push origin main`)
- Создавать новые ветки для разработки
- Предлагать изменения в оригинал через Pull Request


<p align="center">
  <img src="https://yan-toples.ru/Phasalo/phasalopedia_logo.png" width="1500" alt="Phasalo">
</p>

<p align="center">
Phasalopedia<br>
<i>Делаем красиво!</i><br><br>
2025
</p>
