import pyxel
import random

class Kenshi:
    def __init__(self, x:int, w:int) -> None:
        self.x = x
        self.w = w

    def draw(self):
        pyxel.blt(self.x,32, 0, 0,0, self.w,64, colkey=0)


class Ippon:
    def __init__(self, waza_wait:int) -> None:
        """_summary_

        Args:
            waza_wait (int): 技発動までのウェイト
        """
        self.waza_frame = pyxel.frame_count + waza_wait

        #random.choiceは速度的に微妙だが、コンストラクタは速度を求めないので可読性のために使用
        self.winner = random.choice(["white", "red"])

        self.result = None

    def update(self, kenshi_white:Kenshi, kenshi_red:Kenshi):

        if pyxel.frame_count == self.waza_frame :
            if self.winner == "white":
                kenshi_white.x += 32
            elif self.winner == "red":
                kenshi_red.x -= 32

        if self.result is not None :
            return

        flag = None
        # pyxel.btnp : ボタンが押下されたフレームに限ってTrue
        if pyxel.btnp(pyxel.KEY_W):
            flag = "white"
        elif pyxel.btnp(pyxel.KEY_R):
            flag = "red"

        if flag is None:
            return

        delay = self.get_delay()
        #成功条件：旗が勝者と一致しており、なおかつ技発動後すぐであること
        self.result = ( flag == self.winner and (0 < delay and delay < 60) )


    def get_delay(self) -> int:
        """技発動から現在までの経過フレーム数を取得

        Returns:
            int: 遅れフレーム数
        """
        return pyxel.frame_count - self.waza_frame
            

class App:
    def __init__(self):
        pyxel.init(256, 128, title="Kendo", display_scale=4)

        pyxel.load("assets/kenshi.pyxres")

        self.ippon = Ippon(waza_wait=60)

        self.kenshi_white = Kenshi(x=64, w=-64)
        self.kenshi_red = Kenshi(x=128, w=64)

        pyxel.run(self.update, self.draw)

    def update(self):
        # pyxel.btnp : ボタンが押下されたフレームに限ってTrue
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.ippon.update(self.kenshi_white, self.kenshi_red)
            

    def draw(self):
        pyxel.cls(0)

        self.kenshi_white.draw()
        self.kenshi_red.draw()

        # pyxel.btn : ボタンが押されているなら常にTrue
        # if pyxel.btn(pyxel.KEY_R):
        pyxel.text(10, 10, f"{self.ippon.result}", 2)


App()
