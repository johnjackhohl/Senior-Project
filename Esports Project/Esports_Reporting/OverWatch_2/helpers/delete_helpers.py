from OverWatch_2 import models

def deleteTeam(pk):
	team = models.OW_Team.objects.get(id=pk)
	team.delete()