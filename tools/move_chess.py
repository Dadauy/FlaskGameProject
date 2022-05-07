def move_chess(doska, gorizont_here, vertical_here, gorizont_there, vertical_there, figure):
    """определяет правильность хода"""
    if figure[0] == "l":  # ладья
        if gorizont_here == gorizont_there or vertical_here == vertical_there:
            doska[vertical_there * 8 + gorizont_there] = doska[vertical_here * 8 + gorizont_here]
            doska[vertical_here * 8 + gorizont_here] = "_"

    elif figure[0] == "k":  # конь
        move_variant = [(vertical_here - 2, gorizont_here + 1),
                        (vertical_here - 2, gorizont_here - 1),
                        (vertical_here - 1, gorizont_here + 2),
                        (vertical_here - 1, gorizont_here - 2),
                        (vertical_here + 1, gorizont_here + 2),
                        (vertical_here + 1, gorizont_here - 2),
                        (vertical_here + 2, gorizont_here + 1),
                        (vertical_here + 2, gorizont_here - 1),
                        ]
        if (vertical_there, gorizont_there) in move_variant:
            doska[vertical_there * 8 + gorizont_there] = doska[vertical_here * 8 + gorizont_here]
            doska[vertical_here * 8 + gorizont_here] = "_"

    elif figure[0] == "c":  # слон
        if abs(vertical_there - vertical_here) == abs(gorizont_there - gorizont_here):
            doska[vertical_there * 8 + gorizont_there] = doska[vertical_here * 8 + gorizont_here]
            doska[vertical_here * 8 + gorizont_here] = "_"

    elif figure[0] == "f":  # ферзь
        if abs(vertical_there - vertical_here) == abs(gorizont_there - gorizont_here) or \
                (gorizont_here == gorizont_there or vertical_here == vertical_there):
            doska[vertical_there * 8 + gorizont_there] = doska[vertical_here * 8 + gorizont_here]
            doska[vertical_here * 8 + gorizont_here] = "_"

    elif figure[0] == "g":  # король
        if abs(vertical_there - vertical_here) == abs(gorizont_there - gorizont_here) == 1 or \
                (gorizont_here == gorizont_there or vertical_here == vertical_there):
            doska[vertical_there * 8 + gorizont_there] = doska[vertical_here * 8 + gorizont_here]
            doska[vertical_here * 8 + gorizont_here] = "_"

    elif figure[0] == "p":  # пешка
        if figure[1] == "W":
            if vertical_there - vertical_here == 1:
                doska[vertical_there * 8 + gorizont_there] = doska[vertical_here * 8 + gorizont_here]
                doska[vertical_here * 8 + gorizont_here] = "_"

        elif figure[1] == "B":
            if vertical_there - vertical_here == -1:
                doska[vertical_there * 8 + gorizont_there] = doska[vertical_here * 8 + gorizont_here]
                doska[vertical_here * 8 + gorizont_here] = "_"

    return doska
