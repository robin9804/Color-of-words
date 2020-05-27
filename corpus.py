import konlpy
import nltk
import numpy as np

# 크롤링한 데이터 받아오는 부분
import croll

# Reference = https://github.com/neotune/python-korean-handler
class KorToPix:
    def __init__(self, crowling):
        self.crowing = crowling

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

    def tocolor(self, word):
        """
        단어를 넣었을 때 초성, 중성, 종성에 따라 색을 지정해주기
        """
        w = word[0]
        color = hex(w)
        color = "#" + str(color)
        return color

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
