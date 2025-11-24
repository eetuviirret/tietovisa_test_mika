import textwrap

story ='''Welcome to Private jet!
The game whare you win money by answering aviation related questions! 
Are you a true plane enthusiast? Can you name every airport at the drop of a hat? 
This is the game for you!

On each round you will be asked one question and you have to choose an answer from four options. 
There will be 15 rounds.
If you have trouble answering the question, you may use your lifelines; 50/50, Ask the Audience or Call a Friend.

50/50 will eliminate 2 of the wrong answers. 
Ask the audience will give percentage of people that think that the option is correct. 
Call a Friend hear what your friend thinks is the answer. 
Remember, you may only use one(1) lifeline per question!
If you persist until the end the grand prize of 1 000 000€ awaits you!
Ready to play? Good luck!'''

# Set column width to 80 characters
wrapper = textwrap.TextWrapper(width=400, break_long_words=False, replace_whitespace=False)
# Wrap text
word_list = wrapper.wrap(text=story)


def getStory():
    return word_list