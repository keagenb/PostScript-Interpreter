# Keagen Brendle - 11630902
# HW4 Interpreter Part 2

# First pieces to build:
    # 1. operand and dictionary stacks
    # 2. Defining variables (with def) and looking up names
    # 3. The operators that don't involve code arrays. 
        # - All operators EXCEPT repeat loop, if/if else, and calling functions

# Include error checking for all operators

#from psItems import Expr, Value, ArrayValue, FunctionValue
from psItems import Value, ArrayValue, FunctionValue
class Operators:
# NEW # ~-~-||| HW5 - pg. 2 "..scope argument whose value will either be the string "static" or "dynamic"
# Mentioned in lecture: Add an argument: def__init__(self, scoperule):
    def __init__(self, scoperule):
        #stack variables

        # Include evaluated values. In opstack: primitive values, function and variable names, array constants, code-array
        self.opstack = []  #assuming top of the stack is the end of the list
        # Will include the dictionaries where the variable and function definitions are stored
         
        #OLD: self.dictstack = []  #assuming top of the stack is the end of the list
# NEW   # ~-~-||| HW5 - pg. 3 "..where each tuple contains an integer index and a dictionary (static-link-index, dictionary)"
        self.dictstack = [(0,{})]
# NEW   # Mentioned in lecture: self.scope = scoperule
        self.scope = scoperule


        #The builtin operators supported by our interpreter
        self.builtin_operators = {
             # TO-DO in part1
             # include the key value pairs where he keys are the PostScrip opertor names and the values are the function values that implement that operator. 
             # Make sure **not to call the functions** 
             "def":self.psDef,
             "pop":self.pop,
             "push":self.opPush,
             "stack":self.stack,
             "dup":self.dup,
             "copy":self.copy,
             "count":self.count,
             "clear":self.clear,
             "exch":self.exch,
             "roll":self.roll,
             #"dict":self.psDict,
             #"begin":self.begin,
             #"end":self.end,
             "add":self.add,
             "sub":self.sub,
             "mul":self.mul,
             "mod":self.mod,
             "eq":self.eq,
             "lt":self.lt,
             "gt":self.gt,
             "length":self.length,
             "getinterval":self.getinterval,
             "putinterval":self.putinterval,
             "aload":self.aload,
             "astore":self.astore,
             "stack":self.stack,
             "if":self.psIf,
             "ifelse":self.psIfelse,
             "repeat":self.repeat,
             "forall":self.forall
        }
    #-------  Operand Stack Operators --------------
    """
        Helper function. Pops the top value from opstack and returns it.
    """
    # We are assuming the top of the stack is the end of the list, we will pop from there
    def opPop(self):
        if len(self.opstack) > 0:
            return self.opstack.pop(len(self.opstack)-1)
        else:
            return None
        

    """
       Helper function. Pushes the given value to the opstack.
    """
    # Similarly, at end of list but we will push here
    def opPush(self,value):
        self.opstack.append(value)
        
    #------- Dict Stack Operators --------------
    
    """
       Helper function. Pops the top dictionary from dictstack and returns it.
    """   
    def dictPop(self):
        # Pop from dictstack, return it
        return self.dictstack.pop()

    """
       Helper function. Pushes the given dictionary onto the dictstack. 
    """
# NEW - Mentioned in lecture: def dictPush(self,index,d)
    def dictPush(self, index, d):
        # package index and dictionary together as a tuple
        tuple = (index, d)
        self.dictstack.append(tuple)

    """
       Helper function. Adds name:value pair to the top dictionary in the dictstack.
       (Note: If the dictstack is empty, first adds an empty dictionary to the dictstack then adds the name:value to that. 
    """   
    # Keep the '/' in the name constant when you store it in the dictstack
