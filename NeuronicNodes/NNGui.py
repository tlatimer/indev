import wx
import wx.svg
import igraph


class NNGui(wx.Frame):

    def __init__(self, parent, title):
        super().__init__(parent, title=title)

        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        # self.screen = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.screen = wx.GraphicsContext(panel)  # TODO
        vbox.Add(self.screen, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        self.cmd_box = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)
        vbox.Add(self.cmd_box, flag=wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, border=10)

        # self.Bind(wx.EVT_TEXT_ENTER, self.do_enter)
        self.Bind(wx.EVT_CHAR, self.do_char)

        panel.SetSizer(vbox)

        self.Centre()

        self.img = wx.svg.SVGimage.CreateFromFile('output.svg')
        self.Bind(wx.EVT_PAINT, self.on_paint)

    # def do_enter(self, event):
    #     cmd = self.cmd_box.GetValue()
    #     self.screen.AppendText(cmd + '\n')
    #     self.cmd_box.Clear()

    def do_char(self, event):
        # process tab to be new child
        pass

    def on_paint(self, event):
        # https://docs.wxpython.org/wx.svg.html
        dc = wx.PaintDC(self.screen)
        dc.SetBackground(wx.Brush('white'))
        dc.Clear()

        dcdim = min(self.Size.width, self.Size.height)
        imgdim = min(self.img.width, self.img.height)
        scale = dcdim / imgdim
        width = int(self.img.width * scale)
        height = int(self.img.height * scale)

        bmp = self.img.ConvertToBitmap(scale=scale, width=width, height=height)
        dc.DrawBitmap(bmp, 0, 0)


class NNGraph:
    def __init__(self):
        self.g = igraph.Graph.GRG(50, 0.2)

    def write_svg(self, filename='output.svg'):
        assert filename.endswith('.svg')

        igraph.plot(self.g, filename)


def main():
    graph = NNGraph()
    graph.write_svg()
    app = wx.App()
    frame = NNGui(None, title='NeuronicNodes')
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
