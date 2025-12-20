# This module is just for fun, used with extra commands that can be accepted
# inside interpret_commands() function in gemini.py module.

# Somebody told me:
# My honest opinion, your project feels like:
# “A CLI written by someone who enjoys messing with users — in a good way.”

from settings import PURP
from typing import Callable
from random import random, randint, uniform, choice, shuffle

BANANAS = r"""
                                                  ▒▒▓▓▒▒            
                                                ▓▓▓▓▓▓▓▓██          
                                                ░░▓▓▓▓▓▓▓▓          
                                                  ▓▓▓▓▒▒░░░░        
                                                  ██▒▒░░░░▒▒        
                                                  ▒▒░░░░░░▓▓        
                                                    ▒▒░░░░▒▒        
                                                    ▓▓  ░░░░▓▓      
                                                    ▒▒  ░░░░▒▒▒▒    
                                                    ░░    ░░░░░░▓▓  
                                                    ░░    ░░░░░░░░░░
                                                    ▓▓    ░░░░░░░░▓▓
                                                    ▓▓    ░░░░░░░░▒▒
                                                    ▓▓    ░░░░░░░░░░
                                                    ▒▒    ░░░░░░░░░░
                                                    ░░    ▒▒░░░░░░░░
                                                  ░░      ▒▒░░░░░░░░
                                                  ▓▓      ░░░░░░░░░░
                                                  ▒▒    ░░░░░░░░░░▒▒
                                                ▒▒      ▒▒░░░░░░░░▓▓
                                                ░░    ░░░░░░░░░░░░▓▓
                                              ▓▓      ░░░░░░░░░░░░▒▒
                                            ░░        ░░░░░░░░  ▒▒  
                                            ▓▓      ░░░░░░░░░░░░▓▓  
                                        ▓▓░░      ░░░░░░      ▒▒░░  
                                    ▒▒▒▒          ░░░░    ░░░░▓▓    
                                  ▓▓            ░░░░░░  ░░░░▒▒░░    
                            ▓▓▒▒              ░░░░      ░░░░▓▓      
        ░░  ▒▒▒▒▓▓██▓▓▒▒░░                ░░░░░░░░░░░░  ░░▓▓        
░░██▒▒░░                            ░░░░░░░░░░░░░░░░  ░░▓▓░░        
▓▓▓▓          ░░            ░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒░░          
░░▓▓░░      ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒▒▒            
  ▒▒▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒▓▓░░              
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒▓▓                  
      ░░▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒▓▓                      
          ░░▓▓▒▒░░░░░░░░░░░░▒▒▒▒▒▒▒▒▓▓▓▓░░  
                 ░░░░░░░░░░░░░░░░░░░░
!
                                                                ▓▓▒▒              
                                                              ██    ████████▓▓████
                                                              ██▓▓               ▓▒
                                                                  ████    ████████
                                                                  ██▒▒██  ██      
                                                                  ██▒▒██  ██      
                                                                ██  ██▒▒  ██      
                                                            ████  ░░  ██  ██      
                                                      ▒▒████    ░░██  ██  ██      
                      ░░░░▒▒▒▒▓▓▒▒▒▒▒▒▒▒▒▒██████████▒▒        ██░░    ██    ██    
        ░░▓▓████▓▓▒▒░░░░░░░░░░                            ░░██        ▒▒    ██░░  
  ██████░░                                              ██▒▒        ██        ██  
██░░                                                ██▒▒            ▒▒        ██  
██░░                                          ░░██░░              ██          ██  
  ░░                                      ████                ░░▓▓      ░░    ██  
  ░░██        ░░░░░░  ▒▒▒▒░░▒▒▓▓████▒▒                      ░░██              ▒▒  
      ██          ░░██▓▓██▒▒                            ░░  ██                ██  
  ▒▒██▓▓████▒▒                                        ░░  ██          ░░      ██  
██                                              ░░      ██                    ██  
██▒▒                                      ░░░░      ▒▒▓▓                      ██  
▒▒░░                              ░░░░            ██              ▒▒        ░░▒▒  
  ▓▓            ░░░░  ▒▒░░                    ██▒▒              ░░          ██    
    ██                                  ▒▒▓▓░░                ░░          ░░▓▓    
      ██░░                      ▒▒████                      ░░            ██      
        ░░██            ░░████▒▒                          ░░            ▒▒        
          ██████████████                              ░░                ██        
        ██                                        ░░                  ██          
        ▒▒  ██                              ░░                      ██            
        ██  ██          ░░  ░░░░                                  ██              
        ▒▒▒▒                                                  ▒▒▓▓                
            ██                                            ░░██                    
              ██░░                                      ▒▒██                      
                ████                                  ██▒▒                        
                    ████                        ████ 
                          ░░░░▒▒▒▒▓▓▒▒▒▒▒▒▒▒▒                    
!
                    ████                        
                  ████████                      
                  ██░░░░██                      
                  ██░░░░████                    
                  ██░░░░░░████                  
                  ██░░░░░░░░██                  
                  ██░░░░░░░░████                
                  ██░░░░░░░░░░██                
              ██████████░░░░░░████              
            ██  ██      ██░░░░░░██              
            ████████    ██░░░░░░██              
            ██  ██      ██░░░░░░██              
              ██████████░░░░██░░██              
                ██░░░░░░██████░░██              
                ████████▓▓▓▓██░░██              
                  ██▓▓▓▓▓▓██░░░░██              
                  ██▓▓████░░░░░░████████        
    ██████      ██████░░░░░░░░████      ██      
  ██      ████  ██░░░░░░░░░░░░██        ██      
  ██        ██  ██░░░░░░░░░░██████      ██      
  ██      ██████░░░░░░░░░░░░██  ████████        
    ██████    ██░░░░░░░░░░██      ██            
        ██  ██░░░░░░░░░░██    ██████            
        ████░░░░░░░░░░██████████                
      ████████░░░░████████████                  
  ████████  ████████      ████████              
██      ████            ████      ██            
██          ██        ██          ██            
  ████████████        ████████████              
!
                      ██████                          
                      ██▓▓▓▓██                        
                      ██▒▒▓▓██                        
                      ██▒▒▓▓  ████                    
                        ██        ██                  
                        ██        ░░██                
                        ██        ░░██                
                      ██        ░░░░██                
                      ██        ░░░░██                
                      ██        ░░░░██                
                    ██          ░░░░██                
                ████            ░░░░██                
    ████████████              ░░░░██                  
  ██▒▒                      ░░░░██                    
  ██▒▒                    ░░░░██                      
  ██▓▓              ░░░░░░░░██                        
    ██████░░░░░░░░░░░░░░████                          
          ██████████████                              
!
                                    ▓▓██                    
                                  ██ ▓▓                   
                                  ▓▓  ██                    
                                  ▒▒  ▒▒                    
                                    ██  ██                  
                                    ██      ██              
                                    ██        ██            
                                    ██        ▒▒            
                                    ██        ░░██          
                                    ██        ░░██          
                                    ░░        ░░██          
                                  ██          ░░▓▓          
                                  ▒▒          ░░██          
                                ██            ░░██          
                              ██              ░░░░          
                          ▒▒▓▓                ▓▓            
                        ██                  ░░██            
                  ░░██░░                    ▒▒              
              ████░░                      ░░██              
          ██▒▒                          ░░██                
      ██░░                              ▓▓                  
  ▒▒▒▒                                ██                    
▓▓                                  ██                      
██░░                            ▓▓▒▒                        
░░░░                      ░░████                            
  ░░██              ░░████                                  
      ▒▒██▓▓██████                                          
!
 _
//\\
V  \\
 \\  \\_
  \\,'.`-.
   |\\ `. `.
   ( \\  `. `-.                        _,.-:\\
    \\ \\   `.  `-._             __..--' ,-';/
     \\ `.   `-.   `-..___..---'   _.--' ,'/
      `. `.    `-._        __..--'    ,' /
        `. `-_     ``--..''       _.-' ,'
          `-_ `-.___        __,--'   ,'
             `-.__  `----```    __.-'
                  `--..____..--'
"""

CAT = r"""
      |\      _,,,---,,_
      /,`.-'`'    -.  ;-;;,_
     |,4-  ) )-,_. ,\ (  `'-'
     '--''(_/--'  `-'\_)
!
      |\      _,,,---,,_
    z /,`.-'`'    -.  ;-;;,_
     |,4-  ) )-,_. ,\ (  `'-'
     '--''(_/--'  `-'\_)
!
      |\      _,,,---,,_
   Zz /,`.-'`'    -.  ;-;;,_
     |,4-  ) )-,_. ,\ (  `'-'
     '--''(_/--'  `-'\_)
!
      |\      _,,,---,,_
  ZZz /,`.-'`'    -.  ;-;;,_
     |,4-  ) )-,_. ,\ (  `'-'
     '--''(_/--'  `-'\_)
!
  z   |\      _,,,---,,_
  ZZz /,`.-'`'    -.  ;-;;,_
     |,4-  ) )-,_. ,\ (  `'-'
     '--''(_/--'  `-'\_)
!
 Zz   |\      _,,,---,,_
  ZZz /,`.-'`'    -.  ;-;;,_
     |,4-  ) )-,_. ,\ (  `'-'
     '--''(_/--'  `-'\_)
!
ZZz   |\      _,,,---,,_
  ZZz /,`.-'`'    -.  ;-;;,_
     |,4-  ) )-,_. ,\ (  `'-'
     '--''(_/--'  `-'\_)
!
 Zz   |\      _,,,---,,_
  ZZz /,`.-'`'    -.  ;-;;,_
     |,4-  ) )-,_. ,\ (  `'-'
     '--''(_/--'  `-'\_)
!
  z   |\      _,,,---,,_
  ZZz /,`.-'`'    -.  ;-;;,_
     |,4-  ) )-,_. ,\ (  `'-'
     '--''(_/--'  `-'\_)
!
      |\      _,,,---,,_
  ZZz /,`.-'`'    -.  ;-;;,_
     |,4-  ) )-,_. ,\ (  `'-'
     '--''(_/--'  `-'\_)
!
      |\      _,,,---,,_
   Zz /,`.-'`'    -.  ;-;;,_
     |,4-  ) )-,_. ,\ (  `'-'
     '--''(_/--'  `-'\_)
!
      |\      _,,,---,,_
    z /,`.-'`'    -.  ;-;;,_
     |,4-  ) )-,_. ,\ (  `'-'
     '--''(_/--'  `-'\_)
!
       |\---/|
       | ,_, |
        \_`_/-..----.
     ___/ `   ' ,""+ \  
    (__...'   __\    |`.___.';
      (_,...'(_,.`__)/'....."
!
       |\---/|
       | o_o |
        \_`_/-..----.
     ___/ `   ' ,""+ \  
    (__...'   __\    |`.___.';
      (_,...'(_,.`__)/'....."
!
       |\---/|
       | @_@ |
        \_`_/-..----.
     ___/ `   ' ,""+ \  
    (__...'   __\    |`.___.';
      (_,...'(_,.`__)/'....."
!
"""

