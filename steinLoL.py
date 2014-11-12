#The real workhorse here is requests. What a guy. http://docs.python-requests.org/en/latest/
import requests
##########################################################################
#### 					PLEASE READ THE README.TXT					  ####
####					FOR AN EXPLANATION OF CODE					  ####	
##########################################################################

def processSpell(spell, attack, ability, cdr):
	(dam_eff, maxdamage, apscale, adscale, base, dps, s_cost, stat_eff, b_eff) = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
	
	maxrank = spell["maxrank"]
	charge_penalty = 0
	cd = spell["cooldown"][maxrank-1] 
	#charge penalty = recharge/max charges. Remember that recharge is affected by cooldowns. 
	if spell["key"] == "MissileBarrage":
		#Corki's values in the API is not updated. I'm valuing correctness over elegance of code.
		charge_penalty = (8*((100-cdr)/100))/7
	elif spell["key"] == "ViE":
		charge_penalty = (8*((100-cdr)/100))/2
	cd *= ((100-cdr)/100)
	cd += charge_penalty
	# Read the section on this in the README under "Considerations"
	if spell["key"] == "PickACard":
		cd+=1

	#Sadly, there are some hard-to-overcome limitations in the API. Will hardcode some stuff here.
	# if spell["key"] == "BantamTrap":
		#There is no duration field in the API. Time to hard-code for DoT's :)
		

	s_cost = spell["cost"][maxrank-1]
	#Basically, this ignores the toggle-abilities.
	if spell["costType"] == ("Mana" or "Health" or "Heat" or "Energy" or "NoCost"):
		#Find the index for the Damage values. This avoids a healthy chunk of damage values that aren't
		# in effect[1]. 
		try:
			value_index = spell["leveltip"]["label"].index("Damage")+1
		except ValueError:
			try:
				value_index = spell["leveltip"]["label"].index("Base Damage")+1
			except ValueError:
				value_index = 0

		# Check for some malformed damage value indices (That is, the place they are in the ["leveltip"] array 
		# doesn't match its position in ["effect"]). This is our safety net.
		if spell["name"] in ["Tantrum", "Bullet Time", "Overload","Make It Rain"]:
			value_index -= 1
		elif spell["key"] in ["AzirE", "EliseHumanW", "FiddlesticksDarkWind", "XerathLocusOfPower2"]:
			value_index += 2
		elif spell["key"] in ["VolibearE","LuxLightStrikeKugel","YorickDecayed","GragasW","NamiW", "SorakaE", "UFSlash", "CaitlynYordleTrap", "SkarnerImpale", "Volley", "DianaOrbs", "HecarimW", "JarvanIVDemacianStandard", "LucianR"]:
			value_index += 1
		elif spell["key"] in ["JayceStaticField"]:
			value_index+=3
		elif spell["key"] =="PickACard": #Oh dear, this approach just dies on the inside when PaC becomes a thing. Good thing I caught this has fantastic ratios O_O
			value_index=1
		
		#If the damage field is null, then our damage is 0.
		if spell["effect"][value_index] == None:
			return {"stat": stat_eff, "dps": dps, "maxd": maxdamage, "ap": apscale, "ad": adscale, "base": base, "dam_eff": dam_eff, "cd":cd, "cost": s_cost,"b_eff": b_eff}
		else:
			base = spell["effect"][value_index][maxrank-1] # Let's get our basedamage.
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
				b_dps = base/spell["cooldown"][maxrank-1] #For stat efficiency, we need our base dps (dps without ap, cdr, or ad)
				if s_cost == 0:
					s_cost = 1 #Account for no-cost spells. IDK if there's any better way to really do that.
				dam_eff = dps/s_cost
				b_eff = b_dps/s_cost
				#Which spell will use its stats most efficiently? (efficiency with stats)/(efficiency without ap/ad/cdr)
				#Given our input (No mention)
				stat_eff = dam_eff/b_eff


			

			return {"stat": stat_eff, "dps": dps, "maxd": maxdamage, "ap": apscale, "ad": adscale, "base": base, "dam_eff": dam_eff, "cd":cd, "cost": s_cost,"b_eff": b_eff}
	else:
		return {"stat": stat_eff, "dps": dps, "maxd": maxdamage, "ap": apscale, "ad": adscale, "base": base, "dam_eff": dam_eff, "cd":cd, "cost": s_cost,"b_eff": b_eff}



#Gotta declare these as doubles so stuff doesn't go haywire with the DEEPS calculations.
ap_in = 0.0
ad_in = 0.0
cdr_in = 0.0

#Man, python input is dumb sometimes. Oh well, I won't make y'all download any more libraries than request.
ap_in = float(raw_input("Enter your given Ability Power (AP):\n"))
ad_in = float(raw_input("And now for your Attack Damage (AD):\n"))
cdr_in = float(raw_input("Finally, enter your Cooldown Reduction (CDR) as a percent, not a decimal:\n"))
while (cdr_in > 0 and cdr_in < 1) or cdr_in > 40:
	cdr_in = float(raw_input("CDR was malformed (You probably entered it as a decimal, not a whole number) or greater than 40. Please try again: \n"))



#And now, let requests work its magic!
key = "4a956ce8-2409-442a-a003-8f2784580237"
r = requests.get('https://na.api.pvp.net/api/lol/static-data/na/v1.2/champion?champData=spells&api_key='+key)
champList= r.json()["data"]

#This is for fun purposes only. I like to see where the numbers are coming from.
final_dict = {"stat": 0, "dps":0, "maxd":0, "ap":0, "ad":0, "base":0, "dam_eff": 0, "cd":0, "cost": 0, "b_eff":0}
maxname=""
templist = {"stat": 0, "dps":0, "maxd":0, "ap":0, "ad":0, "base":0, "dam_eff": 0, "cd":0, "cost": 0, "b_eff":0}
#So, obviously doing this linearly is the best option. O(n*4) is the best I can do since
#I have to look at every single spell in the game 
for k, v in champList.iteritems():
	#Iterate through this champion's spells
	for i in v["spells"]:
		#process the spell
		tempdict = processSpell(i, ad_in, ap_in, cdr_in)
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