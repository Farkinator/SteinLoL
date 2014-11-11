#The real workhorse here is requests. What a guy. http://docs.python-requests.org/en/latest/
import requests
##########################################################################
#### 					PLEASE READ THE README.TXT					  ####
####					FOR AN EXPLANATION OF CODE					  ####	
##########################################################################

def processSpell(spell, attack, ability, cdr, is1v1, realism):
	(dam_eff, maxdamage, apscale, adscale, base, dps, s_cost, stat_eff) = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
	
	maxrank = spell["maxrank"]

	cd = spell["cooldown"][maxrank-1] * ((100-cdr)/100)


	#Sadly, there are some hard-to-overcome limitations in the API. Will hardcode some stuff here.
	# if spell["key"] == "BantamTrap":
		#There is no duration field in the API. Time to hard-code for DoT's :)
		

	s_cost = spell["cost"][maxrank-1]
	#Basically, this ignores the toggle-abilities.
	if spell["costType"] == ("Mana" or "Health" or "Heat" or "Energy"):
		#Find the index for the Damage values.
		try:
			value_index = spell["leveltip"]["label"].index("Damage")+1
		except ValueError:
			try:
				value_index = spell["leveltip"]["label"].index("Base Damage")+1
			except ValueError:
				value_index = 0

		# Check for some malformed damage value indices (That is, the place they are in the ["leveltip"] array 
		# doesn't match its position in ["effect"].)
		if spell["name"] in ["Tantrum", "Bullet Time", "Overload"]:
			value_index -= 1
		elif spell["key"] in ["AzirE", "EliseHumanW", "FiddlesticksDarkWind", "XerathLocusOfPower2"]:
			value_index += 2
		elif spell["key"] in ["NamiW", "SorakaE", "UFSlash", "CaitlynYordleTrap", "SkarnerImpale", "Volley", "DianaOrbs", "HecarimW", "JarvanIVDemacianStandard", "LucianR"]:
			value_index += 1
		
		#If the damage field is null, then our damage is 0.
		if spell["effect"][value_index] == None:
			return {"stat": stat_eff, "dps": dps, "maxd": maxdamage, "ap": apscale, "ad": adscale, "base": base, "dam_eff": dam_eff, "cd":cd, "cost": s_cost}
		else:
			base = spell["effect"][value_index][maxrank-1] # Normal thing.
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
			#Time for some teamfight considerations.
			if is1v1 == "false":
				#Karthus will ALWAYS do 5x damage with Requiem in a teamfight. Unless, of course, it gets silenced. That'd be mean.
				if spell["key"] == "KarthusFallenOne" and realism != "m":
					maxdamage*=5
					base*=5


			#This is the most basic measure I could come up with. Damage/Cooldown = dps.
			if cd != 0:
				dps = maxdamage/cd
				b_dps = base/spell["cooldown"][maxrank-1] #For stat efficiency, we need our base dps (dps without ap, cdr, or ad)
				if s_cost == 0:
					s_cost = 1 #Account for no-cost spells. IDK if there's any better way to really do that.
				dam_eff = dps/s_cost
				b_eff = b_dps/s_cost
				#Which spell will use its stats most efficiently? (efficiency with stats)/(efficiency without ap/ad/cdr)
				stat_eff = dam_eff/b_eff


			

			return {"stat": stat_eff, "dps": dps, "maxd": maxdamage, "ap": apscale, "ad": adscale, "base": base, "dam_eff": dam_eff, "cd":cd, "cost": s_cost}
	else:
		return {"stat": stat_eff, "dps": dps, "maxd": maxdamage, "ap": apscale, "ad": adscale, "base": base, "dam_eff": dam_eff, "cd":cd, "cost": s_cost}



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
is1v1 = raw_input("1v1(true) or Teamfight?(false)\n")
realism = raw_input("Realism with regards to aoe/skillshots: mean(m), realistic(r), optimistic(o)\n")

#And now, let requests work its magic!
key = "4a956ce8-2409-442a-a003-8f2784580237"
r = requests.get('https://na.api.pvp.net/api/lol/static-data/na/v1.2/champion?champData=spells&api_key='+key)
champList= r.json()["data"]

#This is for fun purposes only. I like to see where the numbers are coming from.
final_dict = {"stat": 0, "dps":0, "maxd":0, "ap":0, "ad":0, "base":0, "dam_eff": 0, "cd":0, "cost": 0}
maxname=""
templist = {"stat": 0, "dps":0, "maxd":0, "ap":0, "ad":0, "base":0, "dam_eff": 0, "cd":0, "cost": 0}
#So, obviously doing this linearly is the best option. O(n*4) is the best I can do since
#I have to look at every single spell in the game 
for k, v in champList.iteritems():
	#Iterate through this champion's spells
	for i in v["spells"]:
		#process the spell
		tempdict = processSpell(i, ad_in, ap_in, cdr_in, is1v1, realism)
		#if the dam_eff is higher, then overwrite our running max.
		if  tempdict["stat"] > final_dict["stat"]:
		 	final_dict = tempdict
		 	#store the name for pretty-factor.
		 	maxname = i["name"]
		 	champ = v["name"]

print maxname + " ("+champ+") is the most efficient spell!"
print "\tStat Efficiency: %.2f" %(final_dict["stat"]) 
print "\tDamage Efficiency: %.2f (%.2f(DPS)/%.2f(Spell Cost))" %(final_dict["dam_eff"], final_dict["dps"], final_dict["cost"])
print "\tDamage: %.2f (%.2f + %.2f(AP) + %.2f(AD)) / %.2f(CD)" % (final_dict["maxd"], final_dict["base"], final_dict["ap"], final_dict["ad"], final_dict["cd"])