# NEW - Mentioned in lecture: Go to tuple at top of stack, insert name and value into second value of that tuple
    def define(self,name, value):
        # If dictstack contains values
        if len(self.dictstack) > 0:
            if type(name) is str:
                (index, d) = self.dictPop()
                d[name] = value
                self.dictPush(index, d)
        # If dictstack is empty
        else:
            # Create empty dictionary
            dict = {}
            # Add name:value pair
            dict = {name: value}
            self.dictPush(0,dict)
        
    """
       Helper function. Searches the dictstack for a variable or function and returns its value. 
       (Starts searching at the top of the dictstack; if name is not found returns None and prints an error message.
        Make sure to add '/' to the begining of the name.)
    """
    # Should look up the value of a given variable in the dictionary stack
# NEW - Mentioned in lecture: Can write two separate functions as helpers for static and dynamic find
    def lookup(self,name):
        newname = "/"+name
    # if scoping rule is static, 
        if self.scope == 'static':
            return self.staticlookup(newname)
    # search AR's (tuples) top to down
    # elif scoping rule is dynamic, 
        elif self.scope == 'dynamic':
            for (link, dict) in reversed(self.dictstack):
                if newname in dict:
                    result = dict[newname]
                    #print("DYNAMIC")
                    #print(result)
                    return result
            return None

    def staticlookup(self, name):
        holder = self.dictstack
        holder.reverse()
        for iter in holder:
            if name in iter[1].keys():
                return iter[1][name]
        return None
            
    # use static-links for the search - similar to lab 3 question 4b

    def findstaticlink(self, fname):
        size = len(self.dictstack)
        if fname[0] != '/':
            fname = "/" + fname 
        if size == 0:
            return None
        else:
            current = size - 1
        while True:
            for iter in reversed(self.dictstack[current][1]):
                if fname in iter:
                    return current
            if current == 0:
                return None
            else:
                current = self.dictstack[current][0]
                return current

    #------- Arithmetic Operators --------------
    # Will be implemented as zero-argument Python functions that manipulate the operand and dictionary stacks
    """
       Pops 2 values from opstack; checks if they are numerical (int); adds them; then pushes the result back to opstack. 
    """   
    def add(self):
        # Verify more than one value on list
        if len(self.opstack) > 1:
            # Pop 2 values from opstack
            op1 = self.opPop()
            op2 = self.opPop()
            # Verify integers
            if isinstance(op1,int) and isinstance(op2,int):
                # Push result to opstack
                self.opPush(op1 + op2)
            else:
                # Display error, push back to stack if not integer(s)
                print("Error: add - one of the operands is not a number value")
                self.opPush(op2)
                self.opPush(op1)    
        # Display error if no 2 values on opstack         
        else:
            print("Error: add expects 2 operands")
 
    """
       Pop 2 values from opstack; checks if they are numerical (int); subtracts them; and pushes the result back to opstack. 
    """   
    def sub(self):
        # Verify more than one value on list
        if len(self.opstack) > 1:
            # Pop 2 values from opstack
            op1 = self.opPop()
            op2 = self.opPop()
            # Verify integers
            if isinstance(op1,int) and isinstance(op2,int):
                # Push result to opstack
                self.opPush(op2 - op1)
            else:
                # Display error, push back to stack if not integer(s)
                print("Error: sub - one of the operands is not a number value")
                self.opPush(op2)
                self.opPush(op1) 
        # Display error if no 2 values on opstack             
        else:
            print("Error: sub expects 2 operands")

    """
        Pops 2 values from opstack; checks if they are numerical (int); multiplies them; and pushes the result back to opstack. 
    """    
    def mul(self):
        # Verify more than 1 value on list
        if len(self.opstack) > 1:
            # Pop 2 values from opstack
            op1 = self.opPop()
            op2 = self.opPop()
            # Verify integers
            if isinstance(op1,int) and isinstance(op2,int):
                # Push result to opstack
                self.opPush(op1 * op2)
            else:
                print("Error: mul - one of the operands is not a number value")
                self.opPush(op2)
                self.opPush(op1)   
        # Display error if no 2 values on opstack           
        else:
            print("Error: mul expects 2 operands")

    """
        Pops 2 values from stack; checks if they are int values; calculates the remainder of dividing the bottom value by the top one; 
        pushes the result back to opstack.
    """ 
    def mod(self):
        # Verify more than one 1 value on list
        if len(self.opstack) > 1:
            # Pop 2 values from opstack
            op1 = self.opPop()
            op2 = self.opPop()
            # Verify integers
            if isinstance(op1,int) and isinstance(op2,int):
                # Push result to opstack
                self.opPush(op2 % op1)
            else:
                print("Error: mod - one of the operands is not a number value")
                self.opPush(op2)
                self.opPush(op1) 
        # Display error if no 2 values from opstack            
        else:
            print("Error: mod expects 2 operands")
    #---------- Comparison Operators  -----------------
    """
       Pops the top two values from the opstack; pushes "True" is they are equal, otherwise pushes "False"
    """ 
    def eq(self):
        # Verify more than one 1 value on list
        if len(self.opstack) > 1:
            # Pop 2 values from opstack
            op1 = self.opPop()
            op2 = self.opPop()
            # Verify integers
            if op1 == op2:
                # Pushes True if they are equal
                self.opPush(True)
            else:
                # Otherwise pushes false
                self.opPush(False)  
        # Display error if no 2 values on opstack            
        else:
            print("Error: eq expects 2 operands")

    """
       Pops the top two values from the opstack; pushes "True" if the bottom value is less than the top value, otherwise pushes "False"
    """ 
    def lt(self):
        # Verify more than one 1 value on list
        if len(self.opstack) > 1:
            # Pop 2 values from opstack
            op1 = self.opPop()
            op2 = self.opPop()
            # Verify integers
            if op1 > op2:
                # Pushes True if bottom value is less than top value
                self.opPush(True)
            else:
                # Otherwise pushes False
                self.opPush(False)  
        # Display error if no 2 values on opstack            
        else:
            print("Error: lt expects 2 operands")

    """
       Pops the top two values from the opstack; pushes "True" if the bottom value is greater than the top value, otherwise pushes "False"
    """ 
    def gt(self):
        # Verify more than one 1 value on list
        if len(self.opstack) > 1:
            # Pop 2 values from opstack
            op1 = self.opPop()
            op2 = self.opPop()
            # Verify integers
            if op1 < op2:
                # Pushes True if bottom value is greater than top value
                self.opPush(True)
            else:
                # Otherwise pushes False
                self.opPush(False)    
        # Display error if no 2 values on opstack          
        else:
            print("Error: lt expects 2 operands")

    # ------- Array Operators --------------
    """ 
       Pops an array value from the operand opstack and calculates the length of it. Pushes the length back onto the opstack.
       The `length` method should support ArrayValue values.
    """
    def length(self):
        # Check for values on opstack 
        if len(self.opstack) > 0:
            # Pops array value from the operand opstack 
            array = self.opPop()
            # Supports ArrayValue values
            if isinstance(array, ArrayValue):
                # Calculates length and pushes it back onto the stack
                self.opPush(len(array.value))

    """ 
        Pops the `count` (int), an (zero-based) start `index`, and an array constant (ArrayValue) from the operand stack.  
        Pushes the slice of the array of length `count` starting at `index` onto the opstack.(i.e., from `index` to `index`+`count`) 
        If the end index of the slice goes beyond the array length, will give an error. 
    """
    # The operand stack should have 3 values. 
    # Top 2 values on the stack are ints (count and index) and third is ArrayValue
    def getinterval(self):
        # Pops 'count' (int)
        count = self.opPop()
        # Pops zero-based start 'index'
        index = self.opPop()
        # Temp array constant
        temp = self.opPop()
        l = []
        if isinstance(temp, ArrayValue):
            # Get slice
            for iter in range(0, count, 1):
                if (iter + index) < len(temp.value):
                    l.insert(iter, temp.value[iter + index])
                    iter+= 1
            #  Pushes the slice of the array of length `count` starting at `index` onto the opstack
            self.opPush(ArrayValue(l))

    """ 
        Pops an array constant (ArrayValue), start `index` (int), and another array constant (ArrayValue) from the operand stack.  
        Replaces the slice in the bottom ArrayValue starting at `index` with the top ArrayValue (the one we popped first). 
        The result is not pushed onto the stack.
        The index is 0-based. If the end index of the slice goes beyond the array length, will give an error. 
    """
    def putinterval(self):
        # Verify that three operands were entered
        if len(self.opstack) > 2:
            # Pops an array constant
            array2 = self.opPop()
            # Pops a start 'index'
            index = self.opPop()
            # Pops an array constant
            array1 = self.opPop()
            # Get the size/length of the array constant
            length = len(array2.value)
            # Verify that what was popped is in fact an array constant, an integer, and another array constant
            if (isinstance(array1, ArrayValue) and isinstance(array2, ArrayValue) and isinstance(index, int)):
                if index < len(array1.value):
                    # Replace slice in bottom array starting at index with top array
                    for iter in range(index, index+length):
                        holder = array2.value.pop(0)
                        array1.value[iter] = holder
        # Display error if not 3 operands                 
        else:
            print("Error: putinterval excpects 3 operands ")
            

    """ 
        Pops an array constant (ArrayValue) from the operand stack.  
        Pushes all values in the array constant to the opstack in order (the first value in the array should be pushed first). 
        Pushes the orginal array value back on to the stack. 
    """
    def aload(self):
        # Verify non empty stack
        if len(self.opstack) > 0:
            # Pops an array constant (ArrayValue) from the operand stack.
            temp = self.opPop()
            # Pushes values in array constant back to opstack in order
            for value in temp.value:
                self.opPush(value)
            # Push original array back onto stack
            self.opPush(temp)
        # Display error if empty stack
        else:
            print("Error: aload - ")
        
    """ 
        Pops an array constant (ArrayValue) from the operand stack.  
        Pops as many elements as the length of the array from the operand stack and stores them in the array constant. 
        The value which was on the top of the opstack will be the last element in the array. 
        Pushes the array value back onto the operand stack. 
    """
    def astore(self):
        # Verify non empty stack
        if len(self.opstack) > 0:
            # Pops array constant from opstack
            temp = self.opPop()
            # Get length of array constant
            length = len(temp.value)
            temp.value.clear()
            # Pops as many elements as the length of the array from the operand stack and stores them in the array constant.
            if isinstance(temp, ArrayValue):
                for iter in range(length):
                    temp.value.insert(iter, self.opPop())
                temp.value.reverse()
                # Pushes array back onto operand stack
                self.opPush(temp)
        # # Display error if empty stack
        else:
            print("Error: astore - ")

    #------- Stack Manipulation and Print Operators --------------

    """
       This function implements the Postscript "pop operator". Calls self.opPop() to pop the top value from the opstack and discards the value. 
    """
    def pop (self):
        # Calls self.opPop() to pop the top value from the opstack
        return self.opPop()

    """
       Prints the opstack. The end of the list is the top of the stack. 
    """
