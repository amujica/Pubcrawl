from soil.agents import FSM, state, default_state
from soil import Environment
from random import random, shuffle, sample
from itertools import islice
import logging
from enum import Enum
from random import randint
import numpy

class Genders(Enum):
    male = 'male'
    female = 'female'

class Venues(Enum):
    pub = 'pub'
    disco = 'disco'
    street = 'street'


class CityPubs(Environment):
  
    level = logging.INFO

    def __init__(self, *args, number_of_pubs=3, number_of_discos=3, number_of_street=3, **kwargs):
                   
                    super(CityPubs, self).__init__(*args, **kwargs)  #Para la clase superior. Constructor super.
                    pubs = {}
                    for i in range(number_of_pubs):
                        newpub = {
                            'name': 'The awesome pub #{}'.format(i),
                            'open': False,
                            'capacity': numpy.random.normal(100,50),
                            'occupancy': 0,
                            'price':randint(5, 8),
                            'type': Venues.pub.value,
                            'entry': 0,
                            'opening_time': 1,
                            'closing_time': randint(20,24),
                        }
                        pubs[newpub['name']] = newpub
                    for i in range(number_of_discos):
                        newpub = {
                            'name': 'The awesome disco #{}'.format(i),
                            'open': False,
                            'capacity': numpy.random.normal(1300,1000) ,
                            'occupancy': 0,
                            'price':randint(7, 12),
                            'type': Venues.disco.value,
                            'entry': randint(15,20),
                            'opening_time': 10,
                            'closing_time': randint(32,36),
                        }
                        pubs[newpub['name']] = newpub
                    for i in range(number_of_street):
                        newpub = {
                            'name': 'The awesome street #{}'.format(i),
                            'open': False,
                            'capacity': 10000 ,
                            'occupancy': 0,
                            'price':randint(2,5),
                            'type': Venues.street.value,
                            'entry': 0,
                            'opening_time': 1,
                            'closing_time': 39,
                        }
                        pubs[newpub['name']] = newpub
            
                        
                    self['pubs'] = pubs




    def return_open (self,pub_name):
        pub = self['pubs'][pub_name]
        return pub['open']

    def return_occupancy (self,pub_name):
        pub = self['pubs'][pub_name]
        return pub['occupancy']

    def return_price(self,pub_name):
        pub = self['pubs'][pub_name]
        return pub['price']

    def return_name(self,pub_name):
        pub = self['pubs'][pub_name]
        return pub['name']

    def return_type(self,pub_name):
        pub = self['pubs'][pub_name]
        return pub['type']

    def return_opening_time(self,pub_name):
        pub = self['pubs'][pub_name]
        return pub['opening_time']

    def return_closing_time(self,pub_name):
        pub = self['pubs'][pub_name]
        return pub['closing_time']

    def set_open(self,pub_name):
        pub = self['pubs'][pub_name]
        pub['open'] = True

    def set_close(self,pub_name):
        pub = self['pubs'][pub_name]
        pub['open'] = False

    def set_capacity(self,pub_name, number):
        pub = self['pubs'][pub_name]
        pub['capacity'] = number  

    def set_occupancy(self,pub_name, number):
        pub = self['pubs'][pub_name]
        pub['occupancy'] = number  


    def enter(self, pub_name, *nodes):

        '''Agents will try to enter. The pub checks if it is possible'''
    
        try:
            pub = self['pubs'][pub_name]
        except KeyError:
            raise ValueError('Pub {} is not available'.format(pub_name))

        for node in nodes:
            if not pub['open'] or (pub['capacity'] < (len(nodes) + pub['occupancy'])) or node['money']< pub['entry']:

                return False

        pub['occupancy'] += len(nodes)
        for node in nodes:
            node['pub'] = pub_name
            node['money'] = node['money'] - pub['entry']


        #El líder hace un link con el bar en cuestión self.env.add_edge(self, pub)
        return True

    def available_pubs_total(self):
        available_venues = []
        for pub in self['pubs'].values():
            if pub['open'] and (pub['occupancy'] < pub['capacity']):
                available_venues.append(pub['name'])

        shuffle(available_venues)
        return available_venues 

    def available_pubs(self):
        available_venues = []
        for pub in self['pubs'].values():
            if pub['open'] and (pub['occupancy'] < pub['capacity']) and pub['type'] == "pub":
                available_venues.append(pub['name'])

        shuffle(available_venues)
        return available_venues 

    def available_discos(self):
        available_venues = []
        for pub in self['pubs'].values():
            if pub['open'] and (pub['occupancy'] < pub['capacity']) and pub['type'] == "disco":
                available_venues.append(pub['name'])

        shuffle(available_venues)
        return available_venues 

    def available_street(self):
        available_venues = []
        for pub in self['pubs'].values():
            if pub['open'] and (pub['occupancy'] < pub['capacity']) and pub['type'] == "street":
                available_venues.append(pub['name'])

        shuffle(available_venues)
        return available_venues 

    def get_venues(self):

        venues = []
        for venue in self['pubs'].values():
            venues.append(venue['name'])
        return venues 

    def reelect_leader(self,*group):
        for node in group:
            self['is_leader']=True
            return
        #Hace un link al bar donde estén



    #Un grupo se va de un pub. La sintaxis "del" es como decir que te vacíe esa variable
    """def exit(self, pub_id, *node_ids):
                    '''Agents will notify the pub they want to leave'''
                    try:
                        pub = self['pubs'][pub_id]
                    except KeyError:
                        raise ValueError('Pub {} is not available'.format(pub_id))
                    for node_id in node_ids:
                        node = self.get_agent(node_id)
                        if pub_id == node['pub']:
                            del node['pub']
                            pub['occupancy'] -= 1
            
                def exit(self, pub_id, *nodes):
                    '''Agents will notify the pub they want to leave'''
                    try:
                        pub = self['pubs'][pub_id]
                    except KeyError:
                        raise ValueError('Pub {} is not available'.format(pub_id))
                    for node in nodes:
                     
                        if pub_id == node['pub']:
                            del node['pub']
                            pub['occupancy'] -= 1
            """
    def exit(self, pub_name, *nodes):

        try:
            pub = self['pubs'][pub_name]
        except KeyError:
            raise ValueError('Pub {} is not available'.format(pub_name))
        
        pub['occupancy'] -= len(nodes)

    
    
        


