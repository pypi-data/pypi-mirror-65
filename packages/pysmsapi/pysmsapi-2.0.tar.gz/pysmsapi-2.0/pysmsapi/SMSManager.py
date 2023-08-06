import requests
from json import JSONDecodeError

class BadKeyError(Exception):
    pass
class SqlError(Exception):
    pass
class BadActionError(Exception):
    pass
class BadServiceError(Exception):
    pass
class NoBalanceError(Exception):
    pass
class NoNumbersError(Exception):
    pass
class NoActionError(Exception):
    pass


class API:

    api_key = None
    phones = {}

    def __init__(self, api_key:str) -> None:
        self.api_key = api_key

    def __getresp__(self,url:str) -> dict:
        min_url = 'https://smshub.org/stubs/handler_api.php?' + url
        try:
            req = requests.get(min_url)
            res = req.json()
        except JSONDecodeError:
            res = req.text
        if isinstance(res, dict):
            return res
        
        if 'BAD_KEY' in res:
            raise BadKeyError("Please set valid api-key!")
        
        elif 'ERROR_SQL' in res:
            raise SqlError(r"Server error! Wait for fix /(~)_(~)\ ")
        
        elif "BAD_ACTION" in res:
            raise BadActionError("Bad action! Please contact to developer.")

        elif 'BAD_SERVICE' in res:
            raise BadServiceError("Bad service! If you use correct service contact to Sms hub!")
        
        elif 'WRONG_SERVICE' in res:
            raise BadServiceError("Wrong service! If you use correct contact to Sms hub!")

        elif 'NO_BALANCE' in res:
            raise NoBalanceError("You don't have money to buy this phone-number!")

        elif 'NO_NUMBERS' in res:
            raise NoNumbersError("There are numbers with your service/country/operator!")

        elif 'NO_ACTIVATION' in res:
            raise NoActionError("You haven't a number with this ID!")

        response = {}
        if 'getBalance' in url:
            response[res.split(':')[0]] = res.split(':')[1]
        elif 'getNumber' in url:
            response['id'] = res.split(':')[1]
            response['number'] = res.split(':')[2]
        elif 'setStatus' in url:
            response['status'] = res.replace(' ', '')
        elif 'getStatus' in url:
            if 'STATUS_WAIT_CODE' in res or 'STATUS_CANCEL' in res:
                response['status'] = res.replace(' ', '')
            else:
                response['status'] = res.split(':')[0]
                response['substatus'] = res.split(':')[1]
        return response 
    
    def balance(self) -> float:
        return self.__getresp__(f'api_key={self.api_key}&action=getBalance')['ACCESS_BALANCE']

    def phone(self,service) -> str:
        response = self.__getresp__(f'api_key={self.api_key}&action=getNumber&service={service}&operator=any&country=0')
        self.phones[response['number']] = response['id']
        return response['number']
        
    def setStatus(self,phone:str, status:int) -> str:
        if phone in self.phones:
            phone_id = self.phones[phone]
        return self.__getresp__(f"api_key={self.api_key}&action=setStatus&status={str(status)}&id={phone_id}")

    def getStatus(self,phone:str) -> str:
        if phone in self.phones:
            phone_id = self.phones[phone]
        return self.__getresp__(f"api_key={self.api_key}&action=getStatus&id={phone_id}")