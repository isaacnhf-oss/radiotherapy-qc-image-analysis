"""Sección de librerias"""
import PySimpleGUI as sg
import cv2
import PySimpleGUI as sg
import numpy as np
from matplotlib import pyplot as plt
import imutils
import math
from numpy.core.fromnumeric import size
from numpy.lib.histograms import histogram

#Entorno gráfico
sg.theme("DarkTeal2")
layout = [[sg.T("")], [sg.Text("Elige las peliculas a analizar: "), 
        sg.Input(key="-IN-"),
        sg.FileBrowse(button_text='Buscar',key="-IN-",file_types=(("Archivos de imagen", "*.jpg"),))],
        [sg.Button("Cargar")]]
window = sg.Window('Análisis de coincidencia', layout, size=(600,150))
layout2 = [[sg.T("")], [sg.Text("Elige la película a analizar")], [sg.Checkbox('Tira Superior'), sg.Checkbox('Tira inferior')],
        [sg.Text("Elige el número de marcas en la tira")], 
         [sg.InputCombo(('1', '2', '3', '4'))],
         [sg.Text("Elige el método a utilizar")], 
         [sg.Checkbox('Método de intensidad media'), sg.Checkbox('Método de ventana binaria')],
         [sg.Button("Analizar")]]


###Funciones de análisis de las películas
"""Selector de maximos"""
def selMax(histo, indi):
    """Encuentra el primer maximo valor del Histograma
    Luego convierte el valor de la posicion en cero para hallar el
    siguiente maximo"""
    max_value = max(histo)
    maxValIndx,_ = np.where(histo==max_value)
    indau = maxValIndx
    indx2 = indau[0]
    histo[indx2] = 0
    for i in range(0,4):
        histo[indx2 + i] = 0
        histo[indx2 - i] = 0
    if indi is not None:
        for i in range(0,4):
            if indi + i == indx2 or indi - i == indx2:
                histo[maxValIndx] = 0
                max_value = max(histo)
                maxValIndx,_ = np.where(histo==max_value)
                indx2 = maxValIndx
    return int(indx2), histo

"""Selector de puntos medios de las marcas"""
def selMin(perfilRoi, miW,miX):
    va = np.zeros((miW, 1))
    for i in range(0,miW):
        va[i] = perfilRoi[i]
    minVal = min(va)
    minVal,_ = np.where(va==minVal)
    puntoMedio = np.percentile(minVal, 50)
    return math.floor(puntoMedio) + miX

"""Puntos medios"""
def medio(point1, point2, recta):
    promedio = (point1 + point2) / 2
    k = 0
    recta2 = []
    for i in recta:
        recta2.append(abs(i - promedio))
        k = k + 1
    posicion = np.where(recta2==min(recta2))
    
    posicion = np.percentile(posicion, 50)

    return math.ceil(posicion)

"""Puntos medios por ventana binaria"""
def medioBinWin(point1, point2, imgBin):
    heightc,_ = imgBin.shape[:2]
    rang = abs(point1 - point2)
    while rang > 4:
        point1 = point1 + 1
        point2 = point2 - 1
        rang = abs(point2 - point1)
    _,vecBin1 = cv2.threshold(imgBin,point1,255,cv2.THRESH_BINARY)
    _,vecBin2 = cv2.threshold(imgBin,point2,255,cv2.THRESH_BINARY_INV)
    rest = vecBin1 & vecBin2
    recta = np.sum(rest, axis=0)

    j = 0 
    for i in recta:
        recta[j] = math.floor(recta[j] / heightc)
        j = j + 1

    posicion = np.where(recta==max(recta))
    posicion = np.percentile(posicion, 50)
    
    return int(posicion) 

"""Compactado de matriz para determinacion de posicion"""
def make2perfX(sec):
    heightc,_ = sec.shape[:2]
    suma = np.sum(sec, axis=0)
    j = 0 
    for i in suma:
        suma[j] = math.floor(i / heightc)
        j = j + 1
    
    return suma

