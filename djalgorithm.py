"""
Module này triển khai thuật toán Deutsch-Jozsa sử dụng Qiskit.
"""
import numpy as np
from qiskit import Aer
from qiskit import QuantumCircuit, assemble, transpile
from qiskit.circuit.instruction import Instruction


class DJAlgorithm:
    """Lớp này triển khai thuật toán Deutsch-Jozsa."""

    @staticmethod
    def simulate(oracle_block: QuantumCircuit) -> dict:
        """
        Chạy thuật toán Deutsch-Jozsa trên máy mô phỏng.

        :param oracle_block: Khối oracle để kiểm tra với thuật toán Deutsch-Jozsa.
        :return: Kết quả của thuật toán dưới dạng từ điển. Kiểm tra thuộc tính "result".
        """
        circuit = DJAlgorithm._construct_the_circuit(oracle_block)
        aer_sim = Aer.get_backend("aer_simulator")
        transpiled_dj_circuit = transpile(circuit, aer_sim)
        qobj = assemble(transpiled_dj_circuit)
        results = aer_sim.run(qobj).result()
        answer = results.get_counts()

        if "0" * (circuit.num_qubits - 1) in answer:
            return {"result": "Constant"}
        else:
            return {"result": "Balanced"}

    @staticmethod
    def give_a_balanced_function(inputs_count: int) -> Instruction:
        """Trả về một hàm oracle cân bằng.

        :param inputs_count: Số lượng qubit đầu vào.
        :return: Hàm oracle cân bằng dưới dạng Instruction.
        """
        # Lấy số lượng qubit đầu vào.
        random_number = np.random.randint(1, 2**inputs_count)
        inputs = format(random_number, "0" + str(inputs_count) + "b")

        # Tạo mạch lượng tử với số lượng qubit đầu vào + 1 qubit đầu ra.
        oracle = QuantumCircuit(inputs_count + 1, inputs_count)

        # Đặt cổng X ở đầu các dòng qubit đầu vào.
        for index, qubit in enumerate(reversed(inputs)):
            if qubit == "1":
                oracle.x(index)

        # Áp dụng khối oracle.
        for index, qubit in enumerate(inputs):
            oracle.cx(index, inputs_count)

        # Đặt cổng X ở cuối các dòng qubit đầu vào.
        for index, qubit in enumerate(reversed(inputs)):
            if qubit == "1":
                oracle.x(index)

        inst = oracle.to_instruction()
        inst.name = "BalancedOracle"
        return inst

    @staticmethod
    def give_a_constant_function(inputs_count: int) -> Instruction:
        """Trả về một hàm oracle hằng số.

        :param inputs_count: Số lượng qubit đầu vào.
        :return: Hàm oracle hằng số dưới dạng Instruction.
        """
        # Tạo mạch lượng tử với số lượng qubit đầu vào + 1 qubit đầu ra.
        oracle = QuantumCircuit(inputs_count + 1)

        if np.random.randint(2) == 1:
            oracle.x(inputs_count)

        inst = oracle.to_instruction()
        inst.name = "ConstantOracle"
        return inst

    @staticmethod
    def _construct_the_circuit(function_block: QuantumCircuit) -> QuantumCircuit:
        """Tạo mạch cho thuật toán Deutsch-Jozsa.

        :param function_block: Khối oracle để kiểm tra với thuật toán Deutsch-Jozsa.
        :return: Mạch cho thuật toán Deutsch-Jozsa.
        """
        # Lấy số lượng qubit đầu vào.
        input_length = function_block.num_qubits - 1

        _circuit = QuantumCircuit(input_length + 1, input_length)

        # Áp dụng cổng Hadamard cho tất cả qubit đầu vào.
        for qubit in range(input_length):
            _circuit.h(qubit)

        # Chuyển qubit cuối cùng sang trạng thái |-⟩.
        _circuit.x(input_length)
        _circuit.h(input_length)
        _circuit.barrier()

        # Áp dụng khối oracle.
        _circuit.append(
            function_block, range(function_block.num_qubits), range(function_block.num_clbits)
        )
        _circuit.barrier()

        # Áp dụng cổng Hadamard cho tất cả qubit đầu vào.
        for qubit in range(input_length):
            _circuit.h(qubit)
        _circuit.barrier()

        # Đo tất cả qubit đầu vào và đặt chúng vào các bit cổ điển.
        for qubit in range(input_length):
            _circuit.measure(qubit, qubit)

        return _circuit


if __name__ == "__main__":
    print("===================================")
    print("Mô phỏng Thuật toán Deutsch-Jozsa")
    print("===================================")

    # Lấy số lượng qubit đầu vào.
    inputs_count = int(input("> Nhập số lượng qubit đầu vào: "))

    # Lấy khối oracle.
    oracle_type = input("> Nhập loại hàm (c)hằng số/(b)cân bằng: ")
    oracle_type = oracle_type.lower()
    if oracle_type == "constant" or oracle_type == "c":
        block_to_test = DJAlgorithm.give_a_constant_function(inputs_count)
    elif oracle_type == "balanced" or oracle_type == "b":
        block_to_test = DJAlgorithm.give_a_balanced_function(inputs_count)
    else:
        print("Loại hàm không hợp lệ.")
        exit(1)

    # Chạy thuật toán.
    result = DJAlgorithm.simulate(block_to_test)
    print("Kết quả: " + result["result"])