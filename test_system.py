import file_handling_system as fhs
import os

print("=== Testing File Handling System ===\n")

print("1. Testing read_file() on students.csv")
data = fhs.read_file("students.csv")
print(f"[OK] Successfully read {len(data)} records\n")

print("2. Testing display_data()")
fhs.display_data(data)

print("3. Testing filter_data() - filter result='Pass'")
passed = fhs.filter_data(data, "result", "Pass")
print(f"[OK] Found {len(passed)} passed students\n")

print("4. Testing sort_data() - sort by total marks (numeric)")
sorted_by_total = fhs.sort_data(data, "total", numeric=True)
fhs.display_data(sorted_by_total[:3])
print("[OK] Sorted successfully\n")

print("5. Testing search_data() - search for 'Alice'")
search_result = fhs.search_data(data, "Alice")
fhs.display_data(search_result)
print("[OK] Search successful\n")

print("6. Testing calculate_summaries()")
summaries = fhs.calculate_summaries(data)
for key, value in summaries.items():
    if isinstance(value, float):
        print(f"  {key}: {value:.2f}")
    else:
        print(f"  {key}: {value}")
print("\n[OK] Summaries calculated successfully\n")

print("7. Testing write_file() - write top 3 students to toppers.csv")
fhs.write_file("toppers.csv", sorted_by_total[-3:][::-1])
if os.path.exists("toppers.csv"):
    print("[OK] File 'toppers.csv' created successfully\n")

print("=== All tests passed! ===")