"""Funcion para detectar los puntos medios de las marcas dadas"""
def roiMarcas(img, imgAu, limTir):
    roi = cv2.selectROI(windowName="roi", img=img, showCrosshair=True, fromCenter=False)
    xr, yr, wr, hr = roi

    if yr < limTir[0] and (yr+hr) > limTir[1]:
        limYsup1 = limTir[0]+3
        limYsup2 = limTir[0]+15
        limYinf1 = limTir[1]-15
        limYinf2 = limTir[1]
    elif yr < limTir[2] and (yr+hr) > limTir[3]:
        limYsup1 = limTir[2]+3
        limYsup2 = limTir[2]+15
        limYinf1 = limTir[3]-15
        limYinf2 = limTir[3]
    roiSecM1 = img[limYsup1:limYsup2, xr:xr+wr]
    roiSecM2 = img[limYinf1:limYinf2, xr:xr+wr]
    _,roiSecM1 = cv2.threshold(roiSecM1,45,255,cv2.THRESH_BINARY )
    _,roiSecM2 = cv2.threshold(roiSecM2,45,255,cv2.THRESH_BINARY )
    perfx1 = make2perfX(roiSecM1)
    perfx2 = make2perfX(roiSecM2)
    marca1 = selMin(perfx1, wr, xr)
    marca2 = selMin(perfx2, wr, xr)
    print(marca1, marca2)
    promMarcas = math.floor((marca1+marca2)/2)
    imgAu = cv2.line(imgAu,(promMarcas,limYsup1-3),(promMarcas, limYinf2),(0,255,0),1)
 

    return imgAu, promMarcas


"""Funcion principal de analisis de cambio de intensidad"""
def cambioIntensidad(peli, imgMod,x,y,h,w, limTir,marTir, medBin):
    roiSel = peli[y:h, x:w]
    #cv2.imshow("Corte", roiSel)
    cutimg = peli[y:h, x:w]

    hist = cv2.calcHist([roiSel], [0], None, [256], [0, 256])
    histAux = cv2.calcHist([roiSel], [0], None, [256], [0, 256])

    #Maximas intensidades
    ind1, histAux = selMax(histAux, indi=None)
    ind2, histAux = selMax(histAux, indi=ind1)
    ind3, histAux = selMax(histAux, indi=ind2)
    ind4, histAux = selMax(histAux, indi=ind3)
    ind5, histAux = selMax(histAux, indi=ind4)

    print(ind1, ind2, ind3, ind4, ind5)

    #perfil en X
    perfX = make2perfX(cutimg)
    rango = range(x,w)

    #Puntos medios
    maximos = [ind1, ind2, ind3, ind4, ind5]
    if marTir == 3:
        maximos[4] = 255
    elif marTir == 3:
        maximos[4] = 255
        maximos[3] = 255
    elif marTir == 1:
        maximos[4] = 255
        maximos[3] = 255
        maximos[2] = 255

    maximos.sort()
    print("maximos =", maximos)
    medios = []

    if medBin is True:
        for i in range(0,marTir):
            medios.append(medioBinWin(maximos[i], maximos[i+1], cutimg, ) +x)
    else:
        for i in range(0,marTir):
            medios.append(medio(maximos[i], maximos[i+1], perfX) +x)

   
    print("medios =", medios)

    "Crea 4 lineas"
    if y > limTir[0] and y < limTir[1]:
        limy1 = limTir[0]
        limy2 = limTir[1]
    elif y > limTir[2] and y < limTir[3]:
        limy1 = limTir[2]
        limy2 = limTir[3]
    for i in range(0,marTir):
        imgMod = cv2.line(imgMod,(medios[i],limy1),(medios[i],limy2),(0,0,255),1)

    return imgMod, medios

"""Funcion para marcar las coincidencias"""
def coincidenciaTiras(img, imagen, puntosref, ymr, numMrk,limTir,tamañoTira):
        for i in range(0,numMrk):
            imagen, mark = roiMarcas(img, imagen, limTir)
            nearpt = np.zeros((numMrk,1))
            for i in range(0,numMrk):
                nearpt[i] = abs(mark - puntosref[i])
            corrpt = min(nearpt)
            corrpt,_ = np.where(nearpt==corrpt)
            corrpt = int(corrpt)
            coincidencia = round((abs(mark - puntosref[corrpt]) * tamañoTira), 2)
            if  ymr > limTir[0] and ymr < limTir[1]:
                postext = (mark+15,math.floor((limTir[0]+limTir[1])/2))
            elif ymr > limTir[2] and ymr < limTir[3]:
                postext = (mark+15,math.floor((limTir[2]+limTir[3])/2))
            cv2.putText(imagen,(str(coincidencia)+" mm"),postext,0,0.4,(255,255,255),1)
            print(puntosref[corrpt],puntosref[i],mark, coincidencia)
        return imagen

