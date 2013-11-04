from django.db import models

class accounts(models.Model):
	twitterid = models.IntegerField()
	credit    = models.IntegerField()
	activate  = models.TextField()
	others    = models.TextField()
	def __unicode__(self):
		return u'Twitter id : %s ,others : %s' % (self.twitterid, self.others)
	class Meta:
		ordering = ['twitterid']
class tokens(models.Model):
	accounts  = models.ForeignKey(accounts)
	tokens    = models.TextField()
	def __unicode__(self):
		return u'Tokens : %s' % (self.tokens)
	
	