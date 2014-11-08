#The real workhorse here is requests. What a guy. http://docs.python-requests.org/en/latest/
import requests
##########################################################################
#### 					PLEASE READ THE README.TXT					  ####
####					FOR AN EXPLANATION OF CODE					  ####	
##########################################################################
def processSpell(spell, attack, ability, cdr):
	(efficiency, maxdamage, apscale, adscale, base, dps) = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
	#Basically, ignore toggles for now.
	maxrank = spell["maxrank"]
	cd = spell["cooldown"][maxrank-1] * ((100-cdr)/100)
	if spell["costType"] == ("Mana" or "Health" or "Heat" or "Energy"):
		

		
		#If the damage field is null, then our damage is 0.
		if spell["effect"][1] == None:
			return {"dps": dps, "maxd": maxdamage, "ap": apscale, "ad": adscale, "base": base, "efficiency": efficiency, "cd":cd}
		else:
			#Here we go boys. 
			base = spell["effect"][1][maxrank-1]
			if "vars" in spell:
				for i in spell["vars"]:
					#vars is our list of scalers. Might throw in mana/souls later, but these are hard to account for b/c they change so often.
					#for now, I'll stick to AP and AD.
					if i["link"] == "spelldamage":
						apscale = ability*i["coeff"][0] #Bonus damage = AP*APc
					elif i["link"] == "attackdamage":
						adscale = attack*i["coeff"][0] #Bonus damage = AD * ADc
			#So we have our maxdamage! maxdamage != efficient, however. More calculations to come.
			maxdamage = base+apscale+adscale
			#This is the most basic measure I could come up with. Damage/Cooldown = dps.
			if cd != 0:
				dps = maxdamage/cd
			


			return {"dps": dps, "maxd": maxdamage, "ap": apscale, "ad": adscale, "base": base, "efficiency": efficiency, "cd":cd}
	else:
		return {"dps": dps, "maxd": maxdamage, "ap": apscale, "ad": adscale, "base": base, "efficiency": efficiency, "cd":cd}



#Gotta declare these as doubles so stuff doesn't go haywire with the DEEPS calculations.
ap_in = 0.0
ad_in = 0.0
cdr_in = 0.0
#Man, python input is dumb sometimes. Oh well, I won't make y'all download any more libraries than request.
ap_in = float(raw_input("Enter your given Ability Power (AP):\n"))
ad_in = float(raw_input("And now for your Attack Damage (AD):\n"))
cdr_in = float(raw_input("Finally, enter your Cooldown Reduction (CDR) as a percent, not a decimal:\n"))
if cdr_in > 0 and cdr_in < 1:
	cdr_in = float(raw_input("CDR was malformed (You probably entered it as a decimal, not a whole number). Please try again: \n"))
#And now, let requests work its magic!
key = "4a956ce8-2409-442a-a003-8f2784580237"
r = requests.get('https://na.api.pvp.net/api/lol/static-data/na/v1.2/champion?champData=spells&api_key='+key)
champList= r.json()["data"]

#This is for fun purposes only. I like to see where the numbers are coming from.
final_dict = {"dps":0, "maxd":0, "ap":0, "ad":0, "base":0, "efficiency": 0, "cd":0}
maxname=""
templist = {"dps":0, "maxd":0, "ap":0, "ad":0, "base":0, "efficiency": 0, "cd":0}
#So, obviously doing this linearly is the best option. O(n*4) is the best I can do since
#I have to look at every single spell in the game 
for k, v in champList.iteritems():
	#Iterate through this champion's spells
	for i in v["spells"]:
		#process the spell
		tempdict = processSpell(i, ad_in, ap_in, cdr_in)
		#if the efficiency is higher, then overwrite our running max.
		if  tempdict["dps"] > final_dict["dps"]:
		 	final_dict = tempdict
		 	#store the name for pretty-factor.
		 	maxname = i["name"]


print maxname + ": %.2f (%.2f + %.2f(AP) + %.2f(AD)) / %.2f(CD)" % (final_dict["dps"], final_dict["base"], final_dict["ap"], final_dict["ad"], final_dict["cd"])

