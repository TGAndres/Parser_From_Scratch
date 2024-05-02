import sys
# I N P U T:
input_file = "input.txt"
output_file = "output.txt"
# Check if the user provided the input and output files
if len(sys.argv) == 2 or len(sys.argv) == 3:
    if len(sys.argv) == 2:
        input_file = sys.argv[1]
        output_file = "output_" + input_file
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]

# Read the file
try:
    with open(input_file, 'r') as file:
        data = file.read()
except Exception as e:
    print(f"An error occurred while reading the file: {e}")
    sys.exit(1)

# Split the data by line
data = data.split('\n')

#Generate the list of tokens:
tokens=[]
for line in data :
    line = line.split()
    for token in line:
        tokens.append(token)

#Add end of input token:
tokens.append('$')

#Grammar rules as list
#For each rule, we store the non terminal, 
#and the number of elements it produces.
Grammar=[
    ('S',2), #rule 0
    ('S',0),
    ('S1',4),
    ('ARGUMENTS',3),
    ('VALUES',3),
    ('VALUES1',0), #rule 5
    ('VALUES1',2),
    ('FUNCTION',4),
    ('LINES',0),
    ('LINES',2),
    ('LINES',3), #rule 10
    ('LINES',4),
    ('RETURN',3),
    ('DECLARE',4),
    ('DECLARE1',0),
    ('DECLARE1',2), #rule 15
    ('MODIFY',4),
    ('V_FUNCTION',6),
    ('ELSE',0),
    ('ELSE',4),
    ('OPERATION',1), #rule 20
    ('OPERATION',3),
    ('COMPARE',3),
    ('S_VALUE',1),
    ('S_VALUE',2),
    ('C_FUNCTION',0), #rule 25
    ('C_FUNCTION',1),
    ('D_ARGS',3),
    ('E_VALUES',2),
    ('E_VALUES1',0),
    ('E_VALUES1',2) #rule 30
    ]

