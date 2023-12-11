import requests


class LolzteamApi:
    def __init__(self, token, userid=None, baseUrl="https://api.zelenka.guru/"):
        self.token = token
        self.userid = userid
        self.baseUrl = baseUrl
        self.session = requests.session()
        self.session.headers = {'Authorization': f'Bearer {self.token}'}

    def market_me(self):
        return self.session.get(self.baseUrl + f'market/me').json()

    def market_list(self, category=None, pmin=None, pmax=None, title=None, parse_sticky_items=None):
        if category:
            data = {}
            if title: data['title'] = title
            if pmin: data['pmin'] = pmin
            if pmax: data['pmax'] = pmax
            if parse_sticky_items: data['parse_sticky_items'] = parse_sticky_items
            return self.session.get(self.baseUrl + f'market/{category}', params=data).json()
        else:
            return self.session.get(self.baseUrl + 'market').json()

    def market_orders(self, category=None, pmin=None, pmax=None, title=None, parse_sticky_items=None):
        if not self.userid:
            raise NotSetUserid
        if category:
            data = {}
            if title: data['title'] = title
            if pmin: data['pmin'] = pmin
            if pmax: data['pmax'] = pmax
            if parse_sticky_items: data['parse_sticky_items'] = parse_sticky_items
            return self.session.get(self.baseUrl +
                                    f'market/user/{self.userid}/orders/{category}', params=data).json()
        else:
            return self.session.get(self.baseUrl + f'market/user/{self.userid}/orders').json()

    def market_fave(self):
        return self.session.get(self.baseUrl + f'market/fave').json()

    def market_viewed(self):
        return self.session.get(self.baseUrl + f'market/viewed').json()

    def market_item(self, item):
        return self.session.get(self.baseUrl + f'market/{item}').json()

    def market_reserve(self, item):
        return self.session.post(self.baseUrl + f'market/{item}/reserve', data={'price': self.market_item(item)['item']['price']}).json()

    def market_cancel_reserve(self, item):
        return self.session.post(self.baseUrl + f'market/{item}/cancel-reserve').json()

    def market_check_account(self, item):
        return self.session.post(self.baseUrl + f'market/{item}/check-account').json()

    def market_confirm_buy(self, item):
        return self.session.post(self.baseUrl + f'market/{item}/confirm-buy').json()

    def market_buy(self, item):
        res = self.market_reserve(item)
        if res['status']:
            res1 = self.market_check_account(item)
            if res1['status']:
                return self.market_confirm_buy()
            else:
                return res1
        else:
            return res

    def market_transfer(self, receiver, receiver_username, amount, secret_answer, currency='rub', comment=None, transfer_hold=None, hold_length_value=None, hold_length_option=None):
        data = {
            'user_id': receiver,
            'username': receiver_username,
            'amount': amount,
            'secret_answer': secret_answer,
            'currency': currency
        }
        if comment: data['comment'] = comment
        if transfer_hold: data['transfer_hold'] = transfer_hold
        if hold_length_value: data['hold_length_value'] = hold_length_value
        if hold_length_option: data['hold_length_option'] = hold_length_option

        return self.session.post(self.baseUrl + f'market/balance/transfer', data=data).json()

    def market_payments(self, type_=None, pmin=None, pmax=None, receiver=None, sender=None, startDate=None, endDate=None, wallet=None, comment=None, is_hold=None):
        if not self.userid:
            raise NotSetUserid
        data = {}
        if type_: data['type'] = type_
        if pmin: data['pmin'] = pmin
        if pmax: data['pmax'] = pmax
        if receiver: data['receiver'] = receiver
        if sender: data['sender'] = sender
        if startDate: data['startDate'] = startDate
        if endDate: data['endDate'] = endDate
        if wallet: data['wallet'] = wallet
        if comment: data['comment'] = comment
        if is_hold: data['is_hold'] = is_hold
        return self.session.get(self.baseUrl + f'market/user/{self.userid}/payments', params=data).json()

    def market_add_item(self, title, price, category_id, item_origin, extended_guarantee, currency='rub', title_en=None, description=None, information=None, has_email_login_data=None, email_login_data=None, email_type=None, allow_ask_discount=None, proxy_id=None):
        """_summary_

        Args:
            title (str): title
            price (int): price account in currency
            category_id (int): category id (readme)
            item_origin (str): brute, fishing, stealer, autoreg, personal, resale
            extended_guarantee (int): -1 (12 hours), 0 (24 hours), 1 (3 days)
            currency (str, optional): cny, usd, rub, eur, uah, kzt, byn, gbp. Defaults to 'rub'.
            title_en (str, optional): title english. Defaults to None.
            description (str, optional): public information about account. Defaults to None.
            information (str, optional): private information about account for buyer. Defaults to None.
            has_email_login_data (bool, optional): true or false. Defaults to None.
            email_login_data (str, optional): login:password. Defaults to None.
            email_type (str, optional): native or autoreg. Defaults to None.
            allow_ask_discount (bool, optional): allow ask discount for users. Defaults to None.
            proxy_id (int, optional): proxy id. Defaults to None.
        """
        data = {
            'title': title,
            'price': price,
            'category_id': category_id,
            'currency': currency,
            'item_origin': item_origin,
            'extended_guarantee': extended_guarantee
        }
        if title_en: data['title_en'] = title_en
        if description: data['description'] = description
        if information: data['information'] = information
        if has_email_login_data: data['has_email_login_data'] = has_email_login_data
        if email_login_data: data['email_login_data'] = email_login_data
        if email_type: data['email_type'] = email_type
        if allow_ask_discount: data['allow_ask_discount'] = allow_ask_discount
        if proxy_id: data['proxy_id'] = proxy_id

        return self.session.post(self.baseUrl + f'market/item/add', data=data).json()

    def market_add_item_check(self, item, login=None, password=None, loginpassword=None, close_item=None):
        data = {}
        if login: data['login'] = login
        if password: data['password'] = password
        if loginpassword: data['loginpassword'] = loginpassword
        if close_item: data['close_item'] = close_item

        return self.session.post(self.baseUrl + f'market/{item}/goods/check', data=data).json()

    def market_get_email(self, item, email):
        return self.session.get(self.baseUrl + f'market/{item}/email-code', params={'email': email}).json()


class NotSetUserid(Exception):
    pass
