# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent

class MyAI ( Agent ):
	dbg = False
	gold_found = False
	shot_wumpus = False
	shot_wumpus_once = False
	no_stench = False
	gold_about_turn = False
	direction = {'L':'LEFT','R':'RIGHT','U':'UP','D':'DOWN'}
	current_direction = direction['R']
	current_position = (0,0)
	safe_spots = []
	traversed = []
	visited = []
	danger = []
	back_tracker = 0
	front_tracker = 0

	def __init__ ( self ):
		self.dbg = False
		self.gold_found = False
		self.gold_about_turn = False
		self.shot_wumpus = False
		self.shot_wumpus_once = False
		self.no_stench = False
		self.current_position = (0,0)
		self.back_tracker = 0
		self.front_tracker = 0
		self.safe_spots.clear()
		self.traversed.clear()
		self.visited.clear()
		self.danger.clear()
		self.traversed.append((0,0))
		self.visited.append((0,0))

	def getOppositeDirection(self, direction):
		if direction == self.direction['L']: return self.direction['R']
		elif direction == self.direction['R']: return self.direction['L']
		elif direction == self.direction['U']: return self.direction['D']
		elif direction == self.direction['D']: return self.direction['U']

	def oppositeDirection(self, direction1,direction2):
		if direction1==self.direction['L'] and direction2 == self.direction['R']: return True
		elif direction1==self.direction['R'] and direction2 == self.direction['L']: return True
		elif direction1==self.direction['U'] and direction2 == self.direction['D']: return True
		elif direction1==self.direction['D'] and direction2 == self.direction['U']: return True
		return False

	def findNextDirection(self, next_direction):
		if self.dbg:
			print('Next Direction :'+next_direction)
			print('Current Direction :'+self.current_direction)
		if self.oppositeDirection(self.current_direction,next_direction):
			return [Agent.Action.TURN_LEFT,Agent.Action.TURN_LEFT,Agent.Action.FORWARD]
		elif self.current_direction==next_direction: return [Agent.Action.FORWARD]
		if next_direction == self.direction['D']:
			if self.current_direction == self.direction['R']:
				return [Agent.Action.TURN_RIGHT,Agent.Action.FORWARD]
			elif self.current_direction == self.direction['L']:
				return [Agent.Action.TURN_LEFT,Agent.Action.FORWARD]
		elif next_direction == self.direction['U']:
			if self.current_direction == self.direction['R']:
				return [Agent.Action.TURN_LEFT,Agent.Action.FORWARD]
			elif self.current_direction == self.direction['L']:
				return [Agent.Action.TURN_RIGHT,Agent.Action.FORWARD]
		elif next_direction == self.direction['L']:
			if self.current_direction == self.direction['U']:
				return [Agent.Action.TURN_LEFT,Agent.Action.FORWARD]
			elif self.current_direction == self.direction['D']:
				return [Agent.Action.TURN_RIGHT,Agent.Action.FORWARD]
		else:
			if self.current_direction == self.direction['U']:
				return [Agent.Action.TURN_RIGHT,Agent.Action.FORWARD]
			elif self.current_direction == self.direction['D']:
				return [Agent.Action.TURN_LEFT,Agent.Action.FORWARD]

	def findXY(self, next_spot):
		x1,y1 = self.current_position
		x2,y2 = next_spot
		if self.dbg:
			print('Going from (%d,%d) to (%d,%d)'%(x1,y1,x2,y2))
		steps = []
		if (-1 <= x2-x1 <= 1) and (-1 <= y2-y1 <= 1):
			if x1==x2:
				if y2==y2: direction_to_focus = self.getOppositeDirection(self.current_direction)
				if y2<y1: direction_to_focus = self.direction['D']
				if y2>y1: direction_to_focus = self.direction['U']
			elif x1>x2: direction_to_focus = self.direction['L']
			else: direction_to_focus = self.direction['R']
			steps.extend(self.findNextDirection(direction_to_focus))
			steps.append(direction_to_focus)
		return steps

	def markDangerTiles(self):
		x,y = self.current_position
		for i in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
			if i not in self.safe_spots:
				self.danger.append(i)

	def unmarkDangerTiles(self, position):
		x,y = position
		for i in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
			if i in self.danger:
				self.danger.remove(i)

	def markSafeTiles(self, position):
		x,y = position
		for i in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
			a,b = i
			if a>=0 and b>=0:
				self.safe_spots.append(i)
				if i in self.danger:
						self.danger.remove(i)

	def backTrack(self):
		plus_one = 1 if self.gold_about_turn else 0
		previous_spot = self.traversed[-1-plus_one]
		previous_spots = self.findXY(previous_spot)[self.back_tracker:]
		self.back_tracker += 1
		if len(previous_spots)==2:
			self.unmarkDangerTiles(self.current_position)
			self.current_position = self.traversed[-2]
			self.back_tracker = 0
			self.current_direction = previous_spots[-1]
			if self.gold_found and not self.gold_about_turn:
				self.gold_about_turn = True
			del self.traversed[-1]
		if self.dbg:
			print(self.traversed)
			print(self.current_position)
			print(self.current_direction)
			print(previous_spots)
		return previous_spots[0]

	def getCandidates(self):
		x,y = self.current_position
		if self.current_direction == self.direction['R']: return [(x+1,y),(x,y+1),(x,y-1),(x-1,y)]
		elif self.current_direction == self.direction['L']: return [(x-1,y),(x,y-1),(x,y+1),(x+1,y)]
		elif self.current_direction == self.direction['U']: return [(x,y+1),(x-1,y),(x+1,y),(x,y-1)]
		else: return [(x,y-1),(x+1,y),(x-1,y),(x,y+1)]

	def getNextSpot(self):
		x,y = self.current_position
		candidates = self.getCandidates()
		for i in candidates:
			a,b = i
			if a>=0 and b>=0:
				if i not in self.danger and i not in self.traversed and i not in self.visited:
					self.unmarkDangerTiles(i)
					return i
		if x==0 and y==0 and (1,0) in self.visited:
			self.gold_found = True
			return (0,0)
		if len(self.traversed)>0:
			self.unmarkDangerTiles(self.traversed[self.traversed.index(self.current_position)-1])
			return self.traversed[self.traversed.index(self.current_position)-1]
		else:
			return -1

	def getAction( self, stench, breeze, glitter, bump, scream ):

		if self.gold_found:
			if self.current_position == (0,0):
				return Agent.Action.CLIMB
			else:
				return self.backTrack()

		if glitter and not self.gold_found:
			self.gold_found = True
			return Agent.Action.GRAB

		if scream:
			self.unmarkDangerTiles(self.current_position)
			self.no_stench = True

		if self.shot_wumpus_once:
			self.shot_wumpus = True

		if (stench and not self.no_stench) or breeze:
			if stench and not self.shot_wumpus_once:
				self.shot_wumpus_once = True
				return Agent.Action.SHOOT
			if self.current_position == (0,0):
				return Agent.Action.CLIMB;
			self.markDangerTiles()
			return self.backTrack()

		if self.current_position == (0,0):
			self.markSafeTiles(self.current_position)

		if bump:
			self.danger.append(self.current_position)
			del self.traversed[-1]
			self.current_position = self.traversed[-1]

		next_spot = self.getNextSpot()
		if next_spot == -1:
			return Agent.Action.CLIMB

		next_spots = self.findXY(next_spot)[self.front_tracker:]
		self.front_tracker += 1
		if len(next_spots)==2:
			previous_spot = self.current_position
			self.current_position = next_spot
			self.front_tracker = 0
			self.current_direction = next_spots[-1]
			if next_spot not in self.traversed : self.traversed.append(next_spot)
			else: self.traversed.remove(previous_spot)
			if next_spot not in self.safe_spots : self.safe_spots.append(next_spot)
			if next_spot not in self.visited : self.visited.append(next_spot)
			self.unmarkDangerTiles(next_spot)
		try:
			return next_spots[0]
		except:
			return Agent.Action.FORWARD

    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================


    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
