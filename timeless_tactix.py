import sys
from collections import deque

from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, \
    QMessageBox

PLAYER1 = "X"
PLAYER2 = "O"

button_style_json = {
    "X": "QPushButton {font-size: 18pt; font-weight: bold; color: red;}",
    "O": "QPushButton {font-size: 18pt; font-weight: bold; color: blue;}"
}

faded_button_style_json = {
    "X": "QPushButton {font-size: 18pt; font-weight: bold; color: grey;}",
    "O": "QPushButton {font-size: 18pt; font-weight: bold; color: grey;}"
}


class GridWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.__play_board = []
        self.__pos_dict = {
            PLAYER1: deque(),
            PLAYER2: deque()
        }
        self.__curr_player = PLAYER1
        self.__init_ui()

    def __init_ui(self):
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        for i in range(3):
            row = []
            for j in range(3):
                button = QPushButton()
                button.setFixedSize(100, 100)
                grid_layout.addWidget(button, i, j)
                button.clicked.connect(
                    lambda _, row=i, col=j: self.__button_clicked(row, col))
                row.append(button)
            self.__play_board.append(row)

        self.setWindowTitle('Fadeaway-TacTix')
        self.setGeometry(100, 100, 300, 300)

    def __button_clicked(self, row, col):
        curr_player = self.__curr_player
        button = self.__play_board[row][col]

        if button.text():
            return

        button.setStyleSheet(button_style_json.get(curr_player))
        button.setText(curr_player)

        self.__pos_dict[curr_player].append((row, col))

        if self.__check_Winner():
            self.__declare_winner()
            return

        self.__remove_initial_moves()
        self.__fade_initial_move()
        self.__swap_turns()

    def __fade_initial_move(self):

        if len(self.__pos_dict[self.__curr_player]) < 3:
            return

        curr_player = self.__curr_player
        first_move_coord = self.__pos_dict[curr_player][0]
        button = self.__play_board[first_move_coord[0]][first_move_coord[1]]
        button.setStyleSheet(faded_button_style_json.get(curr_player))

    def __swap_turns(self):
        self.__curr_player = PLAYER2 if self.__curr_player == PLAYER1 else PLAYER1

    def __remove_initial_moves(self):
        if len(self.__pos_dict[self.__curr_player]) <= 3:
            return

        first_move_coord = self.__pos_dict[self.__curr_player].popleft()
        button = self.__play_board[first_move_coord[0]][first_move_coord[1]]
        button.setText("")

    def __check_Winner(self):
        curr_player = self.__curr_player
        curr_player_nodes = self.__pos_dict[curr_player]

        if len(curr_player_nodes) < 3:
            return

        play_board = self.__play_board
        for i in range(3):
            if (play_board[i][0].text() == play_board[i][1].text() ==
                    play_board[i][2].text() == curr_player):
                return True
            if (play_board[0][i].text() == play_board[1][i].text() ==
                    play_board[2][i].text() == curr_player):
                return True

        if play_board[0][0].text() == play_board[1][1].text() == play_board[2][
            2].text():
            return True

        if play_board[0][-1].text() == play_board[1][1].text() == \
                play_board[-1][0].text():
            return True

        return False

    def __declare_winner(self):
        winner = self.__curr_player
        msg_box = QMessageBox()
        msg_box.setWindowTitle('Game Over!!!')
        msg_box.setText(f'Player "{winner}" wins!')
        msg_box.exec()
        self.__reset_game()

    def __reset_game(self):
        play_board = self.__play_board
        for i in range(3):
            for j in range(3):
                play_board[i][j].setText("")

        self.__pos_dict[PLAYER1].clear()
        self.__pos_dict[PLAYER2].clear()
        self.__curr_player = PLAYER1


def main():
    app = QApplication(sys.argv)
    grid_window = GridWindow()
    grid_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