#Parsing table is a dictionary with state and input as key
#the value is the type of operation and the state/rule
ParseTable={
    (1,'S'):('success',0), # Success state
    (1,'datatype'):('shift',2),
    (2,'S1'):('goto',3),
    (2,'id'):('shift',4),
    (3,'anything'):('reduce',0),
    (4,'ARGUMENTS'):('goto',5),
    (4,'('):('shift',6),
    (5,'FUNCTION'):('goto',9),
    (5,'{'):('shift',11),
    (6,'VALUES'):('goto',7),
    (6,'datatype'):('shift',12),
    (7,')'):('shift',8),
    (8,'anything'):('reduce',3),
    (9,'S'):('goto',10),
    (9,'datatype'):('shift',2),
    (9,'anything'):('reduce',1),
    (10,'anything'):('reduce',2),
    (11,'LINES'):('goto',17),
    (11,'DECLARE'):('goto',34),
    (11,'MODIFY'):('goto',34),
    (11,'while'):('shift',36),
    (11,'if'):('shift',37),
    (11,'datatype'):('shift',47),
    (11,'id'):('shift',48),
    (11,'anything'):('reduce',8),
    (12,'id'):('shift',13),
    (13,'VALUES1'):('goto',14),
    (13,','):('shift',15),
    (13,'anything'):('reduce',5),
    (14,'anything'):('reduce',4),
    (15,'datatype'):('shift',12),
    (15,'VALUES'):('goto',16),
    (16,'anything'):('reduce',6),
    (17,'RETURN'):('goto',18),
    (17,'return'):('shift',20),
    (18,'}'):('shift',19),
    (19,'anything'):('reduce',7),
    (20,'OPERATION'):('goto',21),
    (20,'S_VALUE'):('goto',24),
    (20,'const'):('shift',27),
    (20,'lit'):('shift',27),
    (20,'id'):('shift',23),
    (21,';'):('shift',22),
    (22,'anything'):('reduce',12),
    (23,'C_FUNCTION'):('goto',28),
    (23,'D_ARGS'):('goto',29),
    (23,'('):('shift',30),
    (23,'anything'):('reduce',25),
    (24,'+'):('shift',25),
    (24,'-'):('shift',25),
    (24,'*'):('shift',25),
    (24,'/'):('shift',25),
    (24,'anything'):('reduce',20),
    (25,'id'):('shift',23),
    (25,'S_VALUE'):('goto',26),
    (25,'const'):('shift',27),
    (25,'lit'):('shift',27),
    (26,'anything'):('reduce',21),
    (27,'anything'):('reduce',23),
    (28,'anything'):('reduce',24),
    (29,'anything'):('reduce',26),
    (30,'E_VALUES'):('goto',67),
    (30,'S_VALUE'):('goto',31),
    (30,'const'):('shift',27),
    (30,'lit'):('shift',27),
    (30,'id'):('shift',23),
    (31,'E_VALUES1'):('goto',32),
    (31,','):('shift',33),
    (31,'anything'):('reduce',29),
    (32,'anything'):('reduce',28),
    (33,'E_VALUES'):('goto',66),
    (33,'S_VALUE'):('goto',31),
    (33,'id'):('shift',23),
    (33,'const'):('shift',27),
    (33,'lit'):('shift',27),
    (34,'DECLARE'):('goto',34),
    (34,'MODIFY'):('goto',34),
    (34,'while'):('shift',36),
    (34,'if'):('shift',37),
    (34,'id'):('shift',48),
    (34,'datatype'):('shift',47),
    (34,'LINES'):('goto',35),
    (34,'anything'):('reduce',8),
    (35,'anything'):('reduce',9),
    (36,'('):('shift',57),
    (36,'V_FUNCTION'):('goto',38),
    (37,'('):('shift',57),
    (37,'V_FUNCTION'):('goto',40),
    (38,'DECLARE'):('goto',34),
    (38,'MODIFY'):('goto',34),
    (38,'while'):('shift',36),
    (38,'if'):('shift',37),
    (38,'id'):('shift',48),
    (38,'datatype'):('shift',47),
    (38,'LINES'):('goto',39),
    (38,'anything'):('reduce',8),
    (39,'anything'):('reduce',10),
    (40,'ELSE'):('goto',41),
    (40,'else'):('shift',43),
    (40,'anything'):('reduce',18),
    (41,'DECLARE'):('goto',34),
    (41,'MODIFY'):('goto',34),
    (41,'while'):('shift',36),
    (41,'if'):('shift',37),
    (41,'id'):('shift',48),
    (41,'datatype'):('shift',47),
    (41,'LINES'):('goto',42),
    (41,'anything'):('reduce',8),
    (42,'anything'):('reduce',11),
    (43,'{'):('shift',44),
    (44,'DECLARE'):('goto',34),
    (44,'MODIFY'):('goto',34),
    (44,'while'):('shift',36),
    (44,'if'):('shift',37),
    (44,'id'):('shift',48),
    (44,'datatype'):('shift',47),
    (44,'LINES'):('goto',45),
    (44,'anything'):('reduce',8),
    (45,'}'):('shift',46),
    (46,'anything'):('reduce',19),
    (47,'id'):('shift',49),
    (48,'='):('shift',50),
    (49,'DECLARE1'):('goto',51),
    (49,'='):('shift',53),
    (49,'anything'):('reduce',14),
    (50,'OPERATION'):('goto',54),
    (50,'const'):('shift',27),
    (50,'lit'):('shift',27),
    (50,'S_VALUE'):('goto',24),
    (50,'id'):('shift',23),
    (51,';'):('shift',52),
    (52,'anything'):('reduce',13),
    (53,'OPERATION'):('goto',56),
    (53,'const'):('shift',27),
    (53,'lit'):('shift',27),
    (53,'S_VALUE'):('goto',24),
    (53,'id'):('shift',23),
    (54,';'):('shift',55),
    (55,'anything'):('reduce',16),
    (56,'anything'):('reduce',15),
    (57,'OPERATION'):('goto',61),
    (57,'const'):('shift',27),
    (57,'lit'):('shift',27),
    (57,'S_VALUE'):('goto',24),
    (57,'id'):('shift',23),
    (57,'COMPARE'):('goto',58),
    (58,')'):('shift',59),
    (59,'{'):('shift',60),
    (60,'DECLARE'):('goto',34),
    (60,'MODIFY'):('goto',34),
    (60,'while'):('shift',36),
    (60,'if'):('shift',37),
    (60,'id'):('shift',48),
    (60,'datatype'):('shift',47),
    (60,'LINES'):('goto',64),
    (60,'anything'):('reduce',8),
    (61,'rel'):('shift',62),
    (62,'OPERATION'):('goto',63),
    (62,'const'):('shift',27),
    (62,'lit'):('shift',27),
    (62,'S_VALUE'):('goto',24),
    (62,'id'):('shift',23),
    (63,'anything'):('reduce',22),
    (64,'}'):('shift',65),
    (65,'anything'):('reduce',17),
    (66,'anything'):('reduce',30),
    (67,')'):('shift',68),
    (68,'anything'):('reduce',27)
}

#Stack for evaluating input
#Only contains state 1
stack=[1]

#Index of the on running reading of the input
index=0 
while(True):
    #Read next token
    token=tokens[index]

    #Check actual state
    state=stack[-1]

    #Evaluate input
    if (state,token) not in ParseTable:
        #Not expected token in that state
        if (state,'anything') not in ParseTable:
            print('Parse error in token: ', token)
            print('Actual state was: ', state)
            break
        
        #Reduce
        rule = (ParseTable[(state,'anything')][1])
        precedent = Grammar[rule][0]
        
        #Make 2*elements of the rule pops
        for i in range(Grammar[rule][1]*2):
            stack.pop()

        print('I just used ParseTable\'s rule: ',(state,'anything'), 
            " -> ",ParseTable[(state,'anything')])

        #Update state and token
        state = stack[-1]
        token = precedent

    #Check if parsing is done
    if ParseTable[(state,token)][0] == 'success':
        print("PARSING SUCCESS!!!")
        break

    #In case of shift
    if ParseTable[(state,token)][0] == 'shift':
        index += 1
    
    #In case of shift or goto 
    stack.append(token)
    stack.append(ParseTable[(state,token)][1])
    print('I just used ParseTable\'s rule: ',(state,token), 
            " -> ",ParseTable[(state,token)])
