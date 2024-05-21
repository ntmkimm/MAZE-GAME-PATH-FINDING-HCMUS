def read_maze_from_txt(filename):
    try:
        with open(filename, 'r') as file:
            rows, cols = map(int, file.readline().split())  # Đọc kích thước hàng và cột
            start = file.readline()
            end = file.readline()
            current_y = file.readline().split()
            current_x = file.readline().split()
            grid_cells = []
            for _ in range(rows):
                for _ in range(cols):
                    row_values = file.readline().split()
                    row_bool_values = [eval(cell) for cell in row_values]
                    grid_cells.append(row_bool_values)

            return rows, cols, start, end, current_y, current_x, grid_cells
    except FileNotFoundError:
        print(f"Tệp '{filename}' không tồn tại.")
        return None
    
rows, cols, start, end, current_y, current_x, grid_cells = read_maze_from_txt('maze1.txt')

if grid_cells:
    print(f"Kích thước hàng: {rows}, cột: {cols}")
    print(f"ô bắt đầu{start}ô kết thúc{end}")
    print(f"vị trí hiện tại: {current_y},{current_x}")
    print("Dữ liệu của các ô lưới:")
    for row in grid_cells:
        print(row)
        
        
import pandas as pd
def read_leader(file_path):
    # Đọc file Excel
    df = pd.read_excel(file_path)
    df.index = range(1, len(df) + 1)
    print(df)
read_leader('leaderboard.xlsx')
