import random
import tkinter as tk
from tkinter import simpledialog, messagebox

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "A": 5,
    "B": 6,
    "C": 7,
    "D": 8
}

symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}

class SlotMachineGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Slot Machine Game")

        self.balance = tk.IntVar()
        self.lines = tk.IntVar()
        self.bet = tk.IntVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Current Balance: $").grid(row=0, column=0)
        tk.Entry(self, textvariable=self.balance, state="readonly").grid(row=0, column=1)

        tk.Label(self, text="Number of Lines (1-3):").grid(row=1, column=0)
        tk.Entry(self, textvariable=self.lines, state="readonly").grid(row=1, column=1)

        tk.Label(self, text="Bet Amount ($1-$100):").grid(row=2, column=0)
        tk.Entry(self, textvariable=self.bet).grid(row=2, column=1)

        tk.Button(self, text="Spin", command=self.spin).grid(row=3, column=0, columnspan=2)

    def deposit(self):
        while True:
            amount = simpledialog.askinteger("Deposit", "What would you like to deposit?", minvalue=1)
            if amount is not None:
                break
        return amount

    def get_number_of_lines(self):
        while True:
            lines = simpledialog.askinteger("Number of Lines", "Enter the number of lines to bet on (1-3):", minvalue=1, maxvalue=3)
            if lines is not None:
                break
        return lines

    def get_bet(self):
        while True:
            bet = simpledialog.askinteger("Bet Amount", "What would you like to bet on each line? ($1-$100)", minvalue=1, maxvalue=100)
            if bet is not None:
                break
        return bet

    def spin(self):
        self.lines.set(self.get_number_of_lines())
        total_bet = self.bet.get() * self.lines.get()

        if total_bet > self.balance.get():
            messagebox.showinfo("Insufficient Funds", f"You do not have enough to bet that amount. Your current balance is: ${self.balance.get()}")
            return

        messagebox.showinfo("Bet Information", f"You are betting ${self.bet.get()} on {self.lines.get()} lines. Total bet is equal to: ${total_bet}")

        slots = self.get_slot_machine_spin(ROWS, COLS, symbol_count)
        self.print_slot_machine(slots)
        winnings, winning_lines = self.check_winnings(slots, self.lines.get(), self.bet.get(), symbol_value)
        messagebox.showinfo("Winnings", f"You won ${winnings}.")
        messagebox.showinfo("Winning Lines", f"You won on lines: {winning_lines}")
        
        self.balance.set(self.balance.get() + (winnings - total_bet))

    def get_slot_machine_spin(self, rows, cols, symbols):
        all_symbols = []
        for symbol, symbol_count in symbols.items():
            for _ in range(symbol_count):
                all_symbols.append(symbol)

        columns = []
        for _ in range(cols):
            column = []
            current_symbols = all_symbols[:]
            for _ in range(rows):
                value = random.choice(current_symbols)
                current_symbols.remove(value)
                column.append(value)

            columns.append(column)

        return columns

    def print_slot_machine(self, columns):
        result = ""
        for row in range(len(columns[0])):
            for i, column in enumerate(columns):
                if i != len(columns) - 1:
                    result += column[row] + " | "
                else:
                    result += column[row]

            result += "\n"
        messagebox.showinfo("Slot Machine Result", result)

    def check_winnings(self, columns, lines, bet, values):
        winnings = 0
        winning_lines = []
        for line in range(lines):
            symbol = columns[0][line]
            for column in columns:
                symbol_to_check = column[line]
                if symbol != symbol_to_check:
                    break
            else:
                winnings += values[symbol] * bet
                winning_lines.append(line + 1)

        return winnings, winning_lines

    def start_game(self):
        self.balance.set(self.deposit())
        self.mainloop()

if __name__ == "__main__":
    app = SlotMachineGUI()
    app.start_game()
