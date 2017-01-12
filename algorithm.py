from random import randint, sample,uniform,seed
import math
import operator

#####################################################################################################

'''
Here in user_products should be list of products chosen by user!!!!
'''
user_products = ['apple','vodka','pasta','chicken','salt','ketchup','juice','bread','rice','sausage']

'''
Here in user_x, user_y should be coordinates of user house as integers from 0 to 100:
'''
#####################################################################################################

user_x = 50
user_y = 50

#####################################################################################################


#fix random
#seed(105)


'''
In class Items we store list of all products, on user side this list of products should be displayed
and user chooses products to user_products from this list
'''
class Items:
    list=['apple','banana','carrot','garlic','lemon','mushroom','orange','pea','peanut','pepper',
          'pineapple', 'strawberry', 'potato', 'tomato', 'watermelon','juice','bacon','beans',
          'beer', 'bread', 'cheese', 'chicken', 'coffee','corn','eggs', 'fish','ham','honey',
          'ketchup', 'milk', 'pasta','wine', 'vodka','yogurt','cream', 'onion','salmon','tea',
          'cabbage','rice','butter','sausage','beef','strawberry','cucumber', 'water','sugar',
          'salt','flour','pork']

#####################################################################################################

'''
Fix avarage prices for every item
'''
global prices
prices={}
for item in Items.list:
    prices[item] = round(uniform(1.0,5.0),2)


#####################################################################################################



class Shop:
    def __init__(self, size):
        #random coordinates of shop on the imaginary map
        self.x = randint(0,100)
        self.y = randint(0,100)
        #list of products in the shop
        self.products={}
        #generate list of products in the shop of given amount (size)
        self.list_of_products=sample(Items.list,size)
        #generate price of products in shop +-0.5 from avarage price generated above
        for item in self.list_of_products:
            self.products[item]=round(prices[item]+uniform(-0.5,0.5),2)
        self.average_price=0

    #get list of products in the shop, which are present in user_products list
    def remove_redundant(self, user_products):
        self.new_products={}
        for item in self.products:
            if item in user_products:
                self.new_products[item]=self.products[item]
    #calculate average price of products in shop
    def average(self):
        self.average_price=sum(self.new_products.values())/len(self.new_products)

#####################################################################################################

'''
A bit stupid generation of list with 10 shops, in the shops list instances of class are stored
'''
'''
shops=[]
shops.append(Shop(25))
shops.append(Shop(25))
shops.append(Shop(25))
shops.append(Shop(25))
shops.append(Shop(25))
shops.append(Shop(25))
shops.append(Shop(25))
shops.append(Shop(25))
shops.append(Shop(25))
shops.append(Shop(25))

#list of products in the shop, which are present in user_products list as well as average prices

for i in shops:
    i.remove_redundant(user_products)
    i.average()
'''

#####################################################################################################

routes = []


'''
This function is for the first case, when user want to spend the least possible amount of money to
buy his products
'''
def poor(shops, user_products, user_x, user_y):
    #function to calculate distances between coordinates for future tsp
    def distance(coord1, coord2):
        distance = math.sqrt(((int(coord1[0]) - int(coord2[0])) ** 2 + (int(coord1[1]) - int(coord2[1])) ** 2))
        return distance
    #brute-force tsp function
    def tsp(start, distances, route, d):
        route.append(start)
        if len(route) > 1:
            d += distances[route[-2]][start]
        if (len(distances) == len(route)) and (distances[route[-1]].has_key(route[0])):
            global routes
            route.append(route[0])
            d += distances[route[-2]][route[0]]
            routes.append([d, route])
            # print routes
            return
        for city in distances:
            if (city not in route) and (distances[city].has_key(start)):
                tsp(city, dict(distances), list(route), d)
    '''
    This part finds least price of every product and stores in the dictionary produce, shop
    with least price of this product and price of the product
    '''
    pool = dict((el,(10,999)) for el in user_products)

    for item in user_products:
        for number,shop in enumerate(shops):
            try:
                price = shop.new_products[item]
                if price<pool[item][1]:
                    pool[item]=(number,price)
            except:
                pass
    '''
    In this part we find total price of products, which user bought, as well as prepare output
    in following form: shop, its coordinates and product bought there
    '''
    output={}

    total_price =0
    for item in pool:
        total_price=total_price+shops[pool[item][0]].products[item]
        if pool[item][0] in output:
            output[pool[item][0]][1].append(item)
        else:
            output[pool[item][0]] = ((shops[pool[item][0]].x, shops[pool[item][0]].y), [item])

    '''
    Here dictionary of distances between shops(+home) is calculated in order to do TSP on graph
    '''
    distances={}
    for item in output:
        sub = {}
        sub['Home'] = distance(output[item][0], [user_x,user_y])
        for element in output:
            if item != element:
                sub[element] = distance(output[item][0], output[element][0])
        distances[item] = sub
    #print distances
    sub = {}
    for item in output:
        sub[item]=distance(output[item][0], [user_x,user_y])
    distances['Home'] = sub

    '''
    Calculate TSP, find minimum distance and path
    '''
    tsp('Home', distances, [], 0)
    path = sorted(routes)[0]
    return pool, output, total_price, path


