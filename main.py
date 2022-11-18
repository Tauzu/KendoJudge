import pyxel


class App:
    def __init__(self):
        pyxel.init(256, 128, title="Kendo", display_scale=4)
        pyxel.load("assets/kenshi.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)

        pyxel.blt(0,0, 0, 0,0, 60,64)

        if pyxel.btn(pyxel.KEY_R):
            pyxel.text(10, 10, "Hello World!", 2)


App()
