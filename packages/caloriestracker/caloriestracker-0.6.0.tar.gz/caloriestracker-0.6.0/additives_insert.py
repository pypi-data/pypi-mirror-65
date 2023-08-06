
def string2risk(s):
    if s=="Alta":
        return 3
    elif s=="Media":
        return 2
    elif s=="Baja":
        return 1
    else:
        return "NULL"



f=open("riesgos.html","r")
html=f.read()
f.close()

for i, row in enumerate(html.split("</tr>")):
    name=row.split(".html'>")[1].split("</a>")[0]
    description=row.split(".html'>")[2].split("</a>")[0]
    risk=row.split("'>")[3].split("</td>")[0]
    coderisk=string2risk(risk)

    print ("INSERT INTO (ID, NAME, DESCRIPTION, RISK) VALUES ({},'{}','{}',{});".format(i+1,name,description,coderisk))