def fstr(template: str):
    # print(f"f'{template}'" + " hosted.")
    return eval(f"f'{template}'")


if __name__ == "__main__":
    name = ["deep", "mahesh", "nirbhay"]
    user_input = r"Awarded to : {element}"  # this string i ask from user
    for element in name:
        # print(element)
        print(fstr(user_input))
        # print(r"f'{element}'")
        print(eval(r"f'Ghost Particle :- {element}'"))
        # print()