# NEW - Pg. 4
    def stack(self):
        # Print a line containing "===**opstack**===" to mark the beginning of the opstack content.
        print("===**opstack**===")
        # Print the operand stack one value per line; print the top-of-stack element first.
        # Verify non empty stack list
        if len(self.opstack) > 0:
            # Iterate through opstack
            for iter in self.opstack:
                # Print each item from list
                print(iter)
        # Display error if empty list
        else:
            print("Error: stack - No values to print")
        # Print a line containing "===**dictstack**===" to separate the stack from the dictionary stack.
        print("===**dictstack**===")
        # Print the contents of the dictionary stack,    beginning with the top-of-stack dictionary one name and value per line..
        size = (len(self.dictstack)-1)
        for iter in self.dictstack:
            
            print("----", size, "----", iter[0], "----")
            size -= 1
            for val in iter[1]:
                print(val, "\t", iter[1][val])
            
        # Print a line containing "=================" to separate the dictionary stack from any subsequent output.
        print("=================")

    """
       Copies the top element in opstack.
    """
    def dup(self):
        # Verify that there are values on opstack
        if len(self.opstack) > 0:
            # Pop value from stack and store/hold it
            holder = self.opPop()
            # Push it twice, duplicating it
            self.opPush(holder)
            self.opPush(holder)
        # If no values to duplicate then display error
        else:
            print("Error: dup - No values to copy")

    """
       Pops an integer count from opstack, copies count number of values in the opstack. 
    """
    def copy(self):
        # Hold a value popped from stack
        holder = self.opPop()
        # Temporary array to store copy values
        temp = []
        t1 = 0
        t2 = 0
        # Copies count number of values from opstack to temporary array
        for iter in range(holder):
            popped = self.opPop()
            temp.append(popped)
            t1 += 1
            t2 += 1
        # Return opstack back to normal (starting with -1, end of list AKA top of stack)
        for iter2 in range(holder):
            self.opPush(temp[t1-1])
            t1 -= 1
        # Now place newly copied values from temp array into opstack
        for iter3 in range(holder):
            self.opPush(temp[t2-1])
            t2 -= 1

    """
        Counts the number of elements in the opstack and pushes the count onto the top of the opstack.
    """
    def count(self):
        # Set up count variable
        count = 0
        # Iterate though items in opstack
        for iter in self.opstack:
            # Increment count for each item
            count += 1
        # Push count to top of opstack
        self.opPush(count)

    """
       Clears the opstack.
    """
    def clear(self):
        # Verify that there are values on the opstack
        if len(self.opstack) > 0:
            # Clears the opstack
            self.opstack.clear()
        # If no values to exchange then display error
        else:
            print("Error: clear - No values to exchange")

    """
       swaps the top two elements in opstack
    """
    def exch(self):
        # Verify that there are values on the opstack
        if len(self.opstack) > 0:
            # Pop two elements
            op1 = self.opPop()
            op2 = self.opPop()
            # Push them back in opposite order of popping
            self.opPush(op1)
            self.opPush(op2)
        # If no values to exchange then display error
        else:
            print("Error: exch - No values to exchange")

    """
        Implements roll operator.
        Pops two integer values (m, n) from opstack; 
        Rolls the top m values in opstack n times (if n is positive roll clockwise, otherwise roll counter-clockwise)
    """

    def roll(self):
       # Pops two integers m and n
       m = self.opPop()
       n = self.opPop()
       temp = []
       for i in range(n):
           temp.insert(i, self.opPop())
       temp.reverse()
       for i in range(abs(m)):
           if m > 0:
               temp = temp[-1:] + temp[:-1]
           else:
               temp = temp[1:] + temp[:1]
       for i in range(n):
           self.opPush(temp[i])

    """
       Pops an integer from the opstack (size argument) and pushes an  empty dictionary onto the opstack.
    """
    #def psDict(self):
        # Pushes an integer from the opstack
        #self.opPop()
        # Then pushes an empty dictionary onto the opstack
        #self.opPush({})

    """
       Pops the dictionary at the top of the opstack; pushes it to the dictstack.
    """
    # Begin and end operators are a little different in that they manipulate the dictionary stack in 
    # addition to (or instead of) the operand stack. Remember that the dict operator (i.e., psDict
    # function)affects only the operand stack
    #def begin(self):
        # Holder for value popped from top of stack
        #holder = self.opPop()
        # Verify that it is a dictionary
        #if type(holder) is dict:
            # Push it to the dictionary stack
            #self.dictPush(holder)

    """
       Removes the top dictionary from dictstack.
    """
    #def end(self):
        # Pop from top of dictstack
        #self.dictPop()
        
    """
       Pops a name and a value from opstack, adds the name:value pair to the top dictionary by calling define.  
    """
    # Takes 2 from opstack: a string and a value. Strings start with '/' and represent PS variables. 
    # Second value from the top of the stack is a string starting with '/'
    def psDef(self):
        # Verify that there are value on the opstack
        if len(self.opstack) > 0:
            # Takes 2 from opstack: a string and a value
            value = self.opPop()
            string = self.opPop()
            self.define(string, value)
        # Display error if no values on opstack
        else:
            print("Error: psDef - There are no elements on the opstack")


    # ------- if/ifelse Operators --------------
    """
       Implements if operator. 
       Pops the `ifbody` and the `condition` from opstack. 
       If the condition is True, evaluates the `ifbody`.  
    """
