from .models import User, MoodItem, MoodGroup, Mood, Team
from flask_security import current_user
from pygal import Pie, StackedBar
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

class Moodlist():	
	def __init__(self, name, color):
		self.moods=[]
		self.name=name
		self.color=color

	def __repr__(self):
		return self.name 
		
class PersoHistoChart(StackedBar):
	def __init__(self):
		StackedBar.__init__(self, style=custom_style)
		moods=dict()
		for m in MoodItem.objects.all():
			moods[m.id] = Moodlist(m.name, m.color)
		xlabels = []
		for item in Mood._get_collection().aggregate([ { "$group" : { "_id" : { "month": { "$month": "$date" },  "year": { "$year": "$date" }, "mood" : "$mood" }, 
			"nb" : { "$sum" : 1 } }}  ,
			{"$sort" : { "_id.year" : 1, "_id.month" : 1  } }
			]):
			if item["_id"]["month"] not in xlabels:
				xlabels.append(item["_id"]["month"]) 
			moods[item["_id"]["mood"]].moods.append(item["nb"])
		print (moods)
		self.x_labels = xlabels
		for m in moods:
			print (moods[m].name)
			print (moods[m].moods)
			self.add(moods[m].name, moods[m].moods)
