from abc import ABC, abstractmethod 
from tkinter import *

def is_english(w): 
    try:
        w.encode().decode('ascii') 
    except UnicodeDecodeError:
        return False 
    else:
        return True

class BaseTranslator(ABC):
    def __init__(self, num_key):
        self.num_key = num_key
    @abstractmethod
    def translator(self): 
        pass

class Alphabet(BaseTranslator): 
    def __init__(self, num_key):
        super().__init__(num_key)
        self.alphabet_dict = {
            "0": " ", "1": "a", "12": "b", "14": "c", "145": "d", "15": "e", "124": "f", "1245": "g", 
            "125": "h", "24": "i", "245": "j", "13": "k", "123": "l", "134": "m", "1345": "n", "135": "o",
            "26": "en", "1234": "p", "12345": "q", "1235": "r", "234": "s", "2345": "t", "136": "u", 
            "1236": "v", "1346": "x", "13456": "y", "1356": "z", "16": "ch", "126": "gh", "146": "sh", 
            "1456": "th", "156": "wh", "1246": "ed", "12456": "er", "1256": "ou", "246": "ow", 
            "2456": "w(will)", "2": ",(ea)", "23": ";(bb)", "25": ":(cc)", "256": ".(dis)",
            "235": "!(to)", "2356": "()", "236": "\"(his)", "35": "in", "356": "\"(was)", "34": "/(st)", 
            "346": "ing", "3456": "#(ble)", "345": "ar", "3": "\'", "36": "-(com)"}
    def translator(self):
        for key, value in self.alphabet_dict.items():
            if self.num_key == key:
                return value 
        return self.num_key
    def get_key_from_value(self, v):
        for key, value in self.alphabet_dict.items():
            if v == value: 
                return key
        return "-"
    
class Grade2(BaseTranslator):
    def __init__(self, num_key): 
        super().__init__(num_key) 
        self.grade2_dict = {
            "1": "a", "12": "but", "14": "can", "145": "do",
            "15": "every", "124": "from", "1245": "go",
            "125": "have", "24": "i", "245": "just",
            "13": "knowledge", "123": "like", "134": "more",
            "1345": "not", "135": "o", "1234": "people", "12345": "quite", 
            "1235": "rather", "234": "so", "2345": "that", "136": "us", 
            "1236": "very", "1346": "it", "13456": "you", "1356": "as", "12346": "and", 
            "123456": "for", "12356": "of", "2346": "the", "23456": "with"}
    def translator(self):
        for key, value in self.grade2_dict.items():
            if self.num_key == key: 
                return value
        return "not found"

class Number(BaseTranslator): 
    def __init__(self, num_key):
        super().__init__(num_key)
        self.number_dict = {
            "0": " ", "1": "1", "12": "2", "14": "3", "145": "4", "15": "5", "124": "6", 
            "1245": "7","125": "8", "24": "9", "245": "0"}
    def translator(self):
        for key, value in self.number_dict.items():
            if self.num_key == key: 
                return value
        return "-"

class EngToBraille:
    def __init__(self, char_list):
        self.char_list = char_list
        self.alphabet_dict = {
            " ": " ", "a": "⠁", "b": "⠃", "c": "⠉", "d": "⠙", "e": "⠑", "f": "⠋", "g": "⠛", 
            "h": "⠓", "i": "⠊", "j": "⠚", "k": "⠅", "l": "⠇", "m": "⠍", "n": "⠝", "o": "⠕", 
            "p": "⠏", "q": "⠟", "r": "⠗", "s": "⠎", "t": "⠞", "u": "⠥", "v": "⠧", "w": "⠺", 
            "x": "⠭", "y": "⠽", "z": "⠵", ",": "⠂", ";": "⠆", ":": "⠒", ".": "⠲", "!": "⠖", 
            "(": "⠶", ")": "⠶", "/": "⠌", "#": "⠼", "\'": "⠄", "-": "⠤", "\n": "\n", 
            " \"": "⠦", "\"": "⠴"} 
        
        self.number_dict = {
            "1": "⠁", "2": "⠃", "3": "⠉", "4": "⠙", "5": "⠑", "6": "⠋",
            "7": "⠛", "8": "⠓","9": "⠊", "0": "⠚"} 
        
        self.numeric_indicator = "⠼" 
        self.uppercase_indicator = "⠠"
    def translator(self):
        output_list = []
        key_list = list(self.alphabet_dict.keys())
        value_list = list(self.alphabet_dict.values()) 
        space = True
        for i in range(len(self.char_list)):
            is_found = False
            if self.char_list[i].isupper():
                output_list.append(self.uppercase_indicator)
                self.char_list[i] = self.char_list[i].lower() 
            for j in range(len(self.alphabet_dict)):
                if self.char_list[i] == key_list[j]:
                    is_found = True 
                    output_list.append(value_list[j])
                    if value_list[j] == " " or value_list[j] == "\n": 
                        space = True
                    break

            if not is_found and self.char_list[i].isnumeric(): 
                if space:
                    output_list.append(self.numeric_indicator)
                    space = False
                n_key_list = list(self.number_dict.keys()) 
                n_value_list = list(self.number_dict.values()) 
                for k in range(len(self.number_dict)):
                    if n_key_list[k] == self.char_list[i]: 
                        is_found = True
                        output_list.append(n_value_list[k]) 
                        print(n_value_list[k])
                        break
        return output_list