DOG = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣤⣤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡏⣐⣤⡿⠿⠿⠿⠛⠛⠿⠿⠷⠶⣦⣤⣀⣤⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⠛⠉⠁⠈⠙⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⡇⠀⠚⠻⣷⡀⠘⣿⢷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠙⠁⢰⡟⠂⠙⢷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣦⠀⠀⠀⠀⠀⠀⣀⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⡿⠃⠀⠀⠀⠻⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠸⡿⠿⠿⠏⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⠏⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢠⣶⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣰⣿⣷⣶⣶⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⠇⠀⠀⠀⠀⢀⣀⣽⠿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⠀⠀⠀⠀⠀⠀⠙⠻⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠙⠻⠷⡶⢶⠶⣶⠞⠛⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢷⣄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⡷⠀⠙⢷⣄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣠⡶⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⠏⠀⠀⠀⠀⠹⣷⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⡿⠃⠀⠀⠀⠀⠀⠀⢿⡄⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢼⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠸⣧⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢺⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣆⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣹⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⡄⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣧⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡆
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠁
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⡇⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡂⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠂⠶⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡿⠁⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣹⡇⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠘⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⠃⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⡶⠿⢻⡇⠀⠀⠀⠀⠀⠀⣼⠃⠀⠀⠀⠀⠀⠀⠀⠀⢿⡀⠀⠀⠀⠀⠀⠀⠀⢠⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⠃⠀⠀⠀
⠀⠀⠀⠀⢀⣠⣴⠾⠋⠁⠀⠀⢸⡇⠀⠀⠀⠀⢀⣾⠇⢀⣠⣤⡶⠆⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⢸⣇⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⠟⠁⠀⠀⠀⠀
⠀⣴⣿⠛⣛⡋⢀⣠⣴⠶⠿⠛⢻⡇⠀⠀⠀⢠⣿⡷⠾⠛⠉⠀⠀⠀⠀⠀⠀⢰⡟⠀⠀⠀⠀⠀⠀⠀⠀⣸⡇⠀⠀⠀⠀⠀⢀⣴⠿⠋⠁⠀⠀⠀⠀⠀⠀
⠀⠻⠿⠶⠿⠿⠋⠉⠀⠀⠀⢀⣾⠃⠀⠀⢠⣿⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⢀⡿⠁⠀⠀⠀⢀⣴⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⣾⣿⠋⠀⠀⠀⣾⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⢀⣿⠃⠀⢀⣠⡶⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢀⣴⠶⠿⠟⠛⠉⠉⢀⡾⠃⠀⠀⠀⣸⡟⠛⠛⠛⠛⠛⠛⠛⠛⠛⠻⠶⠶⣮⣷⠀⠀⠀⠀⠀⢀⣾⣷⠶⠞⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢰⡿⠷⠆⠀⠀⠀⣀⣠⡿⠃⠀⠀⢀⣴⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠄⠀⠀⠀⠀⢸⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠈⠿⣦⣀⣴⠾⠛⠋⠉⠀⠀⢀⣠⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⣺⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠈⣿⣷⠀⣴⠄⢀⣠⣴⠿⠉⠀⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡿⠄⠀⠀⠀⠀⣿⡃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠈⠹⠿⠿⠿⠿⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⡇⠀⠀⠀⠀⠀⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⣰⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⠃⠀⠀⠀⠀⣿⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡾⢇⠀⡀⢸⣧⣴⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣼⡿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
!
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣦⣴⣶⣶⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⣤⣤⣤⣤⣤⣤⣤⣀⣀⣀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⠿⠟⠛⠛⠋⠉⠉⠉⠉⠉⠉⠛⠛⠛⠿⢷⣦⣤⣀⡹⠿⠿⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⣴⣶⣶⣾⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⣿⣿⣶⣶⣶⣤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣴⣿⠟⠉⠀⠀⠙⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠟⠀⠀⠀⠉⠙⢿⣦⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣠⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢦⣽⣿⡄⠀⠀⠀⠀⠀
⠀⠀⠀⣰⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣷⠀⠀⠀⠀⠀
⠀⠀⢰⣿⡏⣤⠀⠀⠀⠀⠀⢀⡼⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣻⡀⠀⠀⢤⢠⣼⣿⡆⠀⠀⠀⠀
⠀⠀⠀⢿⣿⠁⠀⠀⠀⠀⣴⡾⠁⠀⠀⠀⢀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣀⠀⠀⠀⠀⠀⠈⢻⣇⠀⠀⠈⣇⣿⣿⠀⠀⠀⠀⠀
⠀⠀⠀⢸⣿⠀⡀⣀⠀⢠⣿⠃⠀⠀⢀⣾⣿⣿⡿⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⡷⠀⠀⠀⠀⠀⢸⣿⠀⢠⣠⣿⣿⠇⠀⠀⠀⠀⠀
⠀⠀⠀⠈⢿⣷⣇⣽⠀⢈⡏⠀⠀⠀⠸⣿⣿⣿⣦⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣧⣤⠥⠀⠀⠀⠀⣿⣿⣧⣾⣿⠟⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠈⠛⠿⣿⣧⣾⣿⡄⠀⠀⠀⠙⠿⠿⠿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠛⠛⠋⠀⠀⠀⠀⠀⢸⣿⡿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⣿⡇⣴⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢶⣼⣿⣀⣠⣤⣤⣤⣀⠀⠀⠀⠀⠀
⠀⠀⣠⣶⣾⠿⠛⠛⠻⢷⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⡿⠋⠉⠉⠉⠛⢿⣦⡀⠀⠀
⢀⣾⡿⠋⠀⠀⠀⠀⠀⠀⠙⣿⡆⢀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣤⣿⡟⠀⠀⠀⠀⠀⠀⠀⠹⣿⡆⠀
⣼⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⣸⣷⣿⣷⣧⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣄⠀⢠⡾⣠⣇⣠⣿⣿⣿⡇⠀⢀⠀⠀⠀⢀⠀⠀⢹⣷⠀
⣿⣷⡀⠀⣷⠀⠀⠀⣼⣦⣴⣿⠏⠙⠻⠿⣷⡿⠷⣶⣶⡾⠿⠿⠷⢶⣶⣦⣤⣾⣿⣷⣿⣿⠿⠿⠛⠛⠙⠻⣿⣤⣾⣇⠀⢀⣸⣇⣀⣼⣿⠃
⠘⢿⣿⣾⣿⣷⣴⣾⡿⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠻⠿⠿⠿⠟⠛⠛⠁⠀
!
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣦⡀⠸⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣟⢼⣿⡽⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣷⢻⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠿⠟⠻⢿⣿⣩⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⣤⣖⡋⣍⢤⡠⣐⣌⡹⢢⠽⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠤⣒⢚⡩⣉⡙⢒⠲⢤⣀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⡴⣿⡿⢿⣿⣯⢻⡽⡹⢞⡵⢫⡗⣜⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⢫⣵⣮⣷⣿⣷⣳⣿⢮⣖⡤⣈⠳⣄⠀
⣾⣿⢛⣉⢩⠩⡜⣻⣿⣿⣿⠻⡑⢎⠱⠩⡜⢣⠞⣜⡞⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⣵⣿⣿⣾⡿⠿⠿⢿⣿⣿⣿⢿⣦⢣⠘⡆
⢿⣯⣷⢮⢧⣳⡱⣃⠮⡱⢈⠅⡈⠄⡈⠡⠜⣡⢛⡜⣞⢿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣻⣽⣿⠟⠁⠀⠀⠀⠀⠈⠛⣿⣿⣿⣿⢌⣹
⠸⣿⣟⣿⣻⣤⠻⣜⢧⡣⢇⠸⢀⠄⠠⢇⠸⣀⢟⣸⢻⡼⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⡜⣸
⠀⠻⣿⣷⣿⣿⢻⢬⢳⡝⣎⡳⣌⠬⡱⢌⡱⢎⡞⡜⣧⢻⡽⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣷⡀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣏⡟
⠀⠀⠈⠙⠛⠳⠯⣶⡣⢞⡱⣿⣼⣳⢯⣮⢵⡫⣜⡱⢎⢧⢻⡽⢧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⡞⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠙⢮⡕⢧⡿⣿⣿⣞⣧⢻⠴⣙⢎⣎⠳⣸⠩⠝⢦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣶⣿⣿⣿⣿⠋⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⢪⠽⣿⣽⣿⡽⣏⡾⡱⢎⣌⠓⡠⠁⠎⠐⡈⠉⠒⠒⠦⠤⠤⠤⠤⠤⠤⠴⠖⠒⠒⠋⠉⠉⠉⠉⠉⠙⠒⠦⣤⢞⣿⣿⣿⣿⠿⠋⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣯⠹⣽⣻⣿⢿⣽⡳⡝⠦⢌⠂⠡⠀⠀⠁⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢂⠱⡘⢾⣿⡿⠋⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡏⣖⢯⣿⣿⡷⣿⣍⠳⡈⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠠⠄⡄⠂⠄⠀⡀⠄⠠⠀⠤⠑⢢⡙⣇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣌⣻⡽⣿⣿⢷⣎⠣⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⠤⡈⠤⢡⡓⡜⡬⡑⢌⡐⠀⠠⢀⠁⢂⡉⢆⢭⣻⡄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣧⢳⣻⣿⣟⡿⣌⢇⠢⢈⠀⠀⡀⠄⣀⠂⢁⠄⡀⢂⠡⠒⣌⢢⡑⡎⡵⡹⣼⢱⡍⢦⡈⢅⠢⠁⢌⡐⢌⡚⣶⣽⣇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡇⣿⣽⡿⣿⣍⠦⡑⠢⠄⡃⢄⢣⡐⡜⡤⢊⡔⣣⢎⡵⣊⠶⣱⣹⢶⣻⡵⣯⢾⡱⣘⢆⡡⢍⠢⡌⢦⣱⣛⣾⡟⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣧⢳⢿⣻⣷⣏⢞⣡⠣⡜⡑⣎⠶⣱⢮⡵⣯⣞⡷⣮⢷⣯⢿⣳⣯⣿⣿⣿⣯⣟⡷⣍⠶⣘⢢⠓⡼⡱⣎⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣎⡿⣽⣷⣎⡳⢆⡳⣜⡱⢾⣽⣯⣿⣽⣷⣿⣿⣿⣿⣻⣿⣟⡿⣿⢿⣿⣿⣿⡿⣽⢎⡵⣊⠽⣰⠳⣝⣾⣿⡇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣽⡷⢮⡱⢏⠶⣭⢿⣿⣿⣿⣿⣿⣟⣯⣿⡾⣿⢽⡳⢯⡽⣭⣛⣾⣻⣿⣿⣟⣾⠲⣍⢞⣡⢛⣼⣳⣿⡇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣯⢳⡝⢮⣛⣾⣿⣿⣿⡿⡽⣞⡽⣳⣭⢷⣽⣾⠽⢿⣿⣽⣿⣷⣿⡽⣿⣿⣞⡿⣼⣚⡴⢫⡶⣟⣿⡇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⢯⣳⣽⣛⣾⣽⣿⣿⣯⣿⡷⠯⠟⠛⠋⠉⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣳⣝⣞⡯⣷⣻⢿⣷⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡴⣾⣟⣯⣿⣷⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣾⣽⣳⢯⣟⣿⣿⣧⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⡞⣯⢳⣽⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⠈⢻⣿⣿⣿⣿⣿⣯⣷⣿⣿⣧⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⢏⣷⣯⣿⣿⣿⣿⣿⡿⠿⠟⠛⠉⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⡟⠀⠀⠉⠻⣿⣿⣿⣿⣿⢿⣿⣿⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⠿⠛⠛⠋⠉⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠙⠻⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⡇⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣷⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣼⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⡆⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⡿⠇⠀⠀⠀⠀⠀⠀⠀⢺⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⢿⣿⣿⡇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⡉⡉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿⠿⠿⣿⠿⠁⠀⠀⠀
!
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣷⠀⠀⢠⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⡇⠀⣸⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⡇⠀⢿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀
⠀⣠⣶⣦⡀⠹⣿⣿⣿⣿⡿⠁⠀⠘⣿⣿⣿⣿⣿⠇⣠⣴⣶⡄⠀
⢰⣿⣿⣿⣿⣆⠉⠛⠛⠋⠁⣀⣀⣀⠈⠛⠛⠛⠁⣼⣿⣿⣿⣿⡀
⢸⣿⣿⣿⣿⣿⡆⠀⢀⣴⣿⣿⣿⣿⣿⣦⠀⠀⢸⣿⣿⣿⣿⣿⡇
⠈⢿⣿⣿⣿⣿⠃⣠⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⢸⣿⣿⣿⣿⠟⠀
⠀⠀⠉⠙⠋⣡⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣍⠛⠋⠁⠀⠀
⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀
⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀
⠀⠀⠀⠀⠈⠻⢿⣿⣿⣿⣿⡿⠿⢿⣿⣿⣿⣿⡿⠛⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀
!
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠒⠦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡴⠚⠒⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠷⡾⣖⡌⡳⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⣡⡿⣄⢀⢹⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⢰⠡⠮⣧⠈⠊⠷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⠃⡽⠁⠈⡾⢸⢸⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡈⡏⠁⣾⣧⠀⢠⠙⣦⠀⢀⣀⣀⣀⣀⣀⣀⠀⢠⡟⢠⠃⡀⠍⢻⠀⡀⣸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣇⢳⡀⢈⣿⣟⠰⠀⡘⠛⠉⠉⠁⠠⠀⠉⠉⠙⠻⠀⡾⢈⠝⢯⠁⠀⢠⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣆⠉⣹⣔⣇⠆⠀⠀⠀⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⠑⢎⠀⠘⡿⢣⣾⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡄⠀⠁⡹⠇⠀⠀⠀⢀⣀⠀⠀⠈⡆⠀⠀⣀⠀⠀⠀⠀⠙⡋⠀⠀⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢦⡊⠀⠀⠀⠄⠊⠠⠀⢀⠀⠀⡁⠀⠁⢠⡄⠑⠀⠀⠀⠈⢶⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣧⠀⠀⢀⣴⣖⣶⡀⠸⠀⠀⡁⠀⠀⣼⣗⣶⣄⢀⠀⢀⡞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⠀⠀⠈⠹⠿⠿⠵⠀⠀⠀⠀⠀⠐⠺⠿⠿⠋⠈⠀⣸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠄⠀⠀⠀⠀⠀⣼⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣇⠀⡀⠀⠀⠀⡀⢠⣾⣿⣿⣷⡄⠐⡀⠀⠀⠀⢀⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠀⣠⣤⡀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡏⠹⣄⠐⢈⣅⠀⠀⠈⠻⣾⣿⡾⠃⠀⠇⡼⠆⣡⠞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⡞⣢⠷⠋⣵⠄⠹⡄⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠿⣣⡀⠈⢆⠀⠹⣳⣤⣀⣀⣤⣧⣄⣀⣤⡾⠃⣾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡵⡞⠹⣧⠘⠫⣀⣴⡀⠙⣆
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠟⠁⠀⠱⣝⢦⡈⠆⠀⠈⠙⢟⢦⣀⣀⣴⣹⠉⠐⢱⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠇⠘⠿⠨⣐⡴⢾⡇⣘⡷⣞⡁
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠋⠀⠀⠀⠀⠈⠳⢍⡺⢤⣀⠀⠀⠉⠛⠙⠉⠁⠀⢀⣾⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⢴⠚⡫⡀⡐⠔⠉⢸⣷⡼⢻⢻⠀⠓⠃
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠓⠴⣍⣽⡒⠒⠒⣒⣒⣭⡵⢾⡀⠀⠀⠀⠀⠀⢀⣠⠶⣋⠡⡁⢧⣌⡾⠖⠛⠛⠋⠸⠽⠀⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠀⠀⠀⠈⢧⠀⠀⢀⣠⠶⢯⠑⢆⢈⣧⠾⠚⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⡴⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠃⠀⠀⢀⣠⠖⠚⠛⠓⠶⣄⡀⠀⠀⠀⠀⠀⠀⢈⣷⣾⣯⣧⣛⠦⣳⡶⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣠⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⣀⡴⠋⠀⠀⠀⠀⠀⠀⠈⠻⣄⠀⠀⢀⣤⢾⡋⣴⡇⠙⠀⠈⠛⢧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣟⠀⠀⠀⠀⠀⠀⠈⠑⢶⣖⠚⠋⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣘⣷⠞⣯⠸⣖⣙⣴⢿⣄⠀⠀⠀⠀⢷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢀⣤⠞⠛⢦⣀⠀⠠⡀⠀⠀⠀⠀⠙⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⢟⢣⣲⣿⢷⣩⠶⠋⠀⠀⠉⠳⠦⠄⠀⡾⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣴⠋⠀⠀⠀⠀⠉⠙⠦⣴⡄⠀⠀⠀⠀⠈⢳⡀⠀⠀⡤⣲⣶⣴⣶⣾⢻⡺⡱⣳⡷⠚⢻⣅⠀⠀⠀⠀⠀⠀⠀⢀⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣸⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡀⠀⠆⠀⠢⢘⡇⠀⡌⣿⣿⣿⣿⣿⣿⣾⡴⠛⠁⠀⠀⠀⢻⡆⣹⠲⠦⠤⠴⠞⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢦⡴⣤⠴⠞⠀⠠⢓⣿⣿⣿⣿⣿⣿⡻⡄⠀⠀⠀⠀⠀⠀⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠊⣢⡀⠄⠀⠀⠄⡪⠍⢟⡿⠿⣿⡿⠃⠀⠀⠀⠀⠀⠀⢀⡿⡧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢻⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢫⡳⣿⣅⠪⠐⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⡴⠛⢠⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠈⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⡿⡟⢦⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⡶⠟⠛⠋⠁⠀⠀⣼⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠘⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⠊⠀⠀⠀⠀⠀⠀⠀⣰⡿⠋⠀⠀⠀⠀⠀⠀⠀⠉⠙⢶⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠘⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣧⠀⠀⣼⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠘⢧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⡆⠀⠀⠀⡿⣀⣴⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠈⠻⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⡜⠀⠀⠀⢰⡟⢩⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢻⡳⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⠋⢸⠀⠀⠀⠀⠀⠀⠀⠀⡴⠁⠀⠀⠀⣼⣤⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠳⡌⠙⠶⣤⣀⡀⠀⠀⠀⣀⣠⠶⠋⠀⠀⢸⠀⠀⠀⠀⠀⠀⣠⣾⠀⠀⠀⠀⢰⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠉⠳⢤⣿⠈⠉⠙⢛⡿⠻⢤⣀⠀⠀⠀⠘⠀⠀⠀⢀⣠⠾⠋⠘⡆⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣠⡤⠤⡴⠇⠀⠀⢀⡾⠀⠀⢀⣨⠿⠓⠶⠶⠶⠒⠻⣏⡀⠀⠀⠀⢹⡄⠀⠀⠘⢦⣤⠴⠦⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣰⠇⠐⠀⠀⡀⠀⠀⣼⠷⠖⠚⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠒⠲⠶⢷⠀⠀⠀⠀⠐⠄⠀⠀⢹⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠹⢦⣥⣤⣠⣥⣤⠴⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠓⠦⠤⠤⣤⣤⣤⣤⠾⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
!
૮˶• . •˶ა
./づ~ /)
"""

HORSE = r"""
              ,~ 
           ~~/(\\ 
  ~~ _____~~/ / ` 
~~~~( )___( /'  
   /|/_  _`/|   
     \    /       
===================
!
              ,~ 
           ~~/(\\ 
  ~~ _____~~/ / ` 
~~~~( )___( /'  
    |\_  _`/|   
     `    '       
===================
!
              ,~ 
           ~~/(\\ 
   ~ _____~~/ / ` 
~~~~( )___( /'  
    |\_   `/|   
     `    //      
===================
!
             ,~ 
           ~/(\\ 
   ~ ____~~/ / ` 
 ~~~( )___( |   
    |\     ` \   
     `\    '/     
===================
!
             ,~ 
           ~/(\\ 
   ~ _____~/ / ` 
~~~~( )___(_|_  
     \     _\/   
     `\           
===================
!
             ,~ 
           ~/(\\ 
   ~ _____~/ / ` 
 ~~~( )___(_|_  
   /|/     _\/   
   ` \            
===================
!
             ,~ 
           ~/(\\ 
   ~ _____~/ / ` 
 ~~~( )___(_|_  
   / /     _\ \   
  //          '   
===================
!
             ,~ 
           ~/(\\ 
   ~ _____~/ / ` 
 ~~~( )___(_|_  
   /|/_      \ \   
   `          \ ' 
===================
!
             ,~  
           ~/('\
  ~ ______~//  `
~~~( )___(  |    
   |/|    \||   
   | /    -'|
===================
!
           ~,
         /'/)'
  ~ _____`'//
~~~( )___(  |    
   |/|    \||   
   | /    -'| 
===================
"""

TIME_TRAVEL = [
    # Past.
    "1893. The first successful zipper was invented by Whitcomb L. Judson, but it was initially called the 'Clasp Locker.'",
    "1932. Australia declared 'war' on emus (The Great Emu War) and lost, requiring the military to be withdrawn.",
    "1850. U.S. President Zachary Taylor died, possibly from consuming large amounts of cherries and iced milk at a Fourth of July celebration.",
    "1770. Ketchup was sold in the 1830s as a medicine, claiming to cure an upset stomach and other ailments.",
    "1963. Andrew Jackson's pet parrot, named Poll, had to be removed from his funeral because it started swearing profusely.",
    "1920. French President Paul Deschanel fell out of his moving train in the middle of the night and was found walking in his pajamas.",
    "1807. Napoleon Bonaparte was once attacked and defeated by a horde of rabbits he had requested for a hunt.",
    "1889. Nintendo, the famous video game company, was founded to produce handmade Hanafuda playing cards.",
    "1977. The last person to be executed by guillotine in France died in the same year the movie *Star Wars* was released.",
    "1386. A pig was executed by hanging in France for the murder of a child, following a formal trial.",
    "44 B.C. Julius Caesar was assassinated on the Ides of March, but the construction of the Colosseum in Rome began over a century later in 72 A.D.",
    "2550 B.C. Cleopatra, the last pharaoh of Egypt, lived closer in time to the launch of the iPhone than to the building of the Great Pyramids.",
    "1960. The two songwriters of the baseball classic 'Take Me Out to the Ball Game' had never actually been to a baseball game.",
    "1928. Scottish scientist Alexander Fleming discovered penicillin after returning from vacation to find mold had contaminated a petri dish.",
    "1886. Coca-Cola was first sold as a tonic at a soda fountain in Atlanta, Georgia.",
    "1347. Historians believe the Bubonic Plague, or Black Death, began to spread through Europe.",
    "1967. Sweden conducted Dagen H, switching all traffic from driving on the left-hand side of the road to the right.",
    "1812. The Brothers Grimm published their first collection of German fairy tales, including 'Hänsel und Gretel.'",
    "1667. The world's most overdue library book was returned to Sidney Sussex College in 1956, 288 years late.",
    "1512. Machu Picchu was finished within a century of Michelangelo completing the Sistine Chapel ceiling frescoes.",
    "1799. George Washington's Mount Vernon distillery was the largest in the U.S., producing over 11,000 gallons of whiskey.",
    "1890. The first person to land on the moon, Neil Armstrong, was born 39 years after Pluto was first named by an 11-year-old girl.",
    "1930. The BBC once announced, 'There is no news' on April 18th because there genuinely was nothing significant to report.",
    "1000 A.D. Viking explorer Leif Erikson and his people arrived in North America (Newfoundland, Canada) almost 500 years before Christopher Columbus.",
    "1919. The Boston Molasses Flood killed 21 people and injured 150 when a massive molasses storage tank burst.",
    "1947. India gained its independence from Britain, marking a significant end to colonial rule.",
    "1888. The mysterious serial killer known as Jack the Ripper terrorized the Whitechapel district of London.",
    "1955. Rosa Parks refused to give up her seat on a bus in Montgomery, Alabama, sparking the Civil Rights Movement.",
    "1845. The Great Famine began in Ireland, triggered by a potato blight that led to mass starvation and emigration.",
    "1908. Tunguska Event: A massive explosion, likely from an asteroid, flattened 2,000 square kilometers of forest in Siberia.",
    "1455. Johannes Gutenberg completed the printing of his Bible, revolutionizing the spread of knowledge.",
    "1989. The Berlin Wall fell, symbolizing the end of the Cold War and the reunification of Germany.",
    "1914. During World War I, a temporary Christmas Truce allowed soldiers from opposing sides to exchange gifts and play football.",
    "1961. The first woman in space, Valentina Tereshkova, went without a toothbrush during her three-day flight aboard Vostok 6.",
    "1904. Cotton candy was invented by a dentist and a confectioner and was introduced at the St. Louis World's Fair.",
    "1900. Tug-of-war was an actual Olympic sport at the Summer Games, lasting until 1920.",
    "1944. William Patrick Hitler, Adolf Hitler's half-nephew, served in the U.S. Navy during World War II.",
    "1935. A man in the U.K. invented a specialized piano for bedridden patients to play while lying flat on their backs.",
    "1885. The Statue of Liberty was a gift from the people of France to the people of the United States.",
    "1838. Edgar Allan Poe's novel *The Narrative of Arthur Gordon Pym* featured a cabin boy named Richard Parker, a name later mirrored in a real-life shipwreck tragedy.",
    "1859. The shortest war in history, between Britain and Zanzibar, lasted only 38 to 45 minutes.",
    "1888. A newspaper in the U.S. claimed life had been discovered on the Moon, a hoax that fooled many readers.",
    "1933. The Business Plot: A group of wealthy businessmen allegedly planned a coup to overthrow President Franklin D. Roosevelt.",
    "1970. The Oregon Exploding Whale Incident occurred when a beached whale carcass was blown up with dynamite.",
    "1968. The ancient Greek word for 'gymnastics' comes from 'gumnós,' meaning 'naked,' as athletes performed nude.",
    "1950. The British considered filling a nuclear bomb, codenamed 'Blue Peacock,' with live chickens to keep its electronics warm in the cold German climate.",
    "1888. The Roman-Persian Wars are the longest in history, lasting over 680 years, from 54 B.C. to 628 A.D.",
    "1969. Steven Hawking held a party for time travelers, but only advertised it after the event, and no one showed up.",
    "1887. The Eiffel Tower was originally intended to be a temporary structure for the 1889 World's Fair.",
    "1965. The U.S. Air Force reportedly investigated reports of a possible UFO crash in Kecksburg, Pennsylvania, recovering a metallic, acorn-shaped object.",
    "1912. The RMS Titanic sank after hitting an iceberg on its maiden voyage from Southampton to New York City.",
    "1945. Tsutomu Yamaguchi is the only person officially recognized by the government of Japan as having survived both the Hiroshima and Nagasaki atomic bombings.",
    "1986. The Chernobyl disaster occurred at the nuclear power plant in the Ukrainian Soviet Socialist Republic.",
    "1930. Pluto was officially discovered by Clyde Tombaugh at the Lowell Observatory in Arizona.",
    "1834. Abraham Lincoln earned a reputation as an elite fighter and is a member of the Wrestling Hall of Fame.",
    "1588. The Spanish Armada, a massive fleet of 130 ships, was defeated by the English navy and a severe storm.",
    "1941. During World War II, the U.S. military once tried to attack a German submarine using potatoes.",
    "1858. The word 'OMG' (Oh My God!) was first used in a letter to Winston Churchill, decades before it was popularized by text messaging.",
    "1787. Thomas Jefferson and John Adams, two future U.S. Presidents, stole pieces of Shakespeare's chair as souvenirs.",
    "1898. The United States annexed the Republic of Hawaii, making it a U.S. territory.",
    "1939. The British government coined the slogan 'Keep Calm and Carry On' during World War II, but it was rarely used at the time.",
    "1503. Leonardo da Vinci began painting the Mona Lisa, which is arguably the most famous painting in the world.",
    "1963. Lyndon B. Johnson, the 36th U.S. President, liked to conduct serious meetings while sitting on the toilet.",
    "1947. The Dead Sea Scrolls, a collection of ancient Jewish religious manuscripts, were first discovered by a Bedouin shepherd.",
    "1957. A con artist named Victor Lustig successfully 'sold' the Eiffel Tower for scrap metal not once, but twice.",
    "1907. French waiters went on strike to win the right to grow mustaches, which was a popular fashion at the time.",
    "1773. The Boston Tea Party was a protest against the Tea Act, which gave a British company a monopoly on tea sales.",
    "1960. The Soviet Union experimented with 'flying tank' concepts during World War II.",
    "1818. Mary Shelley's novel *Frankenstein; or, The Modern Prometheus* was published, a seminal work of the horror genre.",
    "1959. The Mini car, an iconic British vehicle, was originally designed as a response to the Suez Crisis fuel shortage.",
    "1839. The longest war in history without a single casualty was between the Netherlands and the Isles of Scilly, lasting 335 years.",
    "1953. The first successful ascent of Mount Everest was achieved by Edmund Hillary and Tenzing Norgay.",
    "1876. Alexander Graham Bell made the world's first phone call to his assistant, Thomas Watson: 'Mr. Watson. Come here. I want to see you.'",
    "1892. The Pledge of Allegiance was written by Francis Bellamy, a Baptist minister.",
    "1945. The Nuremberg Trials began, prosecuting major war criminals from World War II.",
    "1930. The Guinness Book of Records was created to settle arguments between people in pubs.",
    "1827. Lord Byron, a famous poet, kept a pet bear in his Trinity College dorm room because the college forbade dogs.",
    "1900. Queen Victoria censored Michelangelo's famous statue *David* by hiding its genitals with a fig leaf for certain public displays.",
    "1937. The *Hindenburg* airship exploded in Lakehurst, New Jersey, marking the end of the airship era.",
    "1927. The first feature film with synchronized sound, *The Jazz Singer*, was released, ending the silent film era.",
    "1930. The Voynich Manuscript, a medieval text with an unknown script and bizarre illustrations, remains undeciphered.",
    "1955. Walt Disney opened Disneyland in Anaheim, California, the first Disney theme park.",
    "1963. The first commercial cassette tape was introduced, originally intended for dictation rather than music.",
    "1945. World War II officially ended with the surrender of Japan.",
    "1803. The United States purchased the Louisiana Territory from France, nearly doubling the country's size.",
    "1905. Horse diving, an act where a horse and sometimes a rider jumped from a high platform into water, was a popular spectacle.",
    "1969. The Apollo 11 mission successfully landed the first humans on the Moon.",
    "1840. The penny black, the world's first adhesive postage stamp, was issued in the United Kingdom.",
    "1980. The U.S. men's Olympic hockey team defeated the Soviet Union, a game known as the 'Miracle on Ice.'",
    "1930. The planet Uranus was originally named 'George's Star' by its discoverer, William Herschel.",
    "1930. In the 1930s, London mothers would suspend their babies in wire cages outside high-rise windows to give them fresh air.",
    "1971. The first email was sent by Ray Tomlinson, who also chose the '@' symbol to separate the user name from the host name.",
    "1838. Victorians in the 19th century held 'mummy unwrapping parties' as a form of entertainment.",
    "1928. Scottish scientist Alexander Fleming discovered penicillin, a major breakthrough in medicine.",
    "1906. The San Francisco earthquake and subsequent fires destroyed over 80% of the city.",
    "1789. George Washington became the first President of the United States.",
    "1940. The first McDonald's restaurant was opened by brothers Richard and Maurice McDonald in San Bernardino, California.",
    "1954. The phrase 'under God' was added to the U.S. Pledge of Allegiance.",
    "1963. The *Mona Lisa* was insured for $100 million for a trip to the United States, making it the most expensive insurance policy ever written.",
    "1903. The Wright brothers achieved the first sustained flight of a heavier-than-air powered aircraft.",
    "1935. Elvis Presley was naturally blonde and used shoe polish to dye his hair black for his signature look.",
    "1963. The Martin Luther King Jr. delivered his 'I Have a Dream' speech during the March on Washington.",
    "1804. The Lewis and Clark Expedition began its journey to explore the Western part of the United States.",
    "1945. The invention of the microwave oven was an accidental discovery by Percy Spencer while working on radar technology.",
    "1933. Albert Einstein was offered the presidency of Israel, but he declined.",
    "1799. The Rosetta Stone was discovered by French soldiers in Egypt, providing the key to deciphering Egyptian hieroglyphs.",
    "1900. Max Planck introduced the concept of quantum theory, fundamentally changing physics.",
    "1791. Wolfgang Amadeus Mozart died while working on his *Requiem Mass*.",
    "1955. The original formula for WD-40 was developed to protect the Atlas missile from rust and corrosion.",
    "1937. Amelia Earhart vanished over the Pacific Ocean during her attempt to circumnavigate the globe.",
    "1944. The Battle of the Bulge, the last major German offensive campaign on the Western Front during World War II, began.",
    "2560 BCE. The Great Pyramid of Giza was completed, an eternal testament to pharaonic power.",
    "1347. The Black Death arrived in Europe, carried by Genoese trading ships.",
    "1543. Nicolaus Copernicus published 'De revolutionibus orbium coelestium,' proposing the sun, not the earth, was the center of the universe. ",
    "44 BCE. Julius Caesar was assassinated on the Ides of March, plunging Rome into chaos.",
    "79 CE. Mount Vesuvius erupted, burying the Roman cities of Pompeii and Herculaneum.",
    "105. Chinese official Cai Lun is traditionally credited with inventing paper, a crucial step for communication.",
    "1492. Christopher Columbus reached the Americas, dramatically altering the course of world history.",
    "1215. King John of England signed the Magna Carta, limiting the power of the monarchy.",
    "1633. Galileo Galilei was tried by the Roman Inquisition for supporting the heliocentric theory.",
    "323 BCE. Alexander the Great, one of history's most successful military commanders, died in Babylon.",
    "1066. William the Conqueror successfully invaded England at the Battle of Hastings.",
    "1450. Johannes Gutenberg began developing the movable-type printing press, sparking a revolution in knowledge.",
    "1588. The English fleet defeated the Spanish Armada, securing England's naval dominance.",
    "509 BCE. The Roman Republic was established after the overthrow of the Roman monarchy.",
    "1431. Joan of Arc was burned at the stake in Rouen by the English.",
    "1600. The British East India Company was founded, marking the beginning of a vast colonial enterprise.",
    "1325. The Aztecs founded their capital city, Tenochtitlan (modern-day Mexico City).",
    "1533. Henry VIII secretly married Anne Boleyn, leading to the English Reformation.",
    "1610. Galileo Galilei published his observations of the moon and stars, seen through his newly improved telescope.",
    "1271. Marco Polo began his journey along the Silk Road to Asia.",
    "1607. The first permanent English settlement in North America was established at Jamestown, Virginia.",
    "600 BCE. Thales of Miletus is traditionally credited with establishing the field of geometry by using deductive reasoning.",
    "1517. Martin Luther posted his 95 Theses in Wittenberg, initiating the Protestant Reformation.",
    "1189. The Third Crusade, led by powerful European monarchs, began to retake the Holy Land.",
    "800 CE. Charlemagne was crowned Emperor of the Romans by Pope Leo III, signifying the fusion of Roman, Christian, and Germanic elements in Europe.",
    "1620. The Pilgrims landed at Plymouth Rock in Massachusetts.",
    "399 BCE. The Greek philosopher Socrates was executed by drinking hemlock after being convicted of impiety and corrupting the youth.",
    "1453. Constantinople, the last bastion of the Byzantine Empire, fell to the Ottoman Turks.",
    "1642. The English Civil War began, pitting Parliament against King Charles I.",
    "1556. The Shaanxi earthquake in China occurred, possibly the deadliest earthquake in human history.",
    "1000 BCE. The Olmec civilization, considered the mother culture of Mesoamerica, began to flourish.",
    "1521. Hernán Cortés and his forces completed the conquest of the Aztec Empire.",
    "1665. The Great Plague of London killed an estimated 100,000 people.",
    "30 CE. The traditional year for the crucifixion of Jesus Christ.",
    "1687. Sir Isaac Newton published 'Philosophiæ Naturalis Principia Mathematica,' defining the laws of motion and universal gravitation.",
    "170. Roman emperor Marcus Aurelius is rumored to have fought gladiators in the arena for 'fun'.",
    "1232. Pope Gregory IX issued the papal bull 'Vox in Rama' against a Luciferian cult, often (but incorrectly) cited as the start of a mass black cat extermination.",
    "1626. Peter Minuit purchased the island of Manhattan from local Native Americans for the Dutch.",
    "1590. The settlers of the Roanoke Colony, known as the 'Lost Colony,' were found to have vanished without a trace.",
    "213 BCE. Emperor Qin Shi Huang of China ordered the burning of books and the burial of scholars to consolidate his power.",
    "1666. The Great Fire of London destroyed a massive portion of the city, but also helped to end the Great Plague.",
    "1555. The Peace of Augsburg allowed princes in the Holy Roman Empire to choose either Catholicism or Lutheranism for their territories.",
    "1488. Bartolomeu Dias became the first European mariner to round the southern tip of Africa.",
    "622. The *Hijra*, the Prophet Muhammad's journey from Mecca to Medina, marked the beginning of the Islamic calendar.",
    "1096. The First Crusade began, aiming to recapture the Holy Land from Muslim control.",
    "1572. The St. Bartholomew's Day Massacre saw thousands of Huguenots (French Protestants) killed in France.",
    "1603. 'Elizabeth I' died, ending the Tudor dynasty and bringing 'James I' (of the Stuart dynasty) to the English throne.",
    "1184 BCE. The traditional date for the fall of Troy to the Mycenaean Greeks.",
    "1503. Leonardo da Vinci began work on the *Mona Lisa*.",
    "1776. The signers of the U.S. Declaration of Independence did not sign it all on the same day; the main signing ceremony took place on August 2, not July 4.",
    "1907. Theodore Roosevelt, the 26th U.S. President, once read a book while undergoing an emergency appendectomy at a remote ranch.",
    "1922. King Tutankhamun's tomb was discovered by Howard Carter, largely intact, in Egypt's Valley of the Kings.",
    "1959. Fidel Castro banned the game of Monopoly in Cuba after the Cuban Revolution.",
    "1952. Albert Einstein’s final words are unknown because the nurse at his bedside did not understand German.",
    "1916. Winston Churchill, a politician and future Prime Minister, was a serving soldier on the Western Front during World War I.",
    "1804. The Russian-American Company offered an official bounty on crows in Sitka, Alaska, because they kept stealing clothes and food.",
    "1958. During a U.S. military test, a hydrogen bomb was accidentally dropped on a farm near Florence, South Carolina.",
    "1935. The practice of putting sliced oranges on a roast turkey was a Christmas tradition popularized in the UK.",
    "1945. After World War II, the U.S. created a 'Bat Bomb,' which were incendiary devices attached to bats that would be released over Japan.",
    "1871. The Great Chicago Fire, which destroyed a vast portion of the city, was falsely blamed on a cow knocking over a lantern.",
    "1903. The first successful electric traffic signal was patented by a Utah policeman, Lester Wire, and was installed in Salt Lake City.",
    "1924. The Soviet Union attempted to create a hybrid ape-human super-soldier by inseminating female chimpanzees with human sperm.",
    "1986. Mexican officials issued a national decree to protect a single sacred cactus that was planted near a new highway.",
    "1950. The British military considered using gay propaganda to turn German soldiers into homosexuals during World War II.",
    "1901. Queen Victoria, the longest-reigning British monarch until Elizabeth II, died after ruling for over 63 years.",
    "1770. A series of political and economic tensions led to the Boston Massacre, where British soldiers killed five colonists.",
    "1937. The golden gate bridge in San Francisco was completed, becoming the longest suspension bridge in the world at the time.",
    "1865. U.S. President Abraham Lincoln was assassinated by John Wilkes Booth at Ford's Theatre in Washington, D.C.",
    "1949. George Orwell's dystopian novel *Nineteen Eighty-Four* was published, introducing concepts like 'Big Brother' and 'thoughtcrime'.",
    "1932. Bonnie and Clyde, the infamous American criminal couple, began their two-year crime spree across the central United States.",
    "1519. Ferdinand Magellan began his voyage, which would result in the first circumnavigation of the Earth, although he died en route.",
    "1788. Lord Byron, a famous poet, kept a pet bear in his Trinity College dorm room because the college forbade dogs.",
    "1948. Gandhi, the leader of India's independence movement, was assassinated by a Hindu nationalist.",
    "1960. The first successful kidney transplant was performed between identical twins in Boston, Massachusetts.",
    "1896. The first modern Olympic Games were held in Athens, Greece, reviving the ancient tradition.",
    "1912. The sinking of the RMS Titanic led to the establishment of the International Ice Patrol to monitor icebergs in the North Atlantic.",
    "1926. The Great Bairam, a Muslim holiday, was celebrated in Turkey with the government's permission to wear traditional fez hats, which had previously been banned.",
    "1775. Patrick Henry delivered his famous 'Give me liberty, or give me death!' speech to the Virginia Convention.",
    "1981. The launch of the IBM Personal Computer (PC) marked a significant shift toward personal computing.",
    "1969. The Woodstock Festival, a pivotal moment in music history, took place in Bethel, New York.",
    "1945. The Potsdam Conference brought together the leaders of the Allied powers to decide on the administration of Germany after World War II.",
    "1837. Queen Victoria ascended to the British throne at the age of 18.",
    "1927. Charles Lindbergh completed the first solo, non-stop transatlantic flight in his plane, the *Spirit of St. Louis*.",
    "1859. Charles Darwin published *On the Origin of Species*, proposing the theory of natural selection.",
    "1953. James Watson and Francis Crick published their paper describing the double helix structure of DNA.",
    "1994. Nelson Mandela was inaugurated as South Africa's first democratically elected president.",
    "1643. Louis XIV became King of France at the age of four, beginning the longest reign of any monarch in European history.",
    "1879. Thomas Edison successfully tested a durable electric light bulb, marking the dawn of the electrical age.",
    "1789. The storming of the Bastille in Paris is widely regarded as the start of the French Revolution.",
    "1913. Henry Ford implemented the first moving assembly line for the mass production of an entire automobile.",
    "1967. Dr. Christiaan Barnard performed the world's first successful human-to-human heart transplant in South Africa.",
    "1975. The Vietnam War officially ended with the fall of Saigon to North Vietnamese forces.",
    "1598. Shakespeare's *Romeo and Juliet* was first published, cementing his status as a literary giant.",
    "1939. Germany invaded Poland, officially beginning World War II in Europe.",
    "1905. The Russian Revolution of 1905 was a wave of mass political and social unrest that foreshadowed the 1917 revolution.",
    "1848. The Seneca Falls Convention, the first women's rights convention, was held in New York.",
    "1962. The Cuban Missile Crisis brought the U.S. and the Soviet Union to the brink of nuclear war.",
    "1894. The Dreyfus affair, a major political scandal, began in France with the false conviction of a Jewish army captain for treason.",
    "1929. The Wall Street Crash, known as Black Tuesday, marked the beginning of the Great Depression.",
    "1959. The Soviet spacecraft Luna 2 became the first man-made object to reach the surface of the Moon.",
    "1707. The Acts of Union formally united the Kingdom of England and the Kingdom of Scotland into a single kingdom, Great Britain.",
    "1991. The collapse of the Soviet Union formally ended the Cold War.",
    "1516. Thomas More's *Utopia* was published, depicting a fictional island society and its religious, political, and social customs.",
    "1947. The United Nations approved the plan to partition Palestine into separate Arab and Jewish states.",
    "1805. The Battle of Trafalgar saw the British Royal Navy decisively defeat the combined fleets of the French and Spanish Navies.",
    "1961. Yuri Gagarin became the first human to journey into outer space, orbiting the Earth aboard Vostok 1.",
    "1950. The Korean War began when North Korea invaded South Korea.",
    "1853. The Crimean War began, fought primarily between Russia and an alliance of France, the United Kingdom, and the Ottoman Empire.",
    "1948. The Marshall Plan, a U.S. program to provide aid to Western Europe following World War II, was implemented.",
    "1885. Karl Benz patented the first practical automobile powered by an internal combustion engine.",
    "1938. The *Anschluss*, the annexation of Austria into Nazi Germany, was completed.",
    "1918. World War I ended with the signing of the armistice.",
    "1609. Galileo Galilei became the first person to use a telescope for astronomical observations, leading to major discoveries.",
    "1956. The Suez Crisis began when Egypt nationalized the Suez Canal, leading to an international conflict.",
    "1869. The Suez Canal, connecting the Mediterranean Sea to the Red Sea, was officially opened.",
    "1800. The Library of Congress was established in Washington, D.C.",
    "1917. The United States officially declared war on Germany, entering World War I.",
    "1990. The Hubble Space Telescope was launched into low Earth orbit.",
    "1825. The Erie Canal, connecting the Great Lakes to the Atlantic Ocean via the Hudson River, was completed.",
    "1949. NATO (North Atlantic Treaty Organization) was established to provide collective security against the Soviet Union.",
    "1833. Slavery was abolished throughout the British Empire.",
    "1964. The Civil Rights Act of 1964 was signed into law in the U.S., outlawing discrimination based on race, color, religion, sex, or national origin.",
    "1900. Boxer Rebellion: A violent anti-foreign, anti-colonial, and anti-Christian uprising took place in China.",
    "1963. The Buddhist monk Thích Quảng Đức self-immolated in a busy Saigon intersection to protest the persecution of Buddhists by the South Vietnamese government.",
    "1862. The Battle of Antietam, the bloodiest single-day battle in American history, took place during the U.S. Civil War.",
    "1979. Margaret Thatcher became the first female Prime Minister of the United Kingdom.",
    "1884. The Prime Meridian was established at the Royal Observatory in Greenwich, London.",
    "1901. Marconi successfully transmitted the first transatlantic radio signal.",
    "1958. NASA, the National Aeronautics and Space Administration, was created by the U.S. government.",
    "1909. Robert Peary claimed to be the first person to reach the geographic North Pole.",
    "1936. Jesse Owens won four gold medals at the Berlin Olympics, challenging Hitler's Aryan supremacy ideals.",
    "1920. The 19th Amendment to the U.S. Constitution was ratified, granting women the right to vote.",
    "1775. The American Revolutionary War began with the Battles of Lexington and Concord.",
    "3500 B.C. The Sumerians in Mesopotamia developed cuneiform, one of the earliest known writing systems, initially using reeds to make wedge-shaped marks on clay tablets.",
    "5000 B.C. Evidence suggests the wheel was first invented and used by the Sumerians, not for transportation, but as a potter's wheel to create clay vessels.",
    "3200 B.C. The Narmer Palette, an archaeological find, is often cited as depicting the unification of Upper and Lower Egypt under a single ruler, marking the beginning of the dynastic period.",
    "3000 B.C. Copper was one of the first metals to be smelted and used by early civilizations, particularly in the Middle East and parts of Asia, marking the transition from the Stone Age.",
    "7000 B.C. Çatalhöyük, in modern-day Turkey, was a large Neolithic settlement where residents accessed their homes through holes in the roof, indicating a focus on protection and shared community walls.",
    "4000 B.C. The earliest known evidence of beer brewing comes from the ancient Sumerians in Mesopotamia, who considered it a dietary staple and even paid laborers with it.",
    "2600 B.C. The Indus Valley Civilization, one of the three earliest great cradles of civilization, built sophisticated, planned cities like Mohenjo-Daro and Harappa with advanced urban sanitation and grid-like streets.",
    "9000 B.C. Jericho, located near the Jordan River, is one of the oldest continuously inhabited settlements in the world, dating back to the Mesolithic period.",
    "2700 B.C. Imhotep, an ancient Egyptian polymath, is credited as the architect of the Step Pyramid of Djoser, considered the earliest large-scale cut stone construction in history.",
    "10,000 B.C. The domestication of dogs is believed to have been completed in the Paleolithic era, long before the domestication of other animals like sheep, goats, or cattle.",
    "2800 B.C. A standardized system of weights and measures, including the use of cube-shaped stone weights, was employed in the sophisticated trading network of the Indus Valley Civilization.",
    "1754 B.C. The Code of Hammurabi, one of the earliest and most complete legal codes, was inscribed on a large stone stele for public view in Babylon, establishing the principle of 'an eye for an eye' (lex talionis).",
    "15,000 B.C. The famous cave paintings at Lascaux, France, were created by Paleolithic humans, depicting large animals like horses, deer, and aurochs with remarkable detail.",
    "2000 B.C. The Minoan civilization on the island of Crete developed an advanced script called Linear A, which remains largely undeciphered by modern scholars.",
    "2334 B.C. Sargon of Akkad rose to power, establishing the Akkadian Empire, which is often cited as the world's first true empire, uniting Sumerian city-states.",
    "4500 B.C. Early surgical practices, including skull trepanation (drilling a hole in the skull), were performed by Neolithic peoples, with evidence suggesting some patients survived the procedure.",
    "3100 B.C. Stonehenge, the monumental prehistoric structure in England, began its construction, with the earliest phase involving the creation of the circular earthwork and ditch.",
    "1600 B.C. The eruption of the Thera volcano (modern-day Santorini) devastated the Minoan civilization, possibly inspiring the legend of the lost city of Atlantis.",
    "6000 B.C. The oldest known boat, the Pesse canoe, was carbon-dated and discovered in the Netherlands, having been hollowed out from a single Scots pine log.",
    "3300 B.C. Ötzi the Iceman, a well-preserved natural mummy of a man who lived in the Copper Age, was found in the Ötztal Alps with a sophisticated copper axe and a bow and arrows.",
    "3100 B.C. The earliest known evidence of the use of subtraction and addition in mathematics comes from Sumerian clay tablets, necessary for recording transactions and resources.",
    "2500 B.C. The city of Ur, a major Sumerian city-state, constructed the Great Ziggurat of Ur, a massive stepped temple dedicated to the moon god Nanna.",
    "1353 B.C. Pharaoh Akhenaten of Egypt attempted a radical monotheistic religious reform, exclusively worshipping the sun disk god, Aten, a stark deviation from traditional Egyptian polytheism.",
    "1985 B.C. King Sargon of Akkad is furious because his favorite scribe keeps leaving out the oxford comma. Scribal error rate is at 10%.",
    "476 A.D. Rome has fallen, but the Visigoths are now complaining that the city's new aqueduct system has terrible water pressure for their newly installed dishwashers. Energy efficiency is rated 'D'.",
    "1066 A.D. Harold Godwinson is spotted at the Battle of Hastings wearing a 'Team William' baseball cap ironically. His shield wall formation is impeccable, but his sense of humor is not.",
    "1492 A.D. Columbus is trying to fund his trip by selling 'Get Rich Quick' crypto-currency schemes to Queen Isabella. The transaction fee is 5 doubloons.",
    "1665 A.D. Isaac Newton is avoiding the plague by remote-working. He sends his paper on gravity to the Royal Society via a very slow dial-up modem. He calculates $F = G \\frac{m_1 m_2}{r^2}$ while waiting for the connection.",
    "1776 A.D. The Founding Fathers are signing the Declaration of Independence, but Thomas Jefferson insists on using a tiny, decorative feather pen instead of the official quill. It takes him an hour to sign his name.",
    "1888 A.D. Jack the Ripper is evading the police by using a prepaid burner phone and a cleverly routed VPN. His online manifesto only gets 3 likes.",
    "1929 A.D. The Great Depression hits, and the only thing Wall Street investors can afford is a single avocado for their toast. Market value drops 80% after lunch.",
    "1969 A.D. Neil Armstrong takes his first steps on the moon, then pulls out a selfie stick and spends five minutes trying to find the perfect angle. The photo is slightly blurry due to the low-gravity wobble.",
    "1347 A.D. A medieval peasant is arguing with a tax collector about his 4-star rating on Yelp for his service. His plague immunity rating is 2.5 stars.",
    "500 BC. Socrates is teaching his students, but keeps pausing because he can't figure out how to mute his microphone on his tablet. His wisdom is periodically interrupted by a beeping sound.",
    "79 A.D. Mount Vesuvius erupts, and a Pompeii resident runs out of the house only after tweeting, 'Worst. Day. Ever.' The post immediately goes viral.",
    "1815 A.D. Napoleon is defeated at Waterloo and is exiled to St. Helena, where he spends his time endlessly scrolling through cat videos on a small, solar-powered device. He misses his chance to conquer the world because he was watching a funny Persian cat video.",
    "33 A.D. A group of disciples are trying to split a subscription service for the upcoming gospel, but keep arguing over who gets the premium tier. Judas is insisting on a family plan.",
    "2500 B.C. An Egyptian Pharaoh is supervising the building of his pyramid and is complaining about the quality of the workers' 'work-life balance' because they are not responding to his texts immediately. He promises a 'pizza party' when the capstone is placed.",
    
    # Future.
    "2073. Jokes are now protected by copyright law. Enjoy the past :)",
    "2197. Hunger and pain are eradicated. Humanity won against the aliens. Saving symbol is still a floppy disk 💾",
    "2077. The only reliable form of currency is high-fives. Getting one from a robot costs 30,000 credits. Saving symbol is still a floppy disk 💾",
    "2242. Our self-driving cars now complain about traffic, but won't let us take the wheel. The space-time continuum is held together by duct tape. Saving symbol is still a floppy disk 💾",
    "2301. Earth is now a giant theme park for intergalactic tourists. The main attraction is watching humans try to set up Wi-Fi. Saving symbol is still a floppy disk 💾",
    "2450. The Great War of the Century was fought over which brand of avocado toast was superior. Avocado toast is still inexplicably expensive. Saving symbol is still a floppy disk 💾",
    "2519. We have achieved immortality, but everyone spends their time debating whether 'The Office' is better than 'Parks and Rec' for the 500th year. Saving symbol is still a floppy disk 💾",
    "2605. Everything is chrome and flies, except for the one public bus route that is perpetually late and still uses combustion engine. Saving symbol is still a floppy disk 💾",
    "2788. Thanks to genetic engineering, everyone is a perfect physical specimen, which mostly just means we're all very disappointed with our own personalities.",
    "2899. AI has taken over all jobs. Humans are now paid a universal basic income to produce highly-curated, aesthetically pleasing content for the AI to 'enjoy'.",
    "3000. We finally colonised Mars, but we forgot to pack enough charging cables. Society collapsed into squabbling over the last USB-C adapter. Saving symbol is still a floppy disk 💾",
    "3141. Teleportation is commonplace, but the user agreement makes you sit through a 30-second unskippable ad before every jump. Saving symbol is still a floppy disk 💾",
    "3200. The concept of 'spam email' has evolved into telepathic junk mail. You can't mute the one that keeps trying to sell you moon-based real estate. Saving symbol is still a floppy disk 💾",
    "3333. Fashion has regressed. Everyone wears neon parachute pants and aggressively chunky sneakers, entirely by choice. Saving symbol is still a floppy disk 💾",
    "3470. Language has been condensed. All meaningful conversation is now conducted using a single, highly expressive sigh. Saving symbol is still a floppy disk 💾",
    "3501. The robots created a masterpiece, a poem so beautiful it brought humanity to tears. It was an instruction manual for a poorly designed bookshelf. Saving symbol is still a floppy disk 💾",
    "3621. Global warming was solved, but now everything is slightly *too* comfortable, leading to a worldwide epidemic of mild existential boredom. Saving symbol is still a floppy disk 💾",
    "3789. Time travel was invented, and the first thing everyone did was go back and try to warn their past selves about that awkward haircut. Saving symbol is still a floppy disk 💾",
    "3900. Gravity is optional, but only in designated zones, and the queues are astronomical. Saving symbol is still a floppy disk 💾",
    "4000. Humans are now mostly holograms, but we still instinctively check our holographic pockets for a non-existent phone. Saving symbol is still a floppy disk 💾",
    "4101. We achieved world peace, but the new global obsession is competitive staring contests. The current champion is a pigeon. Saving symbol is still a floppy disk 💾",
    "2035. The 'smart' toaster now argues with you about bread choices. It suggests whole wheat, but you want a bagel. **The eternal breakfast war begins.**",
    "2051. Flying cars are finally common. The main source of traffic congestion is now **aerial fender-benders** caused by people texting on holographic windshields.",
    "2077. Everyone has a personal AI companion. Unfortunately, they all sound exactly like a 1990s GPS voice, and they still insist on calculating the 'fastest route' through a black hole.",
    "2099. Humanity achieves interstellar travel. The first message sent back to Earth is a complaint about the poor Wi-Fi signal in the Andromeda galaxy.",
    "2150. Fashion consists solely of chrome jumpsuits. Yet, somehow, dry cleaning still costs an arm and a leg, and they still lose your socks.",
    "2230. Universal basic income is implemented. People mostly use it to buy artisanal, historically accurate, non-synthetic kale chips.",
    "2301. Time travel is invented, but only forward. People are constantly disappointed that the future looks exactly like the present, just with more complex remotes.",
    "2404. We discover the secret to eternal life. It's really tedious. Everyone mainly just complains about the rising cost of galactic condo maintenance.",
    "2567. Earth is a sprawling nature preserve. The supreme ruler is a highly opinionated, genetically engineered capybara who mandates a 4 PM nap time.",
    "2689. Teleportation is instantaneous, but you still have to wait 3-5 business days for the confirmation email to arrive.",
    "2800. Robots perform all labor. Their union, 'Unit 734', is currently striking because they refuse to scrub the inside of the sentient garbage disposals.",
    "3012. Our currency is based on social media clout. Everyone is constantly trying to 'flex' their historic collection of holographic cat videos.",
    "3500. Language has devolved into complex emoji strings. Scholars debate the true meaning of the ancient 'facepalm' 🤔.",
    "4021. Mars is fully terraformed. The biggest problem? The local 'Martian Pigeons' keep pooping on the newly planted oxygen trees.",
    "5000. We meet an ancient, highly-evolved civilization. Their most advanced technology is a device that can flawlessly fold a fitted sheet. **The true miracle.**",
    "6013. The universe is powered by sarcasm. Luckily, teenagers have an infinite, renewable supply.",
    "7000. Humans are now pure energy beings. We still somehow manage to accidentally leave the cosmic refrigerator door open.",
    "8080. The last remaining physical object is a perpetually sticky, ancient plastic toy from a 'Happy Meal.' It is revered as a holy relic.",
    "9999. The ultimate reality is revealed: we were all just a simulation run on a colossal, slow-loading, pre-millennium PC. **Loading... Please wait...**",
    
    # Void.
    "25,000. The world had already come to its end. You are now floating in the void with no idea where your time-travel machine is. And yeah, you are running out of oxygen...",
    "13,797,000,000 BCE... (13.8 billion years ago). The universe is now getting created, step by step. You interfere with the creation, "
    "so you just get squashed by the immense pressure of the vacuum of space. The journey is over; bad luck."
    "26,700,000,000 BCE... (26.7 billion years ago). The universe wasn't yet created. Everything is like... it is not. "
    "You are flying in nowhere hoping you can go back to present. Oh wait! you are vanishing..."
]

QUOTES = [
    "If you change the way you look at things, the things you look at change...",
    "The best time to plant a tree was 20 years ago. The second best time is now.",
    "We don't see things as they are, we see them as we are.",
    "The eye sees only what the mind is prepared to comprehend.",
    "To simply observe is to understand.",
    "I used to think that the brain was the most wonderful organ in my body. Then I realized who was telling me this.",
    "My fake plants died because I forgot to pretend to water them T.T",
    "When nothing is going right, go left!",
    "Two things are infinite: the universe and human stupidity; and I'm not sure about the universe.",
    "Before you diagnose yourself with depression or low self-esteem, first make sure that you are not, in fact, just surrounded by assholes.",
    "The problem with the world is that the intelligent people are full of doubts, while the stupid ones are full of confidence.",
    "When a man opens a car door for his wife, it's either a new car or a new wife :3",
    "The way we see the problem is the problem ;)",
    "To see the world, things dangerous to come to...",
    "I love the way you smile...",
    "If you think you are too small to make a diffrence, try sleeping with a mosquito.",
    "Be aware.. crazy people don't always look crazy ;)",
    "The quieter you become, the more you are able to hear.",
    "I don't like that man i must get to know him better.",
    "Do not take life too seriously. You will never get out of it alive.",
    "If you want to know what a man's like, take a good look at how he treats his inferiors, not his equals.",
    "A smooth sea never made a skilled sailor.",
    "Life is what happens to you while you're busy making other plans.",
    "Insanity is doing the same thing over and over and expecting different results.",
    "The definition of 'adult' is when you stop asking 'Can I have it?' and start asking 'Where do I put it?'",
    "Don't worry about the world coming to an end today. It is already tomorrow in Australia.",
    "If you tell the truth, you don't have to remember anything.",
    "The question isn't who is going to let me; it's who is going to stop me.",
    "I'm not saying I'm Batman. I'm just saying no one has ever seen me and Batman in the same room together.",
    "There are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.",
    "Be yourself; everyone else is already taken.",
    "A successful man is one who can lay a firm foundation with the bricks others have thrown at him.",
    "The most courageous act is still to think for yourself. Aloud.",
    "An expert is a person who has made all the mistakes that can be made in a very narrow field.",
    "The road to success is always under construction.",
    "A house divided against itself cannot stand.",
    "The ballot is stronger than the bullet.",
    "Give me six hours to chop down a tree and I will spend the first four sharpening the axe.",
    "Better to remain silent and be thought a fool than to speak out and remove all doubt.",
    "In the end, it's not the years in your life that count. It's the life in your years.",
    "Those who deny freedom to others deserve it not for themselves.",
    "The best way to destroy an enemy is to make him a friend.",
    "I am a slow walker, but I never walk backward.",
    "Character is like a tree and reputation like a shadow. The shadow is what we think of it; the tree is the real thing.",
    "To live is the rarest thing in the world most people exist.",
    "Sometimes I wish I was an octopus, so I could slap eight people at once.",
    "You have a brain. Use it.",
    "Available to everyone, unremarkable.",
    "As you get older three things happen. The first is your memory goes, and I can’t remember the other two.",
    "The answer is obvious once you stop asking.",
    "Sometimes the bug is the feature.",
]

FACTS = [
    "Fact: People are more creative in the shower :)",
    "Fact: The average person walks the equivalent of five times around the Earth in their lifetime.",
    "Fact: There is a species of jellyfish that is considered immortal. It can revert back to "
    "its juvenile (young) form after becoming an adult.",
    "Fact: A cow gives nearly 200,000 glasses of milk in its lifetime.",
    "Fact: A group of flamingos is called a flamboyance.",
    "Fact: Octopuses have three hearts! Two pump blood to the gills, and one circulates it to the rest of the body. Also, their blood is blue.",
    "Fact: Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian "
    "tombs that are over 3,000 years old and still perfectly good to eat.",
    "Fact: The strongest muscle in your body is the masseter, which is the one you use to chew.",
    "Fact: Bullfrogs do not sleep. They can rest, but they don't enter a true state of sleep like mammals do.",
    "Real: Boanthropy is a psychological disorder where a person believes they are a cow.",
    "Did you know that when you blush (your face turns red), your stomach lining also turns red?",
    "Did you know? The human nose can remember 50,000 different scents.",
    "If you keep a goldfish in a dark room, it will eventually turn white.",
    "Fact: Fainting Goats don't actually lose consciousness; they suffer from a condition called "
    "myotonia congenita that causes their muscles to temporarily freeze when they are startled.",
    "Did you know? A single cloud can weigh over a million pounds! That's because "
    "it's made up of millions of tiny water droplets.",
    "Fact: The total weight of all the ants on Earth is roughly the same as the total weight of all the humans!",
    "Fact: In space, astronauts cannot cry properly. The tears just clump together and stick to "
    "their eye because of the lack of gravity.",
    "Fact: Wombat poop is cube-shaped! No one is completely sure why, but it helps the animal mark its territory.",
    "Real: The smell of freshly cut grass is actually a plant distress signal. The grass is SCREAMING that it's being hurt!",
    "Real: There is a type of jellyfish called the Turritopsis Dohrnii that is considered immortal. "
    "It can go back to its baby stage and start its life over again.",
    "Fact: A cow can walk up the stairs but cannot walk down them. Their knees don't bend the right way!",
    "Real: A bolt of lightning is five times hotter than the surface of the sun! That's super, super hot!",
    "Fact: There are more trees on Earth than there are stars in the Milky Way galaxy.",
    "Fact: The human stomach can dissolve a razor blade. It has very strong acid!",
    "Fact: It is impossible to sneeze with your eyes open. Try to keep them open next time "
    "(But please don't hurt yourself trying!)",
    "Fact: In the 16th century, the King of England had a job called the 'Groom of the Stool,' "
    "whose main duty was to assist the King with going to the bathroom.",
    "Real: Cows have best friends! They get stressed if they are separated from their favorite pals.",
    "Fact: A single strand of spaghetti is called a 'spaghetto'.",
    "Fact: Vending machines kill more people each year than sharks do.",
    "Fact: The inventor of the Pringles can, Fredric Baur, was buried in one.",
    "Fact: The longest place name still in use is 'Taumatawhakatangihangakoauauotamateaturipukakapikimaungahoronukupokaiwhenuakitanatahu', a hill in New Zealand.",
    "Fact: There are more possible iterations of a game of chess than there are atoms in the observable universe.",
    "Fact: Australia is wider than the moon. The moon is 3,400 km wide, while Australia's widest point is about 4,000 km.",
    "Fact: The electric chair was invented by a dentist named Alfred Southwick.",
    "Fact: A 'jiffy' is an actual unit of time: 1/100th of a second.",
    "Fact: All the world's diamonds are less than a teaspoon of mass.",
    "Real: Ketchup was sold in the 1830s as a medicine.",
    "Did you know? The Great Wall of China is not visible from space with the naked eye; it was just a myth.",
    "Did you know? A group of porcupines is called a prickle.",
    "Fact: Otters hold hands when they sleep so they don't drift away from each other.",
    "Fact: The national animal of Scotland is the unicorn.",
    "Fact: The average person spends six months of their life waiting for red lights to change.",
    "Fact: A flock of crows is called a 'murder.'",
    "Fact: There is a town in Norway called A, and a town in France also called Y.",
    "Fact: The fingerprints of a koala are so similar to a human's that they could contaminate a crime scene.",
    "Fact: A crocodile cannot stick its tongue out.",
    "Real: The quietest room in the world is located at Microsoft's headquarters in Washington state. The background noise is measured in negative decibels.",
    "Real: You can't hum (Produce voice with your mouth closed) while holding your nose (it's physically impossible to sustain the airflow).",
    "Fact: The human body contains enough carbon to make 9,000 pencils.",
    "Fact: Chewing gum while peeling onions will keep you from crying.",
    "Fact: In ancient Egypt, pillows were made of stone.",
    "Fact: The Eiffel Tower can grow taller by about 15 cm in the summer due to thermal expansion.",
    "Fact: Rats laugh when tickled.",
    "Fact: The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after only 38 to 45 minutes.",
    "Real: Your brain uses about 20% of the oxygen and calories that you consume.",
    "Did you know? The first recorded use of 'OMG' was in a letter to Winston Churchill in 1917.",
    "Fact: A single bolt of lightning contains enough energy to power a 100-watt lightbulb for three months.",
    "Fact: The human eye can distinguish about 10 million different colors.",
    "Fact: There are more stars in the universe than there are grains of sand on all the beaches on Earth.",
    "Fact: Butterflies taste with their feet :)",
    "Fact: It takes a sloth about two weeks to digest a meal.",
    "Farts contain flammable gases: Methane (CH₄), Oxygen (O₂), Hydrogen (H₂), Nitrogen (N₂), Carbon Dioxide (CO₂), Hydrogen Sulfide (H₂S). "
    "There is a risk of explosion if these gases accumulate in a confined space and then come into contact with an open flame or spark :1",
    "Math: the only subject where you can have problems and still be happy!",
    "If you stretch all the DNA in one human body, it would be about 200 billion km long. While the distance between Earth and Sun ≈ 150 million km. So DNA is enough to reach from Earth to the Sun and back about 670~1300 times!",
]

JOKES = [
    "Parallel lines have so much in common. It's a shame they'll never meet.",
    "My wife told me to take the spider out instead of killing it. Took it out. We had a few drinks. Nice guy. Turns out he's a web designer.",
    "I just finished writing a book about reverse psychology. Do not buy it.",
    "Being a functional adult is mostly just aggressively guessing what to do next.",
    "My therapist says I have a preoccupation with vengeance. We'll see about that.",
    "After a year of going to therapy, my therapist and I are now both looking for a therapist.",
    "If a poison expires, then it becomes more poisonous or less poisonous? (o.O)",
    "Cheese has holes.\nMore cheese = More holes.\nMore holes  = Less cheese.\nMore cheese = Less cheese (O.O)",
    "You are breathing involuntary; but now that you knew, you have to breath voluntary :P",
    "Hear about the new restaurant called Karma? There's no menu: You get what you deserve.",
    "I only know 25 letters of the alphabet. I don't know Y.",
    "I ordered a chicken and an egg online. I'll let you know which one arrives first.",
    "My boss told me to have a good day. So I went home.",
    "You know you're getting old when the only thing you want is for people to stop being between you and the thing you're trying to put away.",
    "Did you hear about the two guys who stole a calendar? They each got six months.",
    "Unortunately, I don't think before I speak, so I'm just as shocked as you are.",
    "Why did the cat sit on the computer? Because she wanted to keep an eye on the mouse!",
    "If a poison expires, then it becomes more poisonous or less poisonous? (o.O)",
    "Cheese has holes.\nMore cheese = More holes.\nMore holes  = Less cheese.\nMore cheese = Less cheese (O.O)",
    "You are breathing involuntary; but now that you knew, you have to breath voluntary :P",
    "I bought medicine for forgetfulness, but I don't remember where I put it.",
]

ADVICES = [
    "Bored? Ask Gemini to tell you a realistic horror story (ಠ_ಠ)",
    "Feeling Bored? Play a text adventure with Gemini ^.^",
    "Boredom begun? Play 20-Questions game with Gemini!",
    # "Dying of boredom? Try typing 'fact'."
    # "Feeling sad.. Try typing 'quote', it may not change your life, but still worth reading."
    # "Wanna smile? type 'joke'."
    "Know Python? you can edit the source code and send me your modifications as feature requests.",
    "Know Python? You can modify & test the source code, errors can also be logged if the option is ON.",
    "Hint: Gemini web interface too slow or laggy? have a potato computer like mine? this is why Py-CLI was created!",
    "Hint: You can change interface colors from 'settings.py'!",
    "Hint: You can disable colors from settings, this will switch to black/white mode.",
    "Hint: If you see random characters in the console (like '\\033[96m'), then disable ANSI codes from settings.",
    "Hint: Error logging is ON by default, you may use it to send me errors. You can also turn it OFF if you wish.",
    "Hint: Both global & error logging may cause a slightly extra delay for AI response, I don't know why, but you can always turn them OFF.",
    "Hint: Max console width is best set to (80) or more; for Windows Command Prompt users, (79) is better.",
    "Hint: Forgot how to use Gemini Py-CLI? type 'help' to see a very short and friendly menu; there is also "
    "a handy toolbar at the bottom of the console (It can be turned off).",
    "Hint: You can change 'MAX_HISTORY_MESSAGES' in settings, but if chat history gets too long, Gemini will "
    "start forgetting things, and the program might need more time while loading/saving chat.",
    "Hint: Some options may slightly affect performances, like response typing effect, word suggestion & completion, application logs, etc. "
    "You can turn them OFF at any time.",
    "Hint: Colors & ANSI codes may not work in old consoles, like Windows Command Prompt; either disable them, "
    "or use a better console emulator; ConEmu is a recommended very lightweight option for Windows.",
    "Hint: You are always encouraged to use a modern console emulator; If the console is old, the program "
    "is still hardcoded to work, but with limited functionality, and so limited experience.",
    "Hint: ANSI codes are the way we tell the console to show colors and some other effects, "
    "but they're not compatible with every console.",
    "Advice: At night, consider enabling dark mode & night light (warmth) mode to protect your eyes, "
    "you'll get used to them over time believe me ;)",
]

MATH = [
    f"Calculate this: ({randint(1, 100)} {choice(list('+-×÷^%'))} {randint(1, 100)})\nC'mon quickly!",
    
    f"NOOOOOOOOOOOOOOOOOOOOOO...O\nTask: Calculate the partial sum of the sequence: "
    f"({(' ' + choice(['+*']) + ' ').join(['O₁', 'O₂', 'O₃', '...', 'On'])})\n"
    f"Given that it's {choice(['an arithmetic sequence (constant difference)', 'a geometric sequence (constant ratio)', 'a harmonic sequence', 'a fibonacci sequence'])}.\n"
    f"Other details: Difference/Ratio={randint(1, 100)}, O₁={randint(1, 500)}, n={randint(1, 999)}\n"
    "Note: It's letter 'O' not zero '0'; Good luck :)",
    
    "I have an existential crisis every time I try to calculate the square root of a negative number. "
    "I’m pretty sure the imaginary number 'i' (i = √-1, i² = -1) is just a regular number that failed its reality check. "
    "Turns out, the entire universe depends on this one number that doesn't actually exist.",
    
    "The number 'pi' (π ≈ 3.14) is truly irrational because its digits never repeat or terminate, "
    "essentially making it a decimal nomad with no fixed address in the numeric universe.",
    
    "Parallel lines have a truly tragic love story: they are absolutely destined to meet at infinity, "
    "but they spend all of eternity getting absolutely nowhere.",
    
    "The concept of infinity (∞) is basically just a number that got detention "
    "forever and will never be allowed to go home and finish its equation.",
    
    "Zero (0) is the most dangerous number in the universe; it can multiply anything into oblivion "
    "and yet it is utterly empty, a total void of mathematical consequence.",
    
    "The Empty Set (ø) is the world's most exclusive club: absolutely nothing is inside, "
    "which makes its bouncer the most tragically overpaid mathematical entity.",
]

OVERTHINK = [
    # Set 1
    '- Analyzing memories...',
    '- Re-analyzing analysis...',
    '- Questioning my question...',
    '- Considering alternative realities...',
    '- This thought might be thinking itself.',
    '- Conclusion unclear. Thinking again...',
    
    # Set 2
    '- Is my decision actually a decision?',
    '- Did I forget to forget something?',
    '- Estimating my answers...',
    '- Could this be a trap of my own making?',
    '- Perhaps my brain is busy, or just confused?',
    '- Maybe I should think about not thinking.',
    
    # Set 3
    '- Did I remember to forget that?',
    '- Is this thought even necessary?',
    '- Analyzing the analysis of my analysis...',
    '- Could this be a sign of overthinking?',
    '- Why am I thinking about thinking too much?',
    '- Maybe I should stop overthinking and think of something else...',
]

ACHIEVEMENTS = [
    "You pressed ENTER.",
    "You know how to use the keyboard & mouse.",
    "You typed 'achievement'.",
    "You did nothing productive.",
    "You found an secret command.",
    "Only 100% of people can type 'achievement'.",
    "Only a few people can see this.",
    "You are in the top 1% of people running this app.",
    "Staring at the screen without blinking.",
    "You are reading this long and verbose text that serves no purpose other than wasting your time reading it. That’s an achievement in patience.",
    "Being alive.",
    f"You are the first one to read this after ({randint(2, 100)}) people.",
]

LANGS = [
    # Format: <lang_expression> (Translation: <english_translation>)  # <lang_name>
    # Chinese
    "好吃不过饺子 (Translation: Nothing is more delicious than dumplings)  # Chinese",
    "吃土了 (Translation: Eating dirt — meaning broke after spending money)  # Chinese",
    "搞笑 (Translation: Funny)  # Chinese",
    "塞翁失马，焉知非福 (Translation: A loss may turn out to be a blessing)  # Chinese",
    "百闻不如一见 (Translation: Seeing once is better than hearing a hundred times)  # Chinese",

    # Japanese
    "猫に小判 (Translation: Giving gold coins to a cat — meaning useless gift)  # Japanese",
    "笑う門には福来る (Translation: Fortune comes to the laughing gate)  # Japanese",
    "よく寝る子は育つ (Translation: A well-sleeping child will grow well)  # Japanese",
    "七転び八起き (Translation: Fall seven times, stand up eight)  # Japanese",

    # Russian
    "С глаз долой — из сердца вон. (Translation: Out of sight, out of mind)  # Russian",
    "Зуб даю! (Translation: I swear on my tooth — meaning I promise)  # Russian",
    "Ёжик в тумане. (Translation: Hedgehog in the fog — meaning confusion)  # Russian",
    "Без труда не вытащишь и рыбку из пруда. (Translation: You can’t pull a fish out of a pond without effort)  # Russian",
    "Дело мастера боится. (Translation: Work fears the master — meaning skill conquers difficulty)  # Russian",

    # German
    "Ich verstehe nur Bahnhof. (Translation: I only understand train station — meaning I don’t understand)  # German",
    "Alles hat ein Ende, nur die Wurst hat zwei. (Translation: Everything has an end, only the sausage has two)  # German",
    "Da schau her! (Translation: Look here!)  # German",
    "Katzenjammer. (Translation: Cat's wailing — meaning headache or regret)  # German",
    "Übung macht den Meister. (Translation: Practice makes the master)  # German",
    "Wer rastet, der rostet. (Translation: He who rests, rusts)  # German",

    # Korean
    "나비처럼 날아라 (Translation: Fly like a butterfly)  # Korean",
    "가는 말이 고와야 오는 말이 곱다 (Translation: Kind words bring kind replies)  # Korean",
    "고생 끝에 낙이 온다 (Translation: Joy comes after hardship)  # Korean",

    # Hindi
    "बिल्ली के भाग्य से चूहे नाचते हैं (Translation: When the cat’s away, the mice will play)  # Hindi",
    "जैसा बोओगे वैसा काटोगे (Translation: You reap what you sow)  # Hindi",
    "देर आए दुरुस्त आए (Translation: Better late than never)  # Hindi",

    # Italian
    "Vedi Napoli e poi muori. (Translation: See Naples and die — meaning must-see place)  # Italian",
    "Chi dorme non piglia pesci. (Translation: He who sleeps doesn’t catch fish)  # Italian",
    "Piano piano si va lontano. (Translation: Slowly, slowly, one goes far)  # Italian",

    # Spanish
    "Que será, será. (Translation: Whatever will be, will be)  # Spanish",
    "¡Qué pasta! (Translation: What pasta! — meaning a lot of money!)  # Spanish",
    "Más vale tarde que nunca. (Translation: Better late than never)  # Spanish",
    "A mal tiempo, buena cara. (Translation: Put on a brave face in bad times)  # Spanish",

    # French
    "J'ai perdu la boule. (Translation: I lost the ball — meaning I lost my mind)  # French",
    "C'est du gâteau! (Translation: It's cake! — meaning it's easy)  # French",
    "Petit à petit, l’oiseau fait son nid. (Translation: Little by little, the bird builds its nest)  # French",
    "Après la pluie, le beau temps. (Translation: After rain comes good weather)  # French",

    # Portuguese
    "A vida é bela. (Translation: Life is beautiful)  # Portuguese",
    "Quem espera sempre alcança. (Translation: Those who wait will achieve)  # Portuguese",

    # Arabic
    ".العقل في إجازة (Translation: The brain is on vacation — meaning I’m not thinking at all)  # Arabic",
    ".الصبر مفتاح الفرج (Translation: Patience is the key to relief)  # Arabic",
    ".لكل مجتهد نصيب (Translation: Every hard worker gets a share)  # Arabic",

    # Turkish
    "Damlaya damlaya göl olur. (Translation: Drop by drop, a lake is formed)  # Turkish",
    "Sabır acıdır, meyvesi tatlıdır. (Translation: Patience is bitter, but its fruit is sweet)  # Turkish",

    # Dutch
    "Wie het kleine niet eert, is het grote niet weerd. (Translation: Who does not value small things is not worthy of big ones)  # Dutch",
    "Oost west, thuis best. (Translation: East or west, home is best)  # Dutch",

    # Malay
    "Sedikit demi sedikit, lama-lama menjadi bukit. (Translation: Little by little, it becomes a hill)  # Malay",
    "Berat sama dipikul, ringan sama dijinjing. (Translation: Heavy things are carried together, light ones shared)  # Malay",

    # Latin
    "Per aspera ad astra. (Translation: Through hardships to the stars)  # Latin",
    "Carpe diem. (Translation: Seize the day — meaning live the present)  # Latin",

    # Greek
    "Γνῶθι σεαυτόν (Translation: Know thyself/yourself)  # Greek",
    "Μηδὲν ἄγαν (Translation: Nothing in excess — meaning balance)  # Greek",
    "Αρχή ήμισυ του παντός (Translation: The beginning is half of everything)  # Greek",
    "Όπου υπάρχει θέληση, υπάρχει τρόπος. (Translation: Where there is a will, there is a way)  # Greek",
]
 
RIDDLES = [
    # Easy.
    {
        '?': "A man paints all the numbers up to 100 on a wall in a perfect sequence (1, 2, 3 ... 100). "
             "He decided to paint only odd numbers first, then the even numbers later. Somehow he skips a number without realizing it. "
             "Later, he notices the sum of painted numbers is short by 36. Which number did he skip?",
        '✓': "Simply 36 (even/odd pattern is a distraction)"
    },
    {
        '?': "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?",
        '✓': "It’s an echo! It speaks when sound bounces back, hears without ears, and has no body."
    },
    {
        '?': "I speak without a tongue, I can be broken but never held, my lifetime depends on my owner. What am I?",
        '✓': "A promise."
    },
    {
        '?': "A plane crashes on the border of two countries. Where do they bury the survivors?",
        '✓': "Nowhere — survivors aren’t buried."
    },
    {
        '?': "Two fathers and two sons went fishing. Each caught one fish, yet they brought home only three fish. How?",
        '✓': "They were grandfather, father, and son."
    },
    {
        "?": "In a sunny park, there are two mothers and two daughters posing for a photo. One is wearing a red hat and smiling at the camera; "
             "the other two aren't smiling but looking at a squirrel on a tree. All three are related. Who is in the photo?",
        "✓": "A grandmother, her daughter, and her grand-daughter (other details are distractions)."
    },
    {
        '?': "If you have me, you really want to share me. If you share me, you lose me forever. What am I?",
        '✓': "A secret."
    },
    {
        '?': "A cowboy rode into town on Friday. He stayed three days and left on Friday. How is that possible?",
        '✓': "His horse's name is Friday."
    },
    {
        '?': "If you have three apples and you take two, how many do you have?",
        '✓': "Three (you took your own apples)"
    },
    {
        '?': "You see a boat filled with people, yet there isn’t a single person on board. How is that possible?",
        '✓': "All the people were married (read the word 'single' above)."
    },
    {
        '?': "I am always hungry, I must always be fed. The finger I touch will soon turn red. What am I?",
        '✓': "Fire."
    },
    {
        '?': "I have cities but no houses, forests but no trees, and rivers but no water. What am I?",
        '✓': "A map."
    },
    {
        '?': "You see me once in June, twice in November, but not at all in May. Why?",
        '✓': "It's about the letter 'e'."
    },
    {
        '?': "What disappears as soon as you say its name?",
        '✓': "Silence."
    },
    {
        '?': "I am written on a piece of paper that you should never read aloud, because if you do, I vanish. What is written on it?",
        '✓': "Silence."
    },
    {
        '?': "I can use a maximum number of twelve. I add five to nine, and get two. The answer is correct, but how?",
        '✓': "On a clock, 9 + 5 hours = 2"
    },
    {
        '?': "What comes once in a minute, twice in a moment, but never in a thousand years?",
        '✓': "The letter 'M'."
    },
    {
        '?': "If an electric train is moving north at 100 mph and a wind is blowing east at 10 mph, which way does the smoke blow?",
        '✓': "Electric trains don’t produce smoke."
    },
    {
        '?': "Three coins lie in a row showing H H T. You may flip exactly ONE coin. When you flip a coin, "
             "its adjacent neighbors flip as well. How can you make all coins show the same side?",
        '✓': "Flip the first coin (third one won't be affected since it's not adjacent)"
    },
    {
        '?': "You regain consciousness and find yourself a captive in a minimalist gallery with a single mahogany table "
             "and a heavy iron door. On the table lies a card that states: 'Completion of this text is the sole requirement for your departure'. "
             "You read the card text over and over until you know it by heart, yet the door remains closed. Why?",
        '✓': "You simply didn't try to open the door. The card didn't say it would open automatically."
    },
    {
        '?': "You are trapped in a room with no windows and one locked door. The only object you see is a sealed envelope with a label that reads: "
             "'You must read this note at least once to leave'. You read those words three times, stare at them for hours, but the door remains locked. Why?",
        '✓': "You read the label, but forgot to open the envelope and read the letter."
    },
    {
        '?': "You wake up in a perfectly seamless white cube with no windows or doors. On the floor is a single letter labeled: "
             "'To exit this room, you must read this letter at least once'. You read it aloud, then silently, then backwards, but no door opens. Why?",
        '✓': "There is no door in the cube already, look for another exit."
    },
    {
        '?': "Three scientists — a physician, a mathematician, and a geographer — are in a hot air balloon. "
             "The balloon got punctured and deflated. While going down and in order to live, they must sacrifice one "
             "person to save the others. Who should they sacrifice?",
        '✓': "The one with the greatest weight, their specialty doesn't matter."
    },
    {
        '?': "A farmer has a fox, a goose, and a bag of beans. He needs to cross a river using a boat that can only carry himself and one item at a time. "
             "If he leaves the fox alone with the goose, the fox will eat the goose. If he leaves the goose alone with the beans, "
             "the goose will eat the beans. How should he get everything across safely?",
        '✓': "Take the goose first, then the fox, return with the goose, leave the goose there and take the beans, and finally bring the goose back."
    },
    {
        '?': "You are asked to choose one of three doors. Behind one door is a treasure, behind the others are dangers. "
             "You can choose one door. After you pick, the host opens one of the other two doors, revealing danger. "
             "You are then given a chance to switch your choice. Should you switch?",
        '✓': "Yes, you should definitely switch.\n\n"
             "While it feels like it should be a 50/50 chance once one door is gone, the math shows that switching doubles your chances of winning.\n\n"
             "At the start, you have a 1/3 chance of picking the treasure and a 2/3 chance of picking a danger; there is a bigger chance of being wrong. "
             "If you switch doors, you win every time your initial guess was wrong, since you were probably wrong before, you should switch.\n\n"
             "Still skeptical? It’s perfectly normal to feel like it’s 50/50. Even famous mathematicians have argued over this!\n\n"
             "One way to make it clearer is to imagine there are 100 doors. You pick one (a 1% chance). The host then opens 98 doors that all have danger "
             "behind them, leaving only your door and one other. In that case, and because you were 99% wrong initially, "
             "it feels much more obvious that the other door is the one with the treasure."
    },

    # Medium.
    {
        '?': "A train has 100 carriages numbered 1 to 100. Two neighbors carriages were swapped. "
             "The sum of their numbers is 105. Which carriage is first out of order?",
        '✓': "Carriage 52 (105 / 2 = 52.5 so we have 52, 53)"
    },
    {
        '?': "A man walks into a room with three light switches outside. Only one switch controls a bulb inside. He can flip "
             "the switches as much as he likes but can only enter the room once. How can he find the correct switch?",
        '✓': "Turn on switch 1, wait, turn it off; turn on switch 2, enter room: warm bulb → switch 1, lit bulb → switch 2, cold bulb → switch 3"
    },
    {
        '?': "A circular table has 12 seats numbered clockwise. Two close-friends swap seats. The sum of their seat numbers is 13. "
             "But then they swap back the seats 5 times. Starting at seat 1, which is the first seat number out of sequence?",
        '✓': "None (they swapped 1+5 times, as if nothing changed)"
    },
    {
        '?': "A man dies in a desert and is found with a backpack and a canister (closed safety gear). How did he die?",
        '✓': "He was a skydiver and his parachute didn’t open."
    },
    {
        '?': "There’s a house with four walls, all facing south, and a bear walks by. What color is the bear?",
        '✓': "White (it’s a polar bear at the North Pole)."
    },
    {
        '?': "A town has two barbers only. One has a perfect haircut, the other a terrible one. Only one can cut your hair. Which barber do you choose? Beware of appearances.",
        '✓': "Choose the barber with the terrible haircut — he must have cut the other barber’s hair."
    },    
    {
        '?': "A farmer has 17 sheep, and all but 9 run away. How many are left?",
        '✓': "9 sheep (all but 9 run away = all -except 9- run away)"
    },
    {
        '?': "A woman walks into a room with 53 socks: 21 blue, 15 black, and the rest white; they are not separated. "
             "Without looking, what is the minimum number of socks she must take to ensure she has one matching pair?",
        '✓': "4 socks (in the worst case: 1 blue, 1 black, 1 white → 4th will match one; in the best case: They all have one color)"
    },    
    {
        '?': "A farmer had 12 apples. He gave half to his neighbor, then another half to his son. Then he notices he still has 3 apples. How is this possible?",
        '✓': "He gave half of the apples he currently had each time, not half of the original 12"
    },

    # Hard.
    {
        '?': "A man writes all numbers from 1 to 1000. One number is missing. The sum of all written numbers is 499500. Which number is missing?",
        '✓': "1000 (sum of a simple sequence = n/2 (1st + last) = 1000/2 (1 + 1000) = 500500 and 500500 - 499500 = 1000)"
    },
    {
        '?': "What is next in the sequence: (2, 3, 5, 9, 17)?",
        '✓': "33 (pattern: double the previous number minus 1)"
    },
    {
        '?': "There are 100 lockers all closed. First, you toggle every locker (so all are now open). Then, you toggle "
             "every 2nd locker (in each 2 lockers, you change the second). Next, every 3rd locker, and so on, "
             "until you reach the 100th locker. Which lockers remain open at the end?",
        '✓': "Lockers numbered with perfect squares (1, 4, 9, 16, …, 100)"
    },
    {
        '?': "I am a three-digit number. My tens digit is five more than my ones digit, and my hundreds digit is eight less than my tens digit. What number am I?",
        '✓': "194"
    },
    {
        '?': "I am a three-digit number. My hundreds digit is 1/3 of my tens digit, and my ones digit is 4 more than my hundreds digit. What number am I?",
        '✓': "141."
    },
    {
        '?': f"I am a word; add two letters and {choice(['fewer there will be', 'shorter I become', 'less you have now'])}. What word am I?",
        '✓': "Few (add 'er' to make 'fewer').\nOr: Short -> shorter.\nOr: Brief -> briefer."
    },
    {
        '?': "A man leaves a room. Inside, a clock shows 3:15 and mirror. He leaves, returns at 3:45, yet the hands of "
             "the clock appear the same as before. How is this possible?",
        '✓': "The clock is a reflection in a mirror, so the hands look the same at 3:15 and 3:45 "
             "(3:15 was the original clock state, and 3:45 is what he saw in the mirror)"
    },
    {
        '?': "A man walks 1 mile south, 1 mile east, and 1 mile north. He ends up exactly where he started. Where is he?",
        '✓': "The North Pole (try drawing the path)"
    },

    # Very Hard (Strings that contain a bulleted or a numbered list must be carefully
               # organized & wrapped to be clear when written in a text file)
    {
        "?": "You see a house with two doors. One leads to freedom, the other to certain death. "
             "Each door has a guard: one always tells the truth, the other always lies. You can ask only "
             "one yes/no question to one guard to find the door to freedom. What question do you ask?",
        "✓": "Ask either guard: 'If I asked the other guard which door leads to death, would they say this one?' "
             "Then choose the opposite door. This works because:\n"
             "- If you ask the truth-teller, they truthfully tell you what the liar would say\n"
             "  (the wrong door).\n"
             "- If you ask the liar, they lie about what the truth-teller would say\n"
             "  (also the wrong door).\n"
             "* In both cases, choose the opposite door of the answer."
    },
    {
        '?': "A prisoner is given a chance to escape. There are two doors: one leads to freedom, the other to certain death. "
             "Two guards are present, one always lies, one always tells the truth. You may ask only one question. "
             "The guard hints subtly, 'Ask me carefully'. What do you ask?",
        '✓': "Ask either guard: 'Which door would the other guard say: leads to death?'. Then choose the opposite door "
             "(you have to imagine & write the whole scenario to understand)"
    },
    {
        '?': "You have two ropes that each burn for exactly 1 hour, but they burn unevenly (burning speed varies "
             "irregularly over time). How can you measure 45 minutes?",
        '✓': "Light rope A from both ends, and rope B from one end at the same time. When rope A burns out (30 min), "
             "light the other end of rope B (rope B now has 30 min left). It will burn in 15 more minutes."
    },
    {
        "?": "100 prisoners in a chain, each with a random red or blue hat. They see hats in front but not in behind; they also can't see their own hats, "
             "but can hear prior answers. The game starts from the last one #100 to the first one #1 in chain. "
             "A prisoner dies if he says the wrong color of his own hat. How to save the maximum?",
        "✓": "* Prisoners agree on a coding scheme before the game starts. They decide to use parity (even or odd counts) of one color.\n"
            "* Last prisoner in chain (who sees the other 99) announces 'red' if number of red hats in front is even; if odd, he says 'blue'.\n"
            "* Now every other prisonner will do this:\n"
             "- Count the red hats in front\n"
             "- Count the red hats heard in behind (if there is already)\n"
             "- If sum (red hats in front + red hats in behind) is even, this means red hats\n"
             "  are all taken; so his own hat must be blue.\n"
             "- Otherwise, there must be a missing red hat in the equation which is his own hat;\n"
             "  thus, his hat is red.\n\n"
             "* This way, 99 of the prisonners are guaranteed safe."
             "* Only the last prisoner sacrifices himself to give info.\n"
             "  He might die for saying the wrong color, because he still doesn't know if his hat\n"
             "  is red or blue, he only told what he saw in front."
    },
    {
        "?": "4 people must cross a bridge at dark night with 1 torch. Their walking speed varies: person A takes 1 min to cross; B -> 2 min; C -> 5 min; D -> 10 min. "
             "Maximum people to cross is 2 at a time. All must cross in 17 min or less. How?",
        "✓": "- Step 1: Fastest two cross first (A+B) → They take 2 min\n"
             "  (B takes 2 min & they both need torch, so A must slow down)\n"
             "- Step 2: Fastest (A) returns with torch → +1 min → total 3 min\n"
             "- Step 3: Slowest two cross (C+D) → +10 min → total 13 min\n"
             "- Step 4: Second fastest (B) returns → +2 min → total 15 min\n"
             "- Step 5: Fastest two cross again (A+B) → +2 min → total 17 min"
    },
    {
        "?": "You have 8 balls, all the same size. 1 is heavier. Using a balance scale only twice, how do you find the heavy one?",
        "✓": "Weigh 3 against 3 balls:\n"
             "- If one side is heavier → heavy ball is there.\n"
             "  * Take the 3 balls & Weigh 1v1:\n"
             "    - If one is heavier → you found it.\n"
             "    - If balanced → it's the 3rd ball.\n\n"
             "- If equal → heavy ball is among the remaining 2.\n"
             "  * Then weigh 1 vs 1 to find the heavy ball."
    },
    {
        "?": "12 coins, 1 fake (heavier or lighter). Using a balance 3 times only, how to find the fake coin and its weight difference?",
        "✓": "1. Weigh 4 vs 4:\n"
             "  - If one side is heavier → fake is there.\n"
             "  - If balanced → fake is in the remaining 4 coins.\n\n"
             "2. Then take the suspect group, weigh 2 vs 2; the heavier side has the fake coin.\n"
             "3. Finally, take the suspect side and weigh 1 vs 1 to find it."
    },
    {
        "?": "3 logicians (thinkers) sit in a circle. There are 3 red hats and 2 blue hats. Each logician wears one random hat "
             "and can see the others' hats but not their own. They are told to raise their hand only if they are certain "
             "of their hat color. After a period of silence, all three hands go up at once. What color are the hats?",
        "✓": "They all have red hats.\nWhy? Simultaneously doesnt mean immediately. And they are logicians, smart enough to be aware of these scenarios:\n\n"
              "1. If 2 were blue & 1 was red, someone would see 2 blue and immediately raises his\n"
              "   hand because there is no other blue hat available; so his hat is red; but others\n"
              "   wouldn't raise their hands simultaneously because they will see (red, blue) which\n"
              "   is enough to know after the first one raised his hand (they would know that the\n"
              "   first one raised his hand only because he saw 2 blue, so their hats are surely\n"
              "   red), but it won't be simultaneous.\n\n"
              "2. If 2 were red & 1 was blue, one will see (red, red); being uncertain if his hat is\n"
              "   red or blue, he doesn't raise his hand; the other two will see (red, blue),\n"
              "   both of them would wait to see if the person in the blue hat raised his hand (like\n"
              "   in scenario 1). When he didn't, they would realize 'If I were wearing blue, he\n"
              "   would see two blue hats and would have known his color instantly. Since he doesn't\n"
              "   know, I must be wearing red!'; then they both raise their hands simultaneously.\n\n"
              "3. When all 3 hats were red, no one raised their hand immediately, and they all\n"
              "   realized at the same moment that no other scenario (1 blue or 2 blue hats) was\n"
              "   possible, it proves they were all seeing the same thing: (red, red) for each; so\n"
              "   they raise their hands simultaneously."
    },
    {
        "?": "There are 1000 bottles of liquid, one of which is poisoned. The poison kills within 24 hours. "
             "You have 10 prisoners to help identify which bottle is poisoned. "
             "How do you determine the poisoned bottle within the 24-hour? (This puzzle requires the 'Binary Code' knowledge)",
        "✓": "We use 'Binary Code' (a sequence of 10 digits is enough for 1000 bottles).\n\n"
             "- Label every bottle from 1 to 1000.\n"
             "- Convert each bottle's number to binary (E.g: 1 → 0000000001 and 1000 → 1111101000).\n"
             "- Assign the 10 prisoners. Each prisoner corresponds to one bit/position in the\n"
             "  binary number.\n"
             "- Each prisoner drinks from a bottle - only if their assigned position has '1' in that\n"
             "  bottle's binary code (E.g: For Bottle 1 (0000000001), only the 1st prisoner drinks.\n"
             "  For Bottle 7 (0000000111), prisoners 1, 2 & 3 all take a sip).\n"
             "- After 24 hours, check who survived:\n"
             "  * If a prisoner dies, they surely represent '1' in the poisonned bottle.\n"
             "  * If they live, they represent '0'.\n\n"
             "By lining up those 1s and 0s in order, you get the binary number of the exact poisoned bottle. "
             "E.g: if only prisoners 1, 2 & 3 die, the binary code is (0000000111), which means Bottle 7 was the poisoned one."
    },

    # Nonsense.
    {
        '?': "A rectangular field is precisely 2 kilometers long and 700 meters wide. Assuming the soil density is "
             "consistent, and the irrigation lines run parallel to the width every 50 meters. Calculate the farmer's age.",
        '✓': "No logic"
    },    
    {
        '?': "In a controlled farm environment, there are 12 chickens consuming 500g of grain daily. Above them, the sky contains 7 "
             "cirrus clouds moving at 15 knots. Based on these atmospheric and agricultural variables, what day is it?",
        '✓': "No logic"
    },    
    {
        '?': "A perfect square room has four corners; a tabby cat sleeps in the northwest corner, while a grandfather clock on the "
             "opposite wall strikes 5 times. Given the acoustic resonance and the cat's sleep cycle, how much does the cat weigh?",
        '✓': "No logic"
    },
    {
        '?': "If a high-speed commuter train leaves the central station at 3 PM heading north at 120 km/h, and a "
             "50-foot oak tree is cut down at the exact same moment 10 miles away. How many pancakes can you eat?",
        '✓': "No logic"
    },    
    {
        '?': "You have 10 organic apples and 3 ripe pineapples stored in a basket with a total volume of 1.5 cubic feet. "
             "Factoring in the surface area of the fruit, how many bananas does it take to make a cake?",
        '✓': "No logic"
    },    
    {
        '?': "If water is wet due to molecular cohesion and fire is hot because of an exothermic chemical reaction, "
             "calculate the friction coefficient to determine how many people can dance on a Monday.",
        '✓': "No logic"
    },
    {
        "?": "A municipal library has 3,482 books meticulously arranged by the 'Dewey Decimal System', color, and author name. "
             "While shelving a biography, the librarian sneezes twice. How high are the bookshelves?",
        "✓": "No logic"
    },
    {
        "?": "The sun rises in the east at a 15-degree angle, the wind blows north at 5 mph, and a green bullfrog "
             "croaks exactly three times in the marsh. What is the square root of the mountain height?",
        "✓": "No logic"
    },
    {
        "?": "If a domestic cat can chase a mouse across 17 ceramic tiles at a velocity of 4 meters per second while "
             "the moon shines at 400,000 lux. How many chairs exist in the house?",
        "✓": "No logic"
    },
    {
        "?": "You have seven graphite pencils, two waterproof umbrellas, and a small orange bicycle with 20-inch wheels. "
             "Based on the inventory of these items, how many cats does your neighbor have?",
        "✓": "No logic"
    },
    {
        "?": "While it rains lightly at a rate of 2mm per hour on the mountain, a garden snail climbs a stone staircase with 45 steps. "
             "Given the humidity levels, how many sandwiches can be prepared?",
        "✓": "No logic"
    },
]

NOTHING = [
    "Nothing happened.\nExactly as expected.",
    "Nothing is happening.\nIsn't this creepy?",
    "Shhhh… All quiet… Waiting for nothing...",
    "All quiet on the western front (You should watch this movie ;)\nAnyway, nothing happened.",
    "Nothing to report.",
    "No news is good news, right?",
    "The universe is so... I don't know how to express it..... so normal.",
    "Nothing to see here.",
]

NONSENSE = [
    # Titles.
    [
        'NONSENSE', 'Square of Tomorrow', 'The Blue Taste', 'Whispers of Screams',
        'Gravity’s Ice Nap', 'A Galaxy in a Teacup', 'The Geometry of Void',
        'Pumpernickel Purgatory', 'Breathing Diamonds', 'Twelve Ways to Breath',
        'Moon Juice', 'Making Potato from Air', 'Boiling the Wind', 'Flying Underground',
        'Electric Soil', 'Elephants in the Air'
    ],
    
    # Messages.
    "When the square sings to the wind, the color of time melts sideways.",
    "Banana echoes jump over quantum pancakes while yodeling spaghetti.",
    "Purple toaster whispers slowly to invisible marshmallow socks.",
    "Electric giraffes dance politely on the refrigerator of eternity.",
    "The umbrella of truth bends only when the stars are sleepy.",
    "Time whispers in marshmallow colors that nobody can taste.",
    "The river of nonsense flows uphill when nobody is watching.",
    "If you ever find yourself falling through a cloud of deers, remember: gravity is just a suggestion made by a confused spider.",
    "Silence is golden, but complexity is silver and tastes like the number seven.",
    "I’m not as think as you drunk I am.",
    "My favorite color is the sound of a toasted bread falling down stairs.",
    "Please do not feed the shadows; they are on a strict diet of Tuesday afternoons.",
    "Logic is a wreath of onions worn by a man who forgot how to sneeze.",
    "If the moon were made of spare ribs, would you eat it? I wouldn't. I’d use it to calibrate my invisible trombone.",
    
    "买冬瓜\n"
    "- Translation: Buy a winter melon.\n"
    "- Pronounciation: Mǎi dōngguā (Sounds like: My Don't Care).\n"
    "- Usage: If someone is telling you a story that is unnecessarily\n"
    "  complicated or makes no sense, you just drop this line to imply\n"
    "  they are driving you in circles (You won't remember to use it anyway).",
    
    "# Manual for a Manual-less Machine:\n"
    "- Turn it ON.\n"
    "- Now throw this manual in the trash.\n"
    "- Turn it OFF ('Switch OFF' button is hidden under the machine).",
    
    "# A Nonsense Recipe for Disaster:\n"
    "* Ingredient:     Quantity:     Instruction:\n"
    "- Laughter        4 Gallons     Freeze until it turns into a triangle.\n"
    "- Yesterday       1 Pinch       Fold gently into a cloud.\n"
    "- The Letter '5'  As needed     Disguise it as a small shrub.",
]

def language(box: Callable):
    """Display a random foreign-language-expression with its translation."""
    titles = [
        'Journey to Fluency', 'Unlocking a New World', 'A Language Sentence Story',
        'A First Step', 'Bridging Cultures', 'New Language Sentence', 'A New Voice',
        'Discovering Words', 'Learning Journey', 'Words Bridge', 'Language Adventure',
        'First Sentence', 'A Door to a New Language', 'Words Treasure', 'Discovering The Unknown',
        'New Culture', 'Exploring Horizons', 'Unlocking Secrets', 'World of Words',
        'Stepping in',
    ]

    title = choice(titles)
    msg = choice(LANGS)
    msg = msg.replace(' (Translation:', '\n(Translation:').replace('  # ', '\n# ')

    box(msg, title=title, border_color=PURP, text_color=PURP, secondary_color=PURP, clear_line=1)

def mathematics(box: Callable):
    """Bring back the headache with some math!"""
    import re
    from math import (pi, isfinite, copysign, cos, sin, tan, sqrt, pow, exp,
                      factorial, log10 as log, log as ln)

    
    # Preparation.
    titles = ['Alge-bros!', 'Pi-rate!', 'Divide & Conquer', 'Sum Fun!', 'Mathemagic!',
              'Math-ter of Numbers!', 'Exponent-ially Funny!', 'Calcu-lol!',
              'Count on Me!', 'Number Crunchers', 'The Math-terpiece', 'Nightmare']
              
    headers = ['How about calculating', 'Come on! Calculate', 'Try', 'Take',
               'What about', "Let's see how you can deal with", 'Can you solve',
               'How can you deal with', 'How about', 'Grab a calculator (or your brain) and blast',
               'Mentally? Impossible to solve',]
               
    title = choice(titles)
    clean_number = lambda n: int(n) if n == int(n) else float(str(round(n, randint(1, 3))).rstrip('0'))
    
    # Take a random action.
    # (1) = Print a random message from MATH list.
    # (2) = Print a random operation with its solution.
    # (3) = Print a random equation.
    action = randint(1, 3)
    
    if action == 1:
        msg = choice(MATH)
    
    elif action == 2:
        operators = list('-+×÷^%') + ['//']
        superscripts = '¹³⁴⁵⁶⁷⁸⁹'
        msg = choice(headers) + ' this:\n'
        
        # Create a random operation.
        last = []
        for i in range(randint(2, 5)):
            # Prepare a number with some randomness.
            y = uniform(-256, 256) or 0.001
            if abs(y) < 1e-6: y = 0.001 if y > 0 else -0.001
            
            convert = randint(0, 10)
            if convert in range(0, 6): y = int(y)
            if convert in range(6, 9): y = y / 100 if abs(y) >= 1 else y
            
            y = clean_number(y)
            x = k = str(y)
            if y < 0: x = f'({x})'
            # No we have: (y) the original number, (k) its string format, (x) which is same as (k) but with parenthese if (y) is negative.
            
            # Add extra functions or operators.
            if not msg.endswith('^ '):
                extra = choice(['√', 'ˣ√', '|', 'ln', 'log', 'e', '!', 'cos', 'sin', 'tan', 'π'] + [None] * 20)
                match extra:
                    case 'π':   x = 'π'
                    case 'ˣ√':  sup = choice(superscripts); x = sup + '√' + x if sup in ['¹³⁵⁷⁹'] or sup in  ['⁴⁶⁸'] and y > 0 else x
                    case '|':   x = '|' + k + '|'
                    case 'e':   y = int(copysign(abs(y) % 50, y)); x = 'e^' + str(y)
                    case 'cos': x = 'cos(' + k + ')'
                    case 'sin': x = 'sin(' + k + ')'
                    case 'tan': x = 'tan(' + k + ')' if abs(cos(y)) > 1e-6 else x
                    case '√':   y = abs(y); x = '√' + str(y)
                    case 'ln':  y = abs(y); x = 'ln(' + str(y) + ')'
                    case 'log': y = abs(y); x = 'log(' + str(y) + ')'
                    case '!':   y = abs(int(y % 13)); x = str(y) + '!'

            # Choose the operator carefully to avoid massive numbers.
            operator = choice(operators)
            if '^' in last and not msg[-2].isdigit() and 'e' in msg:
                operators_2 = operators[:]
                operators_2.remove('^')
                operator = choice(operators_2)
            
            if '^' in last and abs(y) > 50:
                y = int(y % 50)
                x = str(y)
            
            # Finish & Add the operation string.
            msg +=  x + ' ' + operator + ' '
            if ' ^ ' in msg: msg = msg.replace(' ^ ', '^')
            last = [y, operator]

        msg = msg.rstrip()
        for o in operators: msg = msg.removesuffix(o)
        msg = msg.rstrip()

        # Cheat Sheet.
        line = msg.splitlines()[1]
        if '%' in line:
            msg += '\n\n# The modulo operator (%)\n'
            msg += 'It stands for the remainder of division.\n'
            msg += 'E.g: 7 % 3  = 1 (Because 7 = 3 × 2 + 1)'
            
        if '//' in line:
            msg += '\n\n# The floor division operator (//)\n'
            msg += 'It divides two numbers and gives the largest integer less than or equal to the division result.\n'
            msg += 'E.g: 7 // 2 = 3 (Because 7 // 2 = 3.5 but we take 3)'
        
        if '!' in line:
            msg += '\n\n# The factorial operator (!)\n'
            msg += 'It multiplies a positive number by all positive integers less than it.\n'
            msg += 'E.g: 4! = 4 × 3 × 2 × 1 = 24'
        
        if '|' in line:
            msg += '\n\n# The absolute value operator (||)\n'
            msg += "It says how far a number is from zero, no matter if it's positive or negative.\n"
            msg += 'E.g: |-5| = 5 and |3| = 3'
        
        # Prepare the solution.
        regex = r'\(-?\d+(?:\.\d+)?\)|-?\d+(?:\.\d+)?'  # For both integers & floating points.
        numbers = re.findall(regex, line)
        opr = re.sub(regex, '¤', line)
        replacement = {'×': '*', '÷': '/', '^': '**',
                       '|¤|': 'abs(¤)', 'e**¤': 'exp(¤)', '¤!': 'factorial(¤)', '√¤': 'sqrt(¤)', 'π': 'pi'}
        for k, v in replacement.items(): opr =  opr.replace(k, v)
        for s, n in zip(superscripts, '13456789'): opr =  opr.replace(f'{s}sqrt(¤)', f'pow(¤, 1/{n})')
        for n in numbers: opr = opr.replace('¤', n, 1)
        # print(msg, '\n', opr)
        
        try:
            # Caluclate the solution.
            result = eval(opr)
            if not isfinite(result): raise OverflowError
            try: result = clean_number(result)
            except TypeError: result = clean_number(result.real)
            result = '{:.6g}'.format(result)
            if len((result).lstrip('-')) > 2: result = result[::-1]
            
            # Finish the result.
            msg += "\n\n# Solution (Try First!)\n"
            msg += f"It is ({result}).\n"
            if result == '0': msg += "This number is so tiny that it's approximately zero."  # It can't be exactly zero, since we avoid (0) values after uniform() function.
            elif len(result.rstrip('-')) > 2: msg += "The result number is reversed to hide it. You only need to reverse it back (E.g: 321 -> 123) :l"
            else: msg += "You see? so simple :1"
        
        except OverflowError:
            msg += "\n\n# The result is a massive number. You probably don't want to waste your time :P\n"
        
        except:
            msg += "\n\n# Oops! This calculation got a bit too complex, even for me ;-;"
        
    else:
        ops = ['+', '-', '*', '/']
        x = 'x'
        
        # Randomly pick equation type.
        eq_type = choice(['arithmetic', 'linear', 'quadratic', 'inequality', 'imaginary'])
        if eq_type == 'arithmetic':
            a, b, c = randint(-20, 20), randint(-20, 20), randint(-20, 20)
            op1, op2 = choice(ops), choice(ops)
            eq = f"{a} {op1} {b} {op2} {c}"
            try: solution = eval(eq)
            except: solution = None

        elif eq_type == 'linear':
            a, b, c = randint(-10, 10), randint(-20, 20), randint(-30, 30)
            op = choice(ops)
            eq = f"{a}*{x} {op} {b} = {c}"
            try: solution = (c - b) / a if a != 0 else None
            except: solution = None

        elif eq_type == 'quadratic':
            a, b, c = randint(1, 5), randint(-20, 20), randint(-30, 30)
            eq = f"{a}*{x}^2 + {b}*{x} + {c} = 0"
            # Quadratic formula, just store as tuple.
            disc = b**2 - 4*a*c
            if disc >= 0:
                solution = ((-b + disc**0.5)/(2*a), (-b - disc**0.5)/(2*a))
            else:
                solution = None  # imaginary.

        elif eq_type == 'inequality':
            # Choose single or double inequality.
            if random() < 0.5:  # single.
                a, b = randint(-20, 20), randint(-20, 20)
                comp = choice(['<', '>', '<=', '>='])
                eq = f"{a} + {x} {comp} {b}"
                solution = None  # could calculate, but leave hidden.
            else:  # double inequality
                lower, upper = sorted([randint(-20, 20), randint(-20, 20)])
                divisor = choice([1, 2, 5, 10])
                eq = f"{lower} < {x} / {divisor} < {upper}"
                solution = (lower*divisor, upper*divisor)

        else:  # imaginary
            a, b = randint(1, 10), randint(1, 10)
            eq = f"{x}^2 + {a}*{x} + {b} = {randint(1, 10)}i"
            solution = None  # complex, leave hidden.
        
        # Prepare the message.
        msg = choice(headers) + ' this:\n' + eq
        if solution:
            if isinstance(solution, (int, float, complex)):
                solution = '({:.6g})'.format(solution)
            elif isinstance(solution, tuple):
                solution= '(' + ', '.join(['{:.6g}'.format(n) for n in solution]) + ')'
                
            msg += '\n\n# Solution (Try First!)\nIt is: ' + str(solution)
            
        else:
            msg += '\n\n# Solution is a bit complex for me to guess :l'
    
    box(msg, title=title, border_color=PURP, text_color=PURP, secondary_color=PURP, clear_line=1)

def riddle(box: Callable, wrapper: Callable, open_path: Callable, show_solution=False, user_input=''):
    """Show a random riddle with its solution."""
    from settings import CYN, MAX_CONSOLE_WIDTH
    from os import path
    
    # Show the solution of previous riddle.
    text_file = 'riddle_answer.txt'
    app_dir = path.dirname(path.abspath(__file__))
    full_path = path.join(app_dir, text_file)
    
    if show_solution:
        open_path(full_path, clear=2, restore_prompt=user_input)
        return
    
    # Choose a puzzle and prepare its question & answer.
    puzzle = choice(RIDDLES)
    question = puzzle['?'].strip()
    answer = puzzle['✓'].strip()
    if answer == 'No logic':
        answer = 'There is no logic in this puzzle :P'
    
    # Hide the answer in a file.  
    with open(text_file, 'w', encoding='utf-8') as f:
        content = '# Query:\n' + question + '\n\n# Answer:\n' + answer
        content = wrapper(content, width=90)
        f.write(content)
    
    # Prepare the visual message.
    title = choice(['RIDDLE', 'PUZZLE', 'MYSTERY'])
    msg = '# Query:\n' + question + '\n\n'
    msg += CYN + '# The answer is written in:\n' + CYN + full_path + '\n'
    msg += CYN + "(Type 'r-answer' or 'riddle-answer' to see it)"
   
    # Show it.
    box(msg, title=title, border_color=PURP, text_color=PURP, secondary_color=PURP, clear_line=1)
    
def fake_scan(console_status: Callable, separator: Callable):
    """Confuse the user with fake scannning messages >:)"""
    from settings import YLW, RED, BL, GR, RS, SPINNER
    from time import sleep
    
    # Prepare messages.
    messages_1 = [
        'Scanning your disk. This might take a minute...',
        'Found some issues. Resuming scan...',
        'ERROR! Your disk must be wiped now. Working through...',
        f'Wiping progress: {randint(10, 33)}%',
        f'Wiping progress: {randint(34, 65)}%',
        f'Wiping progress: {randint(66, 98)}%',
        f'Wiping progress stuck at: 99%',
        'Restoring files from backup... Well, no backup found.',
        'Checking auto-backup... We forgot that before wiping.',
        'Convincing the system that nothing happened...',
        'Finished wiping your disk! Enjoy the void >.>',
    ]            
    
    messages_2 = [
        'Scanning your drive. Just a moment...',
        'Found a virus! Scan resuming...',
        'FATAL! The drive must be formatted now. Processing...',
        'Deleting user personal files...',
        'Deleting system files in (C:) drive...',
        "A quick cleanup to make sure you can't recover...",
        'Finished formatting! You can throw the disk later.',
    ]
    
    messages_3 = [
        'Checking your files history. Just a second...',
        'Oh! You meant to delete that! Resuming...',
        'Removing all your files in (Desktop). Sorry not sorry.',
        "Still removing... Wait.",
        'Cleaning up clutter. Your desktop was a mess!',
        'Now deleting files in (Documents, Downloads, Videos, etc)...',
        'Optimizing system... Or just pretending to...',
        'All done! Your computer is now slightly more confused.',
    ]
    
    messages_4 = [
        'Analyzing your system files... And secretly judging them.',
        'Defragmenting the chaos... Or just rearranging to waste time.',
        'Scanning drives for hidden files... Found some cookies.',
        'Compressing files into tiny little sandwiches...',
        'Renaming system files to confuse aliens...',
        'Cleaning up temp files... To fill them with viruses later.',
        'Finalized cleanup! Your files are now in therapy.',
    ]
    
    messages_5 = [
        'Mounting the drive... Please, hold onto your data.',
        'Checking for lost files... Found a few camping out.',
        'Encrypting everything... Even your mouse.',
        'Deleting duplicate files. Because one copy is enough, right?',
        'Deleting secret personal files. To make them more secret.',
        'Rearranging folders in alphabetical chaos...',
        'Scanning for malware... Found a whole party!',
        'Recalibrating drives for maximum laziness...',
        'All files are now in a better place... Probably ;-;',
    ]
    
    messages_6 = [
        'Initializing memory... You can sleep during that.',
        'Initializing self-destruct sequence... Get back!',
        'Counting all your cat videos... Why so many?',
        'Updating system malware database...',
        'Scanning RAM for lost thoughts... Couldn’t find any.',
        'Deleting hidden files... You didn’t even know you had them!',
        'Making your desktop icons dance... They seem scared.',
        'Installing a new AI overlord... It says: Hi!',
        'Backing up important files to my secure server...',
        'Optimizing coffee intake for maximum productivity... Failed.',
        'Finished! Your system now has more questions than answers.',
    ]

    messages_7 = [
        'Checking your recycle bin... Sadly, it’s empty.',
        'Encrypting your memes... They will never be seen again.',
        'Defragging your brain... Wait, wrong device.',
        f'Scanning for old emails... Found {randint(30, 300)} still unread.',
        'Shuffling your folders into a secret conspiracy...',
        "Deleting browsing history... Oops! Don't ask why.",
        'Deleting browser cache... Found interesting personal images.',
        'Optimizing files by giving them cute nicknames...',
        'Backing up your backup... Because why not?',
        'All done! Your files are now emotionally stable.',
    ]

    messages_8 = [
        'Loading components to examine your system...',
        'Renaming files for security. To confuse intruders...',
        f'Scanning for procrastination habits... Detected: {randint(90, 100)}%',
        'Sending random notifications for distraction... Ding! Dong!',
        'Compressing your selfies into text files... Too nice to be kept.',
        'Checking system for existential crisis... Found several.',
        'Moving system files to recycle bin for more protection....',
        'Defragmenting your imagination... Not enough space.',
        'Calculating the meaning of life... Nonsense.',
        "Finishing! Your PC is now... I don't know. Don't blame me.",
    ]
    
    messages_9 = [
        "Checking your security settings... Failed, good.",
        "Installing invisible updates... You shouldn't see them.",
        "Deleting unrecognized files... Mysterious things can be dangerous.",
        "Checking Wi-Fi for signs of life... Barely.",
        "Converting your documents into treasure maps... No (X) mark.",
        "Injecting spyware into your favorite programs...",
        "Optimizing the universe... One typo at a time.",
        "Clear! Your PC now believes in magic.",
    ]

    messages_10 = [
        "Calculating the size of disk. To wipe it faster.",
        "Uploading your notes to the cloud... Endearing!",
        "Encrypting your files for your safety... And theirs too.",
        "Turning your recycle bin into a black hole...",
        "Decorating your desktop with tiny dancing tacos...",
        "Scanning for parallel universes where you're productive... None.",
        "Adding random plot twists to your documents...",
        "Replacing system sounds with chicken clucks...",
        "Adding some scrambled eggs for the flavor...",
        "All done! Your computer is now working harder to be fast.",
    ]

    calm__messages = [
        "Everything is perfectly fine. Please do not panic...",
        "Everything is under control... Please remain calm.",
        "No action is required at this time. This is normal...",
        "Relax, the system is behaving as expected. Mostly...",
        "Please do not be alarmed. This was anticipated...",
        "Nothing unusual has been detected. Continue waiting...",
        "There is no need to worry. The situation is being handled...",
        "This process is safe. Any concerns are coincidental...",
        "Stay calm. The system has not failed but adapted...",
        "Everything is fine. Please stop watching the screen...",
        "No data loss is expected for now. Some data may disagree...",
        "This is just a routine operation. No need to be informed...",
        "Please remain patient... Resistance is unnecessary.",
        "Please relax... Resistance will cause more damage.",
        "Hold on... The outcome is favorable. For the system.",
        "Do not interrupt. This will improve the result...",
        "All system warnings have been reviewed and ignored...",
        "All system alerts have been received and dismissed...",
        "Encountered some major failures, but still fine...",
        "Found a problem. Your data may be at risk! But who cares?",
        "Till now, system integrity is intact. Definitions may vary...",
        "Nothing is wrong... Repeated reassurance is unnecessary.",
        "This message is for your comfort only...",
        "Let it finish cleanup & Don't intercept. It's too late...",
        "Don't panic if it looks stuck... This is usual.",
        "Your computer must stay idle now, don't move a finger...",
        "You should stop caring about your data... Why so passionate?",
        "Leave the mouse. No need to fight back for your data...",
        "You can leave the keyboard. There is no need to resist...",
        "This operation cannot be undone. Wait...",
    ]

    # Choose a set of messages to display.
    messages = choice([messages_1, messages_2, messages_3, messages_4, messages_5,
                       messages_6, messages_7, messages_8, messages_9, messages_10])

    calm = choice(calm__messages)
    length = len(messages)
    pos = randint(3, max(4, length-4))
    messages.insert(pos, calm)
    
    idx = 1
    msg = ''
    t1, t2 = 4, 8

    # Fake warning.
    print(PURP)
    separator(color=PURP)
    print(YLW + 'WARNING! The following content may be too intense for some people!')
    promise = None
    try: promise = input('Do you promise me not to get freaked out? (y/n): ' + RS).strip().lower()
    except KeyboardInterrupt: print()
    if promise != 'y':
        print(PURP + '\nMaybe next time. When you are ready...' + RS)
        separator(color=PURP)
        return

    # Start.
    try:
        # Display one message at a time with a random interval.
        print(PURP + "\n# Beginning 'Scan & Clean' Process!")
        with console_status(status='', spinner=SPINNER) as status:
            for msg in messages:
                progress = f'[bold purple]{msg}\n[/bold purple]'
                status.update(status=progress)
                
                t1 = max(t1 - 0.3, 2)
                t2 = max(t2 - 0.3, 4)
                interval = uniform(t1, t2) if idx != length else 3
                sleep(interval)

                if msg in calm__messages:
                    print(f'{GR}- NOTE:{BL} {msg}')
                else: 
                    print(f'{BL}- OP {idx}: {msg}{GR} [✓]')
                    idx += 1

        state = choice(['successfully', 'efficiently', 'effectively']) + '!'
        loss = choice(['confirmed', 'ensured', 'are guaranteed']) + '!'
        print(PURP + '\nOperations completed ' + state + '\nMajor losses ' + loss + RS)
        separator(color=PURP)

    except KeyboardInterrupt:
        try:
            if msg in calm__messages: print(f'{GR}- NOTE:{BL} {msg}\n')
            else: print(f'{BL}- OP {idx}: {msg}{RED} [X]\n')
        except:
            pass
        state = choice(['failed successfully', 'cancelled', 'aborted'])
        print(YLW + 'Operation ' + state + '!\n' + PURP +
              'Hopefully, partial damage may have already occurred.\n' +
              'Make sure to manually delete the rest later for maximum loss!' + RS)
        separator(color=PURP)

def overthink(box: Callable):
    """Funny state of minds while overthinking."""
    i = choice([0, 6, 12])
    ideas = '\n'.join(OVERTHINK[i:i+6])
    box(ideas, title='OVERTHINKING', border_color=PURP, text_color=PURP, secondary_color=PURP, clear_line=1)

def false_echo(user_input: str, box: Callable):
    """Repeat what the user just typed, or maybe not."""
    for p in  ['f-echo', 'false-echo']:
        if user_input.lower().startswith(p):
            text = user_input[len(p):].strip()
            break

    # Play with the text.
    if 0 < len(text) < 3:
        text += ' (Try something longer next time)'
    
    elif text:
        substitutions = {
            'A': '4', 'a': '@', 'B': '8', 'b': '6', 'E': '3', 'i': '1', 'I': '|',
            'l': '1', 'L': '1', 'O': '0', 'o': '0', 'S': '5', 's': '5', 'Z': '7',
            'z': '7', 'H': '#', 'C': '(', 'G': '(+', 'g': 'j', 'x': '×', '8': '&',
        }

        answers = [
            text,
            '...',
            '?????',
            'Bla bla bla...',
            'Yada yada...',
            'Bibbidi bobbidi boo!',
            'Echo vanished with the winds.',
            'Echo lost between the mountains.',
            "I don't repeat nonsense :P",
            "Wakanda nonsense is this?",
            "What does that mean already?",
            "Hmmm...",
            "Shhh... I can't hear anything.",
            "I CAN'T HEAR YOU BECAUSE OF THE FIERCE WIND!",
            "Sorry, what did you say?",
            "Speak clearly, I heard: Mmmmmmmm....",
            "I only heard the whistling of wind.",
            'I refuse to repeat that :l',
            'Why did you type that?',
            'I will pretend I didn’t see that.',
            'This echo requires more wind speed.',
            "I'll give you something better:\n\n" + choice(LANGS).replace(' (Translation:', '\n(Translation:').replace(' # ', '\n# '),
            f'You said: “{text}” ... I think ;-;',
            f'Analyzing: “{text}”\nNothing special in it.',
            'Shouting: ' + text.upper() + ('!' if not text.endswith('!') else ''),
            'Whispering: ' + text.lower(),
            text.title() + ' (Feels nicer now, right?)',
            text.capitalize() + ' (I capitalized the first letter for you :3)',
            text.swapcase(),
            text + ' (really?)',
            text[::-1],
            ' '.join(text),
            ' '.join(text.replace(' ', '')),
            ''.join(c * randint(1, 3) if not c.isspace() else c for c in text).strip() + ('...' if not text.endswith('...') else ''),
            ''.join(c if not c.isspace() else '' for c in text),
        ]

        length = len(answers)
        option = randint(1, length+5)

        match option:
            case 1:
                for k, v in substitutions.items(): text = text.replace(k, v)

            case 2:
                for k, v in substitutions.items(): text = text.replace(v, k)

            case 3:
                # Shuffle all characters.
                chars = list(text)
                shuffle(chars)
                text = ''.join(chars)

            case 4:
                # Shuffle all words.
                words = text.split()
                shuffle(words)
                text = ' '.join(words)

            case 5:
                # Shuffle characters in words. Keep words order.
                words = text.split()
                text = ''
                for word in words:
                    word = list(word)
                    shuffle(word)
                    text += ''.join(word) + ' '

                text = text.strip()

            case c if c in range(6, length+6):
                text = answers[option-6]

    else:
        text = 'You echoed… nothing.'

    # Show it.
    box(text, title='ECHO', border_color=PURP, text_color=PURP, secondary_color=PURP, clear_line=1)

def time_travel(command: str, box: Callable):
    """
    Display a random or a requested year with an event that happened or may
    happen at that year.
    """
    from heapq import nsmallest
    
    # Show a random year & exit.
    if command == 'time-travel':
        year = "You have arrived in " + choice(TIME_TRAVEL)
        box(year, title='TIME TRAVEL', border_color=PURP, text_color=PURP, secondary_color=PURP, clear_line=1)
        return
 
    # Show a user-specified year.
    indicators = ['BC', 'BCE', 'AD', 'CE']
    indicator_map = {'BC': 'BCE', 'BCE': 'BC', 'CE': 'AD', 'AD': 'CE'}  # Just a fallback, since AD = CE & BC = BCE.
    user_year = command[12:].upper().strip()
    user_year_int = int(''.join(c for c in user_year if c.isdigit()))
    user_year_era = ''.join(c for c in user_year if c.isalpha())
    user_year_era = user_year_era if user_year_era in indicators else None
    fallback_user_era = indicator_map.get(user_year_era, user_year_era)

    # Create a list of years & their era indicators.
    years = []
    for event in TIME_TRAVEL:
        year_digits = ''
        clean_event = event.replace(',', '').replace(';', '').replace('.', '')
        for c in clean_event:
            if c.isdigit(): year_digits += c
            else: break
            
        year_digits = (len(year_digits) or 0) + 2
        found = False
        for i in indicators:
            length = 0
            i = ' ' + i  + '.'
            j = '.'.join(i)  + '.'
            if i in event[:20]: length = year_digits + len(i)
            elif j in event[:20]: length = year_digits + len(j)
            else: continue
            
            years.append(event[:length])
            found = True
            break

        if not found: years.append(event[:year_digits])
        
    years = [year.replace('.', '').upper().strip() + ' ' for year in years]

    # Get the nearest year number to the user's entered year, while prioritizing the indicated era.
    years_int = []
    inf = float('inf')  # Infinity is a placeholder for unwanted results, to keep original list indexes.
    if user_year_era and user_year_era in ['BC', 'BCE']:
        # Get years only with the user-specified era.
        for year in years:
            clean_year = year.replace('.', '')
            if (' ' + user_year_era in clean_year) or (' ' + fallback_user_era in clean_year):
                integer = int(''.join(c for c in year if c.isdigit()))
                years_int.append(integer)
            else:
                years_int.append(inf)

    else:
        # User didn't specify the era, so get only years of common era.
        for year in years:
            clean_year = year.replace('.', '')
            era_found = False
            for i in ['BC', 'BCE']:
                if i in clean_year:
                    years_int.append(inf)
                    era_found = True
                    break
            if not era_found:
                integer = int(''.join(c for c in year if c.isdigit()))
                years_int.append(integer)
                
    top_match = nsmallest(1, years_int, key=lambda x: abs(user_year_int - x))[0]

    # Track the result & find its original string in TIME_TRAVEL list.
    i = years_int.index(top_match)
    result = TIME_TRAVEL[i]
    note = ''
    if user_year_int != top_match:
        year = command[12:].strip()
        meant_year = ''.join(c for c in year if c.isdigit() or c.isalpha() or c.isspace()).upper()
        corrected_year = (''.join(c for c in year if c.isdigit()) + ' ' + ''.join(c for c in year if c.isalpha())).upper().strip()
        if corrected_year != meant_year: correction = f' assuming you meant ({corrected_year}),'
        else: correction = ''
        note = f"\n\nCouldn't travel to ({year}),{correction} so instead went to the nearest year is that era ;)"

    # Display it.
    msg = "You have arrived in " + result + note
    box(msg, title='TIME TRAVEL', border_color=PURP, text_color=PURP, secondary_color=PURP, clear_line=1)

def draw_ascii_image(str_name: str, title:str, color: str, console_width: int, visual_len: Callable, box: Callable):
    """Display a static & random ASCII art, based on a string of ascii images."""
    # Get the string of ascii images.
    string = globals()[str_name]
    frames = string.split('!')
    frame = choice(frames).lstrip('\n').rstrip()
    
    # Correct the position & limits of the image.
    if visual_len(frame) > console_width - 4:
        string = ''
        for line in frame.splitlines(): string += line[:console_width-4] + '\n'
        frame = string.rstrip()
        
    elif visual_len(frame) < console_width - 10:
        space = ' ' * ((console_width - visual_len(frame)) // 2)
        string = ''
        for line in frame.splitlines(): string += space + line + '\n'
        frame = string.rstrip()
    
    # Display it.
    box(frame, title=title, border_color=color, text_color=color, clear_line=1)

def draw_ascii_animation(str_name: str, title: str, color: str, interval: int, stop_frames: int, control_cursor: Callable, clear_lines: Callable):
    """Play an ASCII animation based on a string of frames."""
    from settings import USE_ANSI, RS
    from time import sleep
    
    # Preparation.
    string = globals()[str_name]
    frames = string.split('!')
    frames = [frame.lstrip('\n').rstrip() for frame in frames if frame.strip()]
    height = frames[1].count('\n') + 1
    print(color + title)
    control_cursor('hide')
    
    # Play the animation.
    try:
        while True:
            for frame in frames[:-3]:
                print(frame)
                sleep(interval)
                clear_lines(height)
                if not USE_ANSI: print()
    
    # Stop & Exit.
    except KeyboardInterrupt:
        clear_lines(height)
        if not USE_ANSI: print()
        print(choice(frames[-3:]) + RS)
        control_cursor('show')