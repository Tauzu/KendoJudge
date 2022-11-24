import pyxel
import random

class Kenshi:
    def __init__(self, x:int, w:int) -> None:
        self.x = x
        self.w = w

    def draw(self):
        pyxel.blt(self.x,32, 0, 0,0, self.w,64, colkey=0)

class Judge:
    def __init__(self, x:int, y:int) -> None:
        self.flag = None
        self.x = x
        self.y = y

    def draw(self):
        # pyxel.text(self.x, self.y, f"{self.flag}", 2)
        if self.flag == "white":
            pyxel.blt(self.x,self.y, 1, 0,0, 16,16, colkey=0)
        elif self.flag == "red":
            pyxel.blt(self.x,self.y, 1, 16,0, -16,16, colkey=0)

class MainJudge(Judge):
    def __init__(self, x:int, y:int) -> None:
        super().__init__(x, y)
        self.state = 0

    def draw(self):
        u = 16*self.state + 32
        v = 16
        pyxel.blt(self.x,self.y, 1, u,v, 16,16, colkey=0)

        # pyxel.text(self.x, self.y, f"{self.flag}", 2)
        if self.flag == "white":
            pyxel.blt(self.x-16,self.y, 1, 0,0, 16,16, colkey=0)
        elif self.flag == "red":
            pyxel.blt(self.x+16,self.y, 1, 16,0, -16,16, colkey=0)


class Player(Judge):
    def __init__(self, x:int, y:int) -> None:
        super().__init__(x, y)

    def update(self):
        if self.flag is not None:
            return

        # pyxel.btnp : ボタンが押下されたフレームに限ってTrue
        if pyxel.btnp(pyxel.KEY_W):
            self.flag = "white"
        elif pyxel.btnp(pyxel.KEY_R):
            self.flag = "red"


class Ippon:
    def __init__(self,
        waza_wait:int,
        kenshi_white:Kenshi, kenshi_red:Kenshi,
        mainJudge:MainJudge
        ) -> None:
        """_summary_

        Args:
            waza_wait (int): 技発動までのウェイト
        """
        self.waza_frame = pyxel.frame_count + waza_wait

        self.mainJudge = mainJudge
        self.mainJudge.flag = None

        self.kenshi_white = kenshi_white
        self.kenshi_red = kenshi_red

        self.player = Player(10,60)
        self.subJudge = Judge(210, 60)

        #random.choiceは速度的に微妙だが、コンストラクタは速度を求めないので可読性のために使用
        self.winner = random.choice(["white", "red"])

        self.result = None

        self.last_frame = pyxel.frame_count

    def update(self):
        #結果が判定済みであれば即座にリターン
        if self.result is not None :
            return

        self.player.update()

        if pyxel.frame_count == self.waza_frame :
            if self.winner == "white":
                self.kenshi_white.x += 32
                self.kenshi_red.x -= 8
            elif self.winner == "red":
                self.kenshi_white.x += 8
                self.kenshi_red.x -= 32

        delay = self.get_delay()

        if delay > 60:
            #時間切れ
            self.result = False
            self.mainJudge.flag = self.winner
            self.subJudge.flag = self.winner
        
        elif self.player.flag is not None:
            #プレイヤーが旗を上げた場合
            
            #成功条件：旗が勝者と一致し、なおかつ技発動後
            if delay > 0:
                self.result = ( self.player.flag == self.winner )

                #技発動後であれば他の審判も旗を上げる
                self.mainJudge.flag = self.winner
                self.subJudge.flag = self.winner

            else:
                #技発動前に旗を上げてしまった場合
                self.result = False

        if self.result == True:
            self.mainJudge.state = min(self.mainJudge.state + 1, 2)
        elif self.result == False:
            self.mainJudge.state = max(self.mainJudge.state - 1, -2)

        self.last_frame = pyxel.frame_count


    def get_delay(self) -> int:
        """技発動から現在までの経過フレーム数を取得

        Returns:
            int: 遅れフレーム数
        """
        return pyxel.frame_count - self.waza_frame

    def draw(self):
        self.player.draw()
        self.subJudge.draw()
        self.mainJudge.draw()

        self.kenshi_white.draw()
        self.kenshi_red.draw()

        pyxel.text(10, 10, f"{self.result}", 2)
            

class App:
    def __init__(self):
        pyxel.init(256, 128, title="Kendo", display_scale=4)

        pyxel.load("assets/kenshi.pyxres")

        self.ippon = None

        self.mainJudge = MainJudge(120,16)

        pyxel.run(self.update, self.draw)

    def update(self):
        # pyxel.btnp : ボタンが押下されたフレームに限ってTrue
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if (self.ippon is not None) and (pyxel.frame_count - self.ippon.last_frame < 60):
            self.ippon.update()

        else:
            self.ippon = Ippon(
                waza_wait=60,
                kenshi_white=Kenshi(x=64, w=-64),
                kenshi_red=Kenshi(x=128, w=64),
                mainJudge=self.mainJudge
                )
            

    def draw(self):
        pyxel.cls(0)

        self.ippon.draw()

        # pyxel.btn : ボタンが押されているなら常にTrue
        # if pyxel.btn(pyxel.KEY_R):


App()
