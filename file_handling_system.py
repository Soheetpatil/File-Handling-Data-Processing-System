import csv
import os
from datetime import datetime

def read_file(file_path):
    _, ext = os.path.splitext(file_path)
    data = []
    if ext.lower() == '.csv':
        with open(file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    elif ext.lower() == '.txt':
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                data.append({'line_number': line_num, 'content': line.strip()})
    return data

def display_data(data):
    if not data:
        print("No data to display.")
        return
    print("\n" + "="*80)
    if 'line_number' in data[0]:
        for item in data:
            print(f"{item['line_number']}: {item['content']}")
    else:
        headers = list(data[0].keys())
        print(" | ".join(headers))
        print("-"*80)
        for row in data:
            print(" | ".join([str(row[h]) for h in headers]))
    print("="*80 + "\n")

def write_file(file_path, data, mode='w'):
    _, ext = os.path.splitext(file_path)
    if ext.lower() == '.csv':
        if data:
            headers = list(data[0].keys())
            with open(file_path, mode, newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                if mode == 'w':
                    writer.writeheader()
                writer.writerows(data)
    elif ext.lower() == '.txt':
        with open(file_path, mode, encoding='utf-8') as file:
            for item in data:
                if 'content' in item:
                    file.write(item['content'] + '\n')
                else:
                    file.write(str(item) + '\n')

def filter_data(data, field, value):
    if not data or field not in data[0]:
        return []
    return [row for row in data if str(row[field]).lower() == str(value).lower()]

def sort_data(data, field, numeric=False):
    if not data or field not in data[0]:
        return []
    if numeric:
        return sorted(data, key=lambda x: float(x[field]))
    else:
        return sorted(data, key=lambda x: str(x[field]).lower())

def search_data(data, keyword):
    results = []
    for row in data:
        for key, value in row.items():
            if keyword.lower() in str(value).lower():
                results.append(row)
                break
    return results

def calculate_summaries(data):
    if not data:
        return {}
    summaries = {
        'total_records': len(data)
    }
    numeric_fields = []
    headers = list(data[0].keys())
    for header in headers:
        try:
            float(data[0][header])
            numeric_fields.append(header)
        except ValueError:
            continue
    for field in numeric_fields:
        values = []
        for row in data:
            try:
                values.append(float(row[field]))
            except ValueError:
                pass
        if values:
            summaries[f'{field}_average'] = sum(values) / len(values)
            summaries[f'{field}_max'] = max(values)
            summaries[f'{field}_min'] = min(values)
            summaries[f'{field}_count'] = len(values)
    return summaries

def main():
    current_data = []
    current_file = ""
    
    while True:
        print("\n" + "="*50)
        print("  File Handling & Data Processing System")
        print("="*50)
        print("1. Read File (CSV/TXT)")
        print("2. Display Current Data")
        print("3. Filter Records")
        print("4. Sort Data")
        print("5. Search Records")
        print("6. Calculate Summaries")
        print("7. Write/Export Data")
        print("8. Exit")
        print("="*50)
        
        choice = input("Enter your choice (1-8): ")
        
        try:
            if choice == '1':
                file_path = input("Enter file path: ")
                if not os.path.exists(file_path):
                    raise FileNotFoundError("File not found!")
                current_data = read_file(file_path)
                current_file = file_path
                print(f"Successfully read file: {file_path}")
                display_data(current_data)
            
            elif choice == '2':
                display_data(current_data)
            
            elif choice == '3':
                if not current_data:
                    print("No data loaded! Please read a file first.")
                    continue
                if 'line_number' not in current_data[0]:
                    headers = list(current_data[0].keys())
                    print(f"Available fields: {', '.join(headers)}")
                field = input("Enter field name to filter: ")
                if 'line_number' not in current_data[0] and field not in current_data[0]:
                    print(f"Error: Field '{field}' not found!")
                    continue
                value = input("Enter value to filter by: ")
                filtered = filter_data(current_data, field, value)
                print(f"\nFiltered results ({len(filtered)} records):")
                display_data(filtered)
                save = input("Save filtered results? (y/n): ").lower()
                if save == 'y':
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    out_file = input(f"Enter output file path (default: filtered_{timestamp}.csv): ") or f"filtered_{timestamp}.csv"
                    write_file(out_file, filtered)
                    print(f"Results saved to {out_file}")
            
            elif choice == '4':
                if not current_data:
                    print("No data loaded! Please read a file first.")
                    continue
                if 'line_number' not in current_data[0]:
                    headers = list(current_data[0].keys())
                    print(f"Available fields: {', '.join(headers)}")
                field = input("Enter field name to sort by: ")
                if 'line_number' not in current_data[0] and field not in current_data[0]:
                    print(f"Error: Field '{field}' not found!")
                    continue
                numeric = input("Sort numerically? (y/n): ").lower() == 'y'
                sorted_data = sort_data(current_data, field, numeric)
                print("\nSorted results:")
                display_data(sorted_data)
                save = input("Save sorted results? (y/n): ").lower()
                if save == 'y':
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    out_file = input(f"Enter output file path (default: sorted_{timestamp}.csv): ") or f"sorted_{timestamp}.csv"
                    write_file(out_file, sorted_data)
                    print(f"Results saved to {out_file}")
            
            elif choice == '5':
                if not current_data:
                    print("No data loaded! Please read a file first.")
                    continue
                keyword = input("Enter search keyword: ")
                results = search_data(current_data, keyword)
                print(f"\nSearch results ({len(results)} records):")
                display_data(results)
            
            elif choice == '6':
                if not current_data:
                    print("No data loaded! Please read a file first.")
                    continue
                summaries = calculate_summaries(current_data)
                print("\nData Summaries:")
                print("="*40)
                for key, value in summaries.items():
                    if isinstance(value, float):
                        print(f"{key}: {value:.2f}")
                    else:
                        print(f"{key}: {value}")
                print("="*40)
            
            elif choice == '7':
                if not current_data:
                    print("No data to save!")
                    continue
                out_path = input("Enter output file path: ")
                mode = input("Write mode (w=overwrite, a=append): ").lower()
                if mode not in ['w', 'a']:
                    mode = 'w'
                write_file(out_path, current_data, mode)
                print(f"Data written to {out_path}")
            
            elif choice == '8':
                print("Thank you for using the system!")
                break
            
            else:
                print("Invalid choice! Please try again.")
        
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except PermissionError:
            print("Error: Permission denied!")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
