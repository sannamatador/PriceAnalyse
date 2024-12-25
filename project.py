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
                    'название': 'название',
                    'продукт': 'название',
                    'товар': 'название',
                    'наименование': 'название',
                    'цена': 'цена',
                    'розница': 'цена',
                    'фасовка': 'вес',
                    'масса': 'вес',
                    'вес': 'вес'
                }, inplace=True)

                df = df[['название', 'цена', 'вес']].dropna()
                df['файл'] = filename
                all_data.append(df)

        self.data = pd.concat(all_data, ignore_index=True)
        self.data['цена за кг'] = self.data['цена'] / self.data['вес']

    def find_text(self, search_text):
        filtered_data = self.data[self.data['название'].str.contains(search_text, case=False)]
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
            # Проверяем, сколько столбцов в DataFrame
            num_columns = results.shape[1]
            # Определяем заголовки в зависимости от количества столбцов
            headers = ["№", "Наименование", "Цена", "Вес", "Файл", "Цена за кг"][:num_columns]

            # Вывод результатов в виде таблицы
            print(results.to_string(index=True, header=headers))
        else:
            print("Товары не найдены.")

    # Экспорт данных в HTML
    pm.export_to_html('output.html')
