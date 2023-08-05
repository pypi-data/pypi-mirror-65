
from distutils.core import setup
deskripsi = """
      [!] styling python script with var_animate [!]

[?] need tutorial the modul?

1.Anim Input: ( Suport py2&py3 )

>>> from var_animate import animinput # importing the modul
>>> inpt = animinput()

>>> # input plus
>>> inpt.plus('the text')
>>> # output?: [+] the text: # user input in here

>>> # input ask
>>> inpt.ask('Username?') # if your ask user ex: Username?
>>> # output?: [?] Username?: # user input in here

>>> # input danger
>>> inpt.danger('Exception enter to loop the progam!') # if user excepting input
>>> # output?: [!] Exception enter to loop the progam!: # user input in here


2.Coloring: ( Suport py2&py3 )

>>> from var_animate import color # importing the modul
>>> color = color()
>>> # color.show('ColorName...') # showing the color with name

>>> # what list the color?:
>>> #     Default color     #
>>> color.show('red') # Red color
>>> color.show('yellow') # Yellow color
>>> color.show('green') # Gren color
>>> color.show('blue') # Blue color
>>> color.show('magenta') # Magenta color
>>> color.show('cyan') # Cyan color
>>> color.show('white') # White color
>>> color.show('black') # Black color
>>> color.show('default') # Default color
>>> color.show('reset') # reset color

>>> #      Light color      #
>>> color.show('lightGray') # lightGray color
>>> color.show('darkGray') # darkGray color
>>> color.show('lightRed') # lightRed color
>>> color.show('lightYellow') # lightYellow color
>>> color.show('lightGreen') # lightGreen color
>>> color.show('lightBlue') # lightBlue color
>>> color.show('lightMagenta') # lightMagenta color
>>> color.show('lightCyan') # lightCyan color


3.Anim Variable: ( Suport py2&py3 )

>>> from var_animate import animvar # importing the modul
>>> var = animvar()

>>> # if the condition true then return:
>>> true = var.true('True!')
>>> print(true) # printing var.true()

>>> # if the condition false then return:
>>> false = var.false('False!')
>>> print(false) # printing var.false()


4.Make the bannner script: ( Suport py2&py3 )
>>> import var_animate # importing the modul

>>> banner = var_animate.banner('TheScriptName','AuthorName','ScriptVersion') # Make the banner
>>> print(banner) # printing the banner

>>> # Ex: banner = var_animate.banner('Var_Animate','Dst_207','1.0')
>>> # Ex: print(banner)


Example script with modules var_animate:
github: https://github.com/DH4CK1/var_animate_calculator

"""

setup(
  name = 'varAnimate',         # How you named your package folder (MyLib)
  packages = ['var_animate'],   # Chose the same as "name"
  version = '1.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = deskripsi,   # Give a short description about your library
  author = 'Dst_207',                   # Type in your name
  author_email = 'cyberdhack@gmail.com',      # Type in your E-Mail
  keywords = ['animate', 'anim python', 'animate python'],   # Keywords that define your package best
  install_requires=['pyfiglet'],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)

