# Write your code here
import random
import sqlite3

id1 = 1
# data = dict()
conn = sqlite3.connect("card.s3db")
cur = conn.cursor()
cur.execute("DROP TABLE card")
cur.execute("""CREATE TABLE card (
            id INTEGER,
            number TEXT,
            pin TEXT,
            balance INTEGER DEFAULT 0
            );""")


def number_create(x):
    part1 = random.sample(range(10), x)
    part2 = ""
    for i in part1:
        part2 += str(i)
    return part2


def luhn_algorithm():
    first_9 = number_create(9)
    # first_9 = '837541296'
    card1 = "400000"
    first_15 = card1 + first_9
    sum1 = 0
    for i in range(1, len(first_15) + 1):
        j = int(first_15[i - 1])
        # print(f"num {j}")
        if i % 2 != 0:
            j = j * 2
        if j > 9:
            j -= 9
        # print(j)
        sum1 += j
        # print(sum1)
    # print(sum1)
    last = 10 - sum1 % 10
    if last == 10:
        last = 0
    # print(last)
    return int(first_15 + str(last))


def luhn_algorithm_checker(card2):
    sum2 = 0
    for s in range(1, len(card2)):
        w = int(card2[s - 1])
        if s % 2 != 0:
            w = w * 2
        if w > 9:
            w -= 9
        sum2 += w
    last3 = 10 - sum2 % 10
    if last3 == 10:
        last3 = 0
    if card2[-1] == str(last3):
        return True
    else:
        return False


def create():
    global id1
    card = luhn_algorithm()
    pin = number_create(4)
    # data[card] = pin
    print("\n" + "Your card has been created")
    print("Your card number:")
    print(card)
    print("Your card PIN:" + "\n" + pin + "\n")
    cur.execute(f"""INSERT INTO card(id, number, pin) VALUES
                ({id1}, {str(card)}, {str(pin)});""")
    conn.commit()
    id1 = id1 + 1


def transfer(id3):
    print("\n" + "Transfer")
    acc = input("Enter card number:" + "\n")
    cur.execute(f"SELECT * FROM card;")
    data3 = cur.fetchall()
    accounts = [q[1] for q in data3 for _ in range(4)]
    # print(accounts)
    if data3[id3 - 1][1] == acc:
        print("You can't transfer money to the same account!" + "\n")
    elif not luhn_algorithm_checker(acc):
        print("Probably you made a mistake in the card number. Please try again!" + "\n")
    elif acc not in accounts:
        print("Such a card does not exist." + "\n")
    acc_balance = data3[id3 - 1][3]
    for j in range(len(data3)):
        if data3[j][1] == acc:
            added = int(input("Enter how much money you want to transfer:" + "\n"))
            if added >= acc_balance:
                print("Not enough money!" + "\n")
            else:
                print("Success!" + "\n")
                cur.execute(f"UPDATE card SET balance={acc_balance - added} WHERE id={id3};")
                cur.execute(f"UPDATE card SET balance={data3[j][3] + added} WHERE id={j + 1};")
                conn.commit()


def logged_menu(id2):
    while True:
        print("""1. Balance
2. Add income
3. Do transfer
4. Close account   
5. Log out
0. Exit""")
        choice1 = int(input())
        cur.execute(f"SELECT * FROM card WHERE id={id2};")
        data2 = cur.fetchone()
        bal1 = data2[3]
        if choice1 == 1:
            print("\n" + f"Balance: {bal1}" + "\n")
        elif choice1 == 2:
            new1 = int(input("\n" + "Enter income:" + "\n"))
            bal1 += new1
            print("Income was added!" + "\n")
            cur.execute(f"UPDATE card SET balance={bal1} WHERE id={id2};")
            conn.commit()
        elif choice1 == 3:
            transfer(id2)
        elif choice1 == 4:
            cur.execute(f"DELETE FROM card WHERE id={id2};")
            conn.commit()
            print("\n" + "The account has been closed!" + "\n")
            break
        elif choice1 == 5:
            print("\n" + "You have successfully logged out!" + "\n")
            break
        elif choice1 == 0:
            print("\n" + "Bye!", end="")
            exit()


def log():
    card1 = input("\n" + "Enter your card number:" + "\n")
    pin1 = input("Enter your PIN:" + "\n")
    # if card1 in data and data[card1] == pin1:
    # print("\n" + "You have successfully logged in!" + "\n")
    # logged_menu()
    # else:
    # print("\n" + "Wrong card number or PIN!" + "\n")
    cur.execute("SELECT * FROM card;")
    all1 = cur.fetchall()
    # print(all1)
    for i in range(len(all1)):
        if all1[i][1] == card1 and all1[i][2] == pin1:
            print("\n" + "You have successfully logged in!" + "\n")
            logged_menu(all1[i][0])
    for i1 in range(len(all1)):
        if all1[i1][1] != card1 or all1[i1][2] != pin1:
            print("\n" + "Wrong card number or PIN!" + "\n")


while True:
    print("""1. Create an account
2. Log into account
0. Exit""")
    choice = int(input())
    if choice == 1:
        create()
    elif choice == 2:
        log()
    elif choice == 0:
        print("\n" + "Bye!", end="")
        exit()