class Patron(FSM):
  
    level = logging.INFO

    defaults = {
        'pub': None,
        'drunk': False,
        'pints': 0,
        'max_pints': 5,
        'in_a_group':False,
        'money':20,
        'is_leader': False,
        'group_size':0,
        'num_of_changes':0,
        'intoxicated': False,
        'going_out_time':10,
        'coming_back_time':16,
        'group_size':0,

    }

    @default_state
    @state
    def setting_parameters(self):

    
        '''Setting max_pints'''
        if self['age']==15:
            if self['gender']=="female":
                self['max_pints']=numpy.random.normal(3,1)
            else:
                self['max_pints']=numpy.random.normal(4,1)

        elif self['age']==20:
            if self['gender']=="female":
                self['max_pints']=numpy.random.normal(4,2)
            else:
                self['max_pints']=numpy.random.normal(6,2)

        else:
            if self['gender']=="female":
                self['max_pints']=numpy.random.normal(4,2)
            else:
                self['max_pints']=numpy.random.normal(6,2)



        '''Setting intoxication_drinkthreshold'''
        self['intoxication_drinkthreshold'] = 2*self['max_pints']
        
        '''Setting money'''
        if self['age']==15:
            if self['gender']=="female":
                self['money']=numpy.random.normal(25,10)
            else:
                self['money']=numpy.random.normal(25,15)

        elif self['age']==20:
            if self['gender']=="female":
                self['money']=numpy.random.normal(35,15)
            else:
                self['money']=numpy.random.normal(40,15)

        else:
            if self['gender']=="female":
                self['money']=numpy.random.normal(60,20)
            else:
                self['money']=numpy.random.normal(65,25)



        
        r = random()

        '''Setting coming_back_time'''


        if self['age']==15:

            if r<0.163:
                self['coming_back_time'] = randint(6,9)
                                                
            elif r<0.299:
                                    
                self['coming_back_time'] = randint(10,13)
                                                    
            elif r<0.407:
                                    
                self['coming_back_time'] = randint(14,17)

            elif r<0.543:
                                    
                self['coming_back_time'] = randint(18,21)


            elif r<0.67:
                                    
                self['coming_back_time'] = randint(22,25)

            elif r<0.771:
                                    
                self['coming_back_time'] = randint(26,29)

            elif r<0.863:
                                    
                self['coming_back_time'] = randint(30,33)

            elif r<0.932:
                                    
                self['coming_back_time'] = randint(34,37)

            elif r<0.965:
                                    
                self['coming_back_time'] = randint(38,42)

            else:

                self['coming_back_time'] = randint(6,42)

        elif self['age']==20:

            if r<0.078:
                self['coming_back_time'] = randint(6,9)
                                                
            elif r<0.152:
                                    
                self['coming_back_time'] = randint(10,13)
                                                    
            elif r<0.253:
                                    
                self['coming_back_time'] = randint(14,17)

            elif r<0.409:
                                    
                self['coming_back_time'] = randint(18,21)


            elif r<0.581:
                                    
                self['coming_back_time'] = randint(22,25)

            elif r<0.709:
                                    
                self['coming_back_time'] = randint(26,29)

            elif r<0.811:
                                    
                self['coming_back_time'] = randint(30,33)

            elif r<0.915:
                                    
                self['coming_back_time'] = randint(34,37)

            elif r<0.966:
                                    
                self['coming_back_time'] = randint(38,42)

            else:

                self['coming_back_time'] = randint(6,42)

        else:

            if r<0.082:
                self['coming_back_time'] = randint(6,9)
                                                
            elif r<0.163:
                                    
                self['coming_back_time'] = randint(10,13)
                                                    
            elif r<0.266:
                                    
                self['coming_back_time'] = randint(14,17)

            elif r<0.451:
                                    
                self['coming_back_time'] = randint(18,21)


            elif r<0.604:
                                    
                self['coming_back_time'] = randint(22,25)

            elif r<0.724:
                                    
                self['coming_back_time'] = randint(26,29)

            elif r<0.819:
                                    
                self['coming_back_time'] = randint(30,33)

            elif r<0.908:
                                    
                self['coming_back_time'] = randint(34,37)

            elif r<0.942:
                                    
                self['coming_back_time'] = randint(38,42)

            else:

                self['coming_back_time'] = randint(6,42)

                                    
    
        return self.looking_for_friends



    
    @state
    def looking_for_friends(self):
     
        #ARREGLAR QUE NO ESPERAN LOS PASOS PARA SALIR! Problema de soil, no funcion el self.env.timeout
        

        if(self['in_a_group'] == False):
            self.info('I am looking for friends')
            self['is_leader'] = True
 
            available_friends = list(self.get_agents(drunk=False,
                                                     pub=None,
                                                     in_a_group=False,
                                                     age=self['age']))
                                                     
            if not available_friends or len(available_friends)==1:
                self.info('Life sucks and I\'m alone!')
                return self.at_home

            befriended = self.try_friends(available_friends)
            if befriended:

                group = list(self.get_neighboring_agents())


                r=random()
                if self['age']==15:
                    if(r<0.3963):
                        going_out_time = 2
                    elif(r<(0.3963+0.2642)):
                        going_out_time = randint(3,6)
                    elif(r<(0.3963+0.2642+0.2642)):
                        going_out_time = randint(7,10)
                    else:
                        going_out_time = randint(11,18)

                elif self['age']==20:
                    if(r<0.1519):
                        going_out_time = 2
                    elif(r<(0.1519+0.2658)):
                        going_out_time = randint(3,6)
                    elif(r<(0.1519+0.2658+0.4937)):
                        going_out_time = randint(7,10)
                    else:
                        going_out_time = randint(11,18)

                else:
                    if(r<0.2041):
                        going_out_time = 2
                    elif(r<(0.2041+0.449)):
                        going_out_time = randint(3,6)
                    elif(r<(0.2041+0.449+0.2653)):
                        going_out_time = randint(7,10)
                    else:
                        going_out_time = randint(11,18)

                for friend in group:
                    friend['going_out_time']= going_out_time
                    friend['group_size'] = len(group) +1
                    
               
                self['going_out_time'] = going_out_time
                self['group_size'] =  len(group)+1          
                
                return self.looking_for_pub, self.env.timeout(self['going_out_time']-self.now) 
        else:
            self.debug('{} has a group already' .format(self.id))
            return self.looking_for_pub, self.env.timeout(self['going_out_time']-self.now)

    @state
    def looking_for_pub(self):

        '''Look for a pub that accepts me and my friends'''
        if self['pub'] != None:
            return self.sober_in_pub

         

        self.debug('I am looking for a pub')
        group = list(self.get_neighboring_agents())

        r=random()
        if(self['age'] == 15):

            if (0.429>r):
                available_pubs = self.env.available_pubs()
                    

            elif ((0.429+0.337)>r):
                available_pubs = self.env.available_discos()

            else:
                available_pubs = self.env.available_street()

        elif(self['age'] == 20):

            if (0.509>r):
                available_pubs = self.env.available_pubs()

            elif (0.509+0.337>r):
                available_pubs = self.env.available_discos()

            else:
                available_pubs = self.env.available_street()

        else:

            if (0.629>r):
                available_pubs = self.env.available_pubs()
                    

            elif ((0.629+0.287)>r):
                available_pubs = self.env.available_discos()

            else:
                available_pubs = self.env.available_street()

        if (len(available_pubs)) == 0:
            available_pubs = self.env.available_pubs()
            self.info('No había discos y me voy mejor a un bar')

        if (len(available_pubs)) == 0:
            self.info('Tampoco hay bares, así que mejor nos vamos a casa')
            for friend in group:
                friend.set_state(self.at_home)
            return self.at_home


        for pub in available_pubs:
            
           
            self.debug('We\'re trying to get into {}: total: {}'.format(pub, len(group)))
            if self.env.enter(pub, self, *group):
                self.info('We\'re all {} getting in {}!'.format(len(group)+1, pub))
                capacity = self.env.return_occupancy(pub)
                self.info('{} now has {} people inside'.format(pub,capacity))
                return self.sober_in_pub
            else:
                self.info("We can\'t go inside {}".format(pub))

        if (self.env.return_type(available_pubs[0])=="disco") or  (self.env.return_type(available_pubs[0])=="street"):

            available_pubs = self.env.available_pubs()
            
            for pub in available_pubs:
            
                self.debug('We\'re trying to get into {}: total: {}'.format(pub, len(group)))
                if self.env.enter(pub, self, *group):
                    self.info('We\'re all {} getting in {}!'.format(len(group)+1, pub))
                    capacity = self.env.return_occupancy(pub)
                    self.info('{} now has {} people inside'.format(pub,capacity))
                    return self.sober_in_pub
                else:
                    self.info("We can\'t go inside {}".format(pub))

            self.info('No hay bares por donde salir. Nos vamos')
            for friend in group:
                friend.set_state(self.at_home)
            return self.at_home

        else:
            self.info('No hay bares por donde salir. Nos vamos')
            for friend in group:
                friend.set_state(self.at_home)
            return self.at_home

                
            # Si no puede entrar después de todas la iteraciones dar alternativa dependiendo
            # del caso. Buscan plan de otro tipo, en otro tipo de Venue. Si tampoco pueden, se van a casa
        


    @state
    def sober_in_pub(self):

        group = list(self.get_neighboring_agents())
        #Comprobar si hay razón para irse a casa

           
            #Por cosas relacionadas con peleas


            #Es hora de irse a casa
        if self.now == self['coming_back_time']:

            self.info('Es mi hora de irme a casa')
            return self.at_home
            

            # Quedan pocos amigos

        friends_remaining = len(list(self.get_neighboring_agents()))

        

        if (self['group_size'] * 0.5) >= friends_remaining+1:
            self.info('Me voy a casa porque habíamos salido {} y solo quedamos {}'.format(self['group_size'], friends_remaining+1))
            for friend in group:
                friend.set_state(self.at_home)
                
            return self.at_home


    


        #Option of having a fight
        #Set prob_change_bar
        #Option of changing pub if you are a leader
        #Option of drinking a beverage
        #Check if the Patron is drunk
        #Set prob_fight
        #Set prob_drink

        type = self.env.return_type(self['pub'])




        # ESTO DEPENDE DE LOS ITINERARIOS, QUITAR NUM_OF_CHANGES?
      
        if(type=="disco"):
            self['prob_change_bar'] = 0

        else:
            self['prob_change_bar'] = 0.2


        if (self['is_leader'] and self['prob_change_bar']>random()) or (self['is_leader'] and not self.env.return_open(self['pub'])):
            self.change_bar()
            self['num_of_changes'] = self['num_of_changes']  + 1

        self.drink()

        '''Setting prob_drink'''

        if self['pints'] > self['max_pints']:
            self['drunk'] = True
            self.info('I\'m so drunk.')
            return self.drunk_in_pub

    @state
    def drunk_in_pub(self):
        #Comrpobar si hhay razón para irse a casa
        #Option of having a fight
        #Set prob_change
        #Option of changing pub if you are a leader
        #Option of drinking a beverage
        #Check if the Patron is drunk
        #Set prob_fight
        #Set prob_drink
        

        if (self['is_leader'] and self['prob_change_bar']>random()) or (self['is_leader'] and not self.env.return_open(self['pub'])):
            self.change_bar()
            self['num_of_changes'] = self['num_of_changes']  + 1
        
        self.drink()

        if self['pints'] > self['intoxication_drinkthreshold']:
            self.info('I got intoxicated')
            self['intoxicated'] = True
            return self.at_home

    

    @state
    def at_home(self):
        '''The end'''
        self.info('Life sucks. I\'m home!')
        if self['is_leader']==True:
            group = list(self.get_neighboring_agents())
            self.env.reelect_leader(*group)


        if (self['pub']!=None):
            occupancy = self.env.return_occupancy(self['pub'])
            self.env.set_occupancy(self['pub'], occupancy-1)
            self.info('El bar tenia {} personas y ahora {}'.format(occupancy, self.env.return_occupancy(self['pub']) ))
        

        self.die(remove=True)
    



    def change_bar(self):

            #Que cambien según itinerarios. Si num_changes=0, cambia dependiendo donde esté. 
            #Bar--> disco 
            #bar-->bar -->bar...
            #Street--> bar -->bar ...
            #Street--> disco
            #De las discoteca no sale nadie
            #Si se intenta cambiar a un sitio y no está disponible, se queda donde está (esto lo que hace es suponer que los agentes
            #se saben los horarios de los sitios)

        self.info('This member is going to change pub: {}'.format(self.id))

        current_pub = self['pub']
        type = self.env.return_type(self['pub'])

        group = list(self.get_neighboring_agents())
        r= random()


        #Pensar bien en las posibilidades y ver que hacen si no encuentran el sitio que buscan
        if(type== "disco"):

            available_pubs = self.env.available_discos()


        elif(type== "pub"):

            if self['num_of_changes']>=2:
                available_pubs = self.env.available_pubs()

            else:
                r = random()

                if r<0.5 and self.now>=10:

                    available_pubs = self.env.available_discos()
                    
                else:
                    available_pubs = self.env.available_pubs()
                
        
        else:

            if (0.5>r):
                available_pubs = self.env.available_pubs()

            else:
                available_pubs = self.env.available_discos()

        if len(available_pubs) == 0:

            for friend in group:
                friend.set_state(self.at_home)
                self.info('Me voy a casa en un bucle de estos:{}'.format(friend.id))
            self.info("Nuestro plan se nos ha acabado")
            self.set_state(self.at_home)


        for pub in available_pubs:
            

            if self.env.return_name(pub) != current_pub:
                self.debug('We\'re trying to get into {}: total: {}'.format(pub, len(group)))
                if self.env.enter(pub, self, *group):
                    self.env.exit(current_pub,self, *group)
                    self.info('We\'re all {} changing to {}!'.format(len(group)+1, pub))
                    capacity = self.env.return_occupancy(pub)
                    self.info('{} now has {} people inside'.format(pub,capacity))
                    
                    return
                    
                else:
                    self.info("We can\'t go inside {}. There are {} people inside and is {}".format(pub, self.env.return_occupancy(pub),self.env.return_open(pub)))
                    for friend in group:
                        friend.set_state(self.at_home)
                    
                    self.set_state(self.at_home)
          ##Si no puede entrar después de todas la iteraciones dar alternativa dependiendo
          #del caso. Si no pueden por precio (se quedan donde están), o si no pueden por horario (se quedan donde están)
                #O no caben: , vuelven a otro del tipo anterior donde estaban

        



    
    def drink(self):
        price = self.env.return_price(self['pub'])
        
            
        if(self['prob_drink']>random() and price<self['money']):
            self['pints'] = self['pints'] + 1
            self['money'] = self['money'] -  price
            self.debug('Cheers to that')
            
            self.debug('The price is {} € at {}'.format(price,self['pub']))

    def kick_out(self):
        self.set_state(self.at_home)

    def befriend(self, other_agent):
        '''
        Try to become friends with another agent. The chances of
        success depend on both agents' openness.
        '''
       
        self.env.add_edge(self, other_agent)
        self.debug('Made some friend, agent {}'.format(other_agent.id))
        return True
        

    def try_friends(self, others):
        ''' Look for random agents around me and try to befriend them'''
        n=1
        befriended = False
        r = random()
        if r<0.1:
            k = randint(3,5)
        elif r<0.411:
            k = randint(6,10)
        else:
            k=randint(10,15)

        shuffle(others)
        for friend in islice(others, k):  # random.choice >= 3.7
            if friend == self:
                continue
            if friend.befriend(self):
                self.befriend(friend)
                #self.info('Hooray! new friend: {}'.format(friend.id))
                n = n+1
                befriended = True
            else:
                self.info('{} does not want to be friends'.format(friend.id))

        self['in_a_group'] = True
        
        neighbors_leader = list(self.get_neighboring_agents())

        #print(*neighbors_leader)
        
        for people in neighbors_leader:
            people['in_a_group'] = True
            
            for i in neighbors_leader:
                if (people!=i):
                    people.befriend(i)

        self.info('Now we are a group: ')
        for people in neighbors_leader:
            self.info('{}'.format(people.id))
        return befriended
                        

class Police(FSM):
    '''Simple agent to take intoxicated people out of pubs.'''
    level = logging.INFO

    @default_state
    @state
    def patrol(self):

        '''Abre o cierra los bares'''
        pubs = self.env.get_venues() 


        for pub in pubs:

            if self.now == self.env.return_opening_time(pub):
                self.env.set_open(pub)
                self.info('El {} ha abierto'.format(pub))

            
            if self.now == self.env.return_closing_time(pub):
                self.env.set_close(pub)
                self.info('El {} ha cerrado con {} personas dentro'.format(pub, self.env.return_occupancy(pub)))
                #Echa a toda la gente de dentro, mirar qué hacen los agentes cuando les echan


        '''Echará a los que están intoxicados en un local'''
        intoxicates = list(self.get_agents(intoxicated=True))
        for intoxicate in intoxicates:
            self.info('Kicking out the intoxicated agents: {}'.format(intoxicate.id))
            intoxicate.kick_out()


        '''Echará a los que se han peleado en un local'''



        '''Politicas a probar'''
        """for pub in pubs:
                                    if self.now == 15:
                                        self.env.set_capacity(pub,0)"""

