from flask import Flask, Response, render_template, request, send_from_directory
from camera import generate_frames


user = "not logged in"
user_index = -1
guser_score = int
rs = 50
app = Flask(__name__, template_folder=".")

@app.route("/design.css")
def design_css():
    return send_from_directory(app.root_path, "design.css")

@app.route('/')
@app.route('/home')
def home():
    return render_template('homepage.html', user=user)

@app.route('/result', methods=['POST', 'GET'])
def result():
    global user, guser_score, user_index
    signed = request.form.get("name")
    password = request.form.get("password")
    logs = list(open("logins.env", "r").read().splitlines())
    try:
        logs[0]
    except:
        logs = ["Mitt", "1234", "0"]
    users = logs[0].split(",")
    passwords = logs[1].split(",")
    score = logs[2].split(",")
    if signed in users:
        if password == passwords[users.index(signed)]:
            user = signed
    else:
        signup = open("logins.env", "w")
        logs[0] = logs[0] + "," + signed
        logs[1] = logs[1] + "," + password
        logs[2] = logs[2] + "," + "0"
        signup.write("\n".join(logs) + "\n")
        signup.close()
        user = signed
    try:
        user_score = score[users.index(user)]
    except:
        user_score = "0"

    debugscore = ""
    for i in user_score:
        if i.isnumeric():
            debugscore += i
    guser_score = int(debugscore)
    user_index = users.index(user)
    print(user_index)
    return render_template('homepage.html', user=user, score=str(guser_score))

@app.route('/return_home', methods=['POST', 'GET'])
def return_home():
    global guser_score
    log2 = open("logins.env", "r").read().splitlines()
    guser_score = int(log2[2].split(",")[user_index])
    return render_template('homepage.html', user=user, score=str(guser_score))

@app.route('/demo', methods=['GET', 'POST'])
def demo():
    global guser_score
    return render_template('demo.html', user=user, score=str(guser_score))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    global user
    user = "not logged in"
    return render_template('homepage.html', user=user)

@app.route('/video_feed')
def video_feed():
    return Response(
        generate_frames(user_index=user_index),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/rewards', methods=['GET', 'POST'])
def rewards():
    global guser_score
    lrs = rs * 10
    progress = guser_score % rs
    lp = guser_score % lrs
    po = (100 * progress)/rs
    pl = (100 * lp)/lrs
    return render_template(
        'rewards.html',
        user=user,
        score=str(guser_score),
        progress=progress,
        lp=lp,
        reward_threshold=rs,
        large_reward_threshold=lrs,
        po=po,
        pl=pl
    )

if __name__ == '__main__':
    app.run(debug=True, port=5001)