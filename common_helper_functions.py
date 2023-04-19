text_start = "Здравствуйте. \n\n " \
            "Этот бот поможет вам узнать как хранить вещи на складе с безопасной доставкой.\n\n" \
             "<b>Удобство несомненно в следующих случаях:</b> \n" \
             "- при переезде\n" \
             "- при сезонном мспользовании (напрмер мотоцикл зимой)\n" \
             "- при отложенном использовании (детские вещи, книги)"

text_help = "Часто задаваемые вопросы: \n\n" \
            " <b> Что принимается на хранение: </b> \n" \
            "Мебель\n" \
            "Бытовая техника\n" \
            "Одежда и обувь\n" \
            "Инструменты\n" \
            "Посуда\n" \
            "Книги\n" \
            "Шины\n" \
            "Велосипеды\n" \
            "Мотоциклы и скутеры\n\n" \
            " <b>Что не принимается на хранение:</b>\n" \
            "Алкоголь\n" \
            " Продукты \n" \
            "Деньги и драгоценности \n" \
            "Изделия из натурального меха\n" \
            "Живые цветы и растения\n" \
            "Домашние питомцы\n" \
            "Оружие и боеприпасы \n" \
            "Взрывоопасные вещества и токсины\n" \
            "Лаки и краски в негерметичной таре\n" \
            "Любой мусор и отходы"

text_Contacts = "Имя владельца Николай Николаевич Николаев\n " \
                "e-mail: xxxxxxxx.xxx \n " \
                "ICQ: xxxxxxxxx \n " \
                "Tel: xxxxxxxxx \n " \
                "Адрес: Булькуновка, старый элеватор"


user_db = './stock.db'
sql_create_ssf_table = """ CREATE TABLE IF NOT EXISTS projects (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            dtc_b integer, 
                                            entry_p text,
                                            cond text,
                                            pair text,            
                                            cp integer,           
                                            tp1 integer,          
                                            Pr1 integer,          
                                            tp2 integer,          
                                            Pr2 integer,          
                                            tp3 integer,          
                                            Pr3 integer,          
                                            SL integer,           
                                            sum_inv_fun integer,  
                                            shoulder integer,     
                                            dtc_e integer,        
                                            Dtc_e1 integer,       
                                            Sum_p1 integer,       
                                            Dtc_e2 integer,       
                                            Sum_p2 integer,       
                                            Dtc_e3 integer,       
                                            Sum_p3 integer,       
                                            Dtc_es integer,       
                                            Sum_sl integer,       
                                            sum_b integer,        
                                            sum_e integer,        
                                            delta integer,
                                            ord_1 integer,
                                            ord_2 integer,
                                            ord_3 integer,
                                            ord_4 integer,
                                            ord_5 integer,
                                            status integer         
                                            ); """

sql_create_ssf_table = """ CREATE TABLE IF NOT EXISTS projects (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            client_name text,
                                            client_address text,
                                            client_phone text,
                                            storage text,
                                            start_date date,
                                            end_date date,
                                            space float,          
                                            weight float,          
                                            items text,          
                                            price float,          
                                            ); """