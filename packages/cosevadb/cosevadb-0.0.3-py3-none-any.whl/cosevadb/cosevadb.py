""" Module to execute SQL queries on a csv file
Usage::
    >>> import csv
    >>> result=csv.query("select name from input.csv,heads.csv where native='usa'")
"""
alphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
number=['0','1','2','3','4','5','6','7','8','9']
dot=['.']
operator=['%','/','*','+','-','<','>','!','=','&','|']
a_operator=['%','/','*','+','-']
gt_lt=['<','>']
logical=['&','|']
quote=['"',"'"]
underscore=['_']

rule=[
    ['0',['s','S'],"1",'',''],
    ['1',['e','E'],"2",'',''],
    ['2',['l','L'],"3",'',''],
    ['3',['e','E'],"4",'',''],
    ['4',['c','C'],"5",'',''],
    ['5',['t','T'],"6",'',''],
    ['6',[' '],"7",'',''],
    ['7',['*'],"8",'push',''],
    ['7',alphabet+underscore,"15",'push',''],
    ['8',[' '],"9",'','req'],
    ['9',['f','F'],"10",'',''],
    ['10',['r','R'],"11",'',''],
    ['11',['o','O'],"12",'',''],
    ['12',['m','M'],"13",'',''],
    ['13',[' '],"14",'',''],
    ['14',alphabet+underscore,"17",'push',''],
    ['15',[' '],"9",'','req'],
    ['15',[','],"16",'','req'],
    ['15',alphabet+underscore+number,"15",'push',''],
    #[16,[' '],"state=9"],
    ['16',alphabet+underscore,"15",'push',''],
    #[17,[' '],"state=19"],
    ['17',[','],"18",'','csv'],
    #[17,['#'],"state=end"],
    ['17',['_','.','/','\\',':']+alphabet+number,"17",'push',''],
    #[18,[' '],"state=19"],
    #[18,['#'],"state=end"],
    ['18',alphabet+underscore,"18.1",'push',''],
    ['18.1',['_','.','/','\\',':']+alphabet+number,"18.1",'push',''],
    ['18.1',['#'],'end','','head'],
    ['18.1',[' '],"19",'','head'],
    ['19',['w','W'],"20",'',''],
    ['20',['h','H'],"21",'',''],
    ['21',['e','E'],"22",'',''],
    ['22',['r','R'],"23",'',''],
    ['23',['e','E'],"24",'',''],
    ['24',[' '],"25",'',''],
    ['25',['#'],'end','','exp'],
    ['25','any',"25",'push',''] #important to have 'any' after specific char rules of same state
    ]
    
exp_rules=[
        ["0","(","1",'','ob'],
        ["1","(","1",'','ob'],
        ["1",alphabet+underscore,"2",'varpush',''],
        ["1",number,"3",'operandpush',''],
        ["1",quote,"5",'',''],
        ["2",alphabet+underscore,"2",'operandpush',''],
        ["2",a_operator,"1",'operatorpush','opandop'],
        ["2",gt_lt,"4",'operatorpush','operand'],
        ["2",'!',"9",'operatorpush','operand'],
        ["2",logical,"1",'operatorpush','opandop'],
        ["2",'=',"1",'operatorpush','opandop'],
        ["2",')',"2",'','cb'],
        ["2",'#',"",'','end'],
        ["3",number,"3",'operandpush',''],
        ["3",dot,"7",'operandpush',''],
        ["3",')',"3",'','cb'],
        ["3",'#',"",'','end'],
        ["3",'other',"2",'pass','operand'],
        ["4",'=',"1",'operatorpush','opandop'],
        ["4",'other',"1",'pass','operator'],
        ["5",quote,"6",'','operand'],
        ["5",'any',"5",'operandpush',''],
        ["6",'=',"1",'operatorpush','operator'],
        ["6",'!',"8",'operatorpush',''],
        ["6",')',"6",'','cb'],
        ["6",logical,"1",'operatorpush','opandop'],
        ["6",'#',"",'','end'],
        ["7",number,"7",'operandpush',''],
        ["7",'other',"2",'pass','operand'],
        ["8",'=',"1",'operatorpush','operand'],
        ["9",'=',"1",'operatorpush','operator'],
    ]
