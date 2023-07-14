# import pyqiwi
# from uuid import uuid4
# from dataclasses import dataclass
# import datetime


# from data.config import qiwi_key, qiwi_token, qiwi_phone

# wallet = pyqiwi.Wallet(number=qiwi_phone, token=qiwi_token)


# class NotEnoughMoney(Exception):  # класс поднимающий ошибку в случае если человек заплатил меньше чем нужно 
#     pass


# class NotPaymentFound(Exception): #  класс поднимающий ошибку если траназкция не была проведена 
#     pass


# @dataclass()                        # Люблю.Удобно.
# class Payment:                      # класс куда попадают стоимость оплаты и персональный id
#     amount: int
#     id: str = None

#     def create(self):               # здесь генерируется id(рандомно)
#         self.id = str(uuid4())

#     def check_payment(self):  # здесь мы проверяем наличие оплаты по транзакциям за 2 дня
#         transactions = wallet.history(start_date=datetime.datetime.now() - datetime.timedelta(days=2)).get('transactions')
#         for transaction in transactions:  
#             if transaction.comment:       
#                 if str(self.id) in transaction.comment:  
#                     if float(transaction.total.amount) >= self.amount: # если было переведено недостаточно средств
#                         return True                                    
#                     else:                                              
#                         raise NotEnoughMoney
#         else:                                                         
#             raise NotPaymentFound

#     @property  
#     def invoice(self): # здесь мы формируем ссылку для оплаты  
#         link = "https://oplata.qiwi.com/create?publicKey={publickey}&amount={amount}&comment={comment}"
#         return link.format(publickey=qiwi_key, amount=self.amount, comment=self.id)
  
