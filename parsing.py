test = ["Fall12,PHYS 5A,Fall12,PHYS 5L,Fall12,CMPS 12B,Fall12,CMPS 12L,Fall12,CMPE 16,","Winter13,HCI 131 ,Winter13,CMPS 101 ,Winter13,DANM 250,Winter13,Math 21 ,","Spring13,PHYSC 5C,Spring13,PHYSC 5L,Spring13,AMS 131,","Summer13,CMPS109,Summer13,Math 24,"]
# print test

test2 = [u'PHYS 5A-Fall12,PHYS 5L-Fall12,CMPS 12B-Fall12,CMPS 12L-Fall12,CMPE 16-Fall12,', u'HCI 131 -Winter13,CMPS 101 -Winter13,Math 21 -Winter13,', u'PHYSC 5C-Spring13,DANM 250-Spring13,PHYSC 5L-Spring13,AMS 131-Spring13,', u'CMPS109-Summer13,Math 24-Summer13,']
print test2

#if class isn't in database add it
	#change progress to require class.
	
#don't add class to progress if it's already been added

#restoring these classes and years to database

#figure out if we want to have space between class and number CMPE16 vs CMPE 16

#need to figure out deleting progress for a given user...
#maybe we query for a user, delete all their progress, then post all their new progress.

#taking the same class twice in the same year vs. moving a class around