class sqlerror(Exception):
    sqlcode=0
    message=''
    def __init__(self,code,msg):
        self.sqlcode = code
        self.message = msg

class node:
    parent=None
    
    left=None
    operator=None
    right=None
    result=None
    
    isvar=None
    
    def __init__(self,a):
        self.parent=a

def par(exp):
    ops=['%','/','*','+','-','<','>','!','=','&','|'] #in the order of precedence
    # Replace all the negative operands into (0-operand)
    exp_length=len(exp)
    for n in range(0,exp_length):
        if (exp[n]=='-') and ((n==0) or (exp[n-1]=='(')):
            exp=exp[:n]+'(0'+exp[n:]
            #print(exp)
            n+=3 #Compensating above added 2 chars + 1
            f=False
            br=0
            for m in range(n,len(exp)):
                #print("m start")
                if (exp[m]=='('):
                    br+=1
                    #print("Adding br "+str(br)+exp[m])
                if (exp[m]==')'):
                    if br>0:
                        br-=1
                        #print(br)
                    if br==0:
                        #print("Adding here")
                        exp=exp[:m]+')'+exp[m:]
                        #print(exp)
                        f=True
                        break  
                if (exp[m] in operator) and (br==0):
                    #print("Adding there"+exp[m])
                    exp=exp[:m]+')'+exp[m:]
                    #print(exp)
                    f=True
                    break
            if not f:
                raise sqlerror(-14,"Incomplete condition in where clause")
    #print(exp)
    for op in ops:
        #print('Operator '+op)
        i=0
        while i<len(exp):
            ####print(exp)
            if exp[i]==op:
                #Check if ! operator has = next
                if (exp[i]=='!') and (exp[i+1]!='='):
                    raise sqlerror(-8,"Operator ! must be followed by =")
                #Loop back for open bracket
                if (exp[i]=='=') and (exp[i-1] in ['<','>','!']): #Skip 2 char operators
                    #j=i-2
                    break
                else:
                    j=i-1
                    
                bracket=0
                while j>=0:
                    #print("on : "+exp[j])
                    if bracket==0:
                        if exp[j] in ops:
                            exp=exp[:j+1]+'('+exp[j+1:]
                            i+=1
                            break
                        elif exp[j]==')':
                            bracket+=1
                            #print('bracket added '+str(bracket))
                        elif j==0:
                            exp='('+exp
                            i+=1
                            break
                    else:
                        if exp[j]=='(':
                            bracket-=1
                            #print('bracket subtracted '+str(bracket))
                            if bracket==0:
                                #print('Setting open bracket on :'+str(bracket));
                                exp=exp[:j]+'('+exp[j:]
                                i+=1
                                break
                        elif exp[j]==')':
                            bracket+=1
                            #print('bracket added '+str(bracket))
                        if (j==0)&(bracket!=0):
                            raise sqlerror(-9,"Unbalanced paranthesis on LHS of operator "+op)
                    #print(exp)
                    j-=1
                #Loop forward for close bracket
                ####print("Looped back "+exp)
                j=i+1 #To compensate the additional open bracket added
                bracket=0
                l=len(exp)
                ####print(j)
                if (exp[j]=='=' ) and (exp[j-1] in ['>','<','!']): #Skip 2 char operators
                    j+=1
                while j<l:
                    if bracket==0:
                        if exp[j] in ops:
                            exp=exp[:j]+')'+exp[j:]
                            break
                        elif exp[j]=='(':
                            bracket+=1
                        elif j==(len(exp)-1):
                            exp=exp+')'
                            
                    else:
                        if exp[j]==')':
                            bracket-=1
                            if bracket==0:
                                exp=exp[:j]+')'+exp[j:]
                                break
                        elif exp[j]=='(':
                            bracket+=1
                        if (j==(len(exp)-1)) & (bracket!=0):
                            raise sqlerror(-10,"Unbalanced paranthesis on RHS of operator "+op)
                    j+=1
                    #print(exp)
            i+=1
    #print(exp)
    return exp



