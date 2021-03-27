from utils import *
from robot import Robot

JSON_PATH = './graph.json'
TASK_PATH = './task.txt'

graph = create_graph(JSON_PATH)
tasks = read_task(TASK_PATH) # [init, final, pickup, delivery]

# Find optimal path for each task
optimal_paths = {}
for robot in tasks:
	optimal_paths[robot] = []
	for task in tasks[robot]:
		path1 = shortest_path(graph, task[0], task[1])
		path2 = shortest_path(graph, task[1], task[2])
		path3 = shortest_path(graph, task[2], task[3])
		path = path1 + path2 + path3
		optimal_paths[robot].append(path)

# # Tasks left per robots
# tasks_left = {}
# for robot in optimal_paths:
# 	tasks_left[robot] = len(optimal_paths[robot])

# List of robots
robots = []
for robot in optimal_paths:
	robots.append(Robot(name=robot, optimal_paths=optimal_paths[robot], tasks_left=len(optimal_paths[robot]), graph=graph))

while(tasks_remaining(robots)):
	loc = {} # Dict of (location, robot) to keep track of collisions
	for robot in robots:
		
		# Continue to next robot if all tasks for robot completed.
		if robot.task_idx = -1:
			continue

		robot.loc_idx = robot.loc_idx+1 # Go to next location
		if robot.loc_idx < len(robot.optimal_paths[robot.task_idx]): # Continue the same task
			
			new_loc = robot.optimal_paths[robot.task_idx][robot.loc_idx]
			
			# Collision occurs
			if new_loc in loc: 
				existing_robot = loc[new_loc]
				dist2end_existing = len(existing_robot.optimal_paths[existing_robot.task_idx]) - existing_robot.loc_idx
				dist2end_new = len(robot.optimal_paths[existing_robot.task_idx]) - robot.loc_idx

				# Letting the robot closer to the end of its task to go through
				if dist2end_existing <= dist2end_new: 
					while new_loc in loc:
						robot.reroute()
						new_loc = robot.optimal_paths[robot.task_idx][robot.loc_idx]
						# TODO : If 4 cells around it explored -> exit
				else:
					loc[new_loc] = robot
					while new_loc in loc:	
						existing_robot.reroute()
						new_loc = existing_robot.optimal_paths[existing_robot.task_idx][existing_robot.loc_idx]			

			# If no collision
			else:
				# Add to dict only if not a TS. If TS, others can come in, so don't need to check for collisions.
				if new_loc not in graph('TS'):
					loc[robot.optimal_paths[robot.task_idx][robot.loc_idx]] = robot

		else: # Go to next task if that exists
			robot.task_idx = (robot.task_idx+1) if ((robot.task_idx+1)<len(robot.optimal_paths)) else -1
			robot.tasks_left -= 1
			robot.loc_idx = 0
