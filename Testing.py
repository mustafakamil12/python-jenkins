# For Jenkins Testing Purposes, We will use Pytest in this case. 

def math_test (n): 
 return n+1

def test_answer ():
 assert math_test(3) == 5
