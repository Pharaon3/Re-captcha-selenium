from travelers import TravelersParser
import pandas

if __name__ == '__main__':
    df = pandas.read_csv('./test_data.csv', converters={'zip': str})
    data = df.to_dict(orient='records')
    for i in data:
        print(list(i.values()))
        try:
            result = TravelersParser(True, ["user-maximcrawl:cokeISit@gate.dc.smartproxy.com:20000"]).parse_site(
                *i.values()
            )

            print(f"valid: {result.valid}")
            print(f"cars: {result.cars}")
            print(f"has_car: {result.has_car}")
            print(f"is_customer: {result.is_customer}")
        except Exception as e:
            print(e)