def calculate(a,op,b):
    ops=['%','/','*','+','-','<','<=','>','>=','!=','=','&','|']
    if op not in ops:
        raise sqlerror(-4,"Unsupported operator "+str(op)+" in where clause")
    #Arithmatic and comparison operations
    if op in ['%','/','*','+','-','<','<=','>','>=']:
        #Arithmatic operations allowed only for integer and floats
        #Always returns float
        try:
            a=float(a)
            b=float(b)
        except ValueError:
            raise sqlerror(-5,"Non numeric operand with arithmatic operator "+str(op))
        if op=='%':
            return a%b
        if op=='/':
            return a/b
        if op=='*':
            return a*b
        if op=='+':
            return a+b
        if op=='-':
            return a-b
        if op=='>':
            return a>b
        if op=='>=':
            return a>=b
        if op=='<':
            return a<b
        if op=='<=':
            return a<=b
    #Equality check operators
    if op in ['!=','=']:
        #Arithmatic operations allowed only for integer and floats
        #Always returns float
        try:
            a_temp=float(a)
            b_temp=float(b) #To conserve initial form of a when there is error in b
            a=a_temp
            b=b_temp
        except ValueError:
            a=str(a)
            b=str(b)
        #if ((a[0] not in ["'",'"']) or (a[-1] not in ["'",'"']) or (b[0] not in ["'",'"']) or (b[-1] not in ["'",'"'])):
        #    return "String type error"

        if op=='!=':
            return a!=b
        if op=='=':
            ####print("Inside calc "+a+b)
            return a==b
    #Logical operators
    if op in ['&','|']:
        #Convert a
        if str(a)=='True':
            a=True
        elif str(a)=='False':
            a=False
        else:
            raise sqlerror(-6,"Non boolean operand(LHS) with logical operator "+str(op))
        #Convert a
        if str(b)=='True':
            b=True
        elif str(b)=='False':
            b=False
        else:
            raise sqlerror(-7,"Non boolean operand(RHS) with logical operator "+str(op))
        if op=='&':
            return a and b
        if op=='|':
            return a or b
   

def tree1(exp):
    
    __current_node = None

    
    char_index=0
    state="0"
    isvar=False
    operator_temp=''
    operand_temp=''
    found=False
    passthis=False
    while char_index<len(exp): #For every character in the expression
        ##print(exp[char_index])
        for rule in exp_rules: #Search through all the rules
            if ((state==rule[0]) and ((rule[1] in ['any','other']) or (exp[char_index] in rule[1]))): #if the m
                found=True
                ##print(rule)
                state=rule[2]
                if rule[3]=='operatorpush':
                    ##print("Pushing operator")
                    operator_temp+=exp[char_index]
                if rule[3]=='operandpush':
                    ##print("Pushing operand")
                    operand_temp+=exp[char_index]
                if rule[3]=='varpush':
                    ##print("Var push")
                    isvar=True
                    operand_temp+=exp[char_index]
                if rule[3]=='pass':
                    ##print("Passing this")
                    passthis=True
                    
                if rule[4]=='ob':
                    if __current_node==None: #Check if this is the first node
                        __current_node=node(None) #If yes create one and make this current node
                        ##print('creating new node')
                    else: 
                        if (__current_node.left==None): #Check if already an element present in left
                            __current_node.left = node(__current_node) #Create a new node and assign left
                            __current_node = __current_node.left #And make this current node
                            ##print("Creating a node left and making it current")
                        elif (__current_node.right==None):
                            #Assign operator
                            if operator_temp!='':
                                ##print("Assigning operator")
                                __current_node.operator=operator_temp
                                operator_temp=''
                            __current_node.right = node(__current_node) #Create a new node and assign right
                            __current_node = __current_node.right #And make this current node
                            ##print("Creating a node on right and making it current")
                if rule[4]=='cb':
                    if operand_temp!='':
                        ##print("Adding to right")
                        __current_node.right=operand_temp
                        if isvar:
                            __current_node.isvar="right"
                            ##print("This is a right variable")
                            isvar=None
                    if __current_node.parent!=None:
                        ##print("Moving to parent")
                        __current_node=__current_node.parent
                    operand_temp=''
                if rule[4]=='operator':
                    ##print("Assigning operator")
                    __current_node.operator=operator_temp
                    operator_temp=''
                if rule[4]=='operand':
                    if operand_temp!='':
                        if __current_node.left==None:
                            ##print("Assigning operand on left")
                            __current_node.left=operand_temp
                            if isvar:
                                __current_node.isvar="left"
                                ##print("This is a left variable")
                                isvar=None
                            operand_temp=''
                        else:
                            ##print("Assigning operand on right")
                            __current_node.right=operand_temp
                            if isvar:
                                __current_node.isvar="right"
                                ###print("This is a right variable")
                                isvar=None
                            operand_temp=''
                if rule[4]=='opandop':
                    if operator_temp!='':
                        ##print("Assigning operator")
                        __current_node.operator=operator_temp
                        operator_temp=''
                    if operand_temp!='':
                        if __current_node.left==None:
                            ##print("Assigning operand on left")
                            __current_node.left=operand_temp
                            if isvar:
                                __current_node.isvar="left"
                                ##print("this is a left variable")
                                isvar=None
                        else:
                            ##print("Assigning operand on right")
                            __current_node.right=operand_temp
                            if isvar:
                                __current_node.isvar="right"
                                ##print("this is a right variable")
                                isvar=None
                        operand_temp=''
                    
                break
        if not found:
            raise sqlerror(-3,"Unexpected character "+exp[char_index]+" on where clause")
        else:
            found=False
        if passthis:
            ##print("Actually Passing this")
            passthis=False
        else:
            char_index+=1
    return __current_node