#a,b,c,d = poor(shops,user_products,50,50)



#####################################################################################################



'''
This part for second option, where only thing user cares about is to visit least
amount of shops possible, he doesn't care about price at all
'''
routes2 = []
def minimum_shops (shops,user_products, user_x, user_y):
    #distance for TSP
    def distance(coord1, coord2):
        distance = math.sqrt(((int(coord1[0]) - int(coord2[0])) ** 2 + (int(coord1[1]) - int(coord2[1])) ** 2))
        return distance
    #tsp function
    def tsp2(start2, distances2, route2, d2):
        route2.append(start2)
        if len(route2) > 1:
            d2 += distances2[route2[-2]][start2]
        if (len(distances2) == len(route2)) and (distances2[route2[-1]].has_key(route2[0])):
            global routes2
            route2.append(route2[0])
            d2 += distances2[route2[-2]][route2[0]]
            routes2.append([d2, route2])
            # print routes
            return
        for city in distances2:
            if (city not in route2) and (distances2[city].has_key(start2)):
                tsp2(city, dict(distances2), list(route2), d2)
    '''
    The base for this case is greedy unweighted setcover problem, the main set is list of all
    products, which user wants to buy. Subsets are goods from user list, which can be found in
    each shop. Nothing difficult, just unweighted set cover
    '''
    U = user_products[:]
    Y={}
    for i in range(len(shops)):
        Y[str(i)]=shops[i].new_products.keys()
    count ={}
    intersect={}
    output={}
    while (U):
        for i in Y:
            intersect[i] = set(Y[i]).intersection(U)
            count[i] = len(intersect[i])

        deleted = sorted(count.items(), key=operator.itemgetter(1), reverse=True)[0][0]
        output[int(deleted)]=list(intersect[deleted])
        U = list(set(U) - set(Y[str(deleted)]))
        Y.pop(str(deleted))
        count.pop(str(deleted))
        intersect.pop(str(deleted))

    '''
    Same as above, calculate distance for TSP and than do TSP
    '''
    distances = {}
    for item in output:
        sub = {}
        sub['Home'] = distance([shops[item].x,shops[item].y], [user_x, user_y])
        for element in output:
            if item != element:
                sub[element] = distance([shops[item].x,shops[item].y], [shops[element].x,shops[element].y])
        distances[item] = sub
    sub = {}
    for item in output:
        sub[item] = distance([shops[item].x,shops[item].y],[user_x, user_y])
    distances['Home'] = sub
    tsp2('Home', distances, [], 0)
    path = sorted(routes2)[0]
    return output, path



