''' This is proj10 for CSE231 by Shrey Jindal
this is a game of montana Solitaire
we use function defining and calling to make the program.
the cards module is used '''

#DO NOT DELETE THESE LINES
import cards, random
random.seed(100) #random number generator will always generate
                 #the same random number (needed to replicate tests)


def initialize():
    '''this function has no parameters. It creates, initializes, and returns the tableau in form of list of lists'''
    l1,l2,l3,l4 = [],[],[],[]
    x = cards.Deck()#calling the cards module
    x.shuffle()
    for i in range(52):
        c = x.deal()
        if i<13:
            l1.append(c)
        elif i<26:
            l2.append(c)
        elif i<39:
            l3.append(c)
        else:
            l4.append(c)
    t = [l1,l2,l3,l4]
    return t

def display(tableau):
    '''2t state of the game.
        It display four rows of 13 cards with row and column labels.
        Ace is displayed with a blank.

        parameters:
            tableau: data structure representing the tableau

        Returns: None
    '''

    print("{:3s} ".format(' '), end = '')
    for col in range(1,14):
        print("{:3d} ".format(col), end = '')
    print()

    for r,row_list in enumerate(tableau):
        print("{:3d}:".format(r+1), end = '')
        for c in row_list:
            if c.rank() == 1:
                print("  {}{}".format(' ',' '), end = '')
            else:
                print("{:>4s}".format(str(c)),end = '')
        print()

def validate_move(t,sr,sc,dr,dc):
    ''' This function has five parameters: the data structure representing the tableau and four ints the
source row & column and the destination row & column. Row and column ints are in the
ranges 0 <= row <= 3 and 0 <= column <= 12. The function will return True, if the move is
valid; and False, otherwise'''
    if t[dr][dc].rank() != 1:#to verify that destination is empty
        return False
    elif dc == 0:
        if t[sr][sc].rank() == 2:#special condition for first column in table. Allows only 2
            return True
        else:
            return False
    elif t[dr][dc-1].suit() != t[sr][sc].suit():#suit matching
        return False
    elif t[sr][sc].rank() - t[dr][dc-1].rank() != 1:#sequence matching
        return False
    else:
        return True

def move(t,sr,sc,dr,dc):
    '''That function has five parameters: the data structure representing the tableau and four ints the
source row & column and the destination row & column. Row and column ints are in the
ranges 0 <= row <= 3 and 0 <= column <= 12. If the move is valid, the function will update the
tableau and return True; otherwise, it will do nothing to it and return False'''
    if validate_move(t,sr,sc,dr,dc) == False:#check vilidity of move
        return False
    else:#performing the move, swapping cards at source and destination
        c1 =  t[dr][dc]
        c2 =  t[sr][sc]
        t[dr][dc], = c2
        t[sr][sc] = c1
        return True

def shuffle_tableau(tab):
    '''this fuction shuffles the cards but Only some cards are shuffled: cards that are already in a same-suit sequence starting with a 2 in
the leftmost column are left in place and not shuffled. All other cards are shuffled and then dealt
back into the tableau, but there will be one blank space in each row and it will be at the right end
of the sequence that is left in place (or in the leftmost column, if there is no sequence in that
row)'''
    lolrem = []#empty lists for file mainpulation
    lshuff = []

    for listx in tab:#this decides which data to shuffle and which not
        #print(listx)
        lrem = []
        lrest = []
        n=0
        while  (n<13 and listx[n].suit() == listx[0].suit() and listx[n].rank() == n+2):
            #print(listx)
            lrem.append(listx[n])
            n+=1
            #print(lrem)
        else:
            lrest += listx[n:]
            #print(lrest,'lrest')
        lshuff+= lrest
        #print(lshuff,'lshuff from lrest')
        lolrem.append(lrem)
        #print(lolrem,'lolrem')
        #print(list)
    #print(lolrem)
    #print(lshuff)
    random.shuffle(lshuff)#shufling
    #print(lshuff)
    aces = []
    for i in lshuff:#this helps seperate aces
        if i.rank()==1:
            #print(i)
            lshuff.remove(i)
            aces.append(i)
    for i in lshuff:
        if i.rank()==1:
            #print(i)
            lshuff.remove(i)
            aces.append(i)
    #print(lshuff,'lshuff')
    #print(aces)
    m = 0
    for listx in lolrem:#adding aces to unshuffled pile
        listx.append(aces[m])
        m+=1
    #print(lolrem,'lol')
    for i in tab:#empting existing tableau
        tab.remove(i)
    for i in tab:
        tab.remove(i)
    for i in tab:
        tab.remove(i)
    for listx in lolrem:#adding cards to tablaeu
        l = len(listx)
        #print(l)
        a = 13-l
        #print(a)
        #print(lshuff[:a])
        jk = listx + lshuff[:a]
        #print(jk)
        lshuff = lshuff[a:]
        tab.append(jk)
        #print(tab)
    #print(tab)

def check_win(t):
    '''That function has one parameter: the data structure representing the tableau.
    it uses the tableau and finds if the game has been won.'''
    rlc = [2,3,4,5,6,7,8,9,10,11,12,13]#correct sequence
    rval = 0
    sval = 0

    for i in t:
        spv = 0
        rtr = []
        #print(i)
        for c in i[:12]:
            rtr.append(c.rank())
        #print(rtr)
        if rtr == rlc:
            rval += 1
        suit = i[0].suit()
        for c in i[:12]:
            if c.suit() == suit:
                spv += 1
                #print('adding')
        if spv == 12:
            sval += 1
    if sval+rval == 8:
        return True
    else:
        return False

def main():
    '''the main function porvides a structure to the program.
    It decides what steps to follow, when and what input to take, what to display and which fucntions to call'''
    print("Montana Solitaire.")
    tab = initialize()
    m = 2
    display(tab)
    again= 'n'
    while 1:
        if again == 'y':#when game is restarted at the end, the following steps need to be taken
            print("Montana Solitaire.")
            tab = initialize()
            display(tab)
        choice = input("Enter choice:\n (q)uit, (s)huffle, or space-separated: source_row,source_col,dest_row,dest_col: ")#user input
        if choice.lower() == 'q':
            again = input("Do you want to play again (y/n)?")
            if again == 'y':
                continue
            else:
                print("Thank you for playing.")
                break
        elif choice.lower() == 's':
            if m>0:
                shuffle_tableau(tab)
                m = m-1#to keep count of shuffles
                display(tab)
            else:
                print("No more shuffles remain.")
        else:
            try:#checking for errors
                l = []
                for i in choice.split():
                    l.append(int(i))
            except:
                print("Error: invalid input.  Please try again.")
                continue
            if len(l)!=4:
                print("Error: invalid input.  Please try again.")
            elif (l[1] > 13 or l[2] > 4 or l[3] > 13 or l[0] > 4 or l[0] < 1 or l[1] < 1 or l[2] < 1 or l[3] < 1):#range check
                print("Error: row and/or column out of range. Please Try again.")
            elif validate_move(tab,l[0]-1,l[1]-1,l[2]-1,l[3]-1) == False:#validationg move
                print("Error: invalid move.  Please try again.")
            else:
                move(tab,l[0]-1,l[1]-1,l[2]-1,l[3]-1)#perfomring the move.
                display(tab)
            if check_win(tab) == True:
                print("You won!")
                again = input("Do you want to play again (y/n)?")
                if again == 'n':
                    print("Thank you for playing.")
                    break


if __name__ == "__main__":
    main()
