import ip2location

def get_location_from_ipapi(ip_address):
        db_file = "ip2location.dat" 
        db = ip2location.IP2Location(db_file)
        result = db.get_all(ip_address)
        if result:
            city = result["city"]
            country = result["country_short"]
            return city, country
        else:
            print('Неизвестная ошибка')
            return None, None