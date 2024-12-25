import os
import pandas as pd

class PriceMachine:
    def __init__(self):
        self.data = pd.DataFrame()

    def load_prices(self, directory):
        all_data = []

        for filename in os.listdir(directory):
            if 'price' in filename and filename.endswith('.csv'):
                file_path = os.path.join(directory, filename)
                df = pd.read_csv(file_path)

                df.columns = df.columns.str.lower()
                df.rename(columns={
                    'название': 'наименование',
                    'продукт': 'наименование',
                    'товар': 'наименование',
                    'наименование': 'наименование',
                    'цена': 'цена',
                    'розница': 'цена',
                    'фасовка': 'вес',
                    'масса': 'вес',
                    'вес': 'вес'
                }, inplace=True)

                df = df[['наименование', 'цена', 'вес']].dropna()
                df['файл'] = filename
                all_data.append(df)

        self.data = pd.concat(all_data, ignore_index=True)
        self.data['цена за кг'] = self.data['цена'] / self.data['вес']

    def find_text(self, search_text):
        filtered_data = self.data[self.data['наименование'].str.contains(search_text, case=False)]
        filtered_data = filtered_data.sort_values(by='цена за кг')
        return filtered_data

    def export_to_html(self, output_file):
        self.data.to_html(output_file, index=False)

if __name__ == "__main__":
    pm = PriceMachine()
    pm.load_prices('pricelist')
    while True:
        search_text = input("Введите текст для поиска (или 'exit' для выхода): ")
        if search_text.lower() == 'exit':
            print("Работа программы завершена.")
            break

        results = pm.find_text(search_text)
        if not results.empty:
            # Сбрасываем индексы и начинаем с 1
            results = results.reset_index(drop=True)
            results.index += 1  # Начинаем с 1

            # Добавляем столбец "№" и переименовываем другие столбцы
            results.insert(0, "№", results.index)  # Вставляем номер в начало
            results.columns = ["№", "Наименование", "Цена", "Вес", "Файл", "Цена за кг"]

            # Печатаем результаты с заголовками
            print(results.to_string(index=False, justify='left'))  # Убираем индексы в выводе и выравниваем по левому краю

        else:
            print("Товары не найдены.")

    # Экспорт данных в HTML
    pm.export_to_html('output.html')
