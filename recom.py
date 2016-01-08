#!/usr/bin/python
import cgi
print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head><title>My first cgi</title></head>"
print "<body>"
print '<div align=center>'
print "<h1>Hello!!</h1>"
from math import sqrt

#return similarity between two critics
#using euclidean distance

def sim_critic(prefs,crit1,crit2):
	si=[]
	for item in prefs[crit1]:	
		if item in prefs[crit2]:
			si.append(item)
	if len(si)==0:
		return 0
	sum_of_sq = sum([pow(prefs[crit1][item]-prefs[crit2][item],2)
			for item in prefs[crit1] if item in prefs[crit2]])	
	return 1/(1+sum_of_sq)
	
#use pearson formula to calculate similarity between two persons
def pearson_sim(prefs,p1,p2):
	#list of items rated by both the users	
	si=[]
	for item in prefs[p1]:
		if item in prefs[p2]:
			si.append(item)
	if len(si)==0:
		return 0
	n=len(si)
	#sum of ratings
	sum1=sum([prefs[p1][item] for item in si])
	sum2=sum([prefs[p2][item] for item in si])
	#sum of square of ratings
	sum1sq=sum([pow(prefs[p1][item],2) for item in si])
	sum2sq=sum([pow(prefs[p2][item],2) for item in si])
	#sum of products
	sumpro=sum([prefs[p1][item]*prefs[p2][item] for item in si])
	#pearson formula
	num=sumpro-sum1*sum2/n
	den=sqrt((sum1sq-pow(sum1,2)/n)*(sum2sq-pow(sum2,2)/n))
	if den==0:
		return 0
	return num/den


#return top similar users
def top_matches(prefs,cri,n=5,func=pearson_sim):
	#dict of presons with their similarity
	li=[]
	for person in prefs:
		if person!=cri:
			li.append((func(prefs,cri,person),person))
	li.sort()
	li.reverse()
	return li[0:n]

#get recommendation for a person based on weighted similarities
def get_rec(prefs,person,func=pearson_sim):
	totals={}
	sim_sums={}
	for other in prefs:
		if other==person:
			continue
		sim=func(prefs,person,other)
		if sim<=0 :
			continue
		for item in prefs[other]:
			if item not in prefs[person] or prefs[person][item]==0:
				totals.setdefault(item,0)
				totals[item]+=prefs[other][item]*sim
				sim_sums.setdefault(item,0)
				sim_sums[item]+=sim

	ranking=[(totals[item]/sim_sums[item],item) for item in totals]
	ranking.sort()
	ranking.reverse()
	return ranking 		

#transform preferences 
def trans_pref(prefs):
	result={}
	for person in prefs:
		for item in prefs[person]:
			result.setdefault(item,{})
			result[item][person]=prefs[person][item]
	return result
			

#precompute similar items 
def sim_item(prefs,n=3):
	ans={}
	result=trans_pref(prefs)
	for item in result:
		ans[item]=top_matches(result,item,n=n)
	return ans
	

#getting item recommendations for a person using precomputed similarity between items
def get_rec2(prefs,person,item_sim):
	ans={}
	total={}
	for item in prefs[person]:
		for (sim,item2) in item_sim[item]:
			if item2 in prefs[person]:
				continue
			ans.setdefault(item2,0)
			ans[item2]+=sim*prefs[person][item]
			total.setdefault(item2,0)
			total[item2]+=prefs[person][item]
	ranking=[(ans[item]/total[item],item) for item in ans]			
	ranking.sort()
	ranking.reverse()
	print ranking
	return ranking 

#loading data from movielens
def load_len(path='/home/nisha/Desktop/'):
	movie={}
	for line in open(path+'movies.dat'):
		(id,title,genre)=line.split("::")[:]
		movie[id]=title
	prefs={}
	for line in open(path+'ratings.dat'):
		(user,id,rating,tmp)=line.split("::")[:]
		prefs.setdefault(user,{})
		prefs[user][movie[id]]=float(rating)
	return prefs
	

form = cgi.FieldStorage()
if form.getvalue("name"):
	name = form.getvalue("name")
	
	prefs=load_len()
	print '<h2>Top 10 recommended movies for ' + name + ' are:</h2> '

	yy=get_rec(prefs,name)[0:11]

	for t in yy:
                print "<p><b>Movie :</b> "
                print t[1]
                print "<b>, Expected Rating :</b>"
                print t[0]
                print "</p>"




if form.getvalue("happy"):
	print"<p>Happy!!</p>"
if form.getvalue("sad"):
	print "<p>Sad :( </p>"

print '<form method="post" action="hello2.py">'
print '<div align=center lass="form-group">'
print '<label for="name">USER ID:</label>'
print '<p></p>'
print '<input type="text" name="name" class="form-control" id="name" placeholder="Enter User-id">'
print '<button type="submit" class="btn btn-default">Submit</button>'
print '</div>'
print "</form>"
print "</div>"
print "</body>"
print "</html>"

