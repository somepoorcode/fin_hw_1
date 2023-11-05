import csv
import os
import random


class CSVFileProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self):
        with open(self.file_path, 'r') as file:
            reader = csv.DictReader(file, delimiter=',')
            data = [row for row in reader]
        return data

    def show(self, output_type='top', num_rows=5, separator=','):
        if output_type == 'top':
            output_data = self.data[:num_rows]
        elif output_type == 'bottom':
            output_data = self.data[-num_rows:]
        elif output_type == 'random':
            output_data = random.sample(self.data, num_rows)
        else:
            print("Invalid output type. Only 'top', 'bottom', or 'random' are allowed.")
            return

        for row in output_data:
            row_str = separator.join(row.values())
            print(row_str)

    def info(self):
        num_rows = len(self.data)
        num_columns = len(self.data[0])
        print(f"Number of rows and columns with data: {num_rows}x{num_columns}")

        field_info = {}
        for column_name in self.data[0].keys():
            non_empty_values = [row[column_name] for row in self.data if row[column_name]]
            field_info[column_name] = {
                'Qty': len(non_empty_values),
                'Type': type(next(iter(non_empty_values), None)).__name__,
            }

        for field, info in field_info.items():
            print(f"{field} {info['Qty']} {info['Type']}")

    def del_nan(self):
        self.data = [row for row in self.data if all(row.values())]

    def make_ds(self):
        learning_data = random.sample(self.data, int(0.7 * len(self.data)))
        testing_data = [row for row in self.data if row not in learning_data]

        if not os.path.exists('workdata'):
            os.makedirs('workdata')
        if not os.path.exists('workdata/Learning'):
            os.makedirs('workdata/Learning')
        if not os.path.exists('workdata/Testing'):
            os.makedirs('workdata/Testing')

        learning_file_path = os.path.join('workdata/Learning', 'train.csv')
        testing_file_path = os.path.join('workdata/Testing', 'test.csv')

        with open(learning_file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.data[0].keys(), delimiter=',')
            writer.writeheader()
            writer.writerows(learning_data)

        with open(testing_file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.data[0].keys(), delimiter=',')
            writer.writeheader()
            writer.writerows(testing_data)


if __name__ == "__main__":
    file_path = 'data.csv'
    processor = CSVFileProcessor(file_path)
    processor.show(output_type='top', num_rows=5, separator=',')
    processor.info()
    processor.del_nan()
    processor.make_ds()