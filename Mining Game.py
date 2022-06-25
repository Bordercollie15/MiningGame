from tkinter import *
from tkinter import messagebox
import random
import time
class MinesweeperCell(Label):
    '''represents a Minesweeper cell'''
 
    def __init__(self,master,coord,isBomb = False,neighborBombs=0):
        '''MinesweeperCell(master,coord,isBomb,neighborBombs)
        represents a cell on the Minesweeper frame'''
        Label.__init__(self,master,height=1,width=2,text='',\
                        bg='white',font=('Arial',24),relief=RAISED)
        if self.master.height >= 20 or self.master.width >= 35:
            Label.__init__(self,master,height=1,width=2,text='',\
                           bg='white',font=('Arial',12),relief=RAISED)
        self.colormap = ['','blue','darkgreen','red','purple','maroon','cyan','black','dim gray'] #List of the colors of the numbers
        self.coord = coord  # (row,column) coordinate tuple
        self.row = self.coord[0]
        self.col = self.coord[1]
        self.number = 0  # 0 is an empty cell
        self.readOnly = False     # starts as a changeable cell
        self.exposed = False  # starts as not exposed
        self.neighborBombs = neighborBombs # The number in the cell, the number of bombs by it
        # sets up the listeners
        self.bind('<Button-1>',self.openMine)
        self.bind('<Button-2>',self.flagMine)
        self.isBomb = isBomb
        self.cellColor = self.colormap[self.neighborBombs]
        
    def unFlag(self):
        '''take the flag off the cell'''
        self['text'] = ''
        self.readOnly = False

    def get_coord(self):
        '''returns a tuple of the coordinates'''
        return self.coord

    def is_bomb(self):
        '''returns boolean of whether it is a bomb or not'''
        return self.isBomb
    
    def add_neighbor(self):
        '''MinesweeperSquare.add_neighbor()
        Increases the number of bombs written on the square.'''
        if self.isBomb == False:
            self.neighborBombs += 1
            self.cellColor = self.colormap[self.neighborBombs]

    def is_read_only(self):
        '''checks whether it is clickable'''
        return self.readOnly
    
    def is_flagged(self):
        '''checks whether the cell is flagged'''
        if self['text'] == '⚐':
            return True
        return False
    
    def turn_into_bomb(self):
        '''turns the cell into a cell with a bomb'''
        self.isBomb = True
        
    def is_win(self):
        '''finds out if all bombs are flagged'''
        goodValue = 0
        for bombs in self.master.bombList:
            if bombs.is_flagged() == True:
                goodValue +=1
        if len(self.master.bombList) == goodValue: #If all the bombs are flagged
            endtime = time.time() # It ends the stopwatch
            sec = int(round(endtime - self.master.starttime,0))
            mins = sec // 60
            sec = sec % 60
            hours = mins // 60
            mins = mins % 60
            text = "You took {0} hours, {1} minutes, and {2} seconds to win!!".format(int(hours),int(mins),sec,)
            messagebox.showinfo('Minesweeper','Congratulations -- you won! \n'+text,parent=self)
        if len(self.master.bombList) == 0:
            pass
    def flagMine(self,event):
        '''flags the cell'''
        if self.master.bombLabel['text']=='Impossible!': #If the player placed too many flags
            self.master.bombLabel['bg']= 'light blue'
        else:
            self.master.bombLabel['bg']='white'
        if self.is_read_only() == False:
            if self.master.flags > -1:
                self['text'] = '⚐'
                self.configure(fg='red')
                self.readOnly = True
                self.is_win()
                self.master.flags -= 1
            if self.master.flags > -1:
                self.master.bombLabel['text'] = self.master.flags
                
            else:
                self.master.bombLabel['text'] = 'Impossible!'
                
        elif self.is_flagged() == True:
            self.unFlag()
            self.master.flags += 1
            self.master.bombLabel['text'] = self.master.flags
   
    def end_show_bombs(self):
        '''Will uncover the bombs'''
        self['text'] = '✹'
        self['bg'] = 'lightgrey'
        self['fg'] = 'red'
        self['relief'] = SUNKEN
        self.readOnly = True
    
    def openMine(self,event):
        '''Exposes the number in the cell, or bomb'''
        if not self.readOnly and (self.isBomb is False):  # only act on non-read-only cells and cells that are not bombs 
            self.focus_set()  
            #self.highlighted = True
            self['bg'] = 'lightgrey'
            self['relief'] = SUNKEN
            self.readOnly = True
            self.is_win()
            if self.neighborBombs == 0:
                self['text'] = ''
                self.master.auto_expose(self)
            else:
                self['text'] = self.neighborBombs
                self['fg'] = self.cellColor
        if not self.readOnly and (self.isBomb is True): # If it is an uncovered and unflagged bomb
            self['text'] = '✹'
            self['bg'] = 'lightgrey'
            self['fg'] = 'red'
            messagebox.showerror('Minesweeper','KABOOM! You lose.',parent=self) 
            
            self['relief'] = SUNKEN
            self.readOnly = True
            for bomb in self.master.bombList:
                bomb.end_show_bombs()
            
    
