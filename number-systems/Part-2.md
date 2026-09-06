Do not use any tools or programming to solve these problems. Work it out yourself by hand, and fill in the answers.

Do not convert any binary numbers to decimal when solving a question unless the question explicitly tells you to.

The goal of these exercises is for you to gain an intuition for binary numbers. Using tools to solve the problems defeats the point.

The answers to these questions will require a bit of explanation, not just a simple answer.

Q16: How can you test if a binary number is a power of two (e.g. 1, 2, 4, 8, 16, ...)?
Answer: test whether only the most significant bit is 1

Q17: If reading the byte 0x21 as an ASCII character, what character would it mean?
Answer: `!` according to the ascii table

Q18: If reading the byte 0x21 as a greyscale colour, as described in "Approaches for Representing Colors and Images", what colour would it mean?
Answer: dark grey because `0x00` is black and `0xFF` is white

Q19: If reading the bytes 0xAA00FF as a sequence of three one-byte decimal numbers, what decimal numbers would they be?
Answer: 170,0,255 because `0xAA = 10*16+10` and `0x00 = 0*16+0` and `0xFF = 15*16+15`

Q20: If reading the bytes 0xAA00FF as an RGB colour, as described in "Approaches for Representing Colors and Images", what colour would it mean?
Answer: purple because of mixing red and blue in the 170:255 or 34:51 ratio
