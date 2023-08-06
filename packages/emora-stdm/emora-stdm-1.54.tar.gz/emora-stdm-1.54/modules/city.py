# -*- coding: utf-8 -*-
import json    
cities= {
    "houston": {
        "brief_intro": "houston is the most diverse metropolitan area in texas and has been described as the most racially and ethnically diverse major metropolis in the u.s.", 
        "culture": {
            "music": "houston has a lively music scene and while it can claim no broad genre as its own.", 
            "car love": "automobiles of all kinds have had enormous influence on houston culture, largely a result of the urban sprawl and sparse public transportation that has followed the dismantling of the citys former trolley system."
        }, 
        "reason_for_travel": "it is the perfect city for a friends getaway, a couples retreat, or a family vacation.", 
        "sports": "houston has sports teams for every major professional league except the national hockey league.", 
        "tourist_attraction": {
            "the theater district": "the theater district is a 17-block area in the heart of downtown houston, is home to bayou place entertainment complex, restaurants, movies, plazas, and parks. bayou place is a large multilevel building that is home to restaurants, bars, live music,and so on.", 
            "hermann park": "hermann park houses the houston zoo and the houston museum of natural science, and memorial park.", 
            "space center houston": "space center houston  is the official visitors center of nasas lyndon b. johnson space center. space center houston includes many interactive exhibits including moon rocks and a shuttle simulator in addition to special presentations that tell the story of nasas manned space flight program."
        }, 
        "famous_food": {
            "tex-mex cuisine": "tex-mex cuisine from texas and mexican is an american regional cuisine that derives from the culinary creations of the tejano people of texas.", 
            "cajun food": "cajun food is a style of cooking named for the french-speaking acadian people deported by the british from acadia in canada to what is now called the acadiana region of louisiana."
        }, 
        "event": {
            "houston gay pride parade": "houston gay pride parade is held at the end of june to commemorate the struggle for gay liberation, gay rights, gay pride, and the stonewall riots of the late 1960s in new york city.", 
            "houston livestock show and rodeo": "houston livestock show and rodeo is held over 20 days from late february through early march. the event begins with trail rides that originate from several points throughout the state, all of which convene at reliant park for a barbecue cook-off. the rodeo includes typical rodeo events, as well as concert performances from major artists and carnival rides."
        }
    }, 
    "macau": {
        "brief_intro": "macau is a city and special administrative region on the western side of the pearl river estuary in southern china. ", 
        "culture": {
            "religion": "the primary religion is buddhism. roman catholicism has considerable influence in education and social welfare in macau."
        }, 
        "reason_for_travel": " it is famous for the blend of portuguese and chinese cultures and its gambling industry", 
        "sports": "despite its small area, macau is home to a variety of sports and recreational facilities that have hosted a number of major international sporting events, including the 2005 east asian games, the 2006 lusophony games, and the 2007 asian indoor games.", 
        "tourist_attraction": {
            "the historic centre of macau": "the historic centre of macau includes some twenty-five historic locations"
        }, 
        "famous_food": {
            "galinha portuguesa": "galinha portuguesa is an example of a chinese dish that draws from macanese influences, but is not part of macanese cuisine", 
            "portuguese food": "portuguese food was adapted to use local ingredients, such as fresh seafood, turmeric, coconut milk, and adzuki beans. these adaptations produced macanese variations of traditional portuguese dishes including caldo verde, minchee, and cozido portuguesa."
        }, 
        "event": {
            "lunar chinese new year": "lunar chinese new year is the most important traditional festival and celebration normally takes place in late january or early february.", 
            "macau grand prix": "macau grand prix is a motorsport road race for automobiles and motorcycles held annually in macau. it is the only street circuit racing event in which both cars and motorcycles participate."
        }
    }, 
    "new orleans": {
        "brief_intro": "it is a consolidated city-parish located along the mississippi river in the southeastern region of the u.s. state of louisiana.", 
        "culture": {
            "music": "new orleans has always been a significant center for music with its intertwined european, latin american, and african-american cultures."
        }, 
        "reason_for_travel": "has the mix of cultures, with strong french and spanish influences,and is more reminiscent of the caribbean than the united states. cajun and creole cuisine, jazz music, and the architecture of the french quarter set this city apart and make it a perfect destination for a long weekend getaway.", 
        "sports": "the city also hosts two college football bowl games annually: the new orleans bowl and the sugar bowl. the city also holds the bayou classic, which is an annual college football game between grambling state university and southern university. nine super bowls have been contested in new orleans.", 
        "tourist_attraction": {
            "the french quarter": "the french quarter is the district as a whole has been designated as a national historic landmark, with numerous contributing buildings that are separately deemed significant. it is a prime tourist destination in the city, as well as attracting local residents.", 
            "the natchez": "the natchez is an authentic steamboat with a calliope that cruises the length of the city twice daily.", 
            "the national wwii museum": "the national wwii museum offers a multi building odyssey through the history of the pacific and european theaters.", 
            "treme community": "treme community contains the new orleans jazz national historical park and the new orleans african american museum, a site which is listed on the louisiana african american heritage trail."
        }, 
        "famous_food": {
            "local cuisines": "local cuisines are distinctive and influential. from centuries of amalgamation of local creole, haute creole, cajun, and new orleans french cuisines, new orleans food has developed. local ingredients combined with french, spanish, italian,and so on produce a truly unique and easily recognizable louisiana flavor.", 
            "creole cuisine": "creole cuisine is po boy and italian muffuletta sandwiches; gulf oysters on the half-shell, boiled crawfish, and other seafood as well as creole dishes.", 
            "beignets": "beignets are square-shaped fried pastries that could be called french doughnuts, served with coffee and chicory, known as cafe au lait."
        }, 
        "event": {
            "new orleans jazz & heritage festival": "new orleans jazz & heritage festival is the largest of the citys many musical festivals is the new orleans jazz & heritage festival. commonly referred to simply as, jazz fest, it is one of the largest music festivals in the nation, and features crowds coming from all over the world to experience music, food, arts, and crafts.", 
            "southern decadence": "southern decadence is a new orleans-style celebration of the gay community. it is a six-day event that attracts over 160,000 locals and visitors. the annual event began in 1972 to empower the gay community of south louisiana and has grown to be one of the largest gay events in the nation.", 
            "mardi gras": "mardi gras is held just before the beginning of the catholic liturgical season of lent. mardi gras celebrations include parades and floats; participants toss strings of cheap colorful beads and doubloons to the crowds. the mardi gras season is kicked off with the only parade allowed through the french quarter, a walking parade aptly named krewe du vieux."
        }
    }, 
    "london": {
        "brief_intro": "london is the capital and largest city of england and the united kingdom.", 
        "culture": {
            "music": "london is famous for its rock scene, and was the starting point of some of the greatest 60s and 70s artists such as david bowie, iron maiden"
        }, 
        "reason_for_travel": "cultural tourism is growing as london became the second most visited city in the world in 2017, and many travellers come here to enjoy the british way of living. ", 
        "sports": "london is the home of many professional sport teams and has hosted various international sporting events, including the summer olympics in 1908, 1948, and 2012. football is very popular and london is home to wembley stadium as well as club stadiums such as the emirates stadium, stamford bridge and tottenham hotspur stadium. ", 
        "tourist_attraction": {
            "the tower of london": "the tower of london is a historic castle located on the north bank of the river thames in central london.", 
            "british museum": "british museum , in the bloomsbury area of london, united kingdom, is a public institution dedicated to human history, art and culture.", 
            "the national gallery": "the national gallery is an art museum in trafalgar square in the city of westminster, in central london. "
        }, 
        "famous_food": {
            "sunday roast with yorkshire pudding": "sunday roast with yorkshire pudding sunday roast is a true british classic. traditionally this meal is eaten any time from noon to 5 pm on sundays.", 
            "fish n chips": "fish n chips theres nothing that says british food like fish & chips. known the world over, this traditional british dish is on the top of any foodie list for visitors to london and the u.k.", 
            "full english breakfast": "full english breakfast  traditionally, you need to find a dish that incorporates: sausages, eggs, mushrooms, tomatoes, mushrooms, blood pudding, potatoes, and toast."
        }, 
        "event": {
            "carnaval del pueblo": "carnaval del pueblo is europes greatest latin american festival, held on the first sunday of august each year. seven countries participate in this street procession, which ends in burgess park.", 
            "notting hill carnival": "notting hill carnival is the worlds second largest carnival. it has a distinctly afro-caribbean flavour, and highlights include a competition between londons steelpan bands and a 3-mile street parade with dancing and music"
        }
    }, 
    "san francisco": {
        "brief_intro": "a popular tourist destination, san francisco is known for its cool summers, fog, steep rolling hills, eclectic mix of architecture, and landmarks, including the golden gate bridge, cable cars, the former alcatraz federal penitentiary, fishermans wharf, and its chinatown district.", 
        "culture": {
            "lgbt": "san francisco has long had an lgbt-friendly history. the citys large gay population has created and sustained a politically and culturally active community over many decades, developing a powerful presence in san franciscos civic life.", 
            "liberal activism": "with the arrival of the beat writers and artists of the 1950s and societal changes culminating in the summer of love in the haight-ashbury district during the 1960s, san francisco became a center of liberal activism and of the counterculture that arose at that time.", 
            "technology": "since the 1990s, the demand for skilled information technology workers from local startups and nearby silicon valley has attracted white-collar workers from all over the world and created a high standard of living in san francisco.", 
            "international character": "the international character that san francisco has enjoyed since its founding is continued today by large numbers of immigrants from asia and latin america.", 
            "liberal activism more": "the democrats and to a lesser extent the green party have dominated city politics since the late 1970s, after the last serious republican challenger for city office lost the 1975 mayoral election by a narrow margin."
        }, 
        "reason_for_travel": "as of 2019, san francisco is the highest rated american city on world liveability rankings.", 
        "sports": "major league baseballs san francisco giants have played in san francisco since moving from new york in 1958.", 
        "tourist_attraction": {
            "golden gate bridge": "golden gate bridge is one of the most internationally recognized symbols of san francisco, california, and the united states, the frommers travel guide describes the golden gate bridge as possibly the most beautiful, certainly the most photographed, bridge in the world.", 
            "the alcatraz federal penitentiary": "the alcatraz federal penitentiary is a public museum and one of san franciscos major tourist attractions, attracting some 1 point 5 million visitors annually."
        }, 
        "famous_food": {
            "asian cuisines": "asian cuisines are popular in this city due to its diverse cultural background, san francisco is famous for its authentic asian cuisine from eastern asia and southeast asia, including chinese, korean and filipino cuisines."
        }, 
        "event": {
            "st. patricks day festival and parade": "st. patricks day festival and parade is to celebrate san franciscos irish culture, make a point to attend the st. patricks day parade in town. thousands of people join in the fun here to learn about irish traditions, dancing, songs, and watch colorful floats and marching bands make their way down the street.", 
            "cherry blossom festival": "cherry blossom festival is a fun way to get to know the various cultures of san francisco is to attend the cherry blossom festival in japantown. the event features a parade, cultural performances, martial arts demonstrations, live music, and many more traditional activities that define the way of life in japan. the northern california cherry blossom festival typically takes place in mid-april."
        }
    }, 
    "seattle": {
        "brief_intro": "seattle was the fastest-growing major u.s. city in july 2016, with a 3.1% annual growth rate.seattle is the northernmost large city in the united states.", 
        "culture": {
            "movie house": "the city also has movie houses showing both hollywood productions and works by independent filmmakers.", 
            "performing art": "seattle has been a regional center for the performing arts for many years.", 
            "grunge music": "seattle is considered the home of grunge music."
        }, 
        "reason_for_travel": "seattles mild, temperate, marine climate allows year-round outdoor recreation, including cycling, hiking, snowboarding, and swimming.", 
        "sports": "seattle has three major mens professional sports teams: the national football leagues seattle seahawks, major league baseballs seattle mariners, and major league soccers seattle sounders fc. other professional sports teams include the womens national basketball associations seattle storm, who won the wnba championship on three occasions in 2004 and 2010, and 2018; and the seattle reign of the national womens soccer league.", 
        "tourist_attraction": {
            "cruise": "cruise is a popular choice. since the middle 1990s, seattle has experienced significant growth in the cruise industry, especially as a departure point for alaska cruises. in 2008, a record total of 886,039 cruise passengers passed through the city, surpassing the number for vancouver, bc, the other major departure point for alaska cruises."
        }, 
        "famous_food": {
            "chinese cuisine": "chinese cuisine is very popular in the city because of its large chinese american population and its long chinese immigrant history."
        }, 
        "event": {
            "sea fair": "sea fair has celebrated just that when hosting about eight weeks of events from june through august. the 75 happenings include the torchlight parade and the popular seafair weekend festival, during which everyone with a boat takes to the water to watch the blue angels, hydroplane races and the sunset turning mt. rainier red.", 
            "bumbershoot": "bumbershoot is a three-day festival has been seattleites last summer hurrah since 1971. taking place beneath the space needle and aptly named bumbershoot which an old colloquial term for an umbrella, it is one of the largest annual international music and arts festivals in north america."
        }
    }, 
    "chicago": {
        "brief_intro": "chicago is an international hub for finance, culture, commerce, industry, education, technology, telecommunications, and transportation.", 
        "culture": {
            "artist": "in 1968 and 1969, members of the chicago imagists, such as roger brown and others produced bizarre representational paintings."
        }, 
        "reason_for_travel": "in 2013, chicago was chosen as one of the top ten cities in the united states to visit for its restaurants, skyscrapers, museums, and waterfront, by the readers of cond nast traveler.", 
        "sports": "the city has two major league baseball teams: the chicago cubs of the national league play in wrigley field on the north side; and the chicago white sox of the american league play in guaranteed rate field on the south side. chicago is the only city that has had more than one mlb franchise every year since the al began in 1901.", 
        "tourist_attraction": {
            "the willis tower": "the willis tower has an observation deck open to tourists year round with high up views overlooking chicago and lake michigan. the observation deck includes an enclosed glass balcony that extends 10 feet out on the side of the building. tourists are able to look straight down.", 
            "navy pier": "navy pier is located just east of streeterville, and is 3,000 ft long and houses retail stores, restaurants, museums, exhibition halls and auditoriums. in the summer of 2016, navy pier constructed a dw60 ferris wheel.", 
            "alinea ": "alinea  is one the worlds most decorated restaurants and a recipient of three michelin stars. well-known chefs who have had restaurants in chicago include: charlie trotter and rick tramonto, etc."
        }, 
        "famous_food": {
            "chicken vesuvio": "chicken vesuvio is roasted bone-in chicken cooked in oil and garlic next to garlicky oven-roasted potato wedges and a sprinkling of green peas.", 
            "chicago-style hot dog": "chicago-style hot dog is typically an all-beef hot dog and loaded with an array of toppings that often includes pickle relish, yellow mustard, pickled sport peppers, tomato wedges, dill pickle spear and topped off with celery salt on a poppy seed bun.", 
            "italian beef sandwich": "italian beef sandwich is a distinctly chicago sandwich that is thinly sliced beef simmered in au jus and served on an italian roll with sweet peppers or spicy giardiniera."
        }, 
        "event": {
            "lollapalooza and the pitchfork music festival": "lollapalooza and the pitchfork music festival are annual festivals feature various acts."
        }
    }, 
    "paris": {
        "brief_intro": "paris is the capital and most populous city of france", 
        "culture": {
            "painting and sculpture": "painting and sculpture became the pride of the french monarchy and the french royal family commissioned many parisian artists to adorn their palaces during the french baroque and classicism era. "
        }, 
        "reason_for_travel": "a culturally dynamic city with their history and impressive architecture, paris's monuments undoubtedly contribute to the charm of the french capital. ", 
        "sports": "paris hosted the 1900 and 1924 summer olympics and will host the 2024 summer olympics and paralympic games.", 
        "tourist_attraction": {
            "the arc de triomphe": "the arc de triomphe is one of the most famous monuments in paris, france, standing at the western end of the champs-\\u00c9lys\\u00e9es at the centre of place charles de gaulle", 
            "the sacr\\u00e9 c\\u0153ur basilica": "the sacr\\u00e9 c\\u0153ur basilica is a roman catholic church and minor basilica, dedicated to the sacred heart of jesus, in paris, france. it is a popular landmark and the second most visited monument in paris", 
            "the eiffel tower": "the eiffel tower is a wrought-iron lattice tower on the champ de mars in paris, france. it is named after the engineer gustave eiffel, whose company designed and built the tower."
        }, 
        "famous_food": {
            "falafel": "falafel is just as parisian as a ham sandwich nowadays", 
            "couscous": "couscous a famous type of parisian comfort food", 
            "french oysters": "french oysters  are renowned for their quality, and there are many different varieties from different parts of the french coastline."
        }, 
        "event": {
            "bastille day": "bastille day , a celebration of the storming of the bastille in 1789, the biggest festival in the city, is a military parade taking place every year on 14 july on the champs-\\u00c9lys\\u00e9es, from the arc de triomphe to place de la concorde.", 
            "paris plages": "paris plages is a festive event that lasts from mid-july to mid-august when the right bank of the seine is converted into a temporary beach with sand, deck chairs and palm trees"
        }
    }, 
    "san diego": {
        "brief_intro": "the city is known for its mild year-round climate, natural deep-water harbor, extensive beaches, long association with the united states navy, and recent emergence as a healthcare and biotechnology development center.", 
        "culture": {
            "military": "san diego has been a military town for more than 100 years.", 
            "art": "san diego has a small, but growing art scene."
        }, 
        "reason_for_travel": "the city has beaches and surfing if youre dreaming of long, sunny days spent relaxing on the beach then look no further than san diego.", 
        "sports": "includes one major professional sports team, several teams from minor professional leagues, semi-pro and amateur teams, and college teams, in addition to other sporting events. the most popular sports team in san diego is the san diego padres of major league baseball. also popular are the college sports teams of the san diego state aztecs, which play in ncaa division i.", 
        "tourist_attraction": {
            "balboa park": "balboa park is an urban cultural park in san diego, california, united states.in addition to open space areas, natural vegetation zones, green belts, gardens, and walking paths.", 
            "blacks beach": "blacks beach is the one of the largest nude beaches in the united states and is popular with southern californian nudists and naturists."
        }, 
        "famous_food": {
            "local wines": "local wines include san pasqual valley, rancho bernardo, julian.", 
            "mexican food": "mexican food includes carne asada, street tacos, california burritos, and so on."
        }, 
        "event": {
            "san diego comic-con international ": "san diego comic-con international  is a non-profit multi-genre entertainment and comic book convention held annually in san diego, california, united states. the name, as given on its website, is comic-con international.", 
            "the san diego jewish film festival": "the san diego jewish film festival aims to educate and illuminate audiences by offering an array of films that depict elements of the jewish life, history, and culture in challenging, moving, and humorous ways as never seen before.", 
            "precious festa": "precious festa is the largest italian festival in the western u.s. in little italy."
        }
    }, 
    "philadelphia": {
        "brief_intro": "philadelphia remained the nations largest city until being overtaken by new york city in 1790; the city was also one of the nations capitals during the revolution, serving as temporary u.s. capital while washington, d.c. was under construction.", 
        "culture": {
            "recreations": "areas such as south street and old city have a vibrant night life.", 
            "art museums": "the city contains many art museums, such as the pennsylvania academy of the fine arts and the rodin museum, which holds the largest collection of work by auguste rodin outside france."
        }, 
        "reason_for_travel": "due to its rich historical treasure, and its economic and educational progress, philadelphia is a great place to visit.", 
        "sports": "the city is one of 13 u.s. cities to have teams in all four major league sports: the philadelphia phillies in the national league of major league baseball, the philadelphia eagles of the national football league, the philadelphia flyers of the national hockey league, and the philadelphia 76ers of the national basketball association.", 
        "tourist_attraction": {
            "reading terminal market": "reading terminal market is a historic food market founded in 1893 in the reading terminal building, a designated national historic landmark. the enclosed market is one of the oldest and largest markets in the country, hosting over a hundred merchants offering pennsylvania dutch specialties, artisan cheese and meat and locally grown groceries, etc.", 
            " independence national historical park ": " independence national historical park  is united states national park in philadelphia that preserves several sites associated with the american revolution and the nations founding history."
        }, 
        "famous_food": {
            "city specials": "city specials are its hoagies, roast pork sandwich, and the cheesesteak sandwich which was developed by italian immigrants, etc."
        }, 
        "event": {
            "qflix philadelphia": "qflix philadelphia is philadelphias only lgbtq film festival shows the latest and best queer-centric indie flicks on screens across center city. the week also includes a chance to get out and mingle with other film buffs at networking events and meet some of the films stars and directors.", 
            "israeli film festival": "israeli film festival is the nearly month-long israeli film festival returns to venues across the city with films that celebrate the israeli experience and israeli culture. the festival includes screenings of documentaries and feature-length films encompassing poignant dramas, lighthearted comedies and more."
        }
    }, 
    "kuala lumpur": {
        "brief_intro": "kuala lumpur, commonly known as kl, is the national capital and largest city in malaysia.", 
        "culture": {
            "museum": "kuala lumpur has a craft complex coupled with a museum that displays a variety of textile, ceramic, metal craft and weaved products."
        }, 
        "reason_for_travel": "kuala lumpur is a hub for cultural activities and events in malaysia.it was touted as one of the host cities for the formula one world championship from 1999 to 2017.", 
        "sports": "kuala lumpur has numerous parks, gardens and open spaces for recreational purposes.", 
        "tourist_attraction": {
            "petronas twin towers": "petronas twin towers were the tallest buildings in the world from 1998 to 2004, until they were surpassed by taipei 101.", 
            "the bukit bintang shopping district": "the bukit bintang shopping district is the shopping and entertainment district of kuala lumpur.", 
            "islamic arts museum": "islamic arts museum houses more than seven thousand islamic artefacts including rare exhibits as well as a library of islamic art books, is the largest islamic arts collection in southeast asia."
        }, 
        "famous_food": {
            "curry laksa": "curry laksa is a type of noodle soup made with a fragrant spicy coconut soup base.", 
            "char kuey teow": "char kuey teow of chinese origin from the teochew area. it\\u2019s flat rice noodles stir-fried with egg, sprouts, prawns, and cockles.", 
            "nasi lemak ": "nasi lemak  is malaysia\\u2019s national dish, the simplest version of nasi lemak is just coconut rice, sambal paste, fried anchovies, peanuts, and hard boiled egg. fancier versions will have fried chicken or chicken rendang on the side."
        }, 
        "event": {
            "kreative asia": "kreative asia gathers local, regional and international experts in the creative industry who are involved in the creation, development and delivery of interactive content, arts, community and applications.", 
            "mega sale event": "mega sale event is held three times a year \\u2013 in march, may and december \\u2013 during which all shopping malls are encouraged to participate to boost kuala lumpur as a leading shopping destination in asia which being maintained until present with new mega sales"
        }
    }, 
    "new york": {
        "brief_intro": "it is the most populous city in the united states abd the largest metropolitan area in the world by urban landmass. new york city has been described as the cultural, financial, and media capital of the world, and exerts a significant impact upon commerce,entertainment, research, technology,and sports, etc.", 
        "culture": {
            "art organizations": "new york city has more than 2,000 arts and cultural organizations and more than 500 art galleries of all sizes."
        }, 
        "reason_for_travel": "many districts and landmarks in new york city are well known, including three of the worlds ten most visited tourist attractions in 2013. several sources have ranked new york the most photographed city in the world.", 
        "sports": "new york city is home to the headquarters of the national football league, major league baseball, the national basketball association,the national hockey league,and major league soccer.the new york metropolitan area hosts the most sports teams in the four major north american professional sports leagues with nine, one more than los angeles, and has 11 top-level professional sports teams if major league soccer is included, also one more than los angeles.", 
        "tourist_attraction": {
            "broadway theater": "broadway theater is one of the premier forms of english-language theatre in the world, named after broadway, the major thoroughfare that crosses times square.", 
            "times square": "times square is the brightly illuminated hub of the broadway theater district,one of the worlds busiest pedestrian intersections,and a major center of the worlds entertainment industry.", 
            "the statue of liberty": "the statue of liberty is a figure of libertas, a robed roman liberty goddess. she holds a torch above her head with her right hand, and in her left hand carries a tabula ansata inscribed in roman numerals with july 4th, 1776, the date of the u.s. declaration of independence. a broken shackle and chain lie at her feet as she walks forward, commemorating the recent national abolition of slavery.", 
            "the empire state building": "the empire state building is an american cultural icon. since its opening, the buildings art deco architecture and open-air observation deck has made it a popular attraction, with around 4 million tourists from around the world visiting the buildings 86th and 102nd floor observatories every year."
        }, 
        "famous_food": {
            "central and eastern european cuisine": "central and eastern european cuisine is brought by central and eastern european immigrants, especially jewish immigrants from those regions,who brought bagels, cheesecake, and delicatessens or delis to the city.", 
            "middle eastern cuisine": "middle eastern cuisine includes falafel and kebabs are examples of modern new york street food are popular in this city.", 
            "italian cuisine": "italian cuisine such as new york-style pizza and other italian food, is brought by italian immigrants into the city."
        }, 
        "event": {
            "parades": "parades is very well known in new york city, which celebrate a broad array of themes, including holidays, nationalities, human rights, and major league sports team championship victories. the majority of parades are held in manhattan."
        }
    }, 
    "washington dc": {
        "brief_intro": "it is formally the district of columbia and commonly referred to as d.c., washington, or the district, and is the capital of the united states.", 
        "culture": {
            "indie culture and music": "the district is an important center for indie culture and music in the united states.", 
            "art": "washington, d.c., is a national center for the arts."
        }, 
        "reason_for_travel": "the spring and summer weather here is glorious.", 
        "sports": "washington is one of 13 cities in the united states with teams from all four major professional mens sports and is home to one major professional womens team. the washington wizards in nba, the washington capitals in nhl, and the washington mystics in womens national basketball association play at the capital one arena in chinatown. nationals park, which opened in southeast d.c.", 
        "tourist_attraction": {
            "lincoln memorial": "lincoln memorial is an american national memorial built to honor the 16th president of the united states, abraham lincoln.", 
            "u.s. capitol": "u.s. capitol is among the most architecturally impressive and symbolically important buildings in the world. the senate and the house of representatives have met here for more than two centuries. begun in 1793, the capitol has been built, burnt, rebuilt, extended, and restored; today, it stands as a monument not only to its builders but also to the american people and their government.", 
            "smithsonian national museum of natural history": "smithsonian national museum of natural history established in 1910 and located on the national mall, is part of the smithsonian institution, and holds the worlds most extensive collection of natural history specimens and human artifacts including the remains of dinosaurs and tools used by early man."
        }, 
        "famous_food": {
            "chicken thighs with pepperoni sauce": "chicken thighs with pepperoni sauce are so special that its hard to make top chef judges swoon, so it was quite a surprise when mike isabellas pepperoni sauce turned out to be a real panty dropper on the show. padma and tom both went wild for it.", 
            "half smokes": "half smokes are the dcs trademark sausage has a murky history, but at its spicy, sauced-up best, the hot dog-like concoction really satisfies.", 
            "fried chicken": "fried chicken is made by a french culinary icon. the secret? its in the crust. chef richard breads the chicken with lumps of country bread before frying it in clarified butter. central serves the golden brown goodness with mashed potatoes that are just as addictive."
        }, 
        "event": {
            "dc jazz festival": "dc jazz festival is a cant-miss event on the districts cultural calendar, inviting visitors of all ages to celebrate all things jazz each summer. as the citys premier jazz festival, the event serves up a diverse selection of national and international masterclass jazz artists, performing in a wide array of venues reaching every quadrant and corner of the city. like much of dc, many concerts during the festival are free, so theres no need to worry about costs piling up to catch a great show!", 
            "national cherry blossom festival": "national cherry blossom festival is to welcome spring. nothing signifies the arrival of spring in dc quite like the blooming of the cherry blossom trees and the national cherry blossom festival to celebrate the occasion.", 
            "passport dc": "passport dc is a month-long festival in may that pays tribute to washington, dcs thriving international culture. as part of the festival, the first two saturdays in may are devoted to embassy open houses. thanks to this only-in-dc experience, you can step inside a foreign embassy with the around the world embassy tour and the eu open house."
        }
    }, 
    "singapore": {
        "brief_intro": "singapore is a sovereign city-state and island country located in maritime southeast asia.", 
        "culture": {
            "arts": "since the 1990s when the national arts council was created to spearhead the development of performing arts, visual and literary art forms, to hasten a vibrant cosmopolitan gateway between the east and west", 
            "music": "singapore has a diverse music culture that ranges from pop and rock, to folk and classical. western classical music plays a significant role in the cultural life in singapore"
        }, 
        "reason_for_travel": "singapore promotes itself as a medical tourism hub, with about 200,000 foreigners seeking medical care there each year.", 
        "sports": "water sports are some of the most popular in singapore.singapores table tennis women team reached their peak as silver medalists at the 2008 beijing olympics.", 
        "tourist_attraction": {
            "the orchard road district": "the orchard road district which contains multi-storey shopping centres and hotels, can be considered the center of shopping and tourism in singapore", 
            "the singapore zoo": "the singapore zoo has embraced the open zoo concept whereby animals are kept in enclosures, separated from visitors by hidden dry or wet moats, instead of caging the animals, and the river safari has 300 species of animals, including numerous endangered species."
        }, 
        "famous_food": {
            "hainanese chicken rice": "hainanese chicken rice based on the hainanese dish wenchang chicken, is considered singapores national dish", 
            "street food": "street food has long migrated into hawker centres with communal seating areas. typically, these centres have a few dozen to hundreds of food stalls, with each specialising in a single or a number of related dishes. the choices are almost overwhelming even for locals."
        }, 
        "event": {
            "vesak day": "vesak day is celebrated all over the world by followers of buddhism. it marks the enlightenment and death of buddha. during this festival in singapore, devotees are often found meditating and doing a significant amount of charity work.", 
            "singapore food festival": "singapore food festival celebrates singapores cuisine is held in july annually."
        }
    }, 
    "bangkok": {
        "brief_intro": "bangkok is the capital and most populous city of thailand.", 
        "culture": {
            "art": "traditional thai art, developed within religious and royal contexts, continues to be sponsored by various government agencies in bangkok, including the department of fine arts office of traditional arts. "
        }, 
        "reason_for_travel": "bangkoks multi-faceted sights, attractions and city life appeal to diverse groups of tourists. ", 
        "sports": "as is the national trend, association football and muay thai dominate bangkoks spectator sport scene. horse racing, highly popular at the mid-20th century, still takes place at the royal bangkok sports club.", 
        "tourist_attraction": {
            "the giant swing and erawan shrine": "the giant swing and erawan shrine demonstrate hinduisms deep-rooted influence in thai culture. ", 
            "grand palace and major buddhist temples": "grand palace and major buddhist temples are among bangkoks well-known sights including wat phra kaew, wat pho, and wat arun. ", 
            "vimanmek mansion": "vimanmek mansion in dusit palace is famous as the worlds largest teak building, while the jim thompson house provides an example of traditional thai architecture. "
        }, 
        "famous_food": {
            "thai fried chicken": "thai fried chicken  is out of the world. its even better and more addictive than the ones you get in fast food restaurants! the secret is in the marinade and batter and one will definitely not be enough.", 
            "grilled pork": "grilled pork is a sweet, succulent and tender piece of meat on a stick. this particular stall, moo ping hea owen is recommended by many locals", 
            "sweet potato balls": "sweet potato balls is lightly crisp on the outside and airily soft on the inside. "
        }, 
        "event": {
            "songkran": "songkran during which traditional rituals as well as water fights take place throughout the city.", 
            "loi krathong": "loi krathong ,usually in november, is accompanied by the golden mount fair. "
        }
    }, 
    "honolulu": {
        "brief_intro": "it is the largest city and state capital city of hawaii, within the county of honolulu.", 
        "culture": {
            "visual arts": "the honolulu museum of art is endowed with the largest collection of asian and western art in hawaii.the honolulu museum of art is endowed with the largest collection of asian and western art in hawaii.", 
            "music": "established in 1900, the honolulu symphony is the second oldest us symphony orchestra west of the rocky mountains."
        }, 
        "reason_for_travel": "it is ranked high on world livability rankings, and was also ranked as the 2nd safest city in the u.s.", 
        "sports": "honolulu has no professional sports teams. but still, honolulus tropical climate lends itself to year-round activities. in 2004, mens fitness magazine named honolulu the fittest city in the united states.", 
        "tourist_attraction": {
            "bishop museum": "bishop museum is the largest of honolulus museums. it is endowed with the states largest collection of natural history specimens and the worlds largest collection of hawaiiana and pacific culture artifacts.", 
            "uss arizona memorial": "uss arizona memorial is at pearl harbor in honolulu, hawaii, and marks the resting place of 1102 of the 1177 sailors and marines killed on uss arizona during the japanese surprise attack on pearl harbor on december 7, 1941 and commemorates the events of that day.", 
            "waikiki beach": "waikiki beach is one of americas top beaching destinations, with all the comforts of north america on a beautiful tropical island in the pacific ocean."
        }, 
        "famous_food": {
            "lomi-lomi": "lomi-lomi is a must try for those who love fish. traditionally served as a side salad dish at laus feasts, it consists of chopped raw salmon and diced tomatoes and onions massaged together by hand. lomi lomi means massage in hawaiian.", 
            "poke": "poke is a traditional and healthy hawaiian dish: the poke bowl. the standard poke consists of cubed raw ahi tuna smothered in sauce and served with a side of rice.", 
            "kalua pig": "kalua pig is the centrepiece of hawaiian feasts and once reserved for only the chiefs and king of hawaiian society at laus feasts, kalua pig is now a dish that can be enjoyed by all."
        }, 
        "event": {
            "hawaii international film festival": "hawaii international film festival showcases some of the best films from producers all across the pacific rim and is the largest east meets west style film festival of its sort in the united states", 
            "honolulu marathon": "honolulu marathon is held annually on the second sunday in december, draws more than 20,000 participants each year, about half to two thirds of them from japan."
        }
    }, 
    "atlanta": {
        "brief_intro": "the city serves as the cultural and economic center of the atlanta metropolitan area,home to 5.9 million people and the ninth largest metropolitan area in the nation.revitalization of atlantas neighborhoods, initially spurred by the 1996 summer olympics, has intensified in the 21st century, altering the citys demographics, politics, aesthetics, and culture.", 
        "culture": {
            "art museums": "as a national center for the arts, atlanta is home to significant art museums and institutions.", 
            "street art": "atlanta has become one of the usas best cities for street art in recent years.", 
            "art companies": "atlanta is one of few united states cities with permanent, professional, and resident companies in all major performing arts disciplines."
        }, 
        "reason_for_travel": "atlanta contains a notable number of historical museums and sites.", 
        "sports": "atlanta is home to professional franchises for four major team sports: the atlanta braves of major league baseball, the atlanta hawks of the national basketball association, the atlanta falcons of the national football league, and atlanta united fc of major league soccer.", 
        "tourist_attraction": {
            "georgia aquarium": "georgia aquarium is the most popular attraction among visitors to atlanta, and the worlds largest indoor aquarium.", 
            "the world of coca-cola": "the world of coca-cola features the history of the world-famous soft drink brand and its well-known advertising.", 
            "the atlanta cyclorama & civil war museum": "the atlanta cyclorama & civil war museum houses a massive painting and diorama in-the-round, with a rotating central audience platform, depicting the battle of atlanta in the civil war.", 
            "martin luther king jr. national historic site": "martin luther king jr. national historic site includes the preserved childhood home of dr. martin luther king jr., as well as his final resting place."
        }, 
        "famous_food": {
            "barbecue": "barbecue restaurants here are sure to satisfy anyones craving for spicy, slow-cooked deliciousness.", 
            "burgers": "burgers are popular here. yes, its true that you can get a hamburger pretty much anywhere, but atlanta is home to several burger restaurants that far surpass your typical burger-doodle joint."
        }, 
        "event": {
            "festivals": "festivals in atlanta are more than any city in the southeastern united states.some notable festivals in atlanta include atlanta pride, the little five points halloween festival, and so on."
        }
    }, 
    "dubai": {
        "brief_intro": "dubai is the most populous city in the united arab emirates and the capital of the emirate of dubai", 
        "culture": {
            "dress code": "the emirati attire is typical of several countries in the arabian peninsula.", 
            "night life": "dubai is known for its nightlife. clubs and bars are found mostly in hotels because of liquor laws."
        }, 
        "reason_for_travel": "dubai is one of the few cities in the middle east that are very open to welcoming tourists.", 
        "sports": "football and cricket are the most popular sports in dubai. three teams, al wasl fc, shabab al-ahli dubai fc and al nasr sc, represent dubai in uae pro-league", 
        "tourist_attraction": {
            "burj khalifa": "burj khalifa  is a skyscraper in dubai, united arab emirates. it is the tallest artificial structure in the world, standing at 829.8 m", 
            "the dubai fountain": "the dubai fountain is the world's largest choreographed fountain system set on the 30-acre manmade burj khalifa lake.", 
            "dubai aquarium": "dubai aquarium is one of the largest aquarium in the world. this aquarium houses numerous aquatic species. also, number of endangered species are being conserved in their natural habitat in this aquarium."
        }, 
        "famous_food": {
            "arabic cuisine": "arabic cuisine is very popular and is available everywhere in the city, from the small shawarma diners in deira and al karama to the restaurants in dubai's hotels.", 
            "fast food, south asian, and chinese cuisines": "fast food, south asian, and chinese cuisines  are also very popular and are widely available."
        }, 
        "event": {
            "eid al fitr": "eid al fitr marks the end of ramadan", 
            "dubai international film festival": "dubai international film festival serves as a showcase for arab and middle eastern film making talent."
        }
    }, 
    "miami": {
        "brief_intro": "it is the seat of miami-dade county, and the cultural, economic and financial center of south florida in the united states.", 
        "culture": {
            "entertainment and performing arts": "in addition to annual festivals like the calle ocho festival, miami is home to many entertainment venues, theaters, museums, parks and performing arts centers.", 
            "fashion": "miami is also a major fashion center,home to models and some of the top modeling agencies in the world.", 
            "music": "miami attracts a large number of musicians, singers, actors, dancers, and orchestral players."
        }, 
        "reason_for_travel": "miami is more than just a great beaching destination. wonderful beaches can be found all over florida, but miami offers an atmosphere like no other city in the state.", 
        "sports": "miamis main five sports teams are the miami dolphins of the national football league, the miami heat of the national basketball association, the miami marlins of major league baseball, the florida panthers of the national hockey league, and inter miami cf of major league soccer.", 
        "tourist_attraction": {
            "vizcaya museum and gardens": "vizcaya museum and gardens is a national historic landmark, set on 28 acres,and was the luxurious winter home of 20th century industrialist, james deering. the grounds and gardens contain beautiful italian and french fountains, pools, and sculptures.", 
            "art deco historic district": "art deco historic district has the architectural style that, popular in the 1930s and 40s, dominates the trendy south beach neighborhood.", 
            "miami beach": "miami beach is located on a barrier island and connected to the mainland by a series of bridges and is a mix of quiet neighborhoods, lively entertainment-focused areas, and long stretches of soft-sand beaches."
        }, 
        "famous_food": {
            "cuban cuisine": "cuban cuisine is popular in the city since cuban immigrants in the 1960s originated the cuban sandwich and brought medianoche, cuban espresso, and croquetas, all of which have grown in popularity among all miamians and have become symbols of the citys varied cuisine.", 
            "caribbean and latin american cuisine": "caribbean and latin american cuisine has spawned a unique south florida style of cooking known as floribbean cuisine. it is widely available throughout miami and south florida and can be found in restaurant chains such as pollo tropical."
        }, 
        "event": {
            "calle ocho festival": "calle ocho festival is one of the largest in the world, and over one million visitors attend the calle ocho event. it is a free street festival that showcases pan-american culture.", 
            "food network south beach wine and food festival": "food network south beach wine and food festival is an annual five-day event located in miami beach, lincoln road, typically in mid-february. the event showcases wine, spirits, chefs and culinary personalities. the five-day event consists of dinners, wine seminars, and late-night parties, etc."
        }
    }, 
    "orlando": {
        "brief_intro": " it is a city in the u.s. state of florida and the county seat of orange county. located in central florida, it is the center of the orlando metropolitan area.", 
        "culture": {
            "entertainment and performing arts": "the hip hop music, metal, rock music, reggaeton and latino music scenes are all active within the city. orlando is known as hollywood east because of numerous movie studios in the area.", 
            "local culture": "a substantial amount of the teenage and young adult populations identify as being goth, emo, or punk."
        }, 
        "reason_for_travel": "it is all about the theme parks; walt disney world resort, universal studios, and seaworld are the big attractions. this is one of the best vacation spots in the us for families.", 
        "sports": "orlando is the home city of two major league professional sports teams: the orlando magic of the national basketball association, and orlando city sc of major league soccer.", 
        "tourist_attraction": {
            "camp mack": "camp mack is a fishing lodge, resort campground and recreation event venue in the historic town of lake wales, florida situated on the kissimmee river, in the heart of the kissimmee chain of lakes.", 
            "theme parks": "theme parks is the orlando area that is home to walt disney world, universal orlando, seaworld orlando, legoland, and fun spot america theme parks.", 
            "florida citrus tower": "florida citrus tower is built in 1956 to allow visitors to observe the miles of surrounding orange groves, it was once among the most famous landmarks of the orlando area."
        }, 
        "famous_food": {
            "florida orange juice": "florida orange juice is a good to start your day, with a refreshing, vitamin c-packed glass of oj. sure, you can probably find a fancy juice bar that will charge you $5 a glass, but it cant get any fresher than if you squeeze it at home.", 
            "the cuban sandwich": "the cuban sandwich  is one of the best sandwiches ever invented. these days, you can find it across the state, but the very best ones are made in florida."
        }, 
        "event": {
            "the vans warped tour": "the vans warped tour is a concert containing metalcore, screamo, punk bands, takes place in orlando annually.", 
            "orlando cabaret festival": "orlando cabaret festival showcases local, national, and internationally renowned cabaret artist to mad cow theatre in downtown orlando each spring.", 
            "orlando international fringe theater festival": "orlando international fringe theater festival draws touring companies from around the world, is hosted in various venues over orlandos loch haven park every spring. at the festival, there are also readings and fully staged productions of new and unknown plays by local artists."
        }
    }, 
    "las vegas": {
        "brief_intro": "an internationally renowned major resort city, known primarily for its gambling, shopping, fine dining, entertainment, and nightlife. the las vegas valley as a whole serves as the leading financial, commercial, and cultural center for nevada.", 
        "culture": {
            "art gallery and exhibit": "bellagio gallery of fine art is a facility presenting high-quality art exhibitions from major national and international museums."
        }, 
        "reason_for_travel": "the city bills itself as the entertainment capital of the world, and is famous for its mega casino hotels and associated activities. it is a top three destination in the united states for business conventions and a global leader in the hospitality industry, claiming more aaa five diamond hotels than any other city in the world.", 
        "sports": "las vegas is home to several notable minor league teams, as well as the unlv rebels, and three major professional teams, the las vegas raiders of the national football league, the vegas golden knights of the national hockey league, and the las vegas aces of the womens national basketball association.", 
        "tourist_attraction": {
            "las vegas strip": "las vegas strip is the center of the gambling and entertainment industry is located on the las vegas strip, outside the city limits in the surrounding unincorporated communities of paradise and winchester in clark county. the largest and most notable casinos and buildings are located there.", 
            "downtown casinos": "downtown casinos has the most casinos in vegas and are located on fremont street, with the stratosphere being one of the exceptions. fremont east,  similar to the gaslamp quarter of san diego, the goal being to attract a different demographic than the strip attracts.", 
            "smith center for the performing arts": "smith center for the performing arts is the world-class performing arts center hosts broadway shows and other major touring attractions, as well as orchestral, opera, ballet, choir, jazz, and dance performances."
        }, 
        "famous_food": {
            "celebrity chef specials": "celebrity chef specials is famous in las vegas because las vegas has become a mecca for celebrity chefs. theres a restaurant bearing ones name in nearly every major hotel. as for what they and the tons of other chefs whove flocked to the city make, anything goes. sin citys the place where gluttonous, insta-worthy bites and fine dining overlap."
        }, 
        "event": {
            "preview thursday": "preview thursday is the thursday prior to first friday is known in the arts district as preview thursday. this evening event highlights new gallery exhibitions throughout the district.", 
            "first friday": "first friday is a monthly celebration that includes arts, music, special presentations and food in a section of the citys downtown region called 18b, the las vegas arts district. the festival extends into the fremont east entertainment district as well."
        }
    }, 
    "los angeles": {
        "brief_intro": "los angeles is the cultural, financial, and commercial center of southern california. the city is known for its mediterranean climate, ethnic diversity, hollywood, the entertainment industry, and its sprawling metropolis.", 
        "culture": {
            "museum and art galleries": "there are 841 museums and art galleries in los angeles county, more museums per capita than any other city in the u.s.", 
            "hollywood neighborhood": "the citys hollywood neighborhood has become recognized as the center of the motion picture industry and the los angeles area is also associated as being the center of the television industry."
        }, 
        "reason_for_travel": "the sprawling city of los angeles, in southern california, has long been known internationally in the film and entertainment industry, particularly for hollywood, a place that has drawn aspiring actors and actresses from across the country for over a century. today, la is a culturally diverse city with a reputation for being the creative center of america. visitors will find a thriving culinary scene, incredible shopping, outstanding museums, and fun family attractions.", 
        "sports": "the city of los angeles and its metropolitan area are the home of eleven top level professional sports teams, several of which play in neighboring communities but use los angeles in their name. these teams include the los angeles dodgers and los angeles angels of major league baseball , the los angeles rams and los angeles chargers of the national football league, the los angeles lakers and los angeles clippers of the national basketball association, the los angeles kings and anaheim ducks of the national hockey league, the los angeles galaxy and los angeles football club of major league soccer, and the los angeles sparks of the womens national basketball association.", 
        "tourist_attraction": {
            "griffith park and griffith observatory": "griffith park and griffith observatory are one of the citys most interesting experience-based attractions, and its all free to the public. on the grounds are exhibits and telescopes. the main highlight is a look through the zeiss telescope, used for viewing the moon and planets. you can use the telescopes free each evening the facility is open. also on-site are solar telescopes used for viewing the sun.", 
            "hollywood": "hollywood is a suburb of los angeles and a destination in itself, with its own unique history and iconic sites. the attractions in hollywood are closely associated with the film industry and the glamour of the silver screen. the hillside hollywood sign, hollywood boulevard, and so on can easily fill a day or two of sightseeing. if youre lucky, you might even spot a celebrity or two.", 
            "disneyland resort": "disneyland resort is californias premier family vacation destination, attracting visitors since the 1950s. disneyland park, with rides and experiences in elaborately created theme sets, is what most people picture when they imagine disneyland. the disneyland california adventure park, created during one of the expansions, holds even more action and adventure, with seven lands based on movie themes.", 
            "universal studio theme park": "universal studio theme park is known for its mind-blowing rides based on blockbuster movies, but it is also a working movie studio and an attraction everyone can enjoy. the highlight for most people is the ever-changing selection of rides, which range from simulators to roller-coasters. favorite movie and tv-themed rides and sets include the wizarding world of harry potter, the walking dead, the simpsons, and transformers. new in 2019 is jurassic world - the ride."
        }, 
        "famous_food": {
            "chinese cuisine": "chinese cuisine is never a bad choice. depending on your count, there are upwards of two dozen distinctly regional chinese food styles represented in los angeles county. you can get dim sum at sea harbour, labor over the tongue-numbing sichuan peppercorns at chengdu taste.", 
            "thai cuisine": "thai cuisine is popular in the city since los angeles serves as a home base for some of the nations best thai food. you could drop a glass of thai iced tea in thai town and splash up against half a dozen fantastic eateries.", 
            "tacos": "tacos are quite popular in l a. as if taco trucks werent enough, los angeles has managed to corner the market on all the best tacos, mobile or otherwise."
        }, 
        "event": {
            "l.a. film festival ": "l.a. film festival  is an annual event. los angeles is famous for its filmmaking history, but many people only know the hit blockbusters that come to mainstream movie theaters. to get more involved in the citys diverse film scene and see some incredible productions, attend the l.a. film festival in june.", 
            "the academy awards": "the academy awards also nicknamed the oscars, celebrates the fine art of filmmaking and awards those iconic oscar trophies to top-notch movie stars in february.", 
            "grammy awards": "grammy awards celebrate music recording artists and all of your favorite songs. although the grammys have taken place in other cities in the past, they typically occur in los angeles in february.", 
            "golden dragon parade": "golden dragon parade celebrates lunar new year. the chinese new year isnt just celebrated in china, and in fact, los angeles has an amazing celebration to attend next time youre here in february."
        }
    }, 
    "hong kong": {
        "brief_intro": "hong kong is a city and special administrative region of china in the eastern pearl river delta by the south china sea", 
        "culture": {
            "cantopop": "cantopop is a genre of cantonese popular music which emerged in hong kong during the 1970s. evolving from shanghai-style shidaiqu, it is also influenced by cantonese opera and western pop.", 
            "cinema": "hong kong developed into a filmmaking hub during the late 1940s as a wave of shanghai filmmakers migrated to the territory, and these movie veterans helped rebuild the colonys entertainment industry over the next decade."
        }, 
        "reason_for_travel": "almost any of the districts of hong kong can be considered a tourist destination.", 
        "sports": "despite its small area, the territory is home to a variety of sports and recreational facilities. the city has hosted a number of major sporting events, including the 2009 east asian games, the 2008 summer olympics equestrian events, and the 2007 premier league asia trophy", 
        "tourist_attraction": {
            "victoria harbour": "victoria harbour is a natural landform harbour separating hong kong island in the south from the kowloon peninsula to the north. the harbours deep, sheltered waters and strategic location on the south china sea were instrumental in hong kongs establishment as a british colony and its subsequent development as a trading centre.", 
            "victoria peak": "victoria peak is a hill on the western half of hong kong island. it is also known as mount austin, and locally as the peak. ", 
            "the soho": "the soho district in hong kong is an entertainment zone located in central. ", 
            "lan kwai fong ": "lan kwai fong  is a small square of streets in central, hong kong. the area was dedicated to hawkers before the second world war, but underwent a renaissance in the mid-1980s. it is now a popular expatriate haunt in hong kong for drinking, clubbing and dining."
        }, 
        "famous_food": {
            "dim sum": "dim sum as part of yum cha brunch, is a dining-out tradition with family and friends.", 
            "cha chaan teng": "cha chaan teng means places where local versions of western food are served at"
        }, 
        "event": {
            "international chinese new year night parade": "international chinese new year night parade first organised in 1996, the international chinese new year night parade is one of the most important celebratory events during chinese new year in hong kong. originally it was held during day time on hong kong island, and from 2004 onward the event has been held during night time in tsim sha tsui."
        }
    },
        "Shenzhen":{
            "brief_intro": "it is a major sub-provincial city located on the east bank of the Pearl River estuary on the central coast of southern Guangdong province, People's Republic of China.",
            "culture":{
                # "brief":"",
                "library":"The city has more than 630 libraries and bookstores, with the Shenzhen Library, the Shenzhen Book City, the Shenzhen Scientific-Technical Library, the Library of the Shenzhen University, the Shenzhen Children's Library, and the Luohu District Library being among the largest.",
                "cultural facilities": "Cultural facilities such as the Shenzhen Cultural Center, the Shenzhen Convention and Exhibition Center, and the Shenzhen Children's Palace are located in the Futian District, which is considered the cultural center of the city. "
            },
            "event":{
                "the Beach Music Festival":"aims to raise the quality and quantity of Chinese pop music and strive to become the biggest production and trading platform for Chinese music.",
            },
            "sports":"Shenzhen is the home of a local football club, Shenzhen F.C.. In addition to Shenzen F.C., the city also hosted Shenzhen Ledman F.C., though this club was disbanded in 2018.",
            "famous_food": {
                "Cantonese cuisine":"Cantonese cuisine is the main cuisine of Shenzhen, As with Hong Kong and the surrounding Guangdong province",
                "Chaozhou cuisine":"Chaozhou cuisine is well known for its seafood and vegetarian dishes. Its use of flavouring is much less heavy-handed than most other Chinese cuisines and depends much on the freshness and quality of the ingredients for taste and flavour. ",
                "Hakka cuisine":"Hakka cuisine is the cooking style of the Hakka people, who may also be found in other parts of Taiwan and in countries with significant overseas Hakka communities."    
            },
            "reason_for_travel":"",
            "tourist_attraction": {
                "Overseas Chinese Town East":"Overseas Chinese Town East is a large-scale eco-resort created by the OCT Group. It contains a number of theme parks, including Knight Valley and Tea Stream Resort Valley. Knight Valley is dominated by natural canyon scenery and has exciting aquatic amusement projects. You can experience the Surging down the Rapids ride and an all-glass observation deck over the cliffs. ",
                "Shekou Sea World":"Shekou Sea World Shenzhen is a hub of activity in the Shekou area of the city. Tons of restaurants, bars, coffee shops.",
            }
        },
        "Phuket":{
            "brief_intro":"it is one of the southern provinces (changwat) of Thailand. It consists of the island of Phuket, the country's largest island, and another 32 smaller islands off its coast.",
            "culture":{
                #"brief":"",
                "culture":"The mix of people passing through Phuket over the centuries does create a unique melting pot of cultures, peoples and religions. In Phuket Town you can find Buddhist temples, Chinese shrines, a Mosque, a Catholic church, a Sikh Gurdwara, a Hindu shrine and probably more!"
            },
            "event":{
                "Thao Thep Krasatri-Thao Sri Suntorn Festival":"Thao Thep Krasatri-Thao Sri Suntorn Festival is held on 13 March yearly in memory of the two heroines who led the defense of the island against the Burmese in 1785.",
                "Seafood Festival":"Held around May yearly, is designed to publicize the delicious seafood of Phuket and attract visitors during the rainy season. Activities include a Marine Tourism Resources Parade, seafood stalls, demonstrations of regional cuisines and cultural shows.",
                "Songkran Festival":"Songkran is an important merit making period lasting three day, from April 13th to 15th",
            },
            "sports":"Phuket City football club participates in Thai League 3 Lower Region, the third tier of Thai football league system. The Golden Sloop plays their home matches at Surakul Stadium.",
            "famous_food": {
                "Ah-pong":"Ah-pong can be considered to be the signature snack of Phuket. Ah-Pong snacks are easy to make as the ingredients—flour, egg yolk, coconut milk, sugar; water and yeast— are readily available. ",
                "Ang-Gu":"Ang-Gu is a popular snack eaten during the auspicious ceremony of Phuket. From Chinese belief, turtles are the symbol of eternity so they believe that those who eat this snack will live endlessly like the turtles. ",
                "Oh-Aew":"Oh-Aew is a very famous desert of Phuket, and it originates from Phuket. Oh-Aew is made from jellied banana-flour mixed with boiled red beans, ice and sweet red syrup Extra jellies and fruit is also added to make it sweeter and more flavorful. "    
            },
            "reason_for_travel":"Phuket has the best shopping facilities of any of Thailand's best resorts, great restaurants for both Thai and international cuisine, and a wide range of sights and activities to keep you entertained. ",
            "tourist_attraction": {
                "Two Heroines Monument":"is the monument in Thalang District, a memorial statue of the heroines Thao Thep Kasattri and Thao Sri Sunthon, who rallied islanders in 1785 to repel Burmese invaders. ",
                "Kamala Beach":"Kamala Beach is a large beach approximately 16 km north of Patong Beach. The beach is undeveloped with coral reefs on the north side and surfing in the low season. It is a tourist beach in the high season and a sleepy seaside Muslim village in the low season. ",
                "Phuket Aquarium":"Phuket Aquarium attracts around 300000 visitors each year. Established in 1983 as part of the Phuket Marine Biological Center, it is a research and monitoring station within the Department of Marine and Coastal Resources",
            }
        },
        "Istanbul":{
            "brief_intro": "formerly known as Byzantium and Constantinople, is the most populous city in Turkey and the country's economic, cultural and historic center. ",
            "culture":{
                #"brief":"",
                "culture":"Much of Turkey's cultural scene had its roots in Istanbul, and by the 1980s and 1990s Istanbul reemerged globally as a city whose cultural significance is not solely based on its past glory."
            },
            "event":{
                "Istanbul International Film Festival":"At the city’s leading film festival, Istanbul International Film Festival, in Istanbul in April, you can discover and enjoy remarkable local and international films in competition, at the several culture centers and cinemas in the Beyoglu and Kadikoy districts. ",
                "Istanbul Tulip Festival":"Tulips are very important for the Ottoman Empire and Turkish culture. And to celebrate both spring and this fact, this annual festival takes place at the city’s most famous parks",
            },
            "sports":"Istanbul is home to some of Turkey's oldest sports clubs. The Sinan Erdem Dome, among the largest indoor arenas in Europe, hosted the final of the 2010 FIBA World Championship, the 2012 IAAF World Indoor Championships, as well as the 2011–12 Euroleague and 2016–17 EuroLeague Final Fours",
            "famous_food": {
                "TURKISH BREAKFAST":"Turkish breakfast in all its Mediterranean glory is the best way to start your day in Istanbul.",
                "MENEMEN":"Menemen is another dish commonly eaten for breakfast and may be compared to a soupy plate of scrambled eggs.",
                "meze":"Meze is a set of appetizer dishes that are traditionally served before a meal or alongside it. "    
            },
            "reason_for_travel":"The city is liberally scattered with glorious remnants of its long and illustrious history, and the sightseeing here will impress even the most monument-weary visitor.",
            "tourist_attraction": {
                "Aya Sofya":"The Aya Sofya, formerly the Hagia Sophia, was the Byzantine Emperor Justinians swaggering statement to the world of the wealth and technical ability of his empire. ",
                "Topkapi Palace":" The vast complex of Topkapi Palace is a dazzling display of Islamic art, with opulent courtyards lined with intricate hand-painted tile-work, linking a warren of sumptuously decorated rooms, all bounded by battlemented walls and towers.",
                "Blue Mosque":"Sultan Ahmet I's grand architectural gift to his capital was blue mosque, commonly known as the Blue Mosque today. ",
                "Basilica Cistern":"The Basilica Cistern is one of Istanbul's most surprising tourist attractions. This huge, palace-like underground hall, supported by 336 columns in 12 rows, once stored the imperial water supply for the Byzantine emperors. "
            }
        },
        

#https://www.businessinsider.com/most-popular-destinations-in-the-world-travelers-top-cities-2018-12#5-macau-27
    }

# for city in cities:
#     print(city)
#     for key in cities[city]["famous_food"]:
#         cities[city]["famous_food"][key]= ""+key+" "+cities[city]["famous_food"][key]
#     for key in cities[city]["tourist_attraction"]:
#         cities[city]["tourist_attraction"][key]= ""+key+" "+cities[city]["tourist_attraction"][key]
#     for key in cities[city]["event"]:
#         cities[city]["event"][key]= ""+key+" "+cities[city]["event"][key]



with open('city_json.json', 'w') as f:
    print("dump")
    json.dump(cities, f, indent = 4)


f = open('city_json.json', 'r')
lines = [line.lower() for line in f]
with open('city_json.json', 'w') as out:
    print("change")
    out.writelines(lines)

# print("hi")
# y=json.dumps(city)
# print(y)