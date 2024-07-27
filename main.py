import flask
import pymongo

app = flask.Flask(__name__)


#Index Page
@app.route('/')
def index():
    return flask.render_template('index.html')


#mongodb connection
client = pymongo.MongoClient(
    "mongodb+srv://codex:<password>@cluster0.hmhik.mongodb.net/codex?retryWrites=true&w=majority"
)
mydb = client['codex']
mycol = mydb['user_data']


#Signin
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if flask.request.method == 'POST':
        city = {'Dubai': '1', 'Sharjah': '2', 'Abu Dhabi': '3', 'Ajman': '4'}
        global user_data
        user_data = {
            "username": flask.request.form['username'],
            "password": flask.request.form['password'],
            "email": flask.request.form['email'],
            "state": flask.request.form['state'],
            "city":
            flask.request.form['city' + city[flask.request.form['state']]],
            "category": flask.request.form['category'],
            "friends": ['pet_world'],
            "post": []
        }
        mycol.insert_one(user_data)
        if flask.request.form['category'] == 'business':
            return flask.render_template('business.html')
        elif flask.request.form['category'] == 'vet':
            return flask.render_template('vet.html')
        elif flask.request.form['category'] == 'not_business':
            return flask.render_template('user.html')


#Vet
@app.route('/Pet_Dotor', methods=['POST', 'GET'])
def vet():
    mycol.update_one(
        {
            "username": user_data['username'],
            "password": user_data['password']
        }, {
            '$set': {
                "collage": flask.request.form['collage'],
                "degree": flask.request.form["degree"],
                "clinic": flask.request.form['clinic'],
                "position": flask.request.form['position']
            }
        })
    return flask.render_template('Sucessful.html')


#not_business
@app.route('/not_business', methods=['POST', 'GET'])
def not_business():
    mycol.update_one(
        {
            "username": user_data['username'],
            "password": user_data['password']
        }, {
            '$set': {
                "pet_type": flask.request.form['pet_type'],
                "breed": flask.request.form["breed"]
            }
        })
    return flask.render_template('Sucessful.html')


#business
@app.route('/business', methods=['POST', 'GET'])
def business():
    mycol.update_one(
        {
            "username": user_data['username'],
            "password": user_data['password']
        }, {
            '$set': {
                "shopname": flask.request.form['shopname'],
                "website": flask.request.form['website'],
                "location": flask.request.form['location'],
            }
        })
    return flask.render_template('Sucessful.html')


#bio
@app.route('/bio', methods=['POST', 'GET'])
def bio():
    if flask.request.method == 'POST':
        mycol.update_one({"username": user_data['username']}, {
            '$set': {
                'bio': flask.request.form['bio'],
                "profile_pic": flask.request.files['profile_pic'].read()
            }
        })
    return flask.redirect("/#Signin")


#Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        global email1
        global passwd
        passwd = flask.request.form['password']
        email1 = flask.request.form['email']
        global user_login
        user_login = mycol.find()
        for i in user_login:
            if i['email'] == email1:
                if i['password'] == passwd:
                    return flask.redirect('Home')
                else:
                    return """<h1>Your password is wrong please make sure you enter the correct password</h1>
                    <a href='/'>Enter again</a>
                    """
        else:
            return """<h1>Your username is wrong please make sure you enter the correct username</h1>
                    <a href='/#Signin'>Enter again</a>
                    """


#Home Page
@app.route('/Home')
def home():
    try:
        user_post = mycol.find()
        user_multi = []
        friends = []
        for i in user_post:
            if i['post'] != []:
                for j in i['post']:
                    user_multi.append([])
                    user_multi[-1].append(i['username'])
                    user_multi[-1].append(j)
            if i['email'] == email1:
                print(email1, i['friends'])
                if i['friends'] != []:
                    for j in i['friends']:
                        friends.append(j)
        data = [user_multi, friends]
        user_multi.reverse()
        return flask.render_template('Home.html', data=data)
    except:
        return flask.redirect('/')


#Upload
@app.route('/Upload', methods=['GET', 'POST'])
def upload():
    try:
        return flask.render_template('Upload.html')
    except:
        return flask.redirect('/')


#post
@app.route('/post', methods=['POST', 'GET'])
def post():
    if flask.request.method == 'POST':
        try:
            user_login = mycol.find()
            post = flask.request.form['post']
            for i in user_login:
                if i['email'] == email1:
                    if i['password'] == passwd:
                        global post1
                        post1 = i['post']
            post1.append(post)
            mycol.update_one({
                'email': email1,
                'password': passwd
            }, {'$set': {
                'post': post1
            }})
            "<script>alert('Posted Sucesfully')</script>"
            return flask.redirect("Home")
        except:
            return flask.redirect('/')


#store
@app.route('/store')
def store():
    try:
        user_address = mycol.find()
        for i in user_address:
            if i['email'] == email1:
                if i['password'] == passwd:
                    global address
                    address = i['city']
    except:
        return flask.redirect('/')

    return flask.render_template("store.html", data=user_address)


#healthcare
@app.route('/healthcare', methods=['POST', 'GET'])
def healthcare():
    try:
        if flask.request.method == "GET":
            diseases = {
                "vomiting": "cancer,food poisoning,diarrhea",
                "lumps": "skin cancer,tumor",
                "fever": "pavrovirus,ear infection",
                "itchiness": "ear infection,dermatitis,allergy",
                "odor": "Mites,Urinary Tract Infection,Ear Infection"
            }
            sym = ['vomiting', 'lumps', 'fever', 'itchiness', 'odor']
            return flask.render_template("healthcare.html",
                                         sym=list(diseases.keys()))
        elif flask.request.method == "POST":
            diseases = {
                "vomiting": "cancer,food poisoning,diarrhea",
                "lumps": "skin cancer,tumor",
                "fever": "pavrovirus,ear infection",
                "itchiness": "ear infection,dermatitis,allergy",
                "odor": "Mites,Urinary Tract Infection,Ear Infection"
            }
            pettype = flask.request.form.get("pettype")
            symptoms = flask.request.form.get("symptoms")
            sym = ['vomiting', 'lumps', 'fever', 'itchiness', 'odor']
            alert = f"{pettype} has one of these diseases {diseases[symptoms]}"
            return "<script>alert('" + alert + "')</script>"
    except:
        return flask.redirect('/')


#doctors
@app.route('/doctors')
def doctor():
    doctors = mycol.find()
    data = []
    for i in doctors:
        if i['category'] == 'vet':
            data.append(i['username'])
    return flask.render_template('doctors.html', data=data)


#folowing
@app.route('/<profile>/follow', methods=['GET', "POST"])
def follow(profile):
    try:
        if flask.request.method == 'POST':
            user_data = mycol.find()
            for i in user_data:
                if i['email'] == email1:
                    if i["password"] == passwd:
                        global friends
                        friends = i["friends"]
            if profile in friends:
                friends.remove(profile)
            else:
                friends.append(profile)
            mycol.update_one({
                "email": email1,
                "password": passwd
            }, {'$set': {
                "friends": friends
            }})
            return flask.redirect('/' + profile)
    except:
        return flask.redirect('/')


#Profile
@app.route('/<profile>')
def profile1(profile):
    user_profile = mycol.find()
    data = []
    for j in user_profile:
        if j['email'] == email1:
            print('1')
            if profile in j['friends']:
                data.append('following')
                break
            else:
                data.append('follow')
                break
    for i in user_profile:
        if i['username'] == profile:
            if i['email'] == email1:
                return flask.render_template('profile.html', data=i)
            data.insert(0, i)

    return flask.render_template('user_profile.html', data=data)


#Listening to the port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug='True')
