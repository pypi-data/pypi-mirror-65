info = {'raise_indentation_error1': {'cause': 'In this case, the line identified above\n'
                                       'was expected to begin a new indented block.\n',
                              'message': 'IndentationError: expected an indented block\n',
                              'parsing_error_source': "       1: '''Should raise "
                                                      "IndentationError'''\n"
                                                      '       2: \n'
                                                      '       3: if True:\n'
                                                      '    -->4: pass\n'
                                                      '             ^\n'},
 'raise_indentation_error2': {'cause': 'In this case, the line identified above\n'
                                       'is more indented than expected and \n'
                                       'does not match the indentation of the previous line.\n',
                              'message': 'IndentationError: unexpected indent\n',
                              'parsing_error_source': "       1: '''Should raise "
                                                      "IndentationError'''\n"
                                                      '       2: if True:\n'
                                                      '       3:     pass\n'
                                                      '    -->4:       pass\n'
                                                      '               ^\n'},
 'raise_indentation_error3': {'cause': 'In this case, the line identified above is\n'
                                       'less indented than the preceding one,\n'
                                       'and is not aligned vertically with another block of '
                                       'code.\n',
                              'message': 'IndentationError: unindent does not match any outer '
                                         'indentation level\n',
                              'parsing_error_source': "       1: '''Should raise "
                                                      "IndentationError'''\n"
                                                      '       2: if True:\n'
                                                      '       3:       pass\n'
                                                      '    -->4:     pass\n'
                                                      '                  ^\n'},
 'raise_syntax_error1': {'cause': 'I make an effort below to guess what caused the problem\n'
                                  'but I might guess incorrectly.\n'
                                  '\n'
                                  "You were trying to assign a value to the Python keyword 'def'.\n"
                                  'This is not allowed.\n'
                                  '\n',
                         'message': 'SyntaxError: invalid syntax\n',
                         'parsing_error_source': '       1: """ Should raise SyntaxError"""\n'
                                                 '       2: \n'
                                                 '    -->3: def = 2\n'
                                                 '              ^\n'},
 'raise_syntax_error10': {'cause': 'You wrote an expression like\n'
                                   '    1 = 2\n'
                                   'where <1>, on the left-hand side of the equal sign,\n'
                                   "is or includes an actual object of type 'int'\n"
                                   'and is not simply the name of a variable.\n',
                          'message': "SyntaxError: can't assign to literal\n",
                          'parsing_error_source': '       1: """Should raise SyntaxError: can\'t '
                                                  'assign to literal"""\n'
                                                  '       2: \n'
                                                  '    -->3: 1 = 2\n'
                                                  '         ^\n'},
 'raise_syntax_error11': {'cause': 'I make an effort below to guess what caused the problem\n'
                                   'but I might guess incorrectly.\n'
                                   '\n'
                                   'You wrote something like\n'
                                   '    import pen from turtle\n'
                                   'instead of\n'
                                   '    from turtle import pen\n'
                                   '\n',
                          'message': 'SyntaxError: invalid syntax\n',
                          'parsing_error_source': '       1: """Should raise SyntaxError: invalid '
                                                  'syntax"""\n'
                                                  '       2: \n'
                                                  '    -->3: import pen from turtle\n'
                                                  '                        ^\n'},
 'raise_syntax_error12': {'cause': 'You starting writing a string with a single or double quote\n'
                                   'but never ended the string with another quote on that line.\n',
                          'message': 'SyntaxError: EOL while scanning string literal\n',
                          'parsing_error_source': '       1: """Should raise SyntaxError: EOL '
                                                  'while scanning string literal"""\n'
                                                  '       2: \n'
                                                  "    -->3: alphabet = 'abc\n"
                                                  '                         ^\n'},
 'raise_syntax_error13': {'cause': 'None is a constant in Python; you cannot assign it a value.\n'
                                   '\n',
                          'message': "SyntaxError: can't assign to keyword\n",
                          'parsing_error_source': '       1: """Should raise SyntaxError: cannot '
                                                  'assign to None in Py 3.8\n'
                                                  "       2:    and can't assign to keyword "
                                                  'before."""\n'
                                                  '       3: \n'
                                                  '    -->4: None = 1\n'
                                                  '         ^\n'},
 'raise_syntax_error14': {'cause': '__debug__ is a constant in Python; you cannot assign it a '
                                   'value.\n'
                                   '\n',
                          'message': 'SyntaxError: assignment to keyword\n',
                          'parsing_error_source': '       1: """Should raise SyntaxError: cannot '
                                                  'assign to __debug__ in Py 3.8\n'
                                                  '       2:    and assignment to keyword '
                                                  'before."""\n'
                                                  '       3: \n'
                                                  '    -->4: __debug__ = 1\n'
                                                  '         ^\n'},
 'raise_syntax_error15': {'cause': 'I make an effort below to guess what caused the problem\n'
                                   'but I might guess incorrectly.\n'
                                   '\n'
                                   "The closing parenthesis ')' on line 6 does not match "
                                   'anything.\n'
                                   '\n'
                                   '    6:     3, 4,))\n'
                                   '                 ^\n',
                          'message': 'SyntaxError: invalid syntax\n',
                          'parsing_error_source': '       3: """\n'
                                                  '       4: a = (1,\n'
                                                  '       5:     2,\n'
                                                  '    -->6:     3, 4,))\n'
                                                  '                    ^\n'},
 'raise_syntax_error16': {'cause': 'I make an effort below to guess what caused the problem\n'
                                   'but I might guess incorrectly.\n'
                                   '\n'
                                   "The opening parenthesis '(' on line 2 is not closed.\n"
                                   '\n'
                                   "    2: x = int('1'\n"
                                   '              ^\n',
                          'message': 'SyntaxError: invalid syntax\n',
                          'parsing_error_source': '       1: """Should raise SyntaxError: invalid '
                                                  'syntax"""\n'
                                                  "       2: x = int('1'\n"
                                                  '    -->3: if x == 1:\n'
                                                  '                   ^\n'},
 'raise_syntax_error17': {'cause': 'I make an effort below to guess what caused the problem\n'
                                   'but I might guess incorrectly.\n'
                                   '\n'
                                   "The opening parenthesis '(' on line 2 is not closed.\n"
                                   '\n'
                                   '    2: a = (b+c\n'
                                   '           ^\n',
                          'message': 'SyntaxError: invalid syntax\n',
                          'parsing_error_source': '       1: """Should raise SyntaxError: invalid '
                                                  'syntax"""\n'
                                                  '       2: a = (b+c\n'
                                                  '    -->3: d = a*a\n'
                                                  '          ^\n'},
 'raise_syntax_error18': {'cause': 'I make an effort below to guess what caused the problem\n'
                                   'but I might guess incorrectly.\n'
                                   '\n'
                                   "The closing square bracket ']' on line 2 does not match the "
                                   "opening parenthesis '(' on line 2.\n"
                                   '\n'
                                   '    2: x = (1, 2, 3]\n'
                                   '           ^       ^\n',
                          'message': 'SyntaxError: invalid syntax\n',
                          'parsing_error_source': '       1: """Should raise SyntaxError: invalid '
                                                  'syntax"""\n'
                                                  '    -->2: x = (1, 2, 3]\n'
                                                  '                      ^\n'},
 'raise_syntax_error19': {'cause': 'I make an effort below to guess what caused the problem\n'
                                   'but I might guess incorrectly.\n'
                                   '\n'
                                   "The closing square bracket ']' on line 4 does not match the "
                                   "opening parenthesis '(' on line 2.\n"
                                   '\n'
                                   '    2: x = (1,\n'
                                   '           ^\n'
                                   '    4:      3]\n'
                                   '             ^\n',
                          'message': 'SyntaxError: invalid syntax\n',
                          'parsing_error_source': '       1: """Should raise SyntaxError: invalid '
                                                  'syntax"""\n'
                                                  '       2: x = (1,\n'
                                                  '       3:      2,\n'
                                                  '    -->4:      3]\n'
                                                  '                ^\n'},
 'raise_syntax_error2': {'cause': 'I make an effort below to guess what caused the problem\n'
                                  'but I might guess incorrectly.\n'
                                  '\n'
                                  'You wrote a statement beginning with\n'
                                  "'if' but forgot to add a colon ':' at the end\n"
                                  '\n',
                         'message': 'SyntaxError: invalid syntax\n',
                         'parsing_error_source': '       1: """Should raise SyntaxError"""\n'
                                                 '       2: \n'
                                                 '    -->3: if True\n'
                                                 '                 ^\n'},
 'raise_syntax_error20': {'cause': "Perhaps you need to type print('hello')?\n"
                                   '\n'
                                   "In older version of Python, 'print' was a keyword.\n"
                                   "Now, 'print' is a function; you need to use parentheses to "
                                   'call it.\n',
                          'message': "SyntaxError: Missing parentheses in call to 'print'. Did you "
                                     "mean print('hello')?\n",
                          'parsing_error_source': '       1: """Should raise SyntaxError: Missing '
                                                  'parentheses in call to \'print\' ..."""\n'
                                                  "    -->2: print 'hello'\n"
                                                  '                      ^\n'},
 'raise_syntax_error21': {'cause': 'I make an effort below to guess what caused the problem\n'
                                   'but I might guess incorrectly.\n'
                                   '\n'
                                   "You tried to use the Python keyword 'pass' as a function "
                                   'name.\n',
                          'message': 'SyntaxError: invalid syntax\n',
                          'parsing_error_source': '       1: """Should raise SyntaxError: invalid '
                                                  'syntax"""\n'
                                                  '       2: \n'
                                                  '    -->3: def pass():\n'
                                                  '                 ^\n'},
 'raise_syntax_error22': {'cause': "The Python keyword 'break' can only be used inside a for loop "
                                   'or inside a while loop.\n',
                          'message': "SyntaxError: 'break' outside loop\n",
                          'parsing_error_source': '       1: """Should raise SyntaxError: '
                                                  '\'break\' outside loop"""\n'
                                                  '       2: \n'
                                                  '       3: if True:\n'
                                                  '    -->4:     break\n'
                                                  '             ^\n'},
 'raise_syntax_error23': {'cause': "The Python keyword 'continue' can only be used inside a for "
                                   'loop or inside a while loop.\n',
                          'message': "SyntaxError: 'continue' not properly in loop\n",
                          'parsing_error_source': '       1: """Should raise SyntaxError: '
                                                  '\'continue\' outside loop"""\n'
                                                  '       2: \n'
                                                  '       3: if True:\n'
                                                  '    -->4:     continue\n'
                                                  '             ^\n'},
 'raise_syntax_error24': {'cause': 'I make an effort below to guess what caused the problem\n'
                                   'but I might guess incorrectly.\n'
                                   '\n'
                                   'There appears to be a Python identifier (variable name)\n'
                                   'immediately following a string.\n'
                                   'I suspect that you were trying to use a quote inside a string\n'
                                   'that was enclosed in quotes of the same kind.\n',
                          'message': 'SyntaxError: invalid syntax\n',
                          'parsing_error_source': '       1: """Should raise SyntaxError: invalid '
                                                  'syntax"""\n'
                                                  '       2: \n'
                                                  "    -->3: message = 'don't'\n"
                                                  '                         ^\n'},
 'raise_syntax_error25': {'cause': 'I make an effort below to guess what caused the problem\n'
                                   'but I might guess incorrectly.\n'
                                   '\n'
                                   'It is possible that you forgot a comma between items in a set '
                                   'or dict\n'
                                   'before the position indicated by --> and ^.\n',
                          'message': 'SyntaxError: invalid syntax\n',
                          'parsing_error_source': '       2: \n'
                                                  "       3: a = {'a': 1,\n"
                                                  "       4:      'b': 2\n"
                                                  "    -->5:      'c': 3,\n"
                                                  '                 ^\n'},
 'raise_syntax_error26': {'cause': 'I make an effort below to guess what caused the problem\n'
                                   'but I might guess incorrectly.\n'
                                   '\n'
                                   'It is possible that you forgot a comma between items in a set '
                                   'or dict\n'
                                   'before the position indicated by --> and ^.\n',
                          'message': 'SyntaxError: invalid syntax\n',
                          'parsing_error_source': '       1: """Should raise SyntaxError: invalid '
                                                  'syntax"""\n'
                                                  '       2: \n'
                                                  '    -->3: a = {1, 2  3}\n'
                                                  '                     ^\n'},
 'raise_syntax_error27': {'cause': 'I make an effort below to guess what caused the problem\n'
                                   'but I might guess incorrectly.\n'
                                   '\n'
                                   'It is possible that you forgot a comma between items in a '
                                   'list\n'
                                   'before the position indicated by --> and ^.\n',
                          'message': 'SyntaxError: invalid syntax\n',
                          'parsing_error_source': '       1: """Should raise SyntaxError: invalid '
                                                  'syntax"""\n'
                                                  '       2: \n'
                                                  '    -->3: a = [1, 2  3]\n'
                                                  '                     ^\n'},
 'raise_syntax_error28': {'cause': 'I make an effort below to guess what caused the problem\n'
                                   'but I might guess incorrectly.\n'
                                   '\n'
                                   'It is possible that you forgot a comma between items in a '
                                   'tuple, \n'
                                   'or between function arguments, \n'
                                   'before the position indicated by --> and ^.\n',
                          'message': 'SyntaxError: invalid syntax\n',
                          'parsing_error_source': '       1: """Should raise SyntaxError: invalid '
                                                  'syntax"""\n'
                                                  '       2: \n'
                                                  '    -->3: a = (1, 2  3)\n'
                                                  '                     ^\n'},
 'raise_syntax_error29': {'cause': 'I make an effort below to guess what caused the problem\n'
                                   'but I might guess incorrectly.\n'
                                   '\n'
                                   'It is possible that you forgot a comma between items in a '
                                   'tuple, \n'
                                   'or between function arguments, \n'
                                   'before the position indicated by --> and ^.\n',
                          'message': 'SyntaxError: invalid syntax\n',
                          'parsing_error_source': '       1: """Should raise SyntaxError: invalid '
                                                  'syntax"""\n'
                                                  '       2: \n'
                                                  '       3: \n'
                                                  '    -->4: def a(b, c d):\n'
                                                  '                     ^\n'},
 'raise_syntax_error3': {'cause': 'I make an effort below to guess what caused the problem\n'
                                  'but I might guess incorrectly.\n'
                                  '\n'
                                  "You wrote a 'while' loop but\n"
                                  "forgot to add a colon ':' at the end\n"
                                  '\n',
                         'message': 'SyntaxError: invalid syntax\n',
                         'parsing_error_source': '       1: """Should raise SyntaxError"""\n'
                                                 '       2: \n'
                                                 '    -->3: while True  # a comment\n'
                                                 '                                 ^\n'},
 'raise_syntax_error30': {'cause': 'You wrote the expression\n'
                                   "    len('a') = 3\n"
                                   "where len('a'), on the left-hand side of the equal sign, "
                                   'either is\n'
                                   'or includes a function call and is not simply the name of a '
                                   'variable.\n',
                          'message': "SyntaxError: can't assign to function call\n",
                          'parsing_error_source': '       3: Python 3.8: SyntaxError: cannot '
                                                  'assign to function call\n'
                                                  '       4: """\n'
                                                  '       5: \n'
                                                  "    -->6: len('a') = 3\n"
                                                  '         ^\n'},
 'raise_syntax_error31': {'cause': 'You wrote an expression like\n'
                                   '    my_function(...) = some value\n'
                                   'where my_function(...), on the left-hand side of the equal '
                                   'sign, is\n'
                                   'a function call and not the name of a variable.\n',
                          'message': "SyntaxError: can't assign to function call\n",
                          'parsing_error_source': '       3: Python 3.8: SyntaxError: cannot '
                                                  'assign to function call\n'
                                                  '       4: """\n'
                                                  '       5: \n'
                                                  '    -->6: func(a, b=3) = 4\n'
                                                  '         ^\n'},
 'raise_syntax_error32': {'cause': 'I make an effort below to guess what caused the problem\n'
                                   'but I might guess incorrectly.\n'
                                   '\n'
                                   "It is possible that you used an equal sign '=' instead of a "
                                   "colon ':'\n"
                                   'to assign values to keys in a dict\n'
                                   'before or at the position indicated by --> and ^.\n',
                          'message': 'SyntaxError: invalid syntax\n',
                          'parsing_error_source': '       1: """Should raise SyntaxError: invalid '
                                                  'syntax\n'
                                                  '       2: """\n'
                                                  '       3: \n'
                                                  "    -->4: ages = {'Alice'=22, 'Bob'=24}\n"
                                                  '                         ^\n'},
 'raise_syntax_error33': {'cause': 'In Python, you can define functions with only positional '
                                   'arguments\n'
                                   '\n'
                                   '    def test(a, b, c): ...\n'
                                   '\n'
                                   'or only keyword arguments\n'
                                   '\n'
                                   '    def test(a=1, b=2, c=3): ...\n'
                                   '\n'
                                   'or a combination of the two\n'
                                   '\n'
                                   '    def test(a, b, c=3): ...\n'
                                   '\n'
                                   'but with the keyword arguments appearing after all the '
                                   'positional ones.\n'
                                   'According to Python, you used positional arguments after '
                                   'keyword ones.\n',
                          'message': 'SyntaxError: non-default argument follows default argument\n',
                          'parsing_error_source': '       2: """\n'
                                                  '       3: \n'
                                                  '       4: \n'
                                                  '    -->5: def test(a=1, b):\n'
                                                  '                  ^\n'},
 'raise_syntax_error34': {'cause': 'In Python, you can call functions with only positional '
                                   'arguments\n'
                                   '\n'
                                   '    test(1, 2, 3)\n'
                                   '\n'
                                   'or only keyword arguments\n'
                                   '\n'
                                   '    test(a=1, b=2, c=3)\n'
                                   '\n'
                                   'or a combination of the two\n'
                                   '\n'
                                   '    test(1, 2, c=3)\n'
                                   '\n'
                                   'but with the keyword arguments appearing after all the '
                                   'positional ones.\n'
                                   'According to Python, you used positional arguments after '
                                   'keyword ones.\n',
                          'message': 'SyntaxError: positional argument follows keyword argument\n',
                          'parsing_error_source': '       2: """\n'
                                                  '       3: \n'
                                                  '       4: \n'
                                                  '    -->5: test(a=1, b)\n'
                                                  '                   ^\n'},
 'raise_syntax_error35': {'cause': 'Inside an f-string, which is a string prefixed by the letter '
                                   'f, \n'
                                   'you have another string, which starts with either a\n'
                                   'single quote (\') or double quote ("), without a matching '
                                   'closing one.\n',
                          'message': 'SyntaxError: f-string: unterminated string\n',
                          'parsing_error_source': '       1: """Should raise SyntaxError: '
                                                  'f-string: unterminated string\n'
                                                  '       2: """\n'
                                                  '       3: \n'
                                                  '    -->4: print(f"Bob is {age[\'Bob]} years '
                                                  'old.")\n'
                                                  '               ^\n'},
 'raise_syntax_error36': {'cause': 'I make an effort below to guess what caused the problem\n'
                                   'but I might guess incorrectly.\n'
                                   '\n'
                                   "The opening square bracket '[' on line 5 is not closed.\n"
                                   '\n'
                                   '    5:     return [1, 2, 3\n'
                                   '                  ^\n',
                          'message': 'SyntaxError: invalid syntax\n',
                          'parsing_error_source': '        4: def foo():\n'
                                                  '        5:     return [1, 2, 3\n'
                                                  '        6: \n'
                                                  '    --> 7: print(foo())\n'
                                                  '               ^\n'},
 'raise_syntax_error37': {'cause': 'Python tells us that the it reached the end of the file\n'
                                   'and expected more content.\n'
                                   '\n'
                                   'I will attempt to be give a bit more information.\n'
                                   '\n'
                                   "The opening square bracket '[' on line 5 is not closed.\n"
                                   '\n'
                                   '    5:     return [1, 2, 3,\n'
                                   '                  ^\n',
                          'message': 'SyntaxError: unexpected EOF while parsing\n',
                          'parsing_error_source': '        5:     return [1, 2, 3,\n'
                                                  '        6: \n'
                                                  '        7: print(foo())\n'},
 'raise_syntax_error38': {'cause': 'You are including the statement\n'
                                   '\n'
                                   '        global x\n'
                                   '\n'
                                   "indicating that 'x' is a variable defined outside a function.\n"
                                   "You are also using the same 'x' as an argument for that\n"
                                   'function, thus indicating that it should be variable known '
                                   'only\n'
                                   "inside that function, which is the contrary of what 'global' "
                                   'implied.\n',
                          'message': "SyntaxError: name 'x' is parameter and global\n",
                          'parsing_error_source': '       3: \n'
                                                  '       4: \n'
                                                  '       5: def f(x):\n'
                                                  '    -->6:     global x\n'
                                                  '             ^\n'},
 'raise_syntax_error39': {'cause': 'I make an effort below to guess what caused the problem\n'
                                   'but I might guess incorrectly.\n'
                                   '\n'
                                   'You cannot use the Python keyword pass as an attribute.\n'
                                   '\n',
                          'message': 'SyntaxError: invalid syntax\n',
                          'parsing_error_source': '        9: a = A()\n'
                                                  '       10: \n'
                                                  '       11: a.x = 1\n'
                                                  '    -->12: a.pass = 2\n'
                                                  '                ^\n'},
 'raise_syntax_error4': {'cause': 'I make an effort below to guess what caused the problem\n'
                                  'but I might guess incorrectly.\n'
                                  '\n'
                                  "You meant to use Python's 'elif' keyword\n"
                                  "but wrote 'else if' instead\n"
                                  '\n',
                         'message': 'SyntaxError: invalid syntax\n',
                         'parsing_error_source': '       2: \n'
                                                 '       3: if False:\n'
                                                 '       4:     pass\n'
                                                 '    -->5: else if True:\n'
                                                 '                ^\n'},
 'raise_syntax_error40': {'cause': "You are using the continuation character '\\' outside of a "
                                   'string,\n'
                                   'and it is followed by some other character(s).\n'
                                   'I am guessing that you forgot to enclose some content in a '
                                   'string.\n'
                                   '\n',
                          'message': 'SyntaxError: unexpected character after line continuation '
                                     'character\n',
                          'parsing_error_source': '       2: SyntaxError: unexpected character '
                                                  'after line continuation character\n'
                                                  '       3: """\n'
                                                  '       4: \n'
                                                  '    -->5: print(\\t)\n'
                                                  '                   ^\n'},
 'raise_syntax_error41': {'cause': 'You likely called a function with a named argument:\n'
                                   '\n'
                                   '   a_function(invalid=something)\n'
                                   '\n'
                                   "where 'invalid' is not a valid variable name in Python\n"
                                   'either because it starts with a number, or is a string,\n'
                                   'or contains a period, etc.\n'
                                   '\n',
                          'message': "SyntaxError: keyword can't be an expression\n",
                          'parsing_error_source': '        4: """\n'
                                                  '        5: \n'
                                                  '        6: \n'
                                                  "    --> 7: a = dict('key'=1)\n"
                                                  '                   ^\n'},
 'raise_syntax_error42': {'cause': 'You likely used some unicode character that is not allowed\n'
                                   'as part of a variable name in Python.\n'
                                   'This includes many emojis.\n'
                                   '\n',
                          'message': 'SyntaxError: invalid character in identifier\n',
                          'parsing_error_source': '       3: \n'
                                                  '       4: # Robot-face character below\n'
                                                  '       5: \n'
                                                  "    -->6: 🤖 = 'Reeborg'\n"
                                                  '          ^\n'},
 'raise_syntax_error43': {'cause': 'I make an effort below to guess what caused the problem\n'
                                   'but I might guess incorrectly.\n'
                                   '\n'
                                   'I am guessing that you tried to use the Python keyword\n'
                                   'None as an argument in the definition of a function.\n',
                          'message': 'SyntaxError: invalid syntax\n',
                          'parsing_error_source': '       2: """\n'
                                                  '       3: \n'
                                                  '       4: \n'
                                                  '    -->5: def f(None=1):\n'
                                                  '                   ^\n'},
 'raise_syntax_error44': {'cause': 'I make an effort below to guess what caused the problem\n'
                                   'but I might guess incorrectly.\n'
                                   '\n'
                                   'I am guessing that you tried to use the Python keyword\n'
                                   'True as an argument in the definition of a function.\n',
                          'message': 'SyntaxError: invalid syntax\n',
                          'parsing_error_source': '       2: """\n'
                                                  '       3: \n'
                                                  '       4: \n'
                                                  '    -->5: def f(x, True):\n'
                                                  '                      ^\n'},
 'raise_syntax_error45': {'cause': 'I make an effort below to guess what caused the problem\n'
                                   'but I might guess incorrectly.\n'
                                   '\n'
                                   'I am guessing that you tried to use the Python keyword\n'
                                   'None as an argument in the definition of a function.\n',
                          'message': 'SyntaxError: invalid syntax\n',
                          'parsing_error_source': '       2: """\n'
                                                  '       3: \n'
                                                  '       4: \n'
                                                  '    -->5: def f(*None):\n'
                                                  '                    ^\n'},
 'raise_syntax_error46': {'cause': 'I make an effort below to guess what caused the problem\n'
                                   'but I might guess incorrectly.\n'
                                   '\n'
                                   'I am guessing that you tried to use the Python keyword\n'
                                   'None as an argument in the definition of a function.\n',
                          'message': 'SyntaxError: invalid syntax\n',
                          'parsing_error_source': '       2: """\n'
                                                  '       3: \n'
                                                  '       4: \n'
                                                  '    -->5: def f(**None):\n'
                                                  '                     ^\n'},
 'raise_syntax_error47': {'cause': 'You attempted to delete a function call\n'
                                   '    del f(a)\n'
                                   "instead of deleting the function's name\n"
                                   '    del f\n',
                          'message': "SyntaxError: can't delete function call\n",
                          'parsing_error_source': '       2: """\n'
                                                  '       3: \n'
                                                  '       4: \n'
                                                  '    -->5: del f(a)\n'
                                                  '             ^\n'},
 'raise_syntax_error48': {'cause': "You assigned a value to the variable 'p'\n"
                                   'before declaring it as a global variable.\n',
                          'message': "SyntaxError: name 'p' is assigned to before global "
                                     'declaration\n',
                          'parsing_error_source': '        4: \n'
                                                  '        5: def fn():\n'
                                                  '        6:     p = 1\n'
                                                  '    --> 7:     global p\n'
                                                  '              ^\n'},
 'raise_syntax_error49': {'cause': "You used the variable 'r'\n"
                                   'before declaring it as a global variable.\n',
                          'message': "SyntaxError: name 'r' is used prior to global declaration\n",
                          'parsing_error_source': '        4: \n'
                                                  '        5: def fn():\n'
                                                  '        6:     print(r)\n'
                                                  '    --> 7:     global r\n'
                                                  '              ^\n'},
 'raise_syntax_error5': {'cause': 'I make an effort below to guess what caused the problem\n'
                                  'but I might guess incorrectly.\n'
                                  '\n'
                                  "You meant to use Python's 'elif' keyword\n"
                                  "but wrote 'elseif' instead\n"
                                  '\n',
                         'message': 'SyntaxError: invalid syntax\n',
                         'parsing_error_source': '       2: \n'
                                                 '       3: if False:\n'
                                                 '       4:     pass\n'
                                                 '    -->5: elseif True:\n'
                                                 '                    ^\n'},
 'raise_syntax_error50': {'cause': "You used the variable 'q'\n"
                                   'before declaring it as a nonlocal variable.\n',
                          'message': "SyntaxError: name 'q' is used prior to nonlocal "
                                     'declaration\n',
                          'parsing_error_source': '        6: \n'
                                                  '        7:     def g():\n'
                                                  '        8:         print(q)\n'
                                                  '    --> 9:         nonlocal q\n'
                                                  '                  ^\n'},
 'raise_syntax_error51': {'cause': "You assigned a value to the variable 's'\n"
                                   'before declaring it as a nonlocal variable.\n',
                          'message': "SyntaxError: name 's' is assigned to before nonlocal "
                                     'declaration\n',
                          'parsing_error_source': '        6: \n'
                                                  '        7:     def g():\n'
                                                  '        8:         s = 2\n'
                                                  '    --> 9:         nonlocal s\n'
                                                  '                  ^\n'},
 'raise_syntax_error52': {'cause': 'You wrote an expression like\n'
                                   '    {1, 2, 3} = 4\n'
                                   'where <{1, 2, 3}>, on the left-hand side of the equal sign,\n'
                                   "is or includes an actual object of type 'set'\n"
                                   'and is not simply the name of a variable.\n',
                          'message': "SyntaxError: can't assign to literal\n",
                          'parsing_error_source': '        4: \n'
                                                  '        5:  """\n'
                                                  '        6: \n'
                                                  '    --> 7: {1, 2, 3} = 4\n'
                                                  '          ^\n'},
 'raise_syntax_error53': {'cause': 'You wrote an expression like\n'
                                   '    {1 : 2, 2 : 4} = 5\n'
                                   'where <{1 : 2, 2 : 4}>, on the left-hand side of the equal '
                                   'sign,\n'
                                   "is or includes an actual object of type 'dict'\n"
                                   'and is not simply the name of a variable.\n',
                          'message': "SyntaxError: can't assign to literal\n",
                          'parsing_error_source': '        4: \n'
                                                  '        5:  """\n'
                                                  '        6: \n'
                                                  '    --> 7: {1 : 2, 2 : 4} = 5\n'
                                                  '          ^\n'},
 'raise_syntax_error54': {'cause': 'You wrote an expression like\n'
                                   '    ... = variable_name\n'
                                   'where <...>, on the left-hand side of the equal sign,\n'
                                   'is or includes an actual object \n'
                                   'and is not simply the name of a variable.\n',
                          'message': "SyntaxError: can't assign to literal\n",
                          'parsing_error_source': '       1: """Should raise SyntaxError: can\'t '
                                                  'assign to literal\n'
                                                  '       2: or (Python 3.8) cannot assign to '
                                                  'literal"""\n'
                                                  '       3: \n'
                                                  '    -->4: 1 = a = b\n'
                                                  '         ^\n'},
 'raise_syntax_error55': {'cause': 'I make an effort below to guess what caused the problem\n'
                                   'but I might guess incorrectly.\n'
                                   '\n'
                                   'You appear to be using the operator :=, sometimes called\n'
                                   'the walrus operator. This operator requires the use of\n'
                                   'Python 3.8 or newer. You are using version 3.7.\n',
                          'message': 'SyntaxError: invalid syntax\n',
                          'parsing_error_source': '       1: """Should raise SyntaxError: invalid '
                                                  'syntax\n'
                                                  '       2: or (Python 3.8) cannot use named '
                                                  'assignment with True"""\n'
                                                  '       3: \n'
                                                  '    -->4: (True := 1)\n'
                                                  '                ^\n'},
 'raise_syntax_error56': {'cause': 'You wrote an expression that includes some mathematical '
                                   'operations\n'
                                   'on the left-hand side of the equal sign which should be\n'
                                   'only used to assign a value to a variable.',
                          'message': "SyntaxError: can't assign to operator\n",
                          'parsing_error_source': '       1: """Should raise SyntaxError: can\'t '
                                                  'assign to operator\n'
                                                  '       2: or (Python 3.8) cannot assign to '
                                                  'operator"""\n'
                                                  '       3: \n'
                                                  '    -->4: a + 1 = 2\n'
                                                  '         ^\n'},
 'raise_syntax_error57': {'cause': 'I make an effort below to guess what caused the problem\n'
                                   'but I might guess incorrectly.\n'
                                   '\n'
                                   'You are using the backquote character `.\n'
                                   'This was allowed in Python 2 but is no longer allowed.\n'
                                   'Use the function repr(x) instead of `x`.',
                          'message': 'SyntaxError: invalid syntax\n',
                          'parsing_error_source': '       1: """Should raise SyntaxError: invalid '
                                                  'syntax"""\n'
                                                  '       2: \n'
                                                  '    -->3: a = `1`\n'
                                                  '              ^\n'},
 'raise_syntax_error58': {'cause': 'On the left-hand side of an equal sign, you have a\n'
                                   'generator expression instead of the name of a variable.\n',
                          'message': "SyntaxError: can't assign to generator expression\n",
                          'parsing_error_source': '       1: """Should raise SyntaxError: can\'t '
                                                  '[cannot] assign to generator expression"""\n'
                                                  '       2: \n'
                                                  '    -->3: (x for x in x) = 1\n'
                                                  '         ^\n'},
 'raise_syntax_error59': {'cause': 'On the left-hand side of an equal sign, you have a\n'
                                   'conditional expression instead of the name of a variable.\n'
                                   'A conditional expression has the following form:\n'
                                   '\n'
                                   '    variable = object if condition else other_object',
                          'message': "SyntaxError: can't assign to conditional expression\n",
                          'parsing_error_source': '       1: """Should raise SyntaxError: can\'t '
                                                  '[cannot] assign to conditional expression"""\n'
                                                  '       2: \n'
                                                  '    -->3: a if 1 else b = 1\n'
                                                  '         ^\n'},
 'raise_syntax_error6': {'cause': 'I make an effort below to guess what caused the problem\n'
                                  'but I might guess incorrectly.\n'
                                  '\n'
                                  'You tried to define a function or method and did not use the '
                                  'correct syntax.\n'
                                  'The correct syntax is:\n'
                                  '    def name ( optional_arguments ):\n',
                         'message': 'SyntaxError: invalid syntax\n',
                         'parsing_error_source': '       1: """Should raise SyntaxError"""\n'
                                                 '       2: \n'
                                                 '    -->3: def :\n'
                                                 '              ^\n'},
 'raise_syntax_error7': {'cause': 'I make an effort below to guess what caused the problem\n'
                                  'but I might guess incorrectly.\n'
                                  '\n'
                                  'You tried to define a function or method and did not use the '
                                  'correct syntax.\n'
                                  'The correct syntax is:\n'
                                  '    def name ( optional_arguments ):\n',
                         'message': 'SyntaxError: invalid syntax\n',
                         'parsing_error_source': '       1: """Should raise SyntaxError"""\n'
                                                 '       2: \n'
                                                 '    -->3: def name  :\n'
                                                 '                    ^\n'},
 'raise_syntax_error8': {'cause': 'I make an effort below to guess what caused the problem\n'
                                  'but I might guess incorrectly.\n'
                                  '\n'
                                  'You tried to define a function or method and did not use the '
                                  'correct syntax.\n'
                                  'The correct syntax is:\n'
                                  '    def name ( optional_arguments ):\n',
                         'message': 'SyntaxError: invalid syntax\n',
                         'parsing_error_source': '       1: """Should raise SyntaxError"""\n'
                                                 '       2: \n'
                                                 '    -->3: def ( arg )  :\n'
                                                 '              ^\n'},
 'raise_syntax_error9': {'cause': 'You wrote an expression like\n'
                                  '    1 = a\n'
                                  'where <1>, on the left-hand side of the equal sign,\n'
                                  "is or includes an actual object of type 'int'\n"
                                  'and is not simply the name of a variable. Perhaps you meant to '
                                  'write:\n'
                                  '    a = 1\n'
                                  '\n',
                         'message': "SyntaxError: can't assign to literal\n",
                         'parsing_error_source': '       1: """Should raise SyntaxError: can\'t '
                                                 'assign to literal"""\n'
                                                 '       2: \n'
                                                 '    -->3: 1 = a\n'
                                                 '         ^\n'},
 'raise_syntax_error_walrus': {'cause': 'I make an effort below to guess what caused the problem\n'
                                        'but I might guess incorrectly.\n'
                                        '\n'
                                        'You appear to be using the operator :=, sometimes called\n'
                                        'the walrus operator. This operator requires the use of\n'
                                        'Python 3.8 or newer. You are using version 3.7.\n',
                               'message': 'SyntaxError: invalid syntax\n',
                               'parsing_error_source': '       1: """Prior to Python 3.8, this '
                                                       'should raise SyntaxError: invalid '
                                                       'syntax"""\n'
                                                       '       2: \n'
                                                       '    -->3: print(walrus := True)\n'
                                                       '                       ^\n'},
 'raise_tab_error': {'cause': None,
                     'message': 'TabError: inconsistent use of tabs and spaces in indentation\n',
                     'parsing_error_source': '        4: \n'
                                             '        5: def test_tab_error():\n'
                                             '        6:     if True:\n'
                                             '    --> 7: \tpass\n'
                                             '                ^\n'}}
