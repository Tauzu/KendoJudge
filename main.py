import pyxel
import random

class Kenshi:
    def __init__(self, x:int, w:int) -> None:
        self.x = x
        self.w = w

    def draw(self):
        pyxel.blt(self.x,32, 0, 0,0, self.w,64, colkey=0)

class Player:
    def __init__(self) -> None:
        self.flag = None

    def update(self):
        if self.flag is not None:
            return

        # pyxel.btnp : ボタンが押下されたフレームに限ってTrue
        if pyxel.btnp(pyxel.KEY_W):
            self.flag = "white"
        elif pyxel.btnp(pyxel.KEY_R):
            self.flag = "red"

    def draw(self):
        pyxel.text(10, 30, f"{self.flag}", 2)


class Ippon:
    def __init__(self, waza_wait:int, kenshi_white:Kenshi, kenshi_red:Kenshi) -> None:
        """_summary_

        Args:
            waza_wait (int): 技発動までのウェイト
        """
        self.waza_frame = pyxel.frame_count + waza_wait

        self.player = Player()

        self.kenshi_white = kenshi_white
        self.kenshi_red = kenshi_red

        #random.choiceは速度的に微妙だが、コンストラクタは速度を求めないので可読性のために使用
        self.winner = random.choice(["white", "red"])

        self.result = None

    def update(self):
        self.player.update()

        if pyxel.frame_count == self.waza_frame :
            if self.winner == "white":
                self.kenshi_white.x += 32
            elif self.winner == "red":
                self.kenshi_red.x -= 32

        if (self.result is None) and (self.player.flag is not None):
            delay = self.get_delay()
            #成功条件：旗が勝者と一致しており、なおかつ技発動後すぐであること
            self.result = ( self.player.flag == self.winner and (0 < delay and delay < 60) )


    def get_delay(self) -> int:
        """技発動から現在までの経過フレーム数を取得

        Returns:
            int: 遅れフレーム数
        """
        return pyxel.frame_count - self.waza_frame

    def draw(self):
        self.player.draw()

        self.kenshi_white.draw()
        self.kenshi_red.draw()

        pyxel.text(10, 10, f"{self.result}", 2)
            

class App:
    def __init__(self):
        pyxel.init(256, 128, title="Kendo", display_scale=4)

        pyxel.load("assets/kenshi.pyxres")

        self.ippon = Ippon(
            waza_wait=60,
            kenshi_white=Kenshi(x=64, w=-64),
            kenshi_red=Kenshi(x=128, w=64)
            )

        pyxel.run(self.update, self.draw)

    def update(self):
        # pyxel.btnp : ボタンが押下されたフレームに限ってTrue
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.ippon.update()
            

    def draw(self):
        pyxel.cls(0)

        self.ippon.draw()

        # pyxel.btn : ボタンが押されているなら常にTrue
        # if pyxel.btn(pyxel.KEY_R):


App()
