from .models import User, MoodItem, MoodGroup, Mood, Team
from flask_security import current_user
from pygal import Pie, Bar
from pygal.style import Style
import humanize

custom_style = Style(
  background='transparent',
  plot_background='transparent',
  title_font_size=30,
  opacity='.6',
  opacity_hover='1',
  transition='400ms ease-in')


class PersoPieChart(Pie):
	def __init__(self):
		Pie.__init__(self, inner_radius=0.5, style=custom_style)
		self.title="Personal"
		for label in MoodItem.objects.all():
			value = Mood.objects(user=current_user.id, mood=label).count()
			self.add(label.__str__(), 
				[ { "value" : value, "color" : label.color } ])

class PersoHistoChart(Bar):
	def __init__(self):
		Bar.__init__(self, inner_radius=0.5, style=custom_style)

		for  item in Mood.objects(user=current_user.id):
			self.add(humanize.naturalday(item.date), 
				[ { "value" : 2, "color" : "blue" } ])
		self.x_labels = map(str, range(2015, 2017))