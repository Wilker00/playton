def main():
    # Using loop with if and else statement

    # - ( 1 ) -
    #
    # a = 2
    # b = 4
    # if a < b:
    #     print("i guess this is true ")
    #
    # else:
    #     print("I guess not")
#         ---------------------------------------------
#     - (2) -

    # if a > b:
    #     pass
    # else:
    #     print("do nothing I guess")

#     -----------------------------------------------------
#     - (3) -

    x = 0
    while x < 10  :
        if x == 5:
            break
        print(x)
        x += 1
    print("This code is done")
        # -----------------------------------------------------
    #     - (4) -
    m = 0
    while m < 10:
        m += 1
        if m == 5:
            continue
        print(m)
    print("This too code is done")

main()