class MinesweeperFrame(Frame):
    '''object for a Minesweeper grid'''

    def __init__(self,master,height,width,numBombs):
        '''MinesweeperFrame(master,height,width,numBombs)
        creates a new Minsweeper Frame'''
        # Creates a new frame
        Frame.__init__(self,master,bg='light grey')
        colormap = ['','blue','darkgreen','red','purple','maroon','cyan','black','dim gray']
        self.grid()
        self.numBombs = numBombs
        self.flags = numBombs
        self.bombList = []
        self.height = height
        self.width = width
        self.starttime = time.time()
        #Make the gaps between the cells
        for n in range(1,2*width-1,2):
            if self.height >= 20 or self.width >= 35:
                self.rowconfigure(n,minsize=0)
                self.columnconfigure(n,minsize=0)
            else:
                self.rowconfigure(n,minsize=1)
                self.columnconfigure(n,minsize=1)
        
        self.rowconfigure(2*height-1,minsize=10) # Bigger space at the bottom of the grid
        # create buttons
        self.buttonFrame = Frame(self,bg='white')  # Make a new frame to hold the buttons
        Button(self.buttonFrame,text='➳➵➺ Time',command=self.arrow).grid(row=0,column=0) #Time you have taken so far
        Button(self.buttonFrame,text='Game rules',command=self.print_rules).grid(row=0,column=1) # How to play minesweeper
        Button(self.buttonFrame,text='About',command=self.history).grid(row=0,column=2) #History of the Minesweeper game
        Button(self.buttonFrame,text='Size',command=self.show_size).grid(row=0,column=3)
        
        self.bombLabel = Label(self.buttonFrame,height=1,text=self.flags,\
                       bg='white',font=('Arial',12),relief=RAISED)
        self.bombLabel.grid(row=1,column=1)
        self.bombLabel.bind('<Button-1>',self.tell_player)
        if self.height >= 20 or self.width >= 35:  # This is so the grid fits on the screen
            self.buttonFrame.grid(row=2*height,column=0,columnspan=40)
        else:
            self.buttonFrame.grid(row=2*height,column=0,columnspan=17)
        # MAKE THE CELLS
        self.cells = [] # Create a list for the cells
        for row in range(height):
            rowCells = []
            for column in range(width):
                coord = (row,column)
                
                mine = MinesweeperCell(self,coord)
                rowCells.append(mine)
                mine.grid(row=2*row,column=2*column)
            self.cells.append(rowCells)
        for bomb in range(self.numBombs):
            self.make_bombs(bomb)
        self.cell_number()
        
       
    def auto_expose(self,cell):
        '''Exposes all cells next to the empty cells'''
        rowCol = cell.get_coord()
        # Realized loops are a better way to do this, but...
        # If you do that, you can make it try every combination of two numbers from -1, 0, 1, and check if they are bombs
        # Then do openMine
        # Just a note for later, sorry if I forget to do it!
        # Expose the squares on top,bottom,right,left
        if rowCol[1] < self.width-1 and not self.cells[rowCol[0]][rowCol[1]+1].is_bomb():
            self.cells[rowCol[0]][rowCol[1]+1].openMine('')
        if rowCol[0] > 0 and not self.cells[rowCol[0]-1][rowCol[1]].is_bomb():
            self.cells[rowCol[0]-1][rowCol[1]].openMine('')  # The string is because the method has to take an event to work
        if rowCol[0] < self.height-1 and not self.cells[rowCol[0]+1][rowCol[1]].is_bomb():
            self.cells[rowCol[0]+1][rowCol[1]].openMine('')
        if rowCol[1] > 0 and not self.cells[rowCol[0]][rowCol[1]-1].is_bomb():
            self.cells[rowCol[0]][rowCol[1]-1].openMine('')
        
        # Diagonals
        if rowCol[1] < self.width-1 and rowCol[0] < self.height-1 and not self.cells[rowCol[0]+1][rowCol[1]+1].is_bomb():
            self.cells[rowCol[0]+1][rowCol[1]+1].openMine('')
        if rowCol[1] < self.width-1 and rowCol[0] > 0 and not self.cells[rowCol[0]-1][rowCol[1]+1].is_bomb():
            self.cells[rowCol[0]-1][rowCol[1]+1].openMine('')
        if rowCol[0] < self.height-1 and rowCol[1] > 0 and not self.cells[rowCol[0]+1][rowCol[1]-1].is_bomb():
            self.cells[rowCol[0]+1][rowCol[1]-1].openMine('')
        if rowCol[1] > 0 and rowCol[0] > 0 and not self.cells[rowCol[0]-1][rowCol[1]-1].is_bomb():
            self.cells[rowCol[0]-1][rowCol[1]-1].openMine('')
            
    def make_bombs(self,bomb):
        '''Makes a bomb'''
        RowCell = random.randrange(self.height)
        ColumnCell = random.randrange(self.width)
        bomb = self.cells[RowCell][ColumnCell]
        if bomb in self.bombList:
            self.make_bombs(bomb)
        else:
            bomb.turn_into_bomb()
            self.bombList.append(bomb)

    def cell_number(self):
        '''MinesweeperFrame.set_numbers()
        Sets up the numbers to show number of neighboring bombs'''
        for row in range(self.height): # Does this for every cell in every row and column
            for col in range(self.width): 
                if self.cells[row][col].is_bomb() == False: #Checks whether the cell contains a bomb
                    cell = self.cells[row][col]
                    if row < self.height-1 and self.cells[row+1][col].is_bomb(): #Checks the cell below the current cell
                        cell.add_neighbor() #Adds to the number on the cell
                    if row > 0 and self.cells[row-1][col].is_bomb(): #Above the cell
                        cell.add_neighbor()
                    if col < self.width-1 and self.cells[row][col+1].is_bomb(): #Right side of the cell
                        cell.add_neighbor()
                    if col > 0 and self.cells[row][col-1].is_bomb(): #Left side neighbor
                        cell.add_neighbor()
                    if col > 0 and row > 0 and self.cells[row-1][col-1].is_bomb(): #Upper left corner
                        cell.add_neighbor()
                    if col > 0 and row < self.height-1 and self.cells[row+1][col-1].is_bomb():  #bottom left corner
                        cell.add_neighbor()
                    if row > 0 and col < self.width-1 and self.cells[row-1][col+1].is_bomb(): #Upper right corner
                        cell.add_neighbor()
                    if row < self.height-1 and col < self.width-1 and self.cells[row+1][col+1].is_bomb(): #bottom right corner cell
                        cell.add_neighbor()
                        
    def arrow(self):
        '''time taken in message'''
        soFar = time.time() 
        sec = int(round(soFar - self.starttime,0))  #finds the time 
        mins = sec // 60
        sec = sec % 60
        hours = mins // 60
        mins = mins % 60
        messagebox.showinfo('Minesweeper',"You took {0}:{1}:{2} so far, good job!".format(int(hours),int(mins),sec,),parent=self)

    def print_rules(self):
        '''Minesweeper.print_rules()
        shows how to play Minesweeper'''
        
        messagebox.showerror("Minesweeper", "The point of the game is to uncover all the squares that don't"\
              " have bombs by clicking on them. \nFlag the squares that you think have bombs "\
              "by right clicking on them, or tapping with two fingers on a computer(Mac). "\
              "Be careful because if you uncover a square with a bomb, the game ends!",parent=self)
              

    def show_size(self):
        '''MinsweeperFrame.show_size()
        shows the size of Minesweeper grid'''
        messagebox.showinfo('Minesweeper','☺ This is a '+str(self.height)+' by '+str(self.width)+' board!'\
                            ,parent=self)

    def history(self):
        '''Minesweeper.history()
        shows who invented Minesweeper'''
        messagebox.showinfo('Minesweeper','The Minesweeper game was invented by Robert Donner'\
                            ' and Curt Johnson, who worked in Microsoft, in 1900s.'\
                            ' It was originally created for Windows, but now is a very '\
                            'popular game',parent=self)
    def tell_player(self,event):
        '''Minesweeper.tell_player('')
        shows how to use flags'''
        messagebox.showinfo('Minesweeper','This is the number of flags you have left. Use them to '\
                            'flag bombs, by right-clicking the chosen square.',parent=self)

    

def play_minesweeper(height,width,numBombs):
    if height * width * 0.05 > numBombs:
        print("More bombs, or less cells please! Computer can't handle so many. Plus, more bombs makes the game more fun!!")
        return
    root = Tk()
    root.title('Minesweeper')
    game = MinesweeperFrame(root,height,width,numBombs)
    game.mainloop()
play_minesweeper(25,28,100)

#Sorry if error message shows up, add more bombs or decrease the number of cells
#The reason is auto expose uses a very large loop that repeats many times
#
