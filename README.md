# Thuật toán Deutsch-Jozsa sử dụng Qiskit
Thuật toán Deutsch-Jozsa là một thuật toán lượng tử dùng để xác định tính chất của các hàm Boolean. Cụ thể, nó có thể xác định xem một hàm số cho trước là hàm hằng (constant) hay hàm cân bằng (balanced). Trong đó, hàm hằng luôn trả về cùng một kết quả đầu ra (hoặc 0 hoặc 1), còn hàm cân bằng sẽ trả về kết quả bằng 0 cho một nửa số lượng đầu vào và bằng 1 cho nửa còn lại.

Thuật toán này giải quyết bài toán xác định tính chất của hàm Boolean chỉ với một lần truy vấn (single query), trong khi một thuật toán cổ điển sẽ phải mất ít nhất $2^{n-1} + 1$ lần truy vấn (với $n$ là số lượng bit đầu vào).

Đây là một trong những ví dụ đầu tiên về thuật toán lượng tử đem lại tốc độ tăng trưởng vượt bậc theo hàm mũ (exponential speedup) so với các thuật toán cổ điển tương đương. Dưới đây là sơ đồ mạch của thuật toán Deutsch-Jozsa áp dụng cho đầu vào gồm 3 Qubit:
```
     ┌───┐      ░ ┌─────────────────┐ ░ ┌───┐ ░ ┌─┐     
q_0: ┤ H ├──────░─┤0                ├─░─┤ H ├─░─┤M├───
     ├───┤      ░ │                 │ ░ ├───┤ ░ └╥┘┌─┐
q_1: ┤ H ├──────░─┤1                ├─░─┤ H ├─░──╫─┤M├
     ├───┤┌───┐ ░ │                 │ ░ └───┘ ░  ║ └╥┘
q_2: ┤ X ├┤ H ├─░─┤2 A Oracle Block ├─░───────░──╫──╫─
     └───┘└───┘ ░ │  That We Don't  │ ░       ░  ║  ║ 
c_0: ═════════════╡0     Know       ╞════════════╩══╬═
                  │                 │               ║ 
c_1: ═════════════╡1                ╞═══════════════╩═
                  └─────────────────┘                 
```

## Usage
Khuyến khích sử dụng môi trường ảo (virtual environment) để chạy chương trình. Để cài đặt các thư viện phụ thuộc cần thiết, thực hiện lệnh sau:
```bash
$ pip3 install -r requirements.txt
```

Để khởi chạy giao diện chương trình, thực hiện lệnh sau:
```bash
$ python3 djalgorithm.py
```

## Application Interface
```python
from djalgorithm import DJAlgorithm

n = 4  # Số lượng qubit.

# Tạo một hàm số để kiểm tra.
# some_function = DJAlgorithm.give_a_constant_function(n)
some_function = DJAlgorithm.give_a_balanced_function(n)

# Sử dụng thuật toán Deutsch-Jozsa để xác định xem đó là hàm gì.
result = DJAlgorithm.simulate(some_function)

# In kết quả ra màn hình.
print(result["result"])
```