from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        peg1 = []
        peg2 = []
        peg3 = []
        allPegs = [peg1, peg2, peg3]
        fullRep = []
        
        facts = self.kb.facts
        for fact in facts:
            if(fact.statement.predicate == "on"):
                if(fact.statement.terms[1].term.element == "peg1"):
                    disk = (fact.statement.terms[0].term.element).split("disk")[1]
                    peg1.append(int(disk))
                if(fact.statement.terms[1].term.element == "peg2"):
                    disk = (fact.statement.terms[0].term.element).split("disk")[1]
                    peg2.append(int(disk))
                if(fact.statement.terms[1].term.element == "peg3"):
                    disk = (fact.statement.terms[0].term.element).split("disk")[1]
                    peg3.append(int(disk))
                    
        for peg in allPegs:
            peg = tuple(sorted(peg))
            fullRep.append(peg)
        fullRep = tuple(fullRep)
        #print(fullRep)
        return fullRep        

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        
        disk = (movable_statement.terms[0].term.element)
        initPeg = (movable_statement.terms[1].term.element)
        destPeg = (movable_statement.terms[2].term.element)
        
        #remove facts that are no longer true, involving predicates on, top, and empty
        removeOn = parse_input("fact: (on " + str(disk) + " " + str(initPeg) + ")")
        removeTop = parse_input("fact: (on " + str(disk) + " " + str(initPeg) + ")")
        self.kb.kb_retract(removeOn)
        self.kb.kb_retract(removeTop)
        if(self.kb.kb_ask(parse_input("fact: (empty " + str(destPeg) + ")"))):
            self.kb.kb_retract(parse_input("fact: (empty " + str(destPeg) + ")"))

        
        #assert facts that are now true
        addOn = parse_input("fact: (on " + str(disk) + " " + str(destPeg) + ")")
        addTop = parse_input("fact: (on " + str(disk) + " " + str(destPeg) + ")")
        addEmpty = (parse_input("fact: (empty " + str(initPeg) + ")"))
        self.kb.kb_assert(addOn)
        self.kb.kb_assert(addTop)
        
        if(self.kb.kb_ask(parse_input("fact: (on " + str(disk) + " ?X)")) == False):
            self.kb.kb_assert(addEmpty)
        
        return        


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        row1 = []
        row2 = []
        row3 = []
        allRows = [row1, row2, row3]
        fullRep = []
        
        facts = self.kb.facts
        for fact in facts:
            if(fact.statement.predicate == "coordinate"):
                
                if((fact.statement.terms[0].term.element) == "empty"):
                    tileNum = -1
                else:
                    tileNum = int((fact.statement.terms[0].term.element).split("tile")[1])

                xpos = int((fact.statement.terms[1].term.element).split("pos")[1])
                ypos = int((fact.statement.terms[2].term.element).split("pos")[1])

                
                if(ypos == 1):
                    row1.append([xpos, tileNum])
                if(ypos == 2):
                    row2.append([xpos, tileNum])
                if(ypos == 3):
                    row3.append([xpos, tileNum])

        r1 = []
        r2 = []
        r3 = []

        for row in allRows:
            row = sorted(row, key=lambda x: x[0])

            for tile in row:
                if(len(r1) < 3):
                    r1.append(tile[1])
                    continue
                if(len(r2) < 3):
                    r2.append(tile[1])
                    continue
                if(len(r3) < 3):
                    r3.append(tile[1])
                    continue
        allRs = [r1, r2, r3]
        
        for r in allRs:
            r = tuple(r)
            fullRep.append(r)         
        fullRep = tuple(fullRep)

        return fullRep        

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        tile = (movable_statement.terms[0].term.element)
        initX = (movable_statement.terms[1].term.element)
        initY = (movable_statement.terms[2].term.element)
        destX = (movable_statement.terms[3].term.element)
        destY = (movable_statement.terms[4].term.element)        
        
        #remove facts that are no longer true, involving predicates on, top, and empty
        removeCoordinate = parse_input("fact: (coordinate " + str(tile) + " " + str(initX) + " " + str(initY) + ")")
        removeEmpty = ("fact: (coordinate empty " + str(destX) + " " + str(destY) + ")")
        self.kb.kb_retract(removeCoordinate)
        #self.kb.kb_retract(removeEmpty)
        
        #assert facts that are now true
        assertCoordinate = parse_input("fact: (coordinate " + str(tile) + " " + str(destX) + " " + str(destY) + ")")
        assertEmpty = parse_input("fact: (coordinate empty " + str(initX) + " " + str(initY) + ")")
        self.kb.kb_assert(assertCoordinate)             

        return        

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
