import wx
from random import randint
import sys
sys.setrecursionlimit(2000)


class Window(wx.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.images_dict = {0: "images\\0.png", 1: "images\\1.png", 2: "images\\2.png", 3: "images\\3.png", 4: "images\\4.png", 5: "images\\5.png",
                            6: "images\\6.png", 7: "images\\7.png", 8: "images\\8.png", 9: "images\\hidden.png", 10: "images\\bomb.png",
                            11: "images\\bomb_hit.png", 12: "images\\wrong_flag.png", 13: "images\\flag.png"}
        self.initUI()

    def initUI(self):
        self.SetTitle("Minesweeper")
        self.CreateMenu()
        self.CreatePanel()
        self.Center()
        self.Show()

    def CreateMenu(self):
        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap("images\\flag.png"))
        self.SetIcon(icon)
        self.status_bar = self.CreateStatusBar()
        menu_bar = wx.MenuBar()
        game_btn = wx.Menu()
        new_game_item = wx.MenuItem(
            game_btn, -1, "New Game\tCtrl+R", "Start a new game.")
        beginner_item = wx.MenuItem(
            game_btn, -1, "Beginner\tCtrl+B", "height = 9 width = 9 bombs = 10")
        intermediate_item = wx.MenuItem(
            game_btn, -1, "Intermediate\tCtrl+I", "height = 16 width = 16 bombs = 40")
        expert_item = wx.MenuItem(
            game_btn, -1, "Expert\tCtrl+E", "height = 16 width = 30 bombs = 99")
        quit_item = wx.MenuItem(
            game_btn, -1, "Quit\tCtrl+Q", "Quit the program.")

        game_btn.Append(new_game_item)
        game_btn.Append(beginner_item)
        game_btn.Append(intermediate_item)
        game_btn.Append(expert_item)
        game_btn.Append(quit_item)

        self.SetMenuBar(menu_bar)
        menu_bar.Append(game_btn, "Game")
        game_btn.InsertSeparator(1)
        game_btn.InsertSeparator(5)

        self.Bind(wx.EVT_MENU, self.NewGame, new_game_item)
        self.Bind(wx.EVT_MENU, self.SetBeginnerMode, beginner_item)
        self.Bind(wx.EVT_MENU, self.SetIntermediateMode, intermediate_item)
        self.Bind(wx.EVT_MENU, self.SetExpertMode, expert_item)
        self.Bind(wx.EVT_MENU, self.Quit, quit_item)

    def CreatePanel(self):
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour("#C3C3C3")
        self.SetSize(241, 307) 
        self.rows, self.columns, self.bombs = 9, 9, 10
        self.uncover_to_win = self.rows * self.columns - self.bombs
        self.uncovered = 0
        self.CreateGameField()

    def NewGame(self, e):
        self.panel.DestroyChildren()
        self.uncovered = 0
        self.CreateGameField()

    def SetBeginnerMode(self, e):
        self.panel.DestroyChildren()
        self.SetSize(241, 307)  # formula is (columns*25+16,rows*25+82)
        self.Center()
        self.rows, self.columns, self.bombs = 9, 9, 10
        self.uncover_to_win = self.rows * self.columns - self.bombs
        self.uncovered = 0
        self.CreateGameField()

    def SetIntermediateMode(self, e):
        self.panel.DestroyChildren()
        self.SetSize(416, 482)
        self.Center()
        self.rows, self.columns, self.bombs = 16, 16, 40
        self.uncover_to_win = self.rows * self.columns - self.bombs
        self.uncovered = 0
        self.CreateGameField()

    def SetExpertMode(self, e):
        self.panel.DestroyChildren()
        self.SetSize(766, 482)
        self.Center()
        self.rows, self.columns, self.bombs = 16, 30, 99
        self.uncover_to_win = self.rows * self.columns - self.bombs
        self.uncovered = 0
        self.CreateGameField()

    def Quit(self, e):
        self.Close()

    def PlantBombs(self):
        cnt = self.bombs
        while cnt > 0:
            m = randint(0, self.rows-1)
            n = randint(0, self.columns-1)
            if self.matrix[m][n] == 10:
                continue
            self.matrix[m][n] = 10  # 10 denotes a bomb
            cnt -= 1

    def AddClues(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.matrix[i][j] == 10:
                    self.TraverseAdjacent(i, j)

    def TraverseAdjacent(self, i, j):
        has_north = i != 0
        has_east = j != self.columns - 1
        has_south = i != self.rows - 1
        has_west = j != 0
        has_north_east = has_north and has_east
        has_south_east = has_south and has_east
        has_south_west = has_south and has_west
        has_north_west = has_north and has_west

        if has_north:                  
            if self.matrix[i-1][j] != 10:
                self.matrix[i-1][j] += 1
        if has_north_west:              
            if self.matrix[i-1][j-1] != 10:
                self.matrix[i-1][j-1] += 1
        if has_north_east:   
            if self.matrix[i-1][j+1] != 10:
                self.matrix[i-1][j+1] += 1
        if has_west:
            if self.matrix[i][j-1] != 10:
                self.matrix[i][j-1] += 1
        if has_east:
            if self.matrix[i][j+1] != 10:
                self.matrix[i][j+1] += 1
        if has_south:
            if self.matrix[i+1][j] != 10:
                self.matrix[i+1][j] += 1
        if has_south_west:
            if self.matrix[i+1][j-1] != 10:
                self.matrix[i+1][j-1] += 1
        if has_south_east:
            if self.matrix[i+1][j+1] != 10:
                self.matrix[i+1][j+1] += 1

    def AddCoverImages(self):
        w_spacing, h_spacing, increment = 0, 0, 25
        for i in range(self.rows):
            for j in range(self.columns):
                tile = wx.Button(self.panel, pos=(w_spacing, h_spacing), size=(
                    25, 25), name="" + str(i) + " " + str(j))
                tile.SetBitmap(wx.Bitmap(self.images_dict[9]))
                tile.Bind(wx.EVT_BUTTON, self.OnClick)
                tile.Bind(wx.EVT_LEFT_DOWN, self.OnHold)
                tile.Bind(wx.EVT_LEFT_UP, self.OnRelease)
                tile.Bind(wx.EVT_RIGHT_DOWN, self.SetFlag)
                self.tile_matrix[i][j] = tile
                w_spacing += increment
            w_spacing = 0
            h_spacing += increment

    def CreateGameField(self):
        self.panel.Hide()
        self.matrix = [[0 for i in range(self.columns)]
                       for j in range(self.rows)]
        self.tile_matrix = [[0 for i in range(self.columns)]
                            for j in range(self.rows)]
        self.flagged_matrix = [[False for i in range(self.columns)]
                               for j in range(self.rows)]
        self.open_field_matrix = [[False for i in range(self.columns)]
                                  for j in range(self.rows)]
        self.PlantBombs()
        self.AddClues()
        self.AddCoverImages()
        self.status_bar.SetStatusText(" ")
        self.panel.Show()

    def GetIndexes(self, obj):
        name = obj.GetEventObject().GetName()
        indexes = name.split()
        row, col = int(indexes[0]), int(indexes[1])
        return row, col

    def SetFlag(self, e):
        row, col = self.GetIndexes(e)
        if self.flagged_matrix[row][col] == False and self.open_field_matrix[row][col] == False:
            self.flagged_matrix[row][col] = True
            self.tile_matrix[row][col].SetBitmap(
                wx.Bitmap(self.images_dict[13]))
        elif self.flagged_matrix[row][col] == True and self.open_field_matrix[row][col] == False:
            self.flagged_matrix[row][col] = False
            self.tile_matrix[row][col].SetBitmap(
                wx.Bitmap(self.images_dict[9]))

    def OnHold(self, e):
        row, col = self.GetIndexes(e)
        if self.flagged_matrix[row][col] == False and self.open_field_matrix[row][col] == False:
            self.tile_matrix[row][col].SetBitmap(
                wx.Bitmap(self.images_dict[0]))
        # print("true")
        e.Skip()

    def OnRelease(self, e):
        row, col = self.GetIndexes(e)
        if self.flagged_matrix[row][col] == False and self.open_field_matrix[row][col] == False:
            self.tile_matrix[row][col].SetBitmap(
                wx.Bitmap(self.images_dict[9]))
        # print("false")
        e.Skip()

    def OnClick(self, e):
        row, col = self.GetIndexes(e)
        if self.flagged_matrix[row][col] == False:
            self.Defuse(row, col)

    def Defuse(self, row, col):
        if self.matrix[row][col] == 10:
            self.Explode(row, col)
        elif self.matrix[row][col] >= 0 and self.matrix[row][col] <= 10:
            self.Explore(row, col)

        if self.uncovered == self.uncover_to_win:
            self.status_bar.SetStatusText("You Won!")
            for i in range(self.rows):
                for j in range(self.columns):
                    self.tile_matrix[i][j].Unbind(wx.EVT_BUTTON)
                    self.tile_matrix[i][j].Unbind(wx.EVT_LEFT_DOWN)
                    self.tile_matrix[i][j].Unbind(wx.EVT_LEFT_UP)
                    self.tile_matrix[i][j].Unbind(wx.EVT_RIGHT_DOWN)

    def Explore(self, row, col):
        img_index = self.matrix[row][col]
        has_north = row != 0
        has_east = col != self.columns - 1
        has_south = row != self.rows - 1
        has_west = col != 0
        has_north_east = has_north and has_east
        has_south_east = has_south and has_east
        has_south_west = has_south and has_west
        has_north_west = has_north and has_west

        if self.matrix[row][col] >= 0 and self.matrix[row][col] < 10 and self.flagged_matrix[row][col] == False and self.open_field_matrix[row][col] == False:
            self.tile_matrix[row][col].SetBitmap(
                wx.Bitmap(self.images_dict[img_index]))
            self.open_field_matrix[row][col] = True
            self.uncovered += 1

        if self.matrix[row][col] == 0:
            self.matrix[row][col] = - 1
            if has_north:
                self.Explore(row-1, col)  # explore north
            if has_north_east:
                self.Explore(row-1, col+1)  # explore north east
            if has_east:
                self.Explore(row, col+1)  # explore east 
            if has_south_east:
                self.Explore(row+1, col+1)  # explore south east
            if has_south:
                self.Explore(row+1, col)  # explore south
            if has_south_west:
                self.Explore(row+1, col-1)  # explore south west
            if has_west:
                self.Explore(row, col-1)  # explore west
            if has_north_west:
                self.Explore(row-1, col-1)  # explore north west
            

    def Explode(self, row, col):
        self.status_bar.SetStatusText("You Lost!")
        for i in range(self.rows):
            for j in range(self.columns):
                self.tile_matrix[i][j].Unbind(wx.EVT_BUTTON)
                self.tile_matrix[i][j].Unbind(wx.EVT_LEFT_DOWN)
                self.tile_matrix[i][j].Unbind(wx.EVT_LEFT_UP)
                self.tile_matrix[i][j].Unbind(wx.EVT_RIGHT_DOWN)
                if self.open_field_matrix[i][j] == True:
                    continue
                if self.flagged_matrix[i][j] == True:
                    if self.matrix[i][j] != 10:
                        self.tile_matrix[i][j].SetBitmap(
                            wx.Bitmap(self.images_dict[12]))
                else:
                    self.tile_matrix[i][j].SetBitmap(
                        wx.Bitmap(self.images_dict[self.matrix[i][j]]))
        self.tile_matrix[row][col].SetBitmap(wx.Bitmap(self.images_dict[11]))


if __name__ == "__main__":
    app = wx.App()
    Window(None)
    app.MainLoop()