###Lectura de imágenes
def mainProgram(direccion, tirNum, marTir,imgAnt, metodo):
    img = cv2.imread(direccion, 0)
    img = imutils.resize(img, width=1400)
    imgRef = cv2.imread(direccion)
    imgRef = imutils.resize(imgRef, width=1400)
    img2 = cv2.Canny(img,0,180)
    _,img2 = cv2.threshold(img2,0,255,cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)
    img2 = imutils.resize(img2, width=1400)

    height, width = img.shape[:2]
    anchoSel = math.floor(width * 0.05)
    anchTira = img2[0:height, math.floor(width/2)-anchoSel:math.floor(width/2)+anchoSel]

    """Calculo de los limites de la tira"""
    a = np.zeros((height, 1))
    tiras = np.transpose(np.sum(anchTira, 1))
    for i in range(0, height):
        a[i] = tiras[i]
    tir1, a = selMax(a, indi=None)
    tir2, a = selMax(a, indi=tir1)
    tir3, a = selMax(a, indi=tir2)
    tir4, a = selMax(a, indi=tir3)

    limTir = [tir1, tir2, tir3, tir4]
    limTir.sort()
    print("limites de la tira =", limTir)

    #imagen recortada
    corte = limTir[0] - math.floor(height * 0.04)
    img = img[corte:height, 0:width]
    imgRef = imgRef[corte:height, 0:width]
    height = height - corte
    for i in range(0, 4):
        limTir[i] = limTir[i] - corte
    #cv2.imshow("el corte", img)


    #tamaño de la tira
    tamañoTira = (abs(limTir[0]-limTir[1]) + abs(limTir[2]-limTir[3])) / 2
    tamañoTira = 32 / tamañoTira

    #Seleccion del áre de la tira
    x1 = 5
    w1 = math.floor(width/2) - math.floor(width*0.02)
    x2 = math.floor(width/2) + math.floor(width*0.02)
    w2 = width - 5
  
    if tirNum == True:       
        y1 = limTir[0]+math.floor(height*0.035)
        h1 = limTir[1]-math.floor(height*0.035)
    elif tirNum == False:
        y1 = limTir[2]+math.floor(height*0.035)
        h1 = limTir[3]-math.floor(height*0.035)

    marTir = int(marTir)

    #correccion para unir imagenes
    if imgAnt is not None:
        imgRef = imgAnt

    sg.popup('Analizando lado izquierdo', 'Seleccione las marcas del lado izquierdo de la tira')
    #Calculo de la intensidad media
    imgRef, cambios1 = cambioIntensidad(img, imgRef, x1, y1, h1, w1,limTir,marTir, metodo)

    #Puntos medios de las marcas
    imgRef = coincidenciaTiras(img, imgRef, cambios1, y1, marTir, limTir,tamañoTira)

    sg.popup('Analizando lado derecho', 'Seleccione las marcas del lado derecho de la tira')
    imgRef, cambios2 = cambioIntensidad(img, imgRef, x2, y1, h1, w2,limTir,marTir, metodo)
    imgRef = coincidenciaTiras(img, imgRef, cambios2, y1, marTir, limTir,tamañoTira)


    cv2.imshow("roi", imgRef)
    cv2.waitKey(0)

    cv2.destroyAllWindows()
    return imgRef

###Ejecución del entorno gráfico
while True:
    event, loc = window.read()
    if event == sg.WIN_CLOSED or event=="Salir":
        break
    elif event == "Cargar":
        print(loc["-IN-"])
        if not loc["-IN-"]:
            event = "Salir"
            sg.popup('Programa finalizado', 'No se leyó ningun archivo')
        break
        

if event == sg.WIN_CLOSED or event=="Salir":
    sg.popup('Programa finalizado', 'Click en Ok para terminar')
elif event == "Cargar":

    window = sg.Window('Análisis de coincidencia', layout2, size=(600,220))  

    while True:
        event, opciones = window.read()
        if event == sg.WIN_CLOSED or event=="Salir":
            break
        elif event == "Analizar":
            print("sup der")
            if opciones[0] == opciones[1]:
                sg.popup('Elija una tira para analizar')
            
            if opciones[3] == opciones[4]:
                sg.popup('Elija un método a utilizar')
                
            else:
                if opciones[0] == True:
                    dato = opciones[0]
                elif opciones[1] == True:
                    dato = False
                
                if opciones[4] == True:
                    datoM = opciones[4]
                elif opciones[3] == True:
                    datoM = False
                
                analisis = mainProgram(loc["-IN-"], dato, opciones[2], imgAnt=None,metodo=datoM)

                resp = sg.popup_yes_no("El análisis ha finalizado","¿Desea realizar el análisis con la otra tira?")

                if resp == 'Yes':
                    if opciones[0] == True:
                        dato = False
                    elif opciones[1] == True:
                      dato = True
                    analisis = mainProgram(loc["-IN-"], dato, opciones[2], analisis, metodo=datoM)
                                    
                resp = sg.popup_yes_no("¿Guardar el resultado?")
                if resp == 'Yes':
                    cv2.imwrite("Análisis de coincidencia.jpg", analisis)
                
                sg.popup('Finalizando...')
                break
                        