class GraphicalUserInterface:
    def __init__(self):
        self.window = Tk() 
        self.window.title("Braille Translator") 
        self.window.geometry("850x500") 
        self.window['background'] = '#FBF5F2'
        # text to braille
        self.input_box = Text(self.window)
        self.input_box.place(x=80, y=50, width=320, height=100) 
        self.convert = Button(self.window, highlightbackground='#718A66', text="Translate", width=32, height=2,border=1, command=self.convert_text)
        self.convert.place(x=80, y=170)
        self.clear = Button(self.window, highlightbackground='#718A66', text="Clear", width=32, height=2, border=1, command=self.clear_text2)
        self.clear.place(x=80, y=240)
        self.display_box2 = Text(self.window)
        self.display_box2.place(x=80, y=320, width=320, height=100)
        # braille to text
        self.one = Button(self.window, width=2, height=2, border=0,state=NORMAL, command=self.switch)
        self.one.place(x=470, y=50)
        self.two = Button(self.window, width=2, height=2, border=0,state=NORMAL, command=self.switch2)
        self.two.place(x=470, y=140)
        self.three = Button(self.window, width=2, height=2, border=0,state=NORMAL, command=self.switch3)
        self.three.place(x=470, y=230)
        self.four = Button(self.window, width=2, height=2, border=0,state=NORMAL, command=self.switch4)
        self.four.place(x=570, y=50)
        self.five = Button(self.window, width=2, height=2, border=0,state=NORMAL, command=self.switch5)
        self.five.place(x=570, y=140)
        self.six = Button(self.window, width=2, height=2, border=0,state=NORMAL, command=self.switch6)
        self.six.place(x=570, y=230)
        enter = Button(self.window, highlightbackground='#718A66', text="Enter", width=5, height=2, border=1,command=self.enter_b)
        enter.place(x=680, y=50)
        delete = Button(self.window, highlightbackground='#718A66', text="Del", width=5, height=2, border=1,command=self.clear_button)
        delete.place(x=680, y=130)
        clear = Button(self.window, highlightbackground='#718A66', text="Clear", width=5, height=2, border=1,command=self.clear_text)
        clear.place(x=680, y=210)
        self.display_box = Entry(self.window)
        self.display_box.place(x=450, y=320, width=320, height=100)
        # helper variable
        self.tmp_grade2 = "" 
        self.space_btw = False 
        self.count = 0 
        self.char_list = [] 
        self.not_in_alpha = False 
        self.is_number = False 
        self.is_uppercase = False 
        self.upper_count = 0 
        self.start = True
        self.window.mainloop()  

    def switch(self):
        if self.one['state'] == NORMAL:
            self.one.config(state="disabled")
    def switch2(self):
        if self.two['state'] == NORMAL:
            self.two.config(state="disabled") 
    def switch3(self):
        if self.three['state'] == NORMAL: 
            self.three.config(state="disabled")
    def switch4(self):
        if self.four['state'] == NORMAL:
            self.four.config(state="disabled")
    def switch5(self):
        if self.five['state'] == NORMAL:
            self.five.config(state="disabled")
    def switch6(self):
        if self.six['state'] == NORMAL:
            self.six.config(state="disabled") 
    def clear_text(self):
        self.display_box.delete(0, "end") 
        self.char_list.clear()
    def clear_button(self):
        if self.one['state'] == DISABLED or self.two['state'] == DISABLED or self.three['state'] == DISABLED or self.four['state'] == DISABLED or self.five['state'] == DISABLED or self.six['state'] == DISABLED:
            self.one.config(state="normal") 
            self.two.config(state="normal") 
            self.three.config(state="normal") 
            self.four.config(state="normal") 
            self.five.config(state="normal") 
            self.six.config(state="normal")

    def enter_b(self): 
        input_list = []
        if self.one['state'] == NORMAL and self.two['state'] == NORMAL and self.three['state'] == NORMAL and self.four['state'] == NORMAL and self.five['state'] == NORMAL and self.six['state'] == NORMAL:
            input_list.append("0") 
        else:
            if self.one['state'] == DISABLED: 
                input_list.append("1")
            if self.two['state'] == DISABLED: 
                input_list.append("2")
            if self.three['state'] == DISABLED: 
                input_list.append("3")
            if self.four['state'] == DISABLED:
                input_list.append("4")
            if self.five['state'] == DISABLED:
                input_list.append("5")
            if self.six['state'] == DISABLED:
                input_list.append("6") 
        input_s = ""
        input_str = (input_s.join(input_list))
        print("Input button: " + input_str) 
        self.clear_button()

        ans = ""
        if input_str == "6":
            self.is_uppercase = True 
        elif self.is_number:
            n = Number(input_str)
            ans = n.translator() 
        else:
            b = Alphabet(input_str)
            ans = b.translator()

        if input_str == ans and not self.is_number and not self.is_uppercase: 
            self.tmp_grade2 = ans
            self.display_box.insert(INSERT, "-")
            self.not_in_alpha = True
            self.char_list.append(ans)
        elif input_str != ans and self.is_uppercase and self.upper_count==1:
            self.display_box.insert(INSERT, ans.upper()) 
            self.char_list.append(ans.upper()) 
            self.is_uppercase = False
            self.upper_count = 0
        else:
            self.display_box.insert(INSERT, ans) 
            self.char_list.append(ans)

        if self.count == 1 and ans == "#(ble)": 
            self.is_number = True 
            self.char_list.pop()
            for i in range(6):
                tmp_get = self.display_box.get()
                self.display_box.delete(len(tmp_get) - 1) 
                
        if self.is_number and ans == " ":
            self.is_number = False
        if self.count == 2 and ans != " ": 
            self.count = 0
        if self.count == 1 and ans != " ": 
            self.count = self.count + 1
        elif self.count == 1 and ans == " ": 
            self.count = 0
        if ans == " ":
            self.count = self.count + 1
        if self.count > 3: 
            self.count = 0
        if self.count == 3 and ans != " ":
            self.count = 0
        elif self.count == 3 and ans == " ":
            self.space_btw = True 
            self.count = 1

        print("Count: " + str(self.count))
        print("Is space between: " + str(self.space_btw))
        if self.space_btw:
            # find the real key to translate for grade2 
            key_tmp = ""
            if self.not_in_alpha:
                key_tmp = self.char_list[len(self.char_list) - 2]
                self.not_in_alpha = False 
            else:
                tmp = self.char_list[len(self.char_list) - 2] 
                a = Alphabet("none")
                key_tmp = a.get_key_from_value(tmp)
            # assign that key and use grade2 translator
            c = Grade2(key_tmp) 
            ans_c = c.translator() 
            if ans_c == "not found":
                self.space_btw = False 
            else:
            # delete old char and space
                for i in range(2):
                    self.char_list.pop()
                    tmp_get = self.display_box.get() 
                    self.display_box.delete(len(tmp_get)-1)
                # add grade2 and space to a list and display
                self.char_list.append(ans_c) 
                self.char_list.append(" ") 
                self.display_box.insert(INSERT, ans_c) 
                space = " " 
                self.display_box.insert(INSERT, space)
                # set space btw to default value
                self.space_btw = False
        if self.is_uppercase and self.upper_count == 0: 
            print("Next character will be uppercase")
            self.upper_count = self.upper_count + 1 
        self.start = False
    def clear_text2(self): 
        self.display_box2.delete("1.0", "end")
    def convert_text(self):
        char_tmp = self.input_box.get("1.0", "end") 
        char_list = list(char_tmp)
        can_translate = True
        for i in range(len(char_list)):
            if char_list[i].isnumeric() or is_english(char_list[i]): 
                print("Can translate")
                can_translate = True
            else:
                can_translate = False
                print("Unknown character") 
                self.display_box2.insert(INSERT, "unknown character") 
                break
        if can_translate:
            ch = EngToBraille(char_list)
            ans_ch = ch.translator()
            for i in range(len(ans_ch)): 
                self.display_box2.insert(INSERT, ans_ch[i])

br = GraphicalUserInterface()