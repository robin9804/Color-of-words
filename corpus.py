import numpy as np
import colorsys
import re

# 크롤링한 데이터 받아오는 부분

# Reference = https://github.com/neotune/python-korean-handler
class KorToPix:
    def __init__(self, sentence):
        self.sentence = sentence
        # 문자를 한 글자씩 분리하기
        t = re.compile("[\w]")
        self.words = t.findall(self.sentence)
        self.w1 = []  # 사용된 초성
        self.i1 = []  # 초성에 사용된 모음의 횟수
        self.w2 = []  # 사용된 모음
        self.i2 = []  # 모음당 사용된 횟수

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
        korean_word = str(korean_word[0])
        for w in list(korean_word.strip()):
            if '가' <= w <= '힣':
                ch1 = (ord(w) - ord('가')) // 588
                ch2 = ((ord(w) - ord('가')) - (588 * ch1)) // 28
                ch3 = (ord(w) - ord('가')) - (588 * ch1) - 28 * ch2
                r_lst.append([CHOSUNG_LIST[ch1], JUNGSUNG_LIST[ch2], JONGSUNG_LIST[ch3]])
            else:
                r_lst.append([w])
        return r_lst

    def importance(self):
        """
        사용된 자소에 따른 사용 빈도를 구해주는 함수
        """
        first = []
        second = []
        for i in range(len(self.words)):
            w = self.wordappart(self.words[i])
            second.append(w[0][1])  # 중성 (모음)
            first.append(w[0][0])  # 초성
        self.w1, self.i1 = np.unique(np.array(first), return_counts=True)
        self.w2, self.i2 = np.unique(np.array(second), return_counts=True)

    def selectHue(self, sen):
        """
        초성에 대해서 색상을 배정해주는 함수
        """
        word = self.wordappart(sen)
        first = word[0][0]
        # second = word[0][1]
        # third = word[0][2]
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

    def weightHue(self, sen):
        """
        HUE에 가중치를 부여하는 함수 받침으로 결정한다.
        """
        word = self.wordappart(sen)
        third = word[0][2]
        weight = 0
        JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ',
                         'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
        # 자음에 가중치를 부여하는 순서
        jaum_weight = [' ','ㅍ', 'ㅋ', 'ㅌ', 'ㅊ', 'ㅂ', 'ㅎ', 'ㅅ','ㅈ', 'ㄷ', 'ㅁ', 'ㄹ', 'ㄱ', 'ㄴ']
        for i in range(len(JONGSUNG_LIST)):
            if third == JONGSUNG_LIST[i]:
                # for j in range(len(jaum_weight)):
                weight = ((i+1)/28) * 20
        return round(weight)

    def selectSaturation(self, sen):
        """
        모음을 통해 saturation을 정해주는 함수.
        """
        word = self.wordappart(sen)
        Last = ['ㅐ', 'ㅏ', 'ㅘ', 'ㅙ', 'ㅑ', 'ㅗ','ㅛ' ,'ㅓ','ㅕ', 'ㅔ', 'ㅚ', 'ㅝ', 'ㅞ','ㅒ', 'ㅖ', 'ㅣ', 'ㅡ', 'ㅜ', 'ㅠ', 'ㅟ', 'ㅢ']
        second = str(word[0][1])
        third = str(word[0][2])
        s = 0
        for i in range(21):
            if second == Last[i]:
                s = i * 5
                if third == ' ':
                    s = s + 2
        return s

    def setValue(self, sen):
        word = self.wordappart(sen)
        first = str(word[0][0])  # 초성
        second = str(word[0][1])  # 중성
        v = 80
        i1 = self.i1 / np.max(self.i1)
        i2 = self.i2 / np.max(self.i2)
        for i in range(len(i1)):
            if first == self.w1[i]:
                v = v + i1[i] * 20
        for j in range(len(i2)):
            if second == self.w2[j]:
                v = v + i2[j] * 10
        if v > 100:
            v = 100
        return round(v)

    def tocolor(self):
        """
        단어를 넣었을 때 초성, 중성, 종성에 따라 색을 지정해주기
        """
        # 중요도 추출(아스키코드 순서대로 반환해준다)
        word, importance = np.unique(np.array(self.words), return_counts=True)
        self.importance()
        colorbag = []

        for i in range(len(self.words)):
            h = self.selectHue(self.words[i]) + self.weightHue(self.words[i])
            s = self.selectSaturation(self.words[i])
            v = self.setValue(self.words[i])
            print(self.words[i])
            colorbag.append(list(colorsys.hsv_to_rgb(h/360, s/100, int(v)/100)))
        return colorbag

    def coordinate(self, color):
        """
        색이 지정된 것을 바로 내놓는 함수
        """

        x = int(round(np.sqrt(len(self.words) + 1)))  # 높이
        y = x  # 너비
        canvas = np.zeros((x, y, 3))
        # color = np.array(color) / 255
        try:
            for i in range(x):
                for j in range(y):
                    canvas[i][j] = color[i*x + j]
        except IndexError:
            pass
        # canvas = color.reshape(x, y)  # Grid size define
        return canvas

    def sortCoordinate(self, color):
        """
        정렬해서 쓰는 함수
        """
        x = np.sqrt(len(self.words) + 1)
        y = x
        w = np.sort(np.array(color))