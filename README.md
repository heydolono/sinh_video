# Синхронное воспроизведение видео

## Описание
Этот проект представляет собой приложение для синхронного воспроизведения нескольких видеопотоков в реальном времени с добавлением временных меток и текстовых меток на каждом кадре. Кадры из разных видео отображаются на одном экране в разных углах.

Проект состоит из двух частей:
1. **Серверная часть**: Отправляет кадры видео в реальном времени через сокеты.
2. **Клиентская часть**: Принимает эти кадры и отображает их в графическом интерфейсе с использованием Tkinter и OpenCV.

### Стек технологий
- Python 3.x
- OpenCV
- Tkinter
- ZeroMQ (zmq)
- Pillow (PIL)

## Запуск
### 1. Клонирование репозитория

```
git clone https://github.com/heydolono/sync_video.git
```

```
cd sync_video
```

### 2. Запуск сервера

```
cd server
python main.py
```

### 3. Запуск клиента

```
cd client
python main.py
```

## Разработчик
- [Максим Колесников](https://github.com/heydolono)
- [Резюме](https://career.habr.com/heydolono)