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

    """
    The environment is key in a simulation. It contains the network topology,
    a reference to network and environment agents, as well as the environment
    params, which are used as shared state between agents.
    The environment parameters and the state of every agent can be accessed
    both by using the environment as a dictionary or with the environment's 
    :meth:`soil.environment.Environment.get` method.
    'name': 'The awesome pub #{}'.format(i),
                'open': True,
                'capacity': pub_capacity ,
                'occupancy': 0,
                'price':randint(4, 6),
                'type': Venues.pub.value,
    """

  
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
                            'closing_time': randint(19,23),
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
                            'opening_time': 9,
                            'closing_time': randint(31,35),
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
                            'closing_time': 38,
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

        

    def enter(self, pub_name, *nodes):

        '''Agents will try to enter. The pub checks if it is possible'''
        #A este método se le pasa el id del pub al que quieren entrar, y el grupo de amigos.
        #Hace comprobaciones con la capacidad y viendo si está abierto. Devuelve True si se puede entrar.

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
        return True


    #Devuelve una lista de pubs en los que se puede entrar. Lo hace con yield: se genera un objeto en vez de 
    # una lista. Cuando se llama al método no se genera la lista, se genera un objeto. SOlo cuando intentemos recorrerlo
    # se generará una lista que además solo puede recorrerse una vez --> https://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do
    """def available_pubs(self):
                    
                    for pub in self['pubs'].values():
                        if pub['open'] and (pub['occupancy'] < pub['capacity']):
                            yield pub['name']"""

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
    '''Agent that looks for friends to drink with. It will do three things:
        1) Look for other patrons to drink with
        2) Look for a bar where the agent and other agents in the same group can get in.
        3) While in the bar, patrons only drink, until they get drunk and taken home.
    '''

    """Aquí va un init donde se hace todo"""
    level = logging.INFO

    defaults = {
        'pub': None,
        'drunk': False,
        'pints': 0,
        'max_pints': 5,
        'in_a_group':False,
        #'gender': Genders.male.value,
        'money':20,
        'is_leader': False,
        'group_size':0,
        'num_of_changes':0,
        #'age': 15,
        'altercation_drinkthreshold': 12,
        'intoxicated': False,
        'going_out_time':10,
        'coming_back_time':16
        ##'interval'
    }

    """def __init__(self, *args, number_of_pubs=3, number_of_discos=3, number_of_street=3, **kwargs):
        r=random()
                             if age==15:
                                 if r<0.163:
                                     self['coming_back_time'] = randint()
                             elif age==20:
                     
                             else:

    """


    @default_state
    @state
    def looking_for_friends(self):
        '''Look for friends to drink with'''
        #Dependiendo de la edad podemos hacerles algunas asignaciones de parámetros de esta manera, ya que en el otro
        #lado no se le puede meter código
        if self['age'] == 15:
            self['money'] = randint(17,23) #EN un futuro aquí se pone self['money'] = numpy.random.normal(20) o algo así imaginemos
        elif self['age'] == 20:
            self['money'] = randint(22,27)
        else:
            self['money']=randint(32,40)

        if(self['in_a_group'] == False):
            self.info('I am looking for friends')
            self['is_leader'] = True
            self['num_of_changes'] = int(numpy.random.normal(5.9,2))
            available_friends = list(self.get_agents(drunk=False,
                                                     pub=None,
                                                     in_a_group=False,
                                                     age=self['age']))
                                                     
            if not available_friends or len(available_friends)==1:
                self.info('Life sucks and I\'m alone!')
                return self.at_home
            befriended = self.try_friends(available_friends)
            if befriended:
                #Se les da una hora de salir a todos la misma, quizás hacer en una función
                return self.looking_for_pub#, self.env.timeout(3)--mismo comentario de going_out_time
        else:
            self.info('{} has a group already' .format(self.id))
            return self.looking_for_pub #No pasar al siguiente hasta que pasen going_out_time pasos

    @state
    def looking_for_pub(self):
        '''Look for a pub that accepts me and my friends'''
        if self['pub'] != None:
            return self.sober_in_pub
        self.debug('I am looking for a pub')
        group = list(self.get_neighboring_agents())

        r = random()


        # ESTO DEPENDE DE LOS ITINERARIOS
        # TENDRÁ QUE EMPEZAR CADA UNO EN UN SITIO DEPENDIENDO DE LA EDAD Y LUEGO SIGUEN INTINERARIOS FIJOS
        # CON UNA CIERTA PROBABILIDAD

        #Preguntar como se ponen estas probabilidades en base a los estudios

        if(self['age'] == 15):

            if (0.4>r):
                available_pubs = self.env.available_pubs()
                

            elif (0.75>r):
                available_pubs = self.env.available_discos()

            else:
                available_pubs = self.env.available_street()

        elif(self['age'] == 20):

            if (0.5>r):
                available_pubs = self.env.available_pubs()
                



            elif (0.8>r):
                available_pubs = self.env.available_discos()

            else:
                available_pubs = self.env.available_street()

        else:

            if (0.6>r):
                available_pubs = self.env.available_pubs()
                

            elif (0.9>r):
                available_pubs = self.env.available_discos()

            else:
                available_pubs = self.env.available_street()



        for pub in available_pubs:
            
           
            self.debug('We\'re trying to get into {}: total: {}'.format(pub, len(group)))
            if self.env.enter(pub, self, *group):
                self.info('We\'re all {} getting in {}!'.format(len(group)+1, pub))
                capacity = self.env.return_occupancy(pub)
                self.info('{} now has {} people inside'.format(pub,capacity))
                return self.sober_in_pub
            else:
                self.info("We can\'t go inside {}".format(pub))

    @state
    def sober_in_pub(self):
      

        type = self.env.return_type(self['pub'])




        # ESTO DEPENDE DE LOS ITINERARIOS, QUITAR NUM_OF_CHANGES?
      
        if(type=="disco"):
            self['prob_change_bar'] = 0.01


        else:
            #Street o pub 
            self['prob_change_bar'] = 0.2


        if (self['is_leader'] and self['prob_change_bar']>random()) or (self['is_leader'] and not self.env.return_open(self['pub'])):
            self.change_bar()
            self['num_of_changes'] = self['num_of_changes']  + 1



        '''Drink up.'''
        self.drink()

        if self['pints'] > self['max_pints']:
            self['drunk'] = True
            self.info('I\'m so drunk.')
            return self.drunk_in_pub

    @state
    def drunk_in_pub(self):
        
        #Cuando están borrachos, NO se van a casa, pero pueden tener altercados. Coma etilico (o intoxicacion), pelea o violencia verbal
        #, vandalismo
        #Tanbien puede cambiar de bar. Comprobar lo mismo que en sober pero
        #cambiando parámetros
        if (self['is_leader'] and self['prob_change_bar']>random()) or (self['is_leader'] and not self.env.return_open(self['pub'])):
            self.change_bar()
            self['num_of_changes'] = self['num_of_changes']  + 1
        
        self.drink()

        if self['pints'] > self['altercation_drinkthreshold']:
            self.info('I got intoxicated')
            self['intoxicated'] = True
            return self.at_home

        #UNA VEZ BORRACHOS SU PROBABILIDAD DE ALTERCADOS SUBE, MIRAR COMO PONER LA PROBABILIDAD DE PELEAS
        # Y COMAS ETILICOS INICIAL EN LOS ESTUDIOS
      # out drunk

    @state
    def at_home(self):
        '''The end'''
        self.info('Life sucks. I\'m home!')
        self.die()
    



    def change_bar(self):
        self.info('This member is going to change pub: {}'.format(self.id))

        current_pub = self['pub']
        type = self.env.return_type(self['pub'])

        group = list(self.get_neighboring_agents())
        r= random()

        #ITINERARIOS AQUÍ. SI ESTABAN EN UN BAR PASAN A UN BAR, SI ESTÁN EN DISCOTECA PASAN A OTRA O A UN BAR, SI ESTAN EN
        #BOTELLON PASAN A BAR O A DISCO

        if(type== "disco"):

            available_pubs = self.env.available_discos()


        elif(type== "pub"):

            """if (0.8>r):"""
            available_pubs = self.env.available_pubs()

            """else:
                                                    available_pubs = self.env.available_discos()"""
            """Ahora no hay gente que vaya de bar a disco"""

        else:

            if (0.5>r):
                available_pubs = self.env.available_pubs()

            else:
                available_pubs = self.env.available_discos()

        if len(available_pubs) == 0:

            for friend in group:
                friend.set_state(self.at_home)
            self.info("Todo cerrado. Nos vamos a casa")
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
                    self.info("We can\'t go inside {}".format(pub))
                    #Pues buscan otra opcion
        



    
    def drink(self):
        price = self.env.return_price(self['pub'])
        
            
        if(self['prob_drink']>random() and price<self['money']):
            self['pints'] = self['pints'] + 1
            self['money'] = self['money'] -  price
            self.info('Cheers to that')
            
            self.debug('The price is {} € at {}'.format(price,self['pub']))

    def kick_out(self):
        self.set_state(self.at_home)

    def befriend(self, other_agent):
        '''
        Try to become friends with another agent. The chances of
        success depend on both agents' openness.
        '''
       
        self.env.add_edge(self, other_agent)
        self.info('Made some friend, agent {}'.format(other_agent.id))
        return True
        

    def try_friends(self, others):
        ''' Look for random agents around me and try to befriend them'''
        n=1
        befriended = False
        k = numpy.random.poisson(5.69)#k = randint(4, 6)
        shuffle(others)
        for friend in islice(others, k):  # random.choice >= 3.7
            if friend == self:
                continue
            if friend.befriend(self):
                self.befriend(friend)
                self.info('Hooray! new friend: {}'.format(friend.id))
                n = n+1
                befriended = True
            else:
                self.info('{} does not want to be friends'.format(friend.id))

        self['in_a_group'] = True
        self['group_size'] = n
        neighbors_leader = list(self.get_neighboring_agents())

        #print(*neighbors_leader)
        
        for people in neighbors_leader:
            people['in_a_group'] = True
            people['group_size'] = n
            for i in neighbors_leader:
                if (people!=i):
                    people.befriend(i)
        
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
        intoxicates = list(self.get_agents(intoxicated=True,
                                          state_id=Patron.drunk_in_pub.id))
        for intoxicate in intoxicates:
            self.info('Kicking out the intoxicated agents: {}'.format(intoxicate.id))
            intoxicate.kick_out()


        '''Echará a los que se han peleado en un local'''



        '''Politicas a probar'''
        """for pub in pubs:
                                    if self.now == 15:
                                        self.env.set_capacity(pub,0)"""

