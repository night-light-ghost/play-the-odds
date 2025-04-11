import random
import copy

deck = ["A-Hearts","2-Hearts","3-Hearts","4-Hearts","5-Hearts","6-Hearts","7-Hearts","8-Hearts","9-Hearts","10-Hearts","J-Hearts","Q-Hearts","K-Hearts","A-Spades","2-Spades","3-Spades","4-Spades","5-Spades","6-Spades","7-Spades","8-Spades","9-Spades","10-Spades","J-Spades","Q-Spades","K-Spades","A-Diamonds","2-Diamonds","3-Diamonds","4-Diamonds","5-Diamonds","6-Diamonds","7-Diamonds","8-Diamonds","9-Diamonds","10-Diamonds","J-Diamonds","Q-Diamonds","K-Diamonds","A-Clubs","2-Clubs","3-Clubs","4-Clubs","5-Clubs","6-Clubs","7-Clubs","8-Clubs","9-Clubs","10-Clubs","J-Clubs","Q-Clubs","K-Clubs"]

baseGame = {"dealerHand": {"upCard": [], "downCard": [], "bust": False, "totalVal": 0, "curAces": 0}, "playerHand": {"cards": [], "bust": False, "money": 0, "totalVal": 0, "blackJack": False, "curAces": 0}, "splitHand": [], "curBet": 0, "gameDeck": [], "acesSeen": 0, "marked": False}

rowsPerCard = 5

# Shuffles the deck
# - A basic function, really was only made before I knew random had a shuffle feature
def shuffle(curDeck):
    random.shuffle(curDeck)
    return curDeck

# Cuts the shuffled deck and loads in a marker
# This is mostly a formality, though it allows the player some influence, and the marker is put to set the last round
def cutDeck(curDeck, cut):
# cutting some of the deck
    if(cut==1):
        deckTemp = []
        count = len(curDeck)//4
        #print(count)
        while(len(deckTemp)<len(curDeck)):
            deckTemp.append(curDeck[count])
            count +=1
            if(count==312):
                count = 0;
# cutting half of the deck
    if(cut==2):
        deckTemp = []
        count = len(curDeck)//2
        #print(count)
        while(len(deckTemp)<len(curDeck)):
            deckTemp.append(curDeck[count])
            count +=1
            if(count==312):
                count = 0;
