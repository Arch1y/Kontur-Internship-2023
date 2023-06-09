# Kontur Internship 2023
## Описание проекта

Исходный код находится в директории ```src/lib/``` и представляет из себя Python ноутбук.

Обученный модели rubert-tiny2 находятся на [kaggle](https://www.kaggle.com/datasets/archiy/kontur2023). Модели обучались на тренировочном наборе данных, который разделялся на 5 частей для перекрестной проверки. Таким образом, получены 5 моделей, которые обучались на разных частях набора данных и проверялись на оставшейся.

В директории ```/data``` находится набор данных: тестовый и тренировочный.

Рассмотрены две метрики для оценки качества работы модели:
* Accuracy score - полное совпадение извлекаемой из текста фразы и искомой фразы.
* Jaccard score - мера сходства извлекаемой фразы и искомой фразы.

Обе метрики можно использовать для этой задачи, но, как мне показалось, использование Jaccard score легче в плане обучения модели, так как эта метрика не штрафует ее за неточные выделения нужной фразы. Так, к примеру, модель зачастую вместе с фразой выделяла и знак препинания в конце предложения, что сильно штрафуется Accuracy score, но дает меньший вклад в Jaccard score, поэтому EarlyStopping модели не срабатывает слишком рано.

## Анализ данных
В ходе предварительного анализа данных обнаружено:
* Распределение "классов" (столбец label) между данными примерно одинаково. Для тренировочного и тестового наборов.
* Извлекаемая фраза представляет собой короткое предложение от 0 до ~40 слов.
* Ключевые слова для извлекаемой фразы отличаются для двух "классов", что позволяет их разделить при помощи различных методов.
* Начало ответа имеет крайне несбалансированное распределение, большое число текстов не содержат искомого ответа.
Программа для анализа данных находился в папке ```src/lib/```.

## Рассматриваемый подход к решению задачи
Одним из возможных подходов для решения этой задачи является использование нейронных сетей, в частности, BERT-base моделей, которые используются в задачах NLP (обработки естественного языка). Как оказалось, таких моделей не очень много для русского языка и их еще меньше для обработки таких больших текстов, так что мой выбор остановился на [rubert-tiny2](https://huggingface.co/cointegrated/rubert-tiny2) моделе. Эта модель представляет собой уменьшенную копию BERT модели, которая содержит всего 3 скрытых слоя и поддерживает большие последовательности входных токенов, до 2048. Модель rubert-tiny2 получена путем дистилляция более сложных и больших моделей, что позволяет получать хорошие результаты, используя меньшие вычислительные ресурсы. <br>
После выбора модели задача рассматривалась как Q&A задача, где в качестве вопроса подавался label, поиск производился по всему тексту.

Особенности решения задачи: 
* Тренировочный набор данных разделялся на обучающий и валидационный в соотношении 4 к 1.
* В качестве функции потерь пробовались CrossEntropyLoss и KLDivLoss, последняя показала лучшие результаты Accuracy и Jaccard, поэтому и вошла в финальное решение.
* Использование "Soft targets". В качестве меток ответа использовалась не просто последовательность: [0, 0, 0, 1, 0, 0, 0], где 1 - начало ответа, а некая сглаженная функции: [0.2, 0.4, 0.8, 1, 0, 0, 0]. Такая функция поощряет более близкие ответы и штрафует совсем уж неправильные. Такой подход позволил выиграть еще 5% точности на валидационном наборе.
* На выходе BERT модели использовалось большое значение Dropout=50%, причем оно дублировалось до 5 раз, а значения усреднялись. [Такой подход](https://arxiv.org/abs/1905.09788) позволял получить большую точность и не переобучать выход нейронной сети, так как усложнял запоминание тренировочного набора при обучении.
* В качестве методо оптимизации нейронной сети использовалась AdamW с линейным затуханием learning rate к концу эпохи. Поверх него использовался SWA для получения более лучшей точности на валидационном наборе.
* Для предотвращения переобучения использовался EarlyStopping по метрикам Accuracy/Jaccard.
* После обучения 5 моделей на разных частях тренировочного/валидационного набора данных, их ответы усреднялись при получении меток для тестового набора.

## Запуск
Для запуска понадобится файл ```utils.py```, в котором находятся вспомогательные функции для работы программы. В папке ```src/lib/``` находятся две папки с двумя разными метриками, можно посмотреть оба, но в качестве финального решения я использовал метрику **Accuracy**, которое расположено в папке ```src/lib/BERT_accuracy_metric/predictions.json```.
Все программы написаны на Kaggle и работали на их машинах. Для обучения использовалась GPU P100.

## Заключение
Полученная модель позволяет получить Accuracy 75% и Jaccard 92% на валидационном наборе данных. Однако, после обучения и проверки моделей на всем тренировочном наборе обнаружено, что помимо необходимого фрагмента текста, модель зачастую выделяет еще и знаки после фрагмента:",/:" или целые слова:"цены, контракта, гарантии и т.д.", которые, как мне кажется, не сильно влияют на фрагмент текста, но существенно снижают Accuracy. Из возможных решений этой проблемы могу предложить удалять эти знаки препинания или слова в конце предложения при помощи rstrip(' ,/: контракта гарантии'), но из-за того, что я не знаю какие метки на тестовом наборе, то я не стал этого делать в ответе на задание. <br>
Другим вариантом решения этой проблемы было бы удаление вообще всех знаков препинания во всем тексте, кроме извлекаемого, что уменьшило бы его длину и моделе было бы проще его понять, но я не успел это реализовать. <br>
Эта была интересная и сложная задача, так как раньше я никогда не работал с NLP задачами и у меня мало опыта работы с PyTorch библиотекой. Однако, как мне кажется, получилось неплохое решение, которое позволило получить хороший опыт в этой области на примере такой необычной задачи.