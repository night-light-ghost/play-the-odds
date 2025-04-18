A Casino Blackjack Engine in Python

# BlackJack Odds reading CLI game

This game is designed to simulate a game of blackjack at a casino table.
While at a blackjack table there are some basic understandings of strategy, this is designed to give suggestions beyond the base visible information.
As a computer is pretty darn good at remembering the count of what's happened, we can use it to keep a running log, and give us real-time changing likelihoods.

We'll attempt to have a dashboard of informaton, preinted out in ascii format here on a command line.

Best of luck! And may you be able to know when the odds are in your favour ;-)


## Initial Game setup

The game begins with a shuffled 6 card deck and the player has $500

```
Default Game board:

+++==========||==========||==========||==========+++
|                                                  |
]                                                  [
]                                                  [
]                                                  [
]                                                  [
]                                                  [
|                                                  |
)                                                  (
)                                                  (
|                                                  |
]                                                  [
]                                                  [
]                                                  [
]                                                  [
]                                                  [
|                                                  |
+++==========||==========||==========||==========+++

Game board with cards:

+++==========||==========||==========||==========+++
|                                                  |
]                  PADE PADE CLUB                  [
]                  //\\  /\   /\                   [
]                  \\// /--\ /  \                  [
]                  //\\ |  | \ \/                  [
]                  \\// |  |  \/\                  [
|                                                  |
)                    - - ++ - -                    (
)                    - - ++ - -                    (
|                                                  |
]                  || / //\\ ====                  [
]                  ||/    //   //                  [
]                  ||\   //   //                   [
]                  || \ /___ //                    [
]                  CLUB DMND HART                  [
|                                                  |
+++==========||==========||==========||==========+++

Spit card game:

+++==========||==========||==========||==========+++
|                                                  |
]                  PADE PADE CLUB                  [
]                  //\\  /\   /\                   [
]                  \\// /--\ /  \                  [
]                  //\\ |  | \ \/                  [
]                  \\// |  |  \/\                  [
|                                                  |
)                    - - ++ - -                    (
)                    - - ++ - -                    (
|  ^^^^^^^^^^                                      |
]  //==  ====                          //==  ====  [
]  ||      //                          ||      //  [
]  \\\\   //                           \\\\   //   [
]  __//  //                            __//  //    [
]  DMND  HART                          DMND  HART  [
|                                                  |
+++==========||==========||==========||==========+++

Carats to show the current hand in play



Sample Card ascii art:

    /\      || //     =====       ___        ======     JJJJ   
   //\\     ||//     //   \\     / _ \         ||        JJ
  //__\\    ||\\    ||     ||   | | | |        ||        JJ    _____
 //    \\   || \\    \\  \\//   | |_| |   ||   ||   JJ   JJ    _____
//      \\  ||  \\    ====\\     \__\_\    \\=//     JJJJJ     _____

 //1|       //\\    //\\    //||   //====   //==\\  ====/7   8==8    9==9    0000
// ||      // //      //   // ||   ||       ||         77   ||  ||  ||  ||  00  00
   ||        //      333   ======  |55555\  ||==66    77    88==88   9999   00  00
   ||       //        \\      44        ||  ||  ||   77     ||  ||      ||  00  00
   ||      22===    \\//      44    ====//  66==66  77       8==8     999    0000

                                                                 
  //\\  //\\  | ||  //==  //\\  ====  //\\   //\\   /|| //\\   ____
    //    //  |_||  ||    ||      //  \\//   \\//  //|| ||||  
   //     \\    ||  \\\\  ||\\   //   //\\    //     || ||||  
  /___  \\//    ||  __//  \\//  //    \\//   //      || \\//  

 
  /\        /\        @@       _  _    _____
 /  \      /  \     @@  @@    ( \/ )
<    >    (_  _)   @@@  @@@    \  /
 \  /       /\        /\       \ /
  \/       /__\      /__\       V
       
D     S     C     H    
M     P     L     R
D     D     B     T        
S     S     S     S       
DMND  PADE  CLUB  HART

  /\    || /   /\   ====   /|/\
 /__\   ||/   /  \     |    |||
 |  |   ||\   \ \/     |    |||
 |  |   || \   \/\  \__/    |\/


 /\ D  //\\C     /\  D //\\ C     D /\   C//\\   D  /\   C //\\   D /\   //\\C
/  \M  \\//L    /  \ M \\// L     M/  \  L\\//   M /  \  L \\//   M/  \  \\//L
\ \/D  //\\B    \ \/ D //\\ B     D\ \/  B//\\   D \ \/  B //\\   D\ \/  //\\B
 \/\S  \\//S     \/\ S \\// S     S \/\  S\\//   S  \/\  S \\//   S \/\  \\//S

 /\   //\\     DMDS //\\       DMND  CLUB
/  \  \\//      /\  \\//        /\   //\\
\ \/  //\\     /  \ //\\       /  \  \\//
 \/\  \\//     \ \/ \\//       \ \/  //\\
DMDS  CLBS      \/\ CLBS        \/\  \\//

```