# NEW - Mentioned in lecture, when apply is called we need to pass in the static-link-index as well
    def psIf(self):
        #pops the ifbody
        ifbody = self.opPop()
        # and pops condition from stack
        condition = self.opPop()
        # if condition is True
        if isinstance(condition, bool) and condition == True:
            # evaluates the ifbody
            ifbody.apply(self, (len(self.dictstack)-1))
        # TO-DO in part2

    """
       Implements ifelse operator. 
       Pops the `elsebody`, `ifbody`, and the condition from opstack. 
       If the condition is True, evaluate `ifbody`, otherwise evaluate `elsebody`. 
    """
    def psIfelse(self):
        # maybe add a check for opstack > 0/3
        # pops the elsebody
        elsebody = self.opPop()
        # pops the ifbody
        ifbody = self.opPop()
        # and pops condition from opstack
        condition = self.opPop()
        # if condition is True
        if isinstance(condition, bool) and condition == True:
            # then evaluate ifbody
            #ifbody = iter(ifbody)
            ifbody.apply(self, (len(self.dictstack)-1))
        # otherwise
        else:
            # evaluate elsebody
            elsebody.apply(self, (len(self.dictstack)-1))
        # TO-DO in part2


    #------- Loop Operators --------------
    """
       Implements repeat operator.   
       Pops the `loop_body` (FunctionValue) and loop `count` (int) arguments from opstack; 
       Evaluates (applies) the `loopbody` `count` times. 
       Will be completed in part-2. 
    """  
    def repeat(self):
        # pops the loop_body (FunctionValue)
        loop_body = self.opPop()
        # and pops loop count (int) from opstack
        count = self.opPop()
        # verify that count is an integer and loop body is a FunctionValue
        if isinstance(count, int) and isinstance(loop_body, FunctionValue):
            #evaluates loop_body 'count' times
            for iter in range(count):
                    loop_body.apply(self, (len(self.dictstack)-1))
        #TO-DO in part2
        
    """
       Implements forall operator.   
       Pops a `codearray` (FunctionValue) and an `array` (ArrayValue) from opstack; 
       Evaluates (applies) the `codearray` on every value in the `array`.  
       Will be completed in part-2. 
    """ 
    def forall(self):
        # pops a codearray (FunctionValue)
        codearray = self.opPop()
        # and pops an array (ArrayValue) from the opstack
        array = self.opPop()
        if isinstance(codearray, FunctionValue) and isinstance(array, ArrayValue):
        # evaluates the codearray on every value in the array
            for item in array.value:
                self.opPush(item)
# NEW - Mentioned in lecture: Pass index for apply as length of dictionarystack (len(self.dictstack)-1)
# Do this for if, ifelse, and repeat as well?
                codearray.apply(self,(len(self.dictstack)-1))
        # TO-DO in part2

    #--- used in the setup of unittests 
    def clearBoth(self):
        self.opstack[:] = []
        self.dictstack[:] = []

    def cleanTop(self):
        if len(self.opstack)>1:
            if self.opstack[-1] is None:
                self.opstack.pop()
