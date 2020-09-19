
def function_name(arg):
    print('in fn')
    if arg == 1:
        return 'sdlk'

    print('made it past the if')
    return 'Made it to the end'


response = function_name(1)
print(response)
