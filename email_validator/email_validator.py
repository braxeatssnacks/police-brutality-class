# Valid Email Finder

num = int(input()) 
emails = [] # empty list to which append emails

for i in range(num): 
    emails.append(input())

sep = ["@", "."] # separators

def char_split(s, sep):
    """like split() but with more parameters"""
    stack = [s]
    for char in sep:
        pieces = []
        for substr in stack:
            pieces.extend(substr.split(char))
        stack = pieces
    return stack

sectioned = [char_split(i, sep) for i in emails]

def isValidEmail(part):
    """returns boolean if email is valid"""
    if len(part) == 3:
        username = part[0]
        website = part[1]
        ext = part[2]

        spec = ["_", "-"]

        for i in username:
            if i.isalpha() or i.isdigit() and i or spec:
                pass
            else:
                return False
        for i in website:
            if i.isalpha() or i.isdigit():
                pass
            else:
                return False
        if len(ext) <= 3:
            for i in ext:
                if i.isalpha():
                    pass
                else:
                    return False
            pass
        else:
            return False
        return True
    else:
        return False

bools = [isValidEmail(element) for element in sectioned]

valid = []

for i in range(num):
    if bools[i] == True:
        valid.append(emails[i])
        

print(sorted(valid))