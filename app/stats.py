from .models import User, MoodItem, Mood, Team
from flask_security import current_user
from pygal import Pie, StackedBar
from pygal.style import Style
from collections import OrderedDict
import bson
from datetime import date

CUSTOM_STYLE = Style(
  background='transparent',
  plot_background='white',
  font_family="sans-serif",
  title_font_size=30,
  opacity='.6',
  opacity_hover='1',
  transition='400ms ease-in')


class PersoPieChart(Pie):
	def __init__(self):
		Pie.__init__(self, inner_radius=0.5, style=CUSTOM_STYLE, show_legend=False)
		self.title="Distribution"
		for label in MoodItem.objects.order_by("order"):
			value = Mood.objects(user=current_user.id, mood=label).count()
			self.add(label.__str__(), 
				[ { "value" : value, "color" : label.color } ])


class PersoHistoChart(StackedBar):
	def __init__(self):
		StackedBar.__init__(self, style=CUSTOM_STYLE, order_min=1, show_legend=False)
		self.x_title=str(date.today().year)
		self.title="Monthly history"
		moods= OrderedDict()
		for label in MoodItem.objects.order_by("order"):			
			moods[label.name] = [None] * 12
		self.x_labels = map(str, range(1, 13))
		for item in Mood._get_collection().aggregate([ {"$match":{"user": bson.objectid.ObjectId(  str(current_user.id))  }  },
			{ "$lookup": {"from":"mood_item", "localField":"mood", "foreignField":"_id", "as":"mood"  } },
			{"$group" : {"_id":{ "mood":"$mood.name",  "color" : "$mood.color", "month" : { "$month": "$date"}, "year" : { "$year":"$date"} }, "count": { "$sum":1} }  }]):
			moods[item["_id"]["mood"][0]][item["_id"]["month"]-1] = {"value" : item["count"] , "color" : item["_id"]["color"][0] }
		self.range = (0, 31)
		for m in moods.keys():
			self.add(m, moods[m])
