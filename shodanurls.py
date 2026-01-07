from args import args
shodan_urls=[f"https://www.shodan.io/search?query={args.search}",f"https://www.shodan.io/search?query={args.search}&page=2"]
parameters=['country:US','country:BR','country:DE','country:IT','country:FR','country:GB']
shodan_url=f"https://www.shodan.io/search?query={args.search}"
if args.no_default is True and args.aditional_parameters == None:
    print("You cant use no default parameters and no additional parameters")
    exit()
elif args.no_default is True and args.aditional_parameters != None:
    parameters=[]
if args.aditional_parameters == None:
    args_parameters=args.aditional_parameters
elif args.aditional_parameters != None:
    args_parameters = args.aditional_parameters.split(",")
    for parameter in args_parameters:
        parameters.append(parameter)

for parameter in parameters:
    shodan_urls.append(shodan_url+"%20"+parameter)
    shodan_urls.append(shodan_url+"%20"+parameter+"&page=2")

if args.dont_chain:
    pass
elif not args.dont_chain:
    for parameter in parameters:
        for parameter2 in parameters:
            if parameter2 == parameter:
                pass
            else:
                if "port" in parameter and "port" in parameter2:
                    pass
                elif "country" in parameter and "country" in parameter2:
                    pass
                elif "city" in parameter and "city" in parameter2:
                    pass
                else:
                    shodan_urls.append(shodan_url+"%20"+parameter+"%20"+parameter2)
                    shodan_urls.append(shodan_url+"%20"+parameter+"%20"+parameter2+"&page=2")
        parameters.remove(parameter)