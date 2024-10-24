import sys
from copy import deepcopy

solutions_set = set()


def hash_board(board):
    list_of_tuples = hash(tuple(tuple(inner_list) for inner_list in board))
    return list_of_tuples


def create_board(n):
    return [["." for _ in range(n)] for _ in range(n)]


# Verifica se eu nao vou apontar pra ninguem da minha quadrilha
def is_safe(board, row, col, quadrilha):
    print(f"Verificando a safety para quadrilha {quadrilha}")
    print(f"Linha e coluna atual: {(row, col)}")
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dr, dc in directions:
        print(f"Direções: {(dr, dc)}")
        r, c = row + dr, col + dc
        print(f"Linha e coluna do for: {(r, c)}")
        blocked = False
        while 0 <= r < n and 0 <= c < n:
            cell = board[r][c]
            if cell == ".":
                print("Cell nesta linha e coluna está livre!")
                r += dr
                c += dc
                print(f"Linha e coluna do laço while: {(r, c)}")
                continue
            elif cell == quadrilha:
                print("Cell nesta linha e coluna tem a mesma quadrilha!")
                if not blocked:
                    return False
                else:
                    break
            else:
                blocked = True
            r += dr
            c += dc
            print(f"Linha e coluna do fim do laço while: {(r, c)}")
    return True


def sees_at_least_two_enemies(board, row, col, quadrilha, n):
    print("Verificando se tem pelo menos 2 inimigos...")
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    count = 0
    for dr, dc in directions:
        print(f"Direções: {(dr, dc)}")
        r, c = row + dr, col + dc
        print(f"Linha e coluna do for: {(r, c)}")
        while 0 <= r < n and 0 <= c < n:
            cell = board[r][c]
            if cell == ".":
                print("Cell nesta linha e coluna está livre!")
                r += dr
                c += dc
                print(f"Linha e coluna do laço while: {(r, c)}")
                if count >= 2:
                    print("Temos ao menos dois inimigos!")
                    return True
                continue
            elif cell != quadrilha:
                print("Cell nesta linha e coluna tem um inimigo!")
                count += 1
                break
            else:
                break
        if count >= 2:
            return True
    return count >= 2


def validate_board(board):
    if hash_board(board) not in solutions_set:
        print("Hash deste board não existe!")
        for row in range(n):
            for col in range(n):
                cell = board[row][col]
                if cell != ".":
                    print(f"Cell atual tem uma quadrilha: {cell}, posição: {(row, col)}")
                    if not sees_at_least_two_enemies(board, row, col, cell, n):
                        print("Não há inimigos o suficiente!")
                        return
        solutions_set.add(hash_board(board))
        print("Hash deste board foi adicionado!")
        transforms(board, n)


def print_board(board, solution):
    print("-" * int(len(board[0]) * 4 / 2), solution, "-" * int(len(board[0]) * 4 / 2))
    for row in board:
        print(row)
    print("-" * (len(board[0]) * 5))


def transforms(board, n):
    print("Iniciando rotações...")
    def rotate(board):
        return [[board[n - j - 1][i] for j in range(n)] for i in range(n)]

    def mirror_matrix(board):
        mirrored_board = [row[::-1] for row in board]
        return mirrored_board

    current_board = deepcopy(board)

    for _ in range(3):
        current_board = rotate(current_board)
        solutions_set.add(hash_board(current_board))

    mirrored_board = mirror_matrix(board)
    for _ in range(3):
        current_board = rotate(mirrored_board)
        solutions_set.add(hash_board(current_board))


def backtrack(board, b_restantes, c_restantes, total_positions, index):
    print("starting backtrack...")
    if b_restantes == 0 and c_restantes == 0:
        print("Não há quadrilhas para posicionar - validando board...")
        validate_board(board)
        return

    if index >= total_positions:
        return

    row, col = divmod(index, n)
    print(f"Current row and col: {(row, col)}")
    if board[row][col] == ".":
        print("Board has a free position!")
        # Tenta colocar um 'B'
        if b_restantes > 0 and is_safe(board, row, col, "B"):
            board[row][col] = "B"
            backtrack(board, b_restantes - 1, c_restantes, total_positions, index + 1)
            board[row][col] = "."

        # Tenta colocar um 'C'
        if c_restantes > 0 and is_safe(board, row, col, "C"):
            board[row][col] = "C"
            backtrack(board, b_restantes, c_restantes - 1, total_positions, index + 1)
            board[row][col] = "."

    # Pular a posição atual
    backtrack(board, b_restantes, c_restantes, total_positions, index + 1)


def main():
    from time import time

    start = time()
    global n
    n = int(sys.argv[1])
    b = int(sys.argv[2])
    c = int(sys.argv[3])

    board = create_board(n)
    total_positions = n * n
    backtrack(board, b, c, total_positions, 0)
    print(len(solutions_set))
    print(time() - start)


if __name__ == "__main__":
    main()
