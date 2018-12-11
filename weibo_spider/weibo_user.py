class weibo_user:
    def __init__(self,user_id,name,url):
        self.name=name
        self.userid=user_id
        self.url=url
        self.friend_list = {}
        pass

    def get_id(self):
        return self.userid

    def get_url(self):
        return self.url

    def get_info(self):
        return "\t".join([self.name,self.userid,self.url])

    def get_friends(self):
        return self.friend_list

    def add_friend(self,user):
        if(user.get_id() not in self.friend_list.keys()):
            self.friend_list[user.get_id()]=user