#Original function
def tree(exp):
    #exp="(((name/4)>=b)+a)"
    __current_node = None
    alphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    number=['0','1','2','3','4','5','6','7','8','9']
    dot=['.']
    operator=['%','/','*','+','-','<','>','!','=','&','|']
    quote=['"',"'"]

    temp=''

    for char in exp:
        ###print(char)
        if char=='(': #When the char is (
            if __current_node==None: #Check if this is the first node
                __current_node=node(None) #If yes create one and make this current node
                ###print('creating new node')
            else: 
                if (__current_node.left_node==None) and (__current_node.left==None): #Check if already an element present in left
                    __current_node.left_node = node(__current_node) #Create a new node and assign left
                    __current_node = __current_node.left_node #And make this current node
                    ###print("Creating a node left")
                elif (__current_node.right_node==None) and (__current_node.right==None):
                    __current_node.right_node = node(__current_node) #Create a new node and assign right
                    __current_node = __current_node.right_node #And make this current node
                    ###print("Creating a node on right")
        if char in quote:
            pass #Do not add quote as part of the string
        if char in alphabet+number:
            temp+=char
            ###print("Pushing to temp")
        if char==')':
            if temp!='':
                ###print("Adding "+temp+" to right and moving to parent")
                __current_node.right=temp
                if __current_node.parent!=None:
                    __current_node=__current_node.parent
                temp=''
            else:
                if __current_node.parent!=None:
                    ###print("moving to parent")
                    __current_node=__current_node.parent
        if char in operator:
            if temp!='':
                ###print("Adding "+temp+" to left")
                __current_node.left=temp
                if __current_node.operator==None:
                    __current_node.operator=char
                    ###print("adding operator")
                else:
                    ###print("Appending operator")
                    __current_node.operator+=char
                temp=''
            else:
                if __current_node.operator==None:
                    ###print("Adding operator")
                    __current_node.operator=char
                else:
                    ###print("Appending operator")
                    __current_node.operator+=char
    return __current_node
    #display(__current_node)

