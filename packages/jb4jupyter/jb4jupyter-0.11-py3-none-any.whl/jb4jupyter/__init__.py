from .plotpretty import *

def joke(): return 'nah'

def configlatexprint():
	lines = [
		'((* extends \'article.tplx\' *)) \n',
		'((* block input_group *)) \n',
		'((* endblock input_group *)) \n',
		'((* block execute_result scoped *)) \n',
		'    ((* block display_data scoped *)) \n',
		'        ((( super() ))) \n',
		'    ((* endblock display_data *)) \n',
		'((* endblock execute_result *)) \n'
		]
	with open('jb4jupyter.tplx','w') as txtfile:
		txtfile.writelines(lines)
