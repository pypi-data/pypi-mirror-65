from PyQt5.QtCore import QObject
from caloriestracker.libcaloriestrackerfunctions import a2s, ca2s, rca2s, n2s
from caloriestracker.libmanagers import ObjectManager_With_IdName_Selectable, ObjectManager_With_IdDatetime_Selectable, ManagerSelectionMode
from caloriestracker.ui.myqtablewidget import qleft, qnumber, qnumber_limited, qcrossedout
from colorama import Style, Fore
from decimal import Decimal
## Clase parar trabajar con las opercuentas generadas automaticam
class Meal:
    ##Meal(mem)
    ##Meal(mem,rows) #Uses products_id and users_id in row
    ##Meal(mem,datetime,product,name,amount,users_id,id)
    def __init__(self, *args):        
        def init__create( dt, product, amount, user, system_product, id):
            self.datetime=dt
            self.product=product
            self.amount=amount
            self.user=user
            self.system_product=system_product
            self.id=id
            return self
        # #########################################
        self.mem=args[0]
        if len(args)==1:#Meal(mem)
            init__create(*[None]*6)
        elif len(args)==2:#Meal(mem,rows)
            product=self.mem.data.products.find_by_id_system(args[1]['products_id'], args[1]['system_product'])
            user=self.mem.data.users.find_by_id(args[1]['users_id'])
            init__create(args[1]['datetime'], product, args[1]['amount'], user, args[1]['system_product'], args[1]['id'])
        elif len(args)==7:#Meal(mem,datetime,product, amount,users_id,id)
            init__create(*args[1:])

    def fullName(self):
        return self.product.fullName() 

    def calories(self):
        try:
            return self.amount * self.product.calories/self.product.amount
        except:
            None
        
    def fat(self):
        try:
            return self.amount * self.product.fat/self.product.amount
        except:
            None

    def protein(self):
        try:
            return self.amount * self.product.protein/self.product.amount
        except:
            None

    def carbohydrate(self):
        try:
            return self.amount * self.product.carbohydrate/self.product.amount
        except:
            None

    def salt(self):
        try:
            return self.amount * self.product.salt/self.product.amount
        except:
            None

    def fiber(self):
        try:
            return self.amount * self.product.fiber/self.product.amount
        except:
            None

    def meal_hour(self):
        return str(self.datetime.time())[0:5]

    def product_type(self):
        if self.elaboratedproducts_id==None and self.companies_id==None:
            return "Basic"
        elif self.elaboratedproducts_id!=None:
            return "Personal"
        elif self.companies_id!=None:
            return "Manufactured"
        else:
            return "Rare"
            
    def save(self):
        if self.id==None:
            self.id=self.mem.con.cursor_one_field("insert into meals(datetime,products_id,amount, users_id, system_product) values (%s, %s,%s,%s,%s) returning id",(self.datetime, self.product.id, self.amount, self.user.id, self.system_product))
        else:
            self.mem.con.execute("update meals set datetime=%s,products_id=%s,amount=%s,users_id=%s, system_product=%s where id=%s", (self.datetime, self.product.id, self.amount, self.user.id, self.system_product,  self.id))

    def delete(self):
        self.mem.con.execute("delete from meals where id=%s", (self.id, ))


