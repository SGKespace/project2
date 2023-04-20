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
                "Адрес склада: Булькуновка, старый элеватор"


user_db = './stock.db'

sql_create_ssf_table = """ CREATE TABLE IF NOT EXISTS projects (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            chat_id text,
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
                                            delivery_by_courier INTEGER); """

                                            # id INTEGER PRIMARY KEY AUTOINCREMENT,   он же номер бокса (также его можно использовать для формирования QR кода)
                                            # client_name text,                       ФИО клиента
                                            # client_address text,                    адрес
                                            # client_phone text,                      телефон
                                            # storage text,                           название склада
                                            # start_date date,                        дата начала хранения
                                            # end_date date,                          срок хранения (оплатил до этой даты)
                                            # space float,                            объем хранимых вещей
                                            # weight float,                           вес хранимых вещей
                                            # items text,                             список вещей
                                            # price float,                            стоимость хранения (до конца срока хранения)
                                            # delivery_by_courier bool,               доставка курьером (да/нет)