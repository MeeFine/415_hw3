'''TowersOfHanoi.py
A QUIET Solving Tool problem formulation.
QUIET = Quetzal User Intelligence Enhancing Technology.
The XML-like tags used here serve to identify key sections of this 
problem formulation.  

CAPITALIZED constructs are generally present in any problem
formulation and therefore need to be spelled exactly the way they are.
Other globals begin with a capital letter but otherwise are lower
case or camel case.
'''
#<METADATA>
QUIET_VERSION = "0.1"
PROBLEM_NAME = "Towers of Hanoi"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ['S. Tanimoto']
PROBLEM_CREATION_DATE = "14-APR-2015"
PROBLEM_DESC=\
'''This formulation of the Towers of Hanoi problem uses generic
Python 3 constructs and has been tested with Python 3.4.
It is designed to work according to the QUIET tools interface.
'''
#</METADATA>

#<COMMON_CODE>
def DEEP_EQUALS(s1,s2):
  result = s1['peg1']==s2['peg1'] and s1['peg2']==s2['peg2'] and s1['peg3']==s2['peg3']
  return result

def DESCRIBE_STATE(state):
  # Produces a textual description of a state.
  # Might not be needed in normal operation with GUIs.
  txt = "\n"
  for peg in ['peg1','peg2','peg3']:
      txt += str(state[peg]) + "\n"
  return txt

def HASHCODE(s):
  '''The result should be an immutable object such as a string
  that is unique for the state s.'''
  return str(s['peg1'])+';'+str(s['peg2'])+';'+str(s['peg3'])

def copy_state(s):
  # Performs an appropriately deep copy of a state,
  # for use by operators in creating new states.
  news = {}
  for peg in ['peg1', 'peg2', 'peg3']:
    news[peg]=s[peg][:]
  return news

def can_move(s,From,To):
  '''Tests whether it's legal to move a disk in state s
     from the From peg to the To peg.'''
  try:
   pf=s[From] # peg disk goes from
   pt=s[To]   # peg disk goes to
   if pf==[]: return False  # no disk to move.
   df=pf[-1]  # get topmost disk at From peg..
   if pt==[]: return True # no disk to worry about at To peg.
   dt=pt[-1]  # get topmost disk at To peg.
   if df<dt: return True # Disk is smaller than one it goes on.
   return False # Disk too big for one it goes on.
  except (Exception) as e:
   print(e)

def move(s,From,To):
  '''Assuming it's legal to make the move, this computes
     the new state resulting from moving the topmost disk
     from the From peg to the To peg.'''
  news = copy_state(s) # start with a deep copy.
  pf=s[From] # peg disk goes from.
  df=pf[-1]  # the disk to move.
  news[From]=pf[:-1] # remove it from its old peg.
  news[To]+=[df] # Put disk onto destination peg.
  return news # return new state

def goal_test(s):
  '''If the first two pegs are empty, then s is a goal state.'''
  return s['peg1']==[] and s['peg2']==[]

def goal_message(s):
  return "The Tower Transport is Triumphant!"

class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)

#</COMMON_CODE>

#<COMMON_DATA>
N_disks = 4
#</COMMON_DATA>

#<INITIAL_STATE>
INITIAL_STATE = {'peg1': list(range(N_disks,0,-1)), 'peg2':[], 'peg3':[] }
CREATE_INITIAL_STATE = lambda: INITIAL_STATE
DUMMY_STATE =  {'peg1':[], 'peg2':[], 'peg3':[] }
#</INITIAL_STATE>

#<OPERATORS>
peg_combinations = [('peg'+str(a),'peg'+str(b)) for (a,b) in
                    [(1,2),(1,3),(2,1),(2,3),(3,1),(3,2)]]
OPERATORS = [Operator("Move disk from "+p+" to "+q,
                      lambda s,p=p,q=q: can_move(s,p,q),
                      # The default value construct is needed
                      # here to capture the values of p&q separately
                      # in each iteration of the list comp. iteration.
                      lambda s,p=p,q=q: move(s,p,q) )
             for (p,q) in peg_combinations]
#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>

#<STATE_VIS>
if 'BRYTHON' in globals():
 from TowersOfHanoiVisForBrython import set_up_gui as set_up_user_interface
 from TowersOfHanoiVisForBrython import render_state_svg_graphics as render_state
# if 'TKINTER' in globals(): from TicTacToeVisForTKINTER import set_up_gui
#</STATE_VIS>
