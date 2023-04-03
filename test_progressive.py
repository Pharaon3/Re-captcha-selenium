from progressive import ProgressiveParser
import pandas


if __name__ == '__main__':
    df = pandas.read_csv('./test_data.csv')
    data = df.to_dict(orient='records')
#     data = [
# ["TERRY", "MORT", "702 1ST AVE", "CLINTON", "IA", "52732", "02/01/1970"],
# ["DONNA", "TINSLEY", "17444 MCDOUGALL ST","DETROIT","MI","48212","11/03/1974"],
# ["JOHN", "RALSTON", "67 ASPEN CIR","SHELBURNE","VT","05482","08/31/1983"],
# ["ANTONIO", "OWEN", "338 CHALMERS ST","SOUTH BOSTON","VA","24592","04/06/1984"],
# ["DAVID", "SMITH", "211 KENDRA LN","PIKEVILLE","TN","37367","12/29/1971"],
# ["NATHAN", "BARRIE", "222 LISA PL","NORTH BRUNSWICK","NJ","08902","12/26/1997"],
# ["ESTELLA", "MELCHOR", "5425 NIGHT SWIM LN","LAS VEGAS","NV","89113","08/21/1971"],
# ["RAYMOND", "ALSTON", "72 MARYLAND AVE","FREEPORT","NY","11520","01/09/1958"],
# ["CHARLES", "BERTEL", "1601 9TH ST S","FARGO","ND","58103","09/29/1950"],
# ["WILLIAM", "BOECK", "1567 WALPOLE DR", "CHESTERFIELD","MO","63017","01/13/1961"]
#                             ]
    for i in data:
        print(list(i.values()))

        try:
            result = ProgressiveParser(True, ["user-maximcrawl:cokeISit@gate.dc.smartproxy.com:20000"]).parse_site(
                *i.values()
            )
            print(f"valid: {result.valid}")
            print(f"cars: {result.cars}")
            print(f"has_car: {result.has_car}")
            print(f"is_customer: {result.is_customer}")

        except Exception as e:
            print(e)

