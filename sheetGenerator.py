from datetime import datetime
from bs4 import BeautifulSoup
from config import *
'''
	https://www.crummy.com/software/BeautifulSoup/bs4/doc/
	https://docs.python.org/3/library/random.html
'''
#import pdfkit

# Template of Worksheets (#1, #2) on either side of a section
section_template = '''<div id=section-{} class="container"><div class="columns">
<div class="column"><h1 class="title">{} - Sheet {}</h1>
<div class="table-container">
<table class="left-pane table is-fullwidth">
<tbody class="left-pane"></tbody>
</table></div></div>
<div class="column"><h1 class="title">{} - Sheet {}</h1>
<div class="table-container">
<table class="right-pane table is-fullwidth">
<tbody class="right-pane"></tbody>
</table></div></div>
</div></div>
<div class="sheetbreak"></div>
'''

# Open the 'template2.html' - placeholder of our Worksheets
with open('template2.html', 'r') as raw_doc:
	templ_doc = raw_doc.read()
	raw_doc.close()

save_date = datetime.strftime(datetime.now(),"%b_%d_%Y")
template = BeautifulSoup(templ_doc, 'html.parser')

easy_size = len(easy_pairs)
random_size = len(random_pairs)


'''
	HTML Table Generator
'''
tbody_template = '''<tbody></tbody>'''
template = BeautifulSoup(templ_doc, 'html.parser')
all_sections = BeautifulSoup('', 'html.parser')
sheet_break = BeautifulSoup("<div class=\"sheetbreak\"></div>", 'html.parser')

# Template Generator
def tablePopulator(tbody, number_pairs, operator):
	'''
		tablePopulator from passed pairings
		tbody: table Body <tbody> <bs4>
		number_pairs: list of number pairs <list(list)>
		operator: Operator Symbol defining Worksheet <str> : '+','-'
	'''
	tbody_tag = tbody.tbody
	for pair in number_pairs:
		# <tr></tr>
		trow = tbody.new_tag("tr")
		for idx,no in enumerate(pair):
			# <tr><td>Number 1</td></tr>
			td = tbody.new_tag("td")
			td.string = str(no)
			trow.append(td)
			# <tr><td>Number 1</td><td>Operator</td1></tr>
			if idx == 0:
				td = tbody.new_tag("td")
				td.string = operator
				trow.append(td)
			# <tr><td>Number 1</td><td>Operator</td1></tr>
		td = tbody.new_tag("td")
		td.string = '________'
		trow.append(td)
		# End Of Row
		# Append Row to Body
		tbody_tag.append(trow)
	return tbody

def SectionGenerator(pairs, sheet_length, section_template, 
	tbody_template,all_sections, sheet_number, safety_pairs, operator, exercise_name):
	'''
		Generates <section></section> Each containing Two Worksheets
		pairs : Pairs to Generate Sheets <list(list)>
		sheet_length: Default 20 per worksheet <int>
		section_template: HTML Template of Section <str (in HTML format)>
		tbody_template: HTML Template of tbody <str (in HTML format)>
		all_sections: Soup HTML Parser Object Placeholder for Sheets <bs4>
		sheet_number: Sheet Numbering Default: 3 <int>
		safety_pairs: Filling in the remaining side of a section <list>
		operator: Execercise numericals with operands <str> [+, - , x, /]
		exercise_name: Sheet Name <str> ['Addition' ...]
	'''	
	for idx, looper in enumerate(range(0, len(pairs), 20)):
		sect_number = (idx + 1)

		number_pairs_left = pairs[looper+0:looper+10]
		number_pairs_right = pairs[looper+10:looper+20]
	
		section = BeautifulSoup(
				section_template.format(sect_number, exercise_name, sheet_number-2 , exercise_name, sheet_number-1)
				,'html.parser')
		sheet_number += 2
		# Forced Replace
		if number_pairs_left != []:
			tbody = BeautifulSoup(tbody_template, 'html.parser')
			tbody_tag = tbody.tbody
			generated_easy_body = tablePopulator(tbody, number_pairs_left, operator)	
			left_section = BeautifulSoup(str(section).replace("<tbody class=\"left-pane\"></tbody>", str(generated_easy_body)), 'html.parser')	
		
	
		if number_pairs_right != []:
			tbody = BeautifulSoup(tbody_template, 'html.parser')
			tbody_tag = tbody.tbody
			generated_easy_body = tablePopulator(tbody, number_pairs_right, operator)
			right_section = BeautifulSoup(str(left_section).replace("<tbody class=\"right-pane\"></tbody>", str(generated_easy_body)), 'html.parser')
				
		else:
			tbody = BeautifulSoup(tbody_template, 'html.parser')
			tbody_tag = tbody.tbody
			generated_easy_body = tablePopulator(tbody, safety_pairs[:10], operator)
			right_section = BeautifulSoup(str(left_section).replace("<tbody class=\"right-pane\"></tbody>", str(generated_easy_body)), 'html.parser')


		all_sections.append(right_section)

	return all_sections, sheet_number

all_sections,sheet_number = SectionGenerator(all_pairs, 
											20, 
											section_template, 
											tbody_template,all_sections, 
											sheet_number, 
											safety_pairs,
											operator,
											exercise_name
											)

final_template = BeautifulSoup(str(template).replace("<section class=\"section\"></section>", str(all_sections)), 'html.parser')	

for idx, sheet in enumerate(final_template.select('.sheetbreak')):
	if ( (idx+1)%2 != 0):
		sheet.decompose()

#print(final_template.prettify())
with open('Sheet ' + save_date + '.html', 'w') as raw_doc:
	raw_doc.write(str(final_template))
	raw_doc.close()

print('Done ... Sheet ' + save_date)
# https://pypi.org/project/pdfkit/
# https://wkhtmltopdf.org/usage/wkhtmltopdf.txt
'''print_options = {
    'margin-top': '0.1in',
    'margin-right': '0.25in',
    'margin-bottom': '0.1in',
    'margin-left': '0.25in'
}
#time.sleep(3)
pdfkit.from_file('Sheet ' + save_date + '.html', 'sample.pdf', options=print_options)'''