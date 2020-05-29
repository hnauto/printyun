import subprocess


def pdf(User_tel, User_Macs):
    html = """
    <html>
    <head>
    </head>
    <body>
    <h1 style="text-align=center">
        &nbsp&nbsp&nbsp&nbsp&nbspTel_phone: {}
            <br>
        &nbsp&nbsp&nbsp&nbsp&nbspID: {}
    </h1>
    </body>
    </html>
    """.format(User_tel,User_Macs)
    with open('./static/html/1.html','w') as f:
        f.write(html)
    subprocess.call('libreoffice --headless --norestore --writer --convert-to pdf ./static/html/1.html --outdir ./static/html/',shell=True)
    return