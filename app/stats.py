from .models import User, MoodItem, MoodGroup, Mood, Team
from flask_security import current_user
from pygal import Pie, StackedBar
from pygal.style import Style
from collections import OrderedDict
import bson

custom_style = Style(
  background='transparent',
  plot_background='transparent',
  font_family="sans-serif",
  title_font_size=30,
  opacity='.6',
  opacity_hover='1',
  transition='400ms ease-in')


class PersoPieChart(Pie):
	def __init__(self):
		Pie.__init__(self, inner_radius=0.5, style=custom_style)
		self.title="Personal"
		for label in MoodItem.objects.order_by("order"):
			value = Mood.objects(user=current_user.id, mood=label).count()
			self.add(label.__str__(), 
				[ { "value" : value, "color" : label.color } ])


		
class PersoHistoChart(StackedBar):
	def __init__(self):
		StackedBar.__init__(self, style=custom_style)
		self.title="Personal history"
		moods= OrderedDict()
		for label in MoodItem.objects.order_by("order"):			
			moods[label.name] = [None] * 12
		self.x_labels = map(str, range(1, 13))
		
		for item in Mood._get_collection().aggregate([ {"$match":{"user": bson.objectid.ObjectId(  str(current_user.id))  }  },
			{ "$lookup": {"from":"mood_item", "localField":"mood", "foreignField":"_id", "as":"mood"  } },
			{"$group" : {"_id":{ "mood":"$mood.name",  "color" : "$mood.color", "month" : { "$month": "$date"}, "year" : { "$year":"$date"} }, "count": { "$sum":1} }  }]):
			moods[item["_id"]["mood"][0]][item["_id"]["month"]-1] = {"value" : item["count"] , "color" : item["_id"]["color"][0] }
		
		for m in moods.keys():
			self.add(m, moods[m])
