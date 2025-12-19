# This module is just for fun, used with extra commands that can be accepted
# inside interpret_commands() function in gemini.py module.

# Somebody told me:
# My honest opinion, your project feels like:
# “A CLI written by someone who enjoys messing with users — in a good way.”

from settings import PURP
from typing import Callable
from random import random, randint, uniform, choice

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
    "Fact: Octopuses have three hearts! Two pump blood to the gills, and one circulates it to the rest of the body.",
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

        state = choice(['successfully', 'efficiently', 'effectively'])
        print(PURP + '\nOperations completed ' + state + '!' + YLW + '\nMajor failures ignored.' + RS)
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
    text = user_input.removeprefix('f-echo').removeprefix('false-echo').strip()

    # Play with the text.
    if 0 < len(text) < 3:
        text += ' (Try something longer next time)'
    
    elif text:
        option = randint(1, 24)
        substitutions = {'A': '4', 'a': '@', 'B': '8', 'b': '6', 'E': '3', 'i': '1',
                         'I': '1', 'l': '1', 'L': '1', 'O': '0', 'o': '0', 'S': '5',
                         's': '5', 'Z': '2', 'z': '2'}
        
        match option:
            case 1: pass
            case 2: text = text.upper()
            case 3: text = text.lower()
            case 4: text = text.title()
            case 5: text = text.capitalize()
            case 6: text = text.swapcase()
            case 7: text = text[::-1]
            case 8: text = ' '.join(text)
            case 9: text = text + ' (really?)'
            case 10: text = f'You said: “{text}” ... I think ;-;'
            case 11: text = 'I refuse to repeat that :l'
            case 12: text = 'Why did you type that?'
            case 13: text = 'I will pretend I didn’t see that.'
            case 14: text = 'This echo requires more wind speed.'
            case 15: text = f'Analyzing: “{text}”\nNothing special in it.'
            case 16: text = '...'
            case 17: text = '?????'
            case 18: text = 'Bla bla bla...'
            case 19: text = 'Yada yada...'
            case 20: text = 'Bibbidi bobbidi boo!'
            case 21: text = 'Echo vanished in the winds.'
            case 22: text = 'Echo lost between the mountains.'
            case 23:
                for k, v in substitutions.items(): text = text.replace(k, v)
            case 24:
                for k, v in substitutions.items(): text = text.replace(v, k)

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