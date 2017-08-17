import tornado.ioloop
import tornado.web
import sqlite3
import md5

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("home.html");

class LoginHandler(tornado.web.RequestHandler):
    def post(self):
        con = sqlite3.connect("database.db")
        c = con.cursor()
        # hashing twice for extra security
        secure = md5.new(self.get_argument("password")).hexdigest()
        mostsecure = md5.new(secure).hexdigest()
        login = c.execute("SELECT * FROM users WHERE username = '" + self.get_argument("username") + "' AND password = '" + mostsecure + "'").fetchone()
        if login != None:
            flag = open("flag")
            self.write(flag.read())
        else:
            self.write("wrong login")
        print login

class GetSource(tornado.web.RequestHandler):
    def get(self):
        f = open("server.py")
        self.write(f.read())

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/login", LoginHandler),
        (r"/source", GetSource)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8080) #TODO: Fix port
    tornado.ioloop.IOLoop.current().start()
