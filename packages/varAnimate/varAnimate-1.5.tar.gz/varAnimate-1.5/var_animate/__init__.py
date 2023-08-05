#-*- coding: utf-8 -*-
import os, sys, time, re, random
from pyfiglet import Figlet

class color:
     def __init__(self):
         pass

     def show(self,colorName):
         color = colorName
         if color:
            if 'red' in color:
               return '\033[31;1m'
            elif 'green' in color:
               return '\033[32;1m'
            elif 'magenta' in color:
               return '\033[35;1m'
            elif 'white' in color:
               return'\033[37;1m'
            elif 'yellow' in color:
               return '\033[33;1m'
            elif 'cyan' in color:
               return '\033[36;1m'
            elif 'blue' in color:
               return '\033[34;1m'
            elif 'lightGray' in color:
               return '\033[37;1m'
            elif 'darkGray' in color:
               return '\033[90;1m'
            elif 'lightRed' in color:
               return '\033[91;1m'
            elif 'lightGreen' in color:
               return '\033[92;1m'
            elif 'lightYellow' in color:
               return '\033[93;1m'
            elif 'lightBlue' in color:
               return '\033[94;1m'
            elif 'lightMagenta' in color:
               return '\033[95;1m'
            elif 'lightCyan' in color:
               return '\033[95;1m'
            elif 'black' in color:
               return '\033[30;1m'
            elif 'default' in color:
               return  '\033[39;1m'
            elif 'reset' in color:
               return '\033[0;1m'
            else:
               pass

c = color()
me = c.show('red')
i = c.show('green')
pu = c.show('white')
cy = c.show('cyan')
ku = c.show('yellow')
bi = c.show('blue')
pur = c.show('magenta')
lbi = c.show('lightBlue')
lcy = c.show('lightCyan')
lpur = c.show('lightMagenta')
reset = c.show('reset')

def banner(text,author,version):
    list_warna = [cy,bi,pur,lbi,lcy,lpur]
    rndm = random.choice(list_warna)
    f = Figlet(font='slant').renderText(text)
    text = rndm + f + '\n{}Author{}: {}{}           {}v{}{}{}'.format(cy,me,pu,author,pu,i,version,reset)
    return text

def loading(text,delay):
    for a in list("|/-\|"*int(delay)):
        sys.stdout.write("\r{}[{}{}{}] {}".format(pu,i,a,pu,text))
        sys.stdout.flush()
        time.sleep(.2)

class animinput:
      def __init__(self):
          pass

      def ask(self,text):
          self.text = text
          if sys.version[0] in '2':
             return raw_input('{}[{}?{}] {}{}: {}'.format(pu,ku,pu,self.text,me,cy))
          elif sys.version[0] in '3':
             return input('{}[{}?{}] {}{}: {}'.format(pu,ku,pu,self.text,me,cy))

      def plus(self,text):
          self.text = text
          if sys.version[0] in '2':
             return raw_input('{}[{}+{}] {}{}: {}'.format(pu,i,pu,self.text,me,cy))
          elif sys.version[0] in '3':
             return input('{}[{}+{}] {}{}: {}'.format(pu,i,pu,self.text,me,cy))


      def danger(self,text):
          self.text = text
          if sys.version[0] in '2':
             return raw_input('{}[{}!{}] {}{}: {}'.format(pu,me,pu,self.text,me,cy))
          elif sys.version[0] in '3':
             return input('{}[{}!{}] {}{}: {}'.format(pu,me,pu,self.text,me,cy))


class animvar:
      def __init__(self):
          pass

      def true(self,text):
          self.text = text
          return '{}[{}√{}] {}{}!{}'.format(pu,i,pu,text,i,reset)

      def false(self,text):
          self.text = text
          return '{}[{}!{}] {}{}!{}'.format(pu,me,pu,text,me,reset)
