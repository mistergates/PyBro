import wx
import wx.html2 
import os


class Icons:
    '''Holds icon wx.Bitmap objects for easy reference
    '''
    def __init__(self):
        _icons_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'icons')
        self.refresh = wx.Bitmap(os.path.join(_icons_folder, 'refresh.png'), wx.BITMAP_TYPE_ANY)
        self.send = wx.Bitmap(os.path.join(_icons_folder, 'send.png'), wx.BITMAP_TYPE_ANY)
        self.forward = wx.Bitmap(os.path.join(_icons_folder, 'forward.png'), wx.BITMAP_TYPE_ANY)
        self.back = wx.Bitmap(os.path.join(_icons_folder, 'back.png'), wx.BITMAP_TYPE_ANY)


class MenuBar:
    '''Menu bar (File, Help, etc...)
    '''
    def __init__(self, frame):
        # Setting up the menus
        file_menu= wx.Menu()
        file_menu.Append(wx.ID_EXIT, "&Exit", "Terminate the program")

        help_menu = wx.Menu()
        help_menu.Append(wx.ID_ABOUT, "&About", "Information about this program")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(file_menu, "&File") # Adding the "file_menu" to the MenuBar
        menuBar.Append(help_menu, "&Help") # Adding the "file_menu" to the MenuBar
        frame.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.


class AddressBar:
    '''Address bar and buttons
    '''
    def __init__(self, frame):
        # init icons class
        icons = Icons()

        # Address (URL) bar / Binds
        frame.address_bar = wx.TextCtrl(frame.panel, value="", size=(10000, 25), style=wx.TE_PROCESS_ENTER)
        frame.address_bar.Bind(wx.EVT_TEXT_ENTER, frame.load_url)

        # Refresh Button / Binds
        frame.refresh = wx.BitmapButton(frame.panel, id=wx.ID_REFRESH, bitmap=icons.refresh, size=(25, 25), style=wx.WXK_F5)
        frame.Bind(wx.EVT_BUTTON, frame.reload_url, id=wx.ID_REFRESH)
        frame.Bind(wx.EVT_TEXT, frame.reload_url, id=wx.ID_REFRESH)

        # Back Button / Binds
        frame.back = wx.BitmapButton(frame.panel, id=wx.ID_BACKWARD, bitmap=icons.back, size=(25, 25))
        frame.back.Disable()
        frame.Bind(wx.EVT_BUTTON, frame.go_back_url, id=wx.ID_BACKWARD)

        # Forward Button / Binds
        frame.forward = wx.BitmapButton(frame.panel, id=wx.ID_FORWARD, bitmap=icons.forward, size=(25, 25))
        frame.forward.Disable()
        frame.Bind(wx.EVT_BUTTON, frame.go_forward_url, id=wx.ID_FORWARD)

        # Sizing box - Horizontal
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(frame.back)
        hbox.Add(frame.forward)
        hbox.Add(frame.refresh)
        hbox.Add(frame.address_bar, wx.ALL)
        frame.sizer.Add(hbox)


class Browser:
    '''Browser (renders pages)
    '''
    def __init__(self, frame):
        frame.browser = wx.html2.WebView.New(frame.panel)
        frame.sizer.Add(frame.browser, 1, wx.EXPAND)

        # Listener
        frame.browser.Bind(wx.html2.EVT_WEBVIEW_LOADED, frame.populate_url)


class Frame(wx.Frame):
    '''Main frame that wraps everyhting
    '''
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title)
        self.Maximize(True)
        self.panel = wx.Panel(self, size=(100,100), style=wx.BORDER_RAISED)
        self.Bind(wx.EVT_CLOSE, self.destroy)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # Create Status Bar
        self.CreateStatusBar() # A Statusbar in the bottom of the window

        # Create Menu Bar
        MenuBar(self)

        # Create Address Bar
        AddressBar(self)

        # Create Browser
        Browser(self)

        # Create panel sizer and show panel
        self.panel.SetSizer(self.sizer)
        self.Show()


    #############
    # BINDS
    #############
    def load_url(self, e):
        '''Loads URL in browser window
        '''
        self.browser.LoadURL(self.address_bar.GetValue())
    
    def populate_url(self, e):
        '''Populates the URL in the address bar. Also checks forward/backward history
        and enables/disables the buttons accordingly
        '''
        self.address_bar.SetValue(self.browser.GetCurrentURL())

        # Enaable / Disable Forward & Back Buttons
        if self.browser.GetBackwardHistory():
            self.back.Enable()
        else:
            self.back.Disable()

        if self.browser.GetForwardHistory():
            self.forward.Enable()
        else:
            self.forward.Disable()

    def reload_url(self, e):
        '''Reloads the browser with the current URL
        '''
        self.browser.Reload()

    def go_back_url(self, e):
        '''Navigate backward from history
        ''''
        if self.browser.GetBackwardHistory():
            self.browser.GoBack()

    def go_forward_url(self, e):
        '''Navigate forward from history
        ''''
        if self.browser.GetForwardHistory():
            self.browser.GoForward()
    #############
    # END BINDS
    #############

    def destroy(self, e):
        '''Closes the app
        '''
        self.Destroy()



def main():
    '''Runs PyBro
    '''
    app = wx.App()
    frame = Frame(None, 'PyBro')
    app.MainLoop()


if __name__ == '__main__':
    main()
