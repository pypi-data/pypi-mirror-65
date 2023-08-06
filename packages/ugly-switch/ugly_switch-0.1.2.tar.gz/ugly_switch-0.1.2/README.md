# ugly_switch
  [![Build Status](https://travis-ci.org/RoW171/ugly_switch.svg?branch=master)](https://travis-ci.org/RoW171/ugly_switch)
  [![codecov](https://codecov.io/gh/RoW171/ugly_switch/branch/master/graph/badge.svg)](https://codecov.io/gh/RoW171/ugly_switch)
  [![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](http://choosealicense.com/licenses/mit/)
  
  An ugly pseudo solution for using switches in python.
  
### Installation

    pip install ugly_switch
  
### Usage

    from ugly_switch import switch

  A Switch can be used once:
    
    switch[
        True, door_lock,
        False, door_unlock
    ](not door_state)
    
    # looks the door when it's state is False and vice versa
        
  or can be stored to be used multiple times in the future:
  
    s = switch[
        'a', lambda: print('was a'),
        'b', lambda: print('was b')
    ]
    
    # some stuff
    
    value = 'a'
    s(value)
    
    # OUT: "was a"
    
  When the number of args in the switch is **even**,
  the pairs make up the switch as sets of **cases** and **actions**.
  actions must be **callable methods** or **lambdas**.
  If the number of args may be **odd**, the last item
  will be used as **default**, expecting it to be a callable.
  
  With the example directly above, nothing will happen, if `value`
  happens to be neither `'a'` nor `'b'`.
  
  Below it has a default action.
  
    value = 'c'
    s = switch[
        'a', lambda: print('was a'),
        'b', lambda: print('was b'),
        lambda: print('something else')
    ]
    
    # some stuff
    
    s(value)
    
    # OUT: "something else"