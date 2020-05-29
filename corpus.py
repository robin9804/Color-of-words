import numpy as np
import re

# 크롤링한 데이터 받아오는 부분

# Reference = https://github.com/neotune/python-korean-handler
class KorToPix:
    def __init__(self, sentence):
        self.sentence = sentence
        # 문자를 한 글자씩 분리하기
        t = re.compile("[\w]")
        self.words = t.findall(self.sentence)

    def wordappart(self, korean_word):
        """
        한글 단어를 입력받아서 초성/중성/종성을 구분해주는 함수
        """
        # 초성 리스트. 00 ~ 18
        CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
        # 중성 리스트. 00 ~ 20
        JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ',
                         'ㅢ', 'ㅣ']
        # 종성 리스트. 00 ~ 27 + 1(1개 없음)
        JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ',
                         'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

        r_lst = []
        for w in list(korean_word.strip()):
            if '가' <= w <= '힣':
                ch1 = (ord(w) - ord('가')) // 588
                ch2 = ((ord(w) - ord('가')) - (588 * ch1)) // 28
                ch3 = (ord(w) - ord('가')) - (588 * ch1) - 28 * ch2
                r_lst.append([CHOSUNG_LIST[ch1], JUNGSUNG_LIST[ch2], JONGSUNG_LIST[ch3]])
            else:
                r_lst.append([w])
        return r_lst

    def selectHue(self, word):
        """
        초성에 대해서 색상을 배정해주는 함수
        """
        first = word[0][0]
        second = word[0][1]
        third = word[0][2]
        h = 0  # 0 ~ 360

        # 초성에 대해서 색상의 분포를 정해주기
        if first == 'ㅆ':  # ㅆ은 0 ~ 14
            h = 0
        elif first == 'ㄲ':  # ㄲ은 14 ~ 28
            h = 14
        elif first == 'ㄱ':  # ㄱ은 28 ~ 50
            h = 28
        elif first == 'ㄴ':  # ㄴ은 50 ~ 70
            h = 50
        elif first == 'ㄹ':  # ㄹ은 70 ~ 90
            h = 70
        elif first == 'ㅁ':  # ㅁ은 90 ~ 110
            h = 90
        elif first == 'ㅂ':  # ㅂ은 110 ~ 130
            h = 110
        elif first == 'ㄷ':  # ㄷ은 130 ~ 150
            h = 130
        elif first == 'ㅇ':  # ㅇ은 150 ~ 170
            h = 150
        elif first == 'ㅎ':  # ㅎ은 170 ~ 190
            h = 170
        elif first == 'ㅅ':  # ㅅ은 190 ~ 210
            h = 190
        elif first == 'ㅈ':  # ㅈ은 210 ~ 230
            h = 210
        elif first == 'ㅊ':  # ㅊ은 210 ~ 230
            h = 230
        elif first == 'ㅌ':  # ㅌ은 230 ~ 250
            h = 250
        elif first == 'ㅋ':  # ㅋ은 250 ~ 270
            h = 270
        elif first == 'ㅍ':  # ㅍ은 270 ~ 290
            h = 290
        elif first == 'ㄸ':  # 은 310 ~ 327
            h = 310
        elif first == 'ㅃ':  # ㄲ은 10 ~ 20
            h = 327
        elif first == 'ㅉ':  # ㄲ은 10 ~ 20
            h = 342
        else:
            h = 0
        return h

    def weightHue(self):
        """
        HUE에 가중치를 부여하는 함수
        """

    def tocolor(self):
        """
        단어를 넣었을 때 초성, 중성, 종성에 따라 색을 지정해주기
        """
        # 중요도 추출(아스키코드 순서대로 반환해준다)
        words, importance = np.unique(np.array(self.words), return_counts=True)

        colorbag = []
        for i in len(words):
            h = self.selectHue(words[i])
            s = 0
            if importance[i]
            v = 0

            colorbag.append([h, s, v])

        return colorbag

    def hsvTohex(hsv):
        """
        HSV 좌표로 표현된 색을 16비트 rgb 색으로 표현
        """
        h = hsv[0]  # Hue 는 360까지 범위를 가짐
        s = hsv[1]  # 채도는 0 to 100
        v = hsv[2]  # 명도는 0 to 100 의 범위를 가짐

        s = s / 100
        v = v / 100

        C = v * s
        X = C * (1 - abs((h / 60) % 2 - 1))
        m = v - C
        if 0 <= h < 60:
            r, g, b = C, X, 0
        elif 60 <= h < 120:
            r, g, b = X, C, 0
        elif 120 <= h < 180:
            r, g, b = 0, C, X
        elif 180 <= h < 240:
            r, g, b = 0, X, C
        elif 240 <= h < 300:
            r, g, b = X, 0, C
        elif 300 <= h < 360:
            r, g, b = C, 0, X
        return round((r + m) * 255), round((g + m) * 255), round((b + m) * 255)

    def coordinate(self, color, x, y):
        """
        색이 지정된 것을 정렬하여 내놓는 함수
        """
        w = color.sort()
        canvas = np.zeros([x,y]) # Grid size define
        for x ,y in zip(canvas):
            canvas[x,y] = w[x+y]
        return canvas
