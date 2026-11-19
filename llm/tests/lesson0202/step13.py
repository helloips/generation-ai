from llm.src.lesson0202.step13 import truncate_prompt

assert truncate_prompt('qwe', 4) == 'qwe'
assert truncate_prompt('qwe qwe', 4) == 'qwe...'
assert truncate_prompt('qwe qwe', 2) == '...'
assert truncate_prompt('qwe ', 4) == 'qwe '
assert truncate_prompt('qwe ', 3) == 'qwe...'
