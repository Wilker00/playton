def main():
    import random
    # this is a car selector generator for people who want to buy  cars but don't know which
    #we will be using if/else, random.randint and random.choice as well as dictionaries

    # dictionaries!
    car_brands = {
        "Mazda" : 2000,
        "Toyota" : 2005,
        "Chevrolet":1999,
    }

    print(random.choice(car_brands))

main()