class MealManager(QObject, ObjectManager_With_IdDatetime_Selectable):
    ##MealManager(mem)
    ##MealManager(mem,sql, progress)
    def __init__(self, *args ):
        QObject.__init__(self)
        ObjectManager_With_IdName_Selectable.__init__(self)
        self.mem=args[0]
        if len(args)==2:
            self.load_db_data(*args[1:])
        self.setSelectionMode(ManagerSelectionMode.Object)

    def load_db_data(self, sql):
        rows=self.mem.con.cursor_rows(sql)
        for row in rows:
            self.append(Meal(self.mem, row))
        return self

    def calories(self):
        r=Decimal(0)
        for meal in self.arr:
            if meal.calories()==None:
                return None
            r=r+meal.calories()
        return r
    def fat(self):
        r=Decimal(0)
        for meal in self.arr:
            if meal.fat()==None:
                return None
            r=r+meal.fat()
        return r
    def protein(self):
        r=Decimal(0)
        for meal in self.arr:
            if meal.protein()==None:
                return None
            r=r+meal.protein()
        return r
    def carbohydrate(self):
        r=Decimal(0)
        for meal in self.arr:
            if meal.carbohydrate()==None:
                return None
            r=r+meal.carbohydrate()
        return r
    def salt(self):
        r=Decimal(0)
        for meal in self.arr:
            if meal.salt()==None:
                return None
            r=r+meal.salt()
        return r
    def fiber(self):
        r=Decimal(0)
        for meal in self.arr:
            if meal.fiber()==None:
                return None
            r=r+meal.fiber()
        return r
    def grams(self):
        r=Decimal(0)
        for meal in self.arr:
            if meal.amount==None:
                return None
            r=r+meal.amount
        return r

    def max_name_len(self):
        r=0
        for meal in self.arr:
            if len(meal.fullName())>r:
                r=len(meal.fullName())
        return r
        
    def show_table(self, date):
        maxname=self.max_name_len()
        if maxname<17:#For empty tables totals
            maxname=17
        maxlength=5+2+maxname+2+7+2+7+2+7+2+7+2+7+2+7

        print (Style.BRIGHT+ "="*(maxlength) + Style.RESET_ALL)
        print (Style.BRIGHT+ "{} NUTRICIONAL REPORT AT {}".format(self.mem.user.name.upper(), date).center(maxlength," ") + Style.RESET_ALL)
        print (Style.BRIGHT+ Fore.YELLOW + "{} Kg. {} cm. {} years".format(self.mem.user.last_biometrics.weight, self.mem.user.last_biometrics.height, self.mem.user.age()).center(maxlength," ") + Style.RESET_ALL)
        print (Style.BRIGHT+ Fore.BLUE + "IMC: {} ==> {}".format(round(self.mem.user.last_biometrics.imc(),2),self.mem.user.last_biometrics.imc_comment()).center(maxlength," ") + Style.RESET_ALL)
        print (Style.BRIGHT+ "="*(maxlength) + Style.RESET_ALL)

        print (Style.BRIGHT+ "{}  {}  {}  {}  {}  {}  {}  {}".format("HOUR ","NAME".ljust(maxname," "),"GRAMS".rjust(7,' '), "CALORIE".rjust(7,' '), "CARBOHY".rjust(7,' '), "PROTEIN".rjust(7,' '), "FAT".rjust(7,' '), "FIBER".rjust(7,' ')) + Style.RESET_ALL)
        for meal in self.arr:
            print ( "{}  {}  {}  {}  {}  {}  {}  {}".format(meal.meal_hour(), meal.fullName().ljust(maxname), a2s(meal.amount),a2s(meal.calories()), a2s(meal.carbohydrate()), a2s(meal.protein()), a2s(meal.fat()),a2s(meal.fiber())) + Style.RESET_ALL)

        print (Style.BRIGHT+ "-"*(maxlength) + Style.RESET_ALL)
        total="{} MEALS WITH THIS TOTALS".format(self.length())
        print (Style.BRIGHT + "{}  {}  {}  {}  {}  {}  {}".format(total.ljust(maxname+7), a2s(self.grams()), ca2s(self.calories(),self.mem.user.last_biometrics.bmr()), ca2s(self.carbohydrate(),self.mem.user.last_biometrics.carbohydrate()), ca2s(self.protein(), self.mem.user.last_biometrics.protein()), ca2s(self.fat(),self.mem.user.last_biometrics.fat()), rca2s(self.fiber(),self.mem.user.last_biometrics.fiber())) + Style.RESET_ALL)
        recomendations="RECOMMENDATIONS"
        print (Style.BRIGHT + "{}  {}  {}  {}  {}  {}  {}".format(recomendations.ljust(maxname+7), n2s(), a2s(self.mem.user.last_biometrics.bmr()), a2s(self.mem.user.last_biometrics.carbohydrate()), a2s(self.mem.user.last_biometrics.protein()), a2s(self.mem.user.last_biometrics.fat()), a2s(self.mem.user.last_biometrics.fiber())) + Style.RESET_ALL)
        print (Style.BRIGHT + "="*(maxlength) + Style.RESET_ALL)

    def myqtablewidget(self, wdg):        
        hh=[self.tr("Hour"), self.tr("Name"), self.tr("Foodtype"), self.tr("Grams"), self.tr("Calories"), self.tr("Carbohydrates"), self.tr("Protein"), self.tr("Fat"), self.tr("Fiber")]
        data=[]
        for i, o in enumerate(self.arr):
            foodtype=None if o.product.foodtype is None else o.product.foodtype.name
            data.append([
                o.datetime.time(), 
                o.product.fullName(), 
                foodtype, 
                o.amount, 
                o.calories(), 
                o.carbohydrate(), 
                o.protein(), 
                o.fat(), 
                o.fiber(), 
                o, 
            ])
        wdg.setDataWithObjects(hh, None, data, zonename=self.mem.localzone, additional=self.myqtablewidget_additional)
        
    def myqtablewidget_additional(self, wdg):
        for i, o in enumerate(wdg.objects()):
            wdg.table.item(i, 1).setIcon(o.product.qicon())
        wdg.table.setRowCount(wdg.length()+2)
        if self.mem.user.last_biometrics.height!=None:#Without last_biometrics
            #Totals
            wdg.table.setItem(self.length(), 0, qcrossedout())
            wdg.table.setItem(self.length(), 1, qleft(self.tr("Total")))
            wdg.table.setItem(self.length(), 2, qcrossedout())
            wdg.table.setItem(self.length(), 3, qnumber(self.grams()))
            wdg.table.setItem(self.length(), 4, qnumber_limited(self.calories(), self.mem.user.last_biometrics.bmr()))
            wdg.table.setItem(self.length(), 5, qnumber_limited(self.carbohydrate(), self.mem.user.last_biometrics.carbohydrate()))
            wdg.table.setItem(self.length(), 6, qnumber_limited(self.protein(), self.mem.user.last_biometrics.protein()))
            wdg.table.setItem(self.length(), 7, qnumber_limited(self.fat(), self.mem.user.last_biometrics.fat()))
            wdg.table.setItem(self.length(), 8, qnumber_limited(self.fiber(), self.mem.user.last_biometrics.fiber(), reverse=True))
            #Recomendatios
            wdg.table.setItem(self.length()+1, 0, qcrossedout())
            wdg.table.setItem(self.length()+1, 1, qleft(self.tr("Recomendations")))
            wdg.table.setItem(self.length()+1, 2, qcrossedout())
            wdg.table.setItem(self.length()+1, 3, qcrossedout())
            wdg.table.setItem(self.length()+1, 4, qnumber(self.mem.user.last_biometrics.bmr()))
            wdg.table.setItem(self.length()+1, 5, qnumber(self.mem.user.last_biometrics.carbohydrate()))
            wdg.table.setItem(self.length()+1, 6, qnumber(self.mem.user.last_biometrics.protein()))
            wdg.table.setItem(self.length()+1, 7, qnumber(self.mem.user.last_biometrics.fat()))
            wdg.table.setItem(self.length()+1, 8, qnumber(self.mem.user.last_biometrics.fiber()))
        
