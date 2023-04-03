import os
currentPath = os.path.dirname(os.path.join(os.path.abspath(__file__)))
logPath = os.path.join(currentPath,'log')
reportPath = os.path.join(currentPath, '../templates', 'reports')
unittestPath = os.path.join(currentPath,'test')
screen_shot_path = os.path.join(currentPath, '../static', 'screenshot')