'''
The most interesting part is here. Here we try to find optimal solution for user, where he can
walk not that big distance, visit not that much shops and spent not that much money. We try to
think as real human.
The logic is following: we start from our Home, than we calculated weights for graph
of all shops in specific way: distance multiplied by avarage price of that store. In reality
there are cheapest stores, and more expensive one, so if some shops is more far away than another
but has lowest avarage prices we will visit this store (if avarage price is much lower, or the store
is not that far from us). After choosing first closest store we add all items which can be bought there
to user_pool variable. Then in the while loop we go to the shop with lowest weight until user_pool
contains all products. Afterwards, we get some amount of shops, and than we choose from this shops
where it is better to buy each product. Afterwards we apply TSP as in all above cases
'''
def opt(shops, user_products,user_x,user_y):

    def distance(coord1, coord2):
        distance = math.sqrt(((int(coord1[0]) - int(coord2[0])) ** 2 + (int(coord1[1]) - int(coord2[1])) ** 2))
        return distance

    def tsp3(start3, distances3, route3, d3):
        route3.append(start3)
        if len(route3) > 1:
            d3 += distances3[route3[-2]][start3]
        if (len(distances3) == len(route3)) and (distances3[route3[-1]].has_key(route3[0])):
            global routes3
            route3.append(route3[0])
            d3 += distances3[route3[-2]][route3[0]]
            routes3.append([d3, route3])
            # print routes
            return
        for city in distances3:
            if (city not in route3) and (distances3[city].has_key(start3)):
                tsp3(city, dict(distances3), list(route3), d3)
    to_traverse=['Home']
    for i in range(10):
        to_traverse.append(i)

    #print to_traverse
    user_pool=[]
    distances={}
    visited=[]
    sub={}
    for number, shop in enumerate(shops):
        sub[number]=round(distance([shop.x,shop.y], [user_x,user_y])*shop.average_price,2)
    distances['Home'] = sub
    city_to_go = sorted(distances['Home'].items(), key=operator.itemgetter(1))[0][0]
    user_pool.extend(shops[city_to_go].new_products.keys())
    #print 'DIST',distances['Home']
    #print user_pool
    to_traverse.remove('Home')
    to_traverse.remove(city_to_go)
    #print to_traverse
    visited.append(city_to_go)
    while len(user_pool)<10:
        sub={}
        for item in to_traverse:
            sub[item] = round(distance([shops[item].x,shops[item].y], [shops[visited[-1]].x,shops[visited[-1]].y])*shops[item].average_price,2)
        distances[visited[-1]]=sub
        next_city = sorted(distances[visited[-1]].items(), key=operator.itemgetter(1))[0][0]
        user_pool.extend(shops[next_city].new_products.keys())
        temp = user_pool[:]
        myset = set(temp)
        user_pool = list(myset)
        to_traverse.remove(next_city)
        visited.append(next_city)
    #print 'visited', visited
    shop_products={}
    for item in visited:
        shop_products[item]=shops[item].new_products
    #print shop_products
    where_can_buy = dict((el, []) for el in user_products)
    bought = dict((el,[]) for el in visited)
    #print 'b', bought
    #print where_can_buy
    for key in where_can_buy:
        for item in visited:
            if key in shops[item].new_products.keys():
                where_can_buy[key].append(item)
    #print where_can_buy
    #print 'shalom', shop_products[1]['vodka']
    def choose_min(product):
        stores = where_can_buy[product]
        min = 999
        shop = None
        for store in stores:
            if shop_products[store][product]<min:
                min = shop_products[store][product]
                shop = store
        return min, shop
    total_paid=0
    for item in user_products:
        price, store = choose_min(item)
        total_paid=total_paid+price
        bought[store].append(item)
    #print 'BOUGHT', bought
    for key in bought:
        if len(bought[key])==0:
            visited.remove(key)
    #print total_paid
    #print 'VISITED', visited
    distances = {}
    for item in visited:
        sub = {}
        sub['Home'] = distance([shops[item].x, shops[item].y], [user_x, user_y])
        for element in visited:
            if item != element:
                sub[element] = distance([shops[item].x, shops[item].y], [shops[element].x, shops[element].y])
        distances[item] = sub
    #print distances
    sub = {}
    for item in visited:
        sub[item] = distance([shops[item].x, shops[item].y], [user_x, user_y])
    distances['Home'] = sub
    tsp3('Home', distances, [], 0)
    path = sorted(routes3)[0]
    return bought, total_paid, path


def get_coords(shops):
    coords = {}
    for num, shop in enumerate(shops):
        coords[num] = (shop.x, shop.y)
    return coords

def main_func(set, choice, x, y):
    shops = []
    shops.append(Shop(25))
    shops.append(Shop(25))
    shops.append(Shop(25))
    shops.append(Shop(25))
    shops.append(Shop(25))
    shops.append(Shop(25))
    shops.append(Shop(25))
    shops.append(Shop(25))
    shops.append(Shop(25))
    shops.append(Shop(25))

    for i in shops:
        i.remove_redundant(user_products)
        i.average()
    what_and_where = {}
    total_price=0
    total_path=0
    path=[]
    if choice == 'poor':
        global routes
        routes = []
        a, b, total_price, d = poor(shops, set, x, y)
        total_path = d[0]
        path = d[1]

        for value in b:
            what_and_where[value]=b[value][1]
        coords = get_coords(shops)


    elif choice == 'rich':
        global routes2
        routes2=[]
        what_and_where, all = minimum_shops(shops, set, x, y)
        total_price=None
        path = all[1]
        total_path = all[0]
        coords = get_coords(shops)


    elif choice == 'optimal':
        global routes3
        routes3=[]
        what_and_where, total_price,all = opt(shops, set, x, y)
        path=all[1]
        total_path = all[0]
        coords = get_coords(shops)

    return (total_price, total_path), path, what_and_where

print main_func(user_products,'poor',user_x,user_y)
    #print coords