def evalthis(__current_node,title,value):
    if __current_node==None: #No expression present in the query
        return True;
    if isinstance(__current_node.left,node):
        evalthis(__current_node.left,title,value)
        a=__current_node.left.result
        #a=__current_node.left
    else:
        a=__current_node.left
        ####print(__current_node.left)
    op=__current_node.operator
    #Check the extra paranthesis
    if (__current_node.operator==None) and (__current_node.right==None):
        __current_node.result=__current_node.left.result
        return __current_node.result
    else:
        ####print(__current_node.operator)
        if isinstance(__current_node.right,node):
            evalthis(__current_node.right,title,value)
            b=__current_node.right.result
            #b=__current_node.right
        else:
            ####print(__current_node.right)
            b=__current_node.right
    #Substitute values in variables before calculating
    ####print("a is "+a)
    ####print(title)
    ####print(value)
    #if str(a)[0] not in ['"',"'"]: #If this is not a string value
    if __current_node.isvar=="left":
        if str(a) in title:
            ####print("inside")
            __index=title.index(str(a))
            if (__index>=0) and (__index<len(value)):
                a=str(value[__index])
            else:
                raise sqlerror(-12,"Value for variable "+str(a)+" is missing in atleast one row")
        else:
            raise sqlerror(-11,"No field "+str(a)+" found in header")
    #if str(b)[0] not in ['"',"'"]: #If this is not a string value
    #if ((__current_node.isvar=="right") and (str(b) in title)):
        #b=str(value[title.index(str(b))])
    if __current_node.isvar=="right":
        if str(b) in title:
            ####print("inside")
            __index=title.index(str(b))
            if (__index>=0) and (__index<len(value)):
                b=str(value[__index])
            else:
                raise sqlerror(-12,"Value for variable "+str(b)+" is missing in atleast one row")
        else:
            raise sqlerror(-11,"No field "+str(b)+" found in header")
    
    __current_node.result=calculate(a,op,b)
    ####print(a+b)
    ####print(__current_node.result)
    return __current_node.result

def __evalthis(exp,title,value):
    """ Private function that evaluates given expression and returns true or false
        if expression is blank returns true
    """
    if exp=="":
        return True
    for a in range(0,len(title)):
        if value[a].isdigit():
            r=value[a]
        else:
            r="\""+value[a]+"\""
        exp=exp.replace(str(title[a]),r)
    return eval(exp)
    #Apply BODMAS Rule with proper paranthesis
    


def execute(q):

    q+="#"
    state='0'
    temp=""
    result=[]
    what, cfrom, exp, where, exp='','','','',''
    etree=None
    required_fields=[]
    csvfile,headfile='',''
    #For each character in a query
    end= False
    found=False
    for i in range(0,len(q)):
        #for every rule in rule table
        if not end:
            for j in range(0,len(rule)):
                #if state is equal to current state and it allows current char
                if (rule[j][0]==state)&((rule[j][1]=='any')|(q[i] in rule[j][1])):
                    #Execute required and stop rule search
                    #exec(rule[j][2],globals(),locals())
                    found=True
                    state=rule[j][2]
                    if rule[j][3]!='': #push
                        temp+=q[i]
                    if rule[j][4]=="req": #clean
                        required_fields.append(temp)
                        temp=''
                    elif rule[j][4]=="csv":
                        csvfile=temp
                        temp=''
                    elif rule[j][4]=="head":
                        headfile=temp
                        temp=''
                    elif rule[j][4]=="exp":
                        exp=temp
                        temp=''
                        #Apply BODMAS Rule with proper paranthesis
                        exp=par(exp)
                        
                        #VALIDATION to be performed (!to be added)
                        ###print(exp)
                        #Create tree
                        etree=tree1(exp)
                    if state=='end':
                        end=True
                    break
            if not found:
                raise sqlerror(-2,"Unexpected character "+q[i]+" at position "+str(i+1))
            else:
                found=False
    
    csv=open(csvfile,"r").read().splitlines()
    head=open(headfile,"r").readline().split(",")

    #Start searcing csv file with query
    for a in range(0,len(csv)):
        csv[a]=(csv[a].split(","))

    for b in range(0,len(csv)):
        exec_result=evalthis(etree,head,csv[b])
        if(exec_result==True):
            if required_fields[0]=='*':
                ###print("Adding to result")
                result.append(csv[b])
            else:
                temp_result=[]
                for i in range(0,len(required_fields)):
                    for j in range(0,len(head)):
                        if head[j]==required_fields[i]:
                            temp_result.append(csv[b][j])
                            break
                result.append(temp_result)
        elif exec_result==False:
            pass
        else:
            raise sqlerror(-13,"Where clause condition returns non-boolean result")
    if len(result)==0:
        return [1,'Empty',result]
    return [0,'Success',result]

def query(q):
    """Parse and execute the query
    :param: Query string with mandatory input and header files.
    :return: Matching list of rows
    :return: -1 if error
    :return: Empty list if no rows match
    """
    try:
        return execute(q)
    except sqlerror as e:
        return [e.sqlcode,e.message,[]]
