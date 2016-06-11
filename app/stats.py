from .models import User, MoodItem, MoodGroup, Mood, Team
from flask_security import current_user
from chartjs import chart

class PersoPieChart(chart):
	def __init__(self):
		chart.__init__(self, title="Personal rate", ctype="Pie")
		self.canvas="canvas1"
		labels = []
		dataset = []
		for label in MoodItem.objects.all():
			labels.append(label)
			dataset.append(Mood.objects(user=current_user.id, mood=label).count())
		self.set_labels(labels)
		self.set_colors([ "#FF0000", "#0000FF", "#00FF00"])
		self.set_highlights([ "#AA0000", "#0000AA", "#00AA00"])
		self.add_dataset(dataset)

class PersoHistoChart(chart):
	def __init__(self):
		chart.__init__(self, title="Personal rate", ctype="Bar" )
		self.canvas="canvas2"
		self.set_labels([ "#FF0000", "#0000FF", "#00FF00"])
		self.set_colors([ "#FF0000", "#0000FF", "#00FF00"])
		self.set_highlights([ "#AA0000", "#0000AA", "#00AA00"])
		self.add_dataset([1,2,3])