# cutting most of the deck
    if(cut==3):
        deckTemp = []
        count = 3*(len(curDeck)//4)
        #print(count)
        while(len(deckTemp)<len(curDeck)):
            deckTemp.append(curDeck[count])
            count +=1
            if(count==312):
                count = 0;
    deckTemp.insert(261, "marker")
    return deckTemp

# generates a new 6-deck stack, shuffled and prompting the user to cut it
# 
def newDeck():
    print("Welcome here, I'm Nancy")
    deckStack = []
    deckStack += deck + deck + deck + deck + deck + deck
    shuffle(deckStack)
    print("How much of deck to cut?")
    cut = 0
    while(cut!=1 and cut!=2 and cut!=3):
        try:
            cut = int(input("Enter 1 for some, 2 for about half, 3 for most: "))
        except:
            print("Input must be one of the above digits")
    deckStack = cutDeck(deckStack, cut)
    return deckStack

# figure out results after game (can probably be a log of each game round in cleanBoard
def newGame(gameDeck):
    results = []
    noBustOrBlackJack = False
    deckTrash = []
    deckTrash.append(gameDeck.pop())
    gameStatus = baseGame.deepCopy()
    gamestatus["gameDeck"] = gameDeck
    # outer loop is the whole game of 6 decks
    choice = 0
    while(gameStatus['marked']==False):
        gameStatus = dealhands(gameStatus)
        print("-------------------------------------------------------------------------")
        # inner loop is a round
        while(choice!=1 and cut!=2 and cut!=3 and choice!=4):
            printGame(gameStatus)
            gameStatus['playerHand'] = checkPlayerHand(gameStatus)
            if gameStatus['bust']:
                print("You played that hand well")
                # adjust value
            elif gameStatus['blackJack']:
                print("ka-ching")
                #adjust value
            else:
                try:
                    choice = int(input("Enter 1 to hit, 2 to stay, 3 to double down, and 4 to split (iff you have doubles): "))
                except:
                    print("Input must be one of the above digits")
                if(choice==1):
                    gameStatus = hitPlayerhand(gameStatus)
                if(choice==2):
                    gameStatus = checkDealerBust(gameStatus)
                if(choice==3):
                    gameStatus = doubleDown(gameStatus)
                    # requires value
                if(choice==4):
                    if(doubles(gameStatus['playerHand'])):
                        gameStatus = splitHands(gameStatus)
                choice = 0
        results.append(cleanBoard(gameStatus))
    return

# Deals a card, with the code from setup
def hitPlayerHand(gameStatus):
    card = gameStatus['gameDeck'].pop()
    if(card=="marker"):
        gameStatus["marked"] = True
        card = gameStatus['gameDeck'].pop()
    gameStatus["playerHand"]["cards"].append(card)
    gameStatus['playerHand'] = checkPlayerhand(gameStatus['playerHand'])
    return gameStatus

# Deals a card, with the code from setup
def hitSplitHand(gameStatus):
    card = gameStatus['gameDeck'].pop()
    if(card=="marker"):
        gameStatus["marked"] = True
        card = gameStatus['gameDeck'].pop()
    gameStatus["splitHand"].append(card)
    gameStatus['splitHand'] = checkSplithand(gameStatus)
    return gameStatus

# Checks for bust or blackjack
def checkPlayerHand(gameStatus):
    handTotal = 0
    for playerCard in gameStatus['playerHand']['cards']:
        stringValue = playerCard.split("-")[0]
        try:
            intValue = int(stringValue)
            handTotal = handTotal + intValue
        except:
            if(stringValue=="J"):
                handTotal = handTotal + 10
            elif(stringValue=="Q"):
                handTotal = handTotal + 10
            elif(stringValue=="K"):
                handTotal = handTotal + 10
            elif(stringValue=="A"):
                handTotal = handTotal + 1
                gameStatus['acesSeen'] = gameStatus['acesSeen'] + 1
                gameStatus['playerHand']['curAces'] = gameStatus['playerHand']['curAces'] + 1
    if handTotal >= 22:
        gameStatus['playerHand']['bust'] = True
        gameStatus['playerHand']['totalVal'] = handTotal
        return gameStatus['playerHand']
    elif handTotal == 11:
        if len(gameStatus['playerHand']['cards']) == 2:
            if gameStatus['playerHand']['curAces'] == 1:
                gameStatus['playerHand']['blackJack'] = True
    else:
        gameStatus['playerHand']['totalVal'] = handTotal
        return gameStatus['playerHand']

# check if the Dealer busts, and then who wins
def checkDealerBust(gameStatus):
    handTotal = 0
    gameStatus = gameStatus['dealerHand']['upCard'].append(gameStatus['dealerHand']['downCard'].pop()
    print("Flipped Dealer card")
    printGame(gameStatus)
    # print with flipped card, then determine value
    for dealerCard in gameStatus['dealerHand']['upCard']:
        stringValue = dealerCard.split("-")[0]
        try:
            intValue = int(stringValue)
            handTotal = handTotal + intValue
        except:
            if(stringValue=="J"):
                handTotal = handTotal + 10
            elif(stringValue=="Q"):
                handTotal = handTotal + 10
            elif(stringValue=="K"):
                handTotal = handTotal + 10
            elif(stringValue=="A"):
                handTotal = handTotal + 1
                gameStatus['acesSeen'] = gameStatus['acesSeen'] + 1
                gameStatus['dealerHand']['curAces'] = gameStatus['dealerHand']['curAces'] + 1
    if handTotal >= 22:
        gameStatus['dealerHand']['bust'] = True
        gameStatus['dealerHand']['totalVal'] = handTotal
        return gameStatus['dealerHand']
    elif handTotal == 11:
        if len(gameStatus['dealerHand']['cards']) == 2:
            if gameStatus['dealerHand']['curAces'] == 1:
                gameStatus['dealerHand']['blackJack'] = True
    elif handTotal >= 17:
        if gameStatus['dealerHand']['curAces'] == 0:
            # compare dealer and player hands
    elif handTotal >= 8:
        if gameStatus['dealerHand']['curAces'] >= 1;
            if handTotal >
    else: # dealer hits
        gameStatus['dealerHand']['totalVal'] = handTotal
        return gameStatus['dealerHand']
    return

# 
def doubleDown(gameStatus):
    return

# 
def splitHands(gameStatus):
    gameStatus['splitHand'].append(gameStatus['playerHand']['cards'].pop())
    return

# Deal the dealer and player's hands
def dealHands(gameStatus):
    card = gameStatus['gameDeck'].pop()
    if(card=="marker"):
        gameStatus["marked"] = True
        card = gameStatus['gameDeck'].pop()
    gameStatus["playerHand"]['cards'].append(card)
    card = gameStatus['gameDeck'].pop()
    if(card=="marker"):
        gameStatus["marked"] = True
        card = gameStatus['gameDeck'].pop()
    gameStatus["playerhand"].append(card)
    card = gameStatus['gameDeck'].pop()
    if(card=="marker"):
        gameStatus["marked"] = True
        card = gameStatus['gameDeck'].pop()
    gameStatus["dealerHand"]["downCard"].append(card)
    card = gameStatus['gameDeck'].pop()
    if(card=="marker"):
        gameStatus["marked"] = True
        card = gameStatus['gameDeck'].pop()
    gameStatus["dealerHand"]["upCard"].append(card)
    

# get hand size across
def handSize(hand):
    if (len(hand)>1):
        spacing = len(hand)-1
        handwidth = (4 * len(hand)) + spacing
        return handwidth
    else:
        handwidth = 4
        return handwidth

# dealerhand prints cards from upCards
def dealerHandSplits(hand):
    if (len(hand)>1):
        handString = []
        for card in hand:
            handString.append(dealerCardSplits(card))
        return handString
    else:
        return dealerCardSplits(hand[0])

# takes a card string and generates array of rasterizing slices (dealer has suit on top)
def dealerCardSplits(card):
    numberSuit = card.split("-")
    cardSplit = []
    cardSplit.append(suitShortName(numberSuit[1]))
    for cardRow in cardSlices(numberSuit[0]):
        cardSplit.append(cardRow)
    return cardSplit

# takes a card string and generates array of rasterizing slices (player has suit on bottom)
def playerCardSplits(card):
    numberSuit = card.split("-")
    cardSplit = []
    for cardRow in cardSlices(numberSuit[0]):
        cardSplit.append(cardRow)
    cardSplit.append(suitShortName(numberSuit[1]))
    return cardSplit

# dealerhand prints cards from upCards
def playerHandSplits(hand):
    handString = []
    for card in hand:
        handString.append(playerCardSplits(card))
    return handString



# Get slices of card number string
def cardSlices(number):
    if(number=="A"):
        return [" /\\ ", "/--\\", "|  |", "|  |"]
    if(number=="2"):
        return ["//\\\\", "  //", " // ", "/___"]
    if(number=="3"):
        return ["//\\\\", "  //", "  \\\\", "\\\\//"]
    if(number=="4"):
        return ["| ||", "|_||", "  ||", "  ||"]
    if(number=="5"):
        return ["//==", "||  ", "\\\\\\\\", "__//"]
    if(number=="6"):
        return ["//\\\\", "||  ", "||\\\\", "\\\\//"]
    if(number=="7"):
        return ["====", "  //", " // ", "//  "]
    if(number=="8"):
        return ["//\\\\", "\\\\//", "//\\\\", "\\\\//"]
    if(number=="9"):
        return ["//\\\\", "\\\\//", " // ", "//  "]
    if(number=="10"):
        return ["/|/\\", " |||", " |||", " |\\/"]
    if(number=="J"):
        return ["====", "   |", "   |", "\\__/"]
    if(number=="Q"):
        return [" /\\ ", "/  \\", "\\ \\/", " \\/\\"]
    if(number=="K"):
        return ["|| /", "||/ ", "||\\ ", "|| \\"]

# Get suit name
def suitShortName(suit):
    if(suit=="Hearts"):
        return "HART"
    if(suit=="Clubs"):
        return "CLUB"
    if(suit=="Diamonds"):
        return "DMND"
    if(suit=="Spades"):
        return "PADE"



# Print the status of the current game
def printGame(gameStatus):    
# print up card (do this in a loop, as the down card becomes an up card once player is locked in)
    gameBoard = "+++==========||==========||==========||==========+++\n"
    gameBoard = gameBoard + "|                                                  |\n"
    boardWidth = 46 # width of row across
    boardWidth = boardWidth - handSize(gameStatus["dealerHand"]["upCard"])
    dealerHandString = dealerHandSplits(gameStatus["dealerHand"]["upCard"])
    if (len(dealerHandString)==5): # Here we're dealing with an array of a single card
        for row in dealerHandString:
            gameBoard = gameBoard + "]  "
            lws = boardWidth // 2 # lws is leftWhiteSpace
            while(lws>0):
                gameBoard = gameBoard + " "
                lws = lws - 1
            gameBoard = gameBoard + row
            rws = boardWidth // 2 # rws is rightWhiteSpace
            while(rws>0):
                gameBoard = gameBoard + " "
                rws = rws - 1
            gameBoard = gameBoard + "  [\n"
    else: # Here we're dealing with an array of arrays
        cardsInHand = len(dealerHandString)
        currentRow = 0
        while (currentRow<rowsPerCard):
            gameBoard = gameBoard + "]  "
            currentCard = 0
            lws = boardWidth // 2 # lws is leftWhiteSpace
            while(lws>0):
                gameBoard = gameBoard + " "
                lws = lws - 1
            while(currentCard<cardsInHand): 
                gameBoard = gameBoard + dealerHandString[currentCard][currentRow]
                gameBoard = gameBoard + " "
                currentCard = currentCard + 1
            rws = boardWidth // 2 # rws is rightWhiteSpace
            if( (len(dealerHandString) % 2) == 1 ):
                rws = rws - 1 # removing an extra whitespce when printing odd numbers of cards
            while(rws>0):
                gameBoard = gameBoard + " "
                rws = rws - 1
            gameBoard = gameBoard + "  [\n"
            currentRow = currentRow + 1
    # This section to print the divider between the boards
    gameBoard = gameBoard + "|                                                  |\n"
    gameBoard = gameBoard + ")                    - - ++ - -                    (\n"
    gameBoard = gameBoard + ")                    - - ++ - -                    (\n"
    gameBoard = gameBoard + "|                                                  |\n"
    boardWidth = 46 # width of row across
    boardWidth = boardWidth - handSize(gameStatus["playerHand"]['cards'])
    playerHandString = playerHandSplits(gameStatus["playerHand"]['cards'])
    cardsInHand = len(playerHandString)
    currentRow = 0
    while (currentRow<rowsPerCard):
        gameBoard = gameBoard + "]  "
        currentCard = 0
        lws = boardWidth // 2 # lws is leftWhiteSpace
        while(lws>0):
            gameBoard = gameBoard + " "
            lws = lws - 1
        while(currentCard<cardsInHand): 
            gameBoard = gameBoard + playerHandString[currentCard][currentRow]
            gameBoard = gameBoard + " "
            currentCard = currentCard + 1
        rws = boardWidth // 2 # rws is rightWhiteSpace
        if( (len(playerHandString) % 2) == 1 ):
            rws = rws - 1 # removing an extra whitespce when printing odd numbers of cards
        while(rws>0):
            gameBoard = gameBoard + " "
            rws = rws - 1
        gameBoard = gameBoard + "  [\n"
        currentRow = currentRow + 1
    gameBoard = gameBoard + "|                                                  |\n"
    gameBoard = gameBoard + "+++==========||==========||==========||==========+++\n"
    print(gameBoard)
        
# testing printGame
def testPrintGame():
    print("printing a board of a one card dealer hand\n")
    gameStatus = {"dealerHand": {"upCard": ["Q-Spades"]},"playerHand": {"cards": ["K-Clubs","10-Diamonds"]} }
    printGame(gameStatus)
    print("\n")
    print("printing a board of a two card dealer hand\n")
    gameStatus = {"dealerHand": {"upCard": ["8-Spades","A-Spades"]},"playerHand": {"cards": ["K-Clubs","10-Diamonds"]} }
    printGame(gameStatus)
    print("\n")
    print("printing a board of a three card dealer hand\n")
    gameStatus = {"dealerHand": {"upCard": ["8-Spades", "A-Spades", "Q-Clubs"]},"playerHand": {"cards": ["K-Clubs","10-Diamonds"]} }
    printGame(gameStatus)
    print("printing a board of a three card player and one card dealer hand\n")
    gameStatus = {"dealerHand": {"upCard": ["Q-Spades"]},"playerHand": {"cards": ["K-Clubs","2-Diamonds","7-Hearts"]} }
    printGame(gameStatus)
    print("\n")
    print("printing a board of a three card player two card dealer hand\n")
    gameStatus = {"dealerHand": {"upCard": ["8-Spades","A-Spades"]},"playerHand": {"cards": ["K-Clubs","2-Diamonds","7-Hearts"]} }
    printGame(gameStatus)
    print("\n")
    print("printing a board of a three card player three card dealer hand\n")
    gameStatus = {"dealerHand": {"upCard": ["8-Spades", "A-Spades", "Q-Clubs"]},"playerHand": {"cards": ["K-Clubs","2-Diamonds","7-Hearts"]} }
    printGame(gameStatus)
    print("\n")
    print("printing a board with a split player Hand and a three card dealer hand\n")
    gameStatus = {"dealerHand": {"upCard": ["8-Spades", "A-Spades", "Q-Clubs"]},"playerHand": {"cards": ["5-Diamonds","5-Diamonds","7-Hearts"]} }
    printGame(gameStatus)

# do-while loops don't work!
def main():
    wantToPlay = True
    gameDeck = newDeck()
    while(wantToPlay):
        results = newGame(gameDeck)
        print(results)
        while(answer!="Y" and answer!="N"):
            try:
                choice = input("Do you want to play again? Y/N")
            except:
                print("Input must be Y or N")
        if(choice=="Y"):
            print("Gettin' pretty cold back east...")
        if(choice=="N"):
            print("Suit yourself Darlin'")
            wantToPlay = False
    

testPrintGame()
