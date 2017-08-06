#You have a string s that consists of English letters, punctuation marks, whitespace characters, and brackets.
#It is guaranteed that the parentheses in s form a regular bracket sequence.
#Your task is to reverse the strings contained in each pair of matching parentheses, starting from the innermost pair. 
#The results string should not contain any parentheses.
#Example:
#For string s = "a(bc)de", the output should be
#reverseParentheses(s) = "acbde".

def reverseParentheses(s):
    npars = len([c for c in s if c == "("])
    newstr = ""
    addstr = ""
    pcount = 0
    stop = 0
    
    if npars == 0:
        return s
    else:    
        for c in s:
            if pcount == npars and stop == 0:
                if not c == ")":
                    addstr = c + addstr
                else:
                    newstr = newstr + addstr
                    stop = 1
                    
            elif pcount < (npars -1) and stop == 0:
                newstr = newstr + c
                if c == "(":
                    pcount +=1
        
            elif pcount == (npars -1) and stop == 0:
                if c == "(":
                    pcount += 1
                else:
                    newstr = newstr + c
                    
            elif pcount == npars and stop == 1:
                newstr = newstr + c
    
    return reverseParentheses(newstr)

