import math
import random
import string

WORDLIST_FILENAME = "words.txt"


vowels = 'aeiou'
consonants = 'bcdfghjklmnpqrstvwxyz'
hand_size = 7
SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*':0
}

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)                   #dont need this function, thought that it might be useful but its not needed.
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

def get_word_score(word,n):
    """Returns the score for a word. Assumes the word is a
    valid word.
    The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.
"""
    word = word.lower()
    pts = 0
    for e in word:
        pts = SCRABBLE_LETTER_VALUES[e] + pts
    sec_comp = max((7*len(word) - 3*(n-len(word))),1)
    return pts*sec_comp

#print(get_word_score('weed',7))

def display_hand(hand):
    """ Displays the letters currently in the hand."""
    for e in hand:
        for i in range(hand[e]):
            print(e, end = ' ')
    print()

def deal_hand(n):
    """ Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.
"""
    hand  = {}
    num_vowels = int(math.ceil(n/3))
    hand['*'] = 1
    for i in range(num_vowels-1):
        x = random.choice(vowels)
        hand[x] = hand.get(x,0) + 1

    for i in range(num_vowels, n):
        x = random.choice(consonants)
        hand[x] = hand.get(x,0) + 1
    return hand

def update_hand(hand,word):
    """ Letters in word that don't
    appear in hand are ignored. Letters that appear in word more times
    than in hand dont result in a negative count; instead, sets the
    count in the returned hand to 0."""
    hand1 = hand.copy()
    word = word.lower()
    for e in word:
        try:
            if hand1[e]>0:
                hand1[e] -= 1
        except:
            pass
    return hand1

hand = {'e':1, 'v':2, 'n':1, 'i':1, 'l':2}
#display_hand(hand)
#print(update_hand(hand,'Evil'))
def is_valid_word(word,hand,word_list):
    """checks if the word is valid. Words valid if its in the word list and it can be spelled from the letters in the hand."""
    hand1 = hand.copy()
    word = word.lower()
    if '*' not in word:                                     
        if word not in word_list:
            return False
        else:
            for e in word:
                if e not in hand1:
                    return False
                else:
                    if hand1[e] == 0:
                        return False
                    else:
                        hand1[e] -= 1
            return True
        
    else:
        pw = []                     #possible word list
        for v in vowels:
            if word.replace('*',v) in  word_list:
                pw.append(word.replace('*',v))
        if len(pw) >=1:                 #check if the letters in word are in the hand
            for e in word:
                if e not in hand1:
                    return False
                else:
                    if hand1[e] == 0:
                        return False
                    else:
                        hand1[e] -= 1
            return True            
        

def calc_handlen(hand):
    """returns the total number of letters in the hand"""
    n= 0    
    for e in hand.values():
        n += e
    return n

#handd = {'j':2, 'l':2, 'w':1, 'n':2, 'y':2, 'b':2, 'o':2, 's':1, 'i':1, 'e':1, '*':1}

#print(calc_handlen(handd))

def play_hand(hand, word_list):
    """displays hand, asks user for word. word(valid or invalid) uses letters in the hand.
     An invalid word is rejected, asks again till there are letters in the hand or till the user doesnt tells it to stop.
      Every correct word's score is displayed and added to the total of the hand. """
    total = 0
    while calc_handlen(hand) != 0:
        display_hand(hand)
        word = input('Enter word or "!!" to stop: ')
        if word == '!!':
            break
        else:
            if is_valid_word(word, hand, word_list):
                score = get_word_score(word,calc_handlen(hand))
                print(word, 'earned', score, 'points')
                total += score
            else:
                print('Invalid Word')
            hand = update_hand(hand,word)
    print('total for this hand is:', total )
    return(total)        

def substitute_hand(hand,letter):
    """allows the user to change all instances of a letter of his/her choice to another random letter that was not already in the hand"""
    listh = list(hand.keys())
    lista2z = list(vowels+consonants)
    for e in listh:
        if e in lista2z[:]:
            lista2z.remove(e)
    if letter not in listh:
        return hand
    else:
        count = hand[letter]
        letter2 = random.choice(lista2z)
        hand[letter] = 0
        hand[letter2] = count
        return hand


def play_game(word_list):
    """Allows the user to play multiple times by asking number of hands he/she wants to play.
    adds the total of each hand to the grand total of the game.Asks the user if he/she wants to substitute a letter and also
      if he/she wants to replay a particular hand
    """
    num_hands = int(input('Enter how many times do you want to play the hand:'))
    i = 0
    subs = 0
    rep_no = 0                          #replay number
    grand_total = 0
    while(i < num_hands):
        hand_total = 0
        tot2 = 0
        hand = deal_hand(hand_size)
        display_hand(hand)

        if subs == 0:
            decision = input('Do you want to substitute a letter? yes or no.')
            if decision.lower() == 'yes':
                letr = input('which letter do you want to replace: ')
                letter = letr.lower()
                hand = substitute_hand(hand,letter)
                subs = 1
        tot1 = play_hand(hand, word_list)
        
        if rep_no == 0:

            rply = input('Do you want to replay the hand? yes or no')
            replay = rply.lower()
            if replay == 'yes':
                tot2 = play_hand(hand, word_list)
                rep_no = 1
        hand_total  = max(tot1,tot2)
        grand_total += hand_total
        i+=1
    return grand_total



if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)

