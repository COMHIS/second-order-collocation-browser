import os, math

def get_HTML(imagepath, year, pos, texts, index, scale, sizes):

    HTML = '<html><meta charset="UTF-8"><head><link rel="stylesheet" type="text/css" href="../text_viewer.css"></head>\n<body><div id="image-window" style="background-image:'+"url('"+imagepath+".png');"+'">\n'
    for p in range(len(pos)):
        x,y,s = scaling(pos[p], scale[1], sizes[p])
        HTML += '<div id="'+index[p]+'" class="dot" style="left:'+str(x)+'px; bottom:'+str(y)+'px;"><div class="dot-hiding"><img src="../dot.png", width="'+str(s)+'" height="'+str(s)+'"></div></div>'
    HTML += '</div><div id="text-box"><p id="text-box"</p></div>'
    HTML += '<div id="link-box">'
    if str(year-1)+".html" in os.listdir("html/"):
        HTML += '<a href="'+str(year-1)+'.html"> < Taakse päin vuoteen '+str(year-1)+'</a>'
    HTML += '<a href="'+str(year+1)+'.html"> Eteen päin vuoteen '+str(year+1)+' ></a>'
    HTML += "</div>"
    HTML += '</body>\n<script src="../jquery-3.1.0.min.js"></script>\n<script>'

    HTML += "var texts = "+str(texts)+";\n"
    
    
    HTML += 'var text_div = document.getElementById("text-box");\n'
    
    HTML += "$(document).ready(function() { $('.dot').hover(function() { \n$(text_div).text($(this).attr('id'));\n});\n});\n</script>\n</html>"

    return HTML
        
def scaling(pos, scale, size):
    RATIO = 1000/1920
    OFF_X = 231*RATIO
    OFF_Y = (144+1920-1440)*RATIO-200
    size = math.sqrt(size)*(1/RATIO)
    return (pos[0]+scale)/(2*scale)*1490*RATIO+OFF_X-size/4, (pos[1]+scale)/(2*scale)*1152*RATIO+OFF_Y-size/2, size
