from tkinter import filedialog
from tkinter import *
from PIL import Image
import wave
import math

hostFileType = "image"
inputFileLength = 0
maxSizeFile = 1024**3
storeBitsFile = 0
ISLoaded = False
FileLoaded = False
toobig = True

def getbits(byteData):
    bitData = [0] * len(byteData) * 4
    for i in range(len(byteData)):
        bitData[4*i] = byteData[i]&3
        bitData[4*i+1] = (byteData[i]&12)>>2
        bitData[4*i+2] = (byteData[i]&48)>>4
        bitData[4*i+3] = (byteData[i]&192)>>6
    return bitData

def getbytes(bitData):
    byteLength = math.ceil(len(bitData)/4)
    byteData = bytearray(byteLength)
    bitConvert = [0] * 4
    for i in range(byteLength):
        bitConvert[0] = bitData[4*i]
        bitConvert[1] = (bitData[4*i + 1])<<2
        bitConvert[2] = (bitData[4*i + 2])<<4
        bitConvert[3] = (bitData[4*i + 3])<<6

        byteData[i] = bitConvert[0] + bitConvert[1] + bitConvert[2] + bitConvert[3]

    byteDataOutput = bytes(byteData)
    return byteDataOutput

def getMaxSizeImage(imgData):
    maxSize = imgData.size[0]*imgData.size[1]*6
    return maxSize

def fileSizeStoreBitsImage(maxSize):
    storeBit = math.log2(maxSize)
    storePixels = math.ceil(storeBit/6)
    storeBits = storePixels*3
    return storeBits

def getMaxSizeSound(soundData):
    maxSize = soundData.getnframes()*2
    return maxSize

def fileSizeStoreBitsSound(maxSize):
    storeBit = math.log2(maxSize)
    storeBits = math.ceil(storeBit/2)
    return storeBits

def checkFileSizes():
    global toobig
    if inputFileLength*2 >= maxSizeFile - storeBitsFile*2:
        toobig = True
        warninglabel.config(text="Input file is too big!")
    else:
        warninglabel.config(text="")
        toobig = False

def loadimage():
    global img
    global pixels
    global maxSizeFile
    global storeBitsFile
    global outputFileSize
    global inputFileType
    global ISLoaded
    global hostFileType
    ISfilename = filedialog.askopenfilename(title = "Select Image File",filetypes = (("png files","*.png"),("bmp files","*.bmp"),("jpg files","*.jpg")))
    img = Image.open(ISfilename)
    pixels = img.load()

    maxSizeFile = getMaxSizeImage(img)
    storeBitsFile = fileSizeStoreBitsImage(maxSizeFile)
    maxStorableBytes = math.ceil((maxSizeFile - storeBitsFile*2)/8)
    if math.floor(maxStorableBytes/1024/1024) == 0:
        tempstring = str(round(maxStorableBytes/1024,1)) + " KB (" + str(maxStorableBytes) + " Bytes)"
        maxsize.config(text = tempstring, fg="black")
    else:
        tempstring = str(round(maxStorableBytes/1024/1024,1)) + " MB (" + str(maxStorableBytes) + " Bytes)"
        maxsize.config(text = tempstring, fg="black")
    imagesoundpath.config(text = ISfilename, fg="black")

    bitFileSize = [0] * storeBitsFile
    for i in range(math.ceil(storeBitsFile/3)):
        bitFileSize[3*i] = (pixels[img.size[0]-1,img.size[1]-1-i][0])&3
        bitFileSize[3*i+1] = (pixels[img.size[0]-1,img.size[1]-1-i][1])&3
        bitFileSize[3*i+2] = (pixels[img.size[0]-1,img.size[1]-1-i][2])&3
    
    outputFileSize = 0
    for i in range(storeBitsFile):
        outputFileSize = outputFileSize + (bitFileSize[i]<<(2*i))

    if math.floor((outputFileSize/4)/1024/1024) == 0:
        tempstring = str(round((outputFileSize/4)/1024,1)) + " KB (" + str(math.ceil(outputFileSize/4)) + " Bytes)"
        outputsize.config(text = tempstring, fg="black")
    else:
        tempstring = str(round((outputFileSize/4)/1024/1024,1)) + " MB (" + str(math.ceil(outputFileSize/4)) + " Bytes)"
        outputsize.config(text = tempstring, fg="black")
    hostFileType = "image"
    checkFileSizes()
    ISLoaded = True

def loadsound():
    global sound
    global soundFrames
    global maxSizeFile
    global storeBitsFile
    global outputFileSize
    global inputFileType
    global numFrames 
    global numChannels 
    global sampWidth
    global sampFreq
    global ISLoaded
    global hostFileType
    ISfilename = filedialog.askopenfilename(title = "Select Sound File",filetypes = [("wav files","*.wav")])
    sound = wave.open(ISfilename,"rb")
    
    soundFrames = [bytearray(4)]*sound.getnframes()
    for i in range(sound.getnframes()):
        soundFrames[i] = bytearray(sound.readframes(1))

    numFrames = sound.getnframes()
    numChannels = sound.getnchannels()
    sampWidth = sound.getsampwidth()
    sampFreq = sound.getframerate()

    maxSizeFile = getMaxSizeSound(sound)
    storeBitsFile = fileSizeStoreBitsSound(maxSizeFile)

    sound.close()

    maxStorableBytes = math.ceil((maxSizeFile - storeBitsFile*2)/8)
    if math.floor(maxStorableBytes/1024/1024) == 0:
        tempstring = str(round(maxStorableBytes/1024,1)) + " KB (" + str(maxStorableBytes) + " Bytes)"
        maxsize.config(text = tempstring, fg="black")
    else:
        tempstring = str(round(maxStorableBytes/1024/1024,1)) + " MB (" + str(maxStorableBytes) + " Bytes)"
        maxsize.config(text = tempstring, fg="black")
    imagesoundpath.config(text = ISfilename, fg="black")

    bitFileSize = [0] * storeBitsFile
    for i in range(storeBitsFile):
        bitFileSize[i] = (soundFrames[numFrames-1-i][0])&3
    
    outputFileSize = 0
    for i in range(storeBitsFile):
        outputFileSize = outputFileSize + (bitFileSize[i]<<(2*i))

    if math.floor((outputFileSize/4)/1024/1024) == 0:
        tempstring = str(round((outputFileSize/4)/1024,1)) + " KB (" + str(math.ceil(outputFileSize/4)) + " Bytes)"
        outputsize.config(text = tempstring, fg="black")
    else:
        tempstring = str(round((outputFileSize/4)/1024/1024,1)) + " MB (" + str(math.ceil(outputFileSize/4)) + " Bytes)"
        outputsize.config(text = tempstring, fg="black")
    hostFileType = "sound"
    checkFileSizes()
    ISLoaded = True

def exitprogram():
    quit()

def loadfile():
    global inputFileBits
    global inputFileLength
    global FileLoaded
    Inputfilename = filedialog.askopenfilename(title = "Select Input File",filetypes = [("all types","*.*")])
    inputFile = open(Inputfilename,"rb")
    inputFileBytes = inputFile.read()
    inputFile.close()
    inputFileBits = getbits(inputFileBytes)
    inputFileLength = len(inputFileBits)

    inputfilepath.config(text = Inputfilename, fg="black")

    if math.floor((inputFileLength/4)/1024/1024) == 0:
        tempstring = str(round((inputFileLength/4)/1024,1)) + " KB (" + str(math.ceil(inputFileLength/4)) + " Bytes)"
        inputfilesize.config(text = tempstring, fg="black")
    else:
        tempstring = str(round((inputFileLength/4)/1024/1024,1)) + " MB (" + str(math.ceil(inputFileLength/4)) + " Bytes)"
        inputfilesize.config(text = tempstring, fg="black")
    checkFileSizes()
    FileLoaded = True


def recoverfile():
    if not ISLoaded:
        print("Image/Sound File is not loaded")
    else:
        OutFileName = filedialog.asksaveasfilename(title = "Save Hidden File",filetypes = [("all files","*.*")])
        outputFileBits = [0] * outputFileSize
        if hostFileType == "sound":
            for i in range(outputFileSize):
                outputFileBits[i] = soundFrames[i][0]&3
        elif hostFileType == "image":
            position = 0
            finish = False
            for i in range(img.size[0]):
                for j in range(img.size[1]):
                    currentBitsInt = [0]*3
            
                    currentBitsInt[0] = pixels[i,j][0]&3
                    currentBitsInt[1] = pixels[i,j][1]&3
                    currentBitsInt[2] = pixels[i,j][2]&3

                    for k in range(3):
                        if position < outputFileSize:
                            outputFileBits[position] = currentBitsInt[k]
                            position += 1
                        else:
                            finish = True
            
                    if finish:
                        break

                if finish:
                    break
        
        outputFile = open(OutFileName,"wb")

        outputFileBytes = getbytes(outputFileBits)

        outputFile.write(outputFileBytes)
        outputFile.close()

def hidefile():
    if not FileLoaded:
        print("Input File is not loaded")
    elif not ISLoaded: 
        print("Image/Sound File is not loaded")
    elif toobig:
        print("Input File is too big")
    else:
        if hostFileType == "sound":
            OutFileName = filedialog.asksaveasfilename(title = "Save Sound File",filetypes = [("wav files","*.wav")])
            bitFileSize = [0] * storeBitsFile

            for i in range(storeBitsFile):
                mask = 3<<(2*i)
                soundFrames[numFrames-1-i][0] = (soundFrames[numFrames-1-i][0]&252) + ((inputFileLength&mask)>>(2*i))


            for i in range(inputFileLength):
                soundFrames[i][0] = (soundFrames[i][0]&252) + inputFileBits[i] 

            soundBytes = [bytes(4)]*len(soundFrames)

            for i in range(len(soundFrames)):
                soundBytes[i] = bytes(soundFrames[i])

            soundOut = wave.open(OutFileName,"wb")

            soundOut.setnframes(numFrames)
            soundOut.setnchannels(numChannels)
            soundOut.setsampwidth(sampWidth)
            soundOut.setframerate(sampFreq)
            soundOut.writeframes(b''.join(soundBytes))

            soundOut.close()
        elif hostFileType == "image":
            position = 0
            finish = False
            OutFileName = filedialog.asksaveasfilename(title = "Save Image File",filetypes = (("png files","*.png"),("bmp files","*.bmp"),("jpg files","*.jpg")))
            bitFileSize = [0] * storeBitsFile

            for i in range(storeBitsFile):
                mask = 3<<(2*i)
                bitFileSize[i] = (inputFileLength&mask)>>(2*i)


            for i in range(math.ceil(storeBitsFile/3)):
                colorReplace = [0] * 3

                colorReplace[0] = (pixels[img.size[0]-1,img.size[1]-1-i][0]&252) + bitFileSize[3*i]
                colorReplace[1] = (pixels[img.size[0]-1,img.size[1]-1-i][1]&252) + bitFileSize[3*i+1]
                colorReplace[2] = (pixels[img.size[0]-1,img.size[1]-1-i][2]&252) + bitFileSize[3*i+2]

                pixels[img.size[0]-1,img.size[1]-1-i] = (colorReplace[0],colorReplace[1],colorReplace[2])

            for i in range(img.size[0]):
                for j in range(img.size[1]):
                    currentBitsInt = [0] * 3
                    for k in range(3):
                        if 3*position + k < inputFileLength:
                            currentBitsInt[k] = inputFileBits[3*position + k]
                        else:
                            finish = True
                            currentBitsInt[k] = 0
        
                    position += 1

                    colorReplace = [0] * 3

                    colorReplace[0] = (pixels[i,j][0]&252) + currentBitsInt[0]
                    colorReplace[1] = (pixels[i,j][1]&252) + currentBitsInt[1]
                    colorReplace[2] = (pixels[i,j][2]&252) + currentBitsInt[2]

                    pixels[i,j] = (colorReplace[0],colorReplace[1],colorReplace[2])

                    if finish:
                        break
            
                if finish:
                    break    

            img.save(OutFileName)    

window = Tk()

window.title("GSteganoPy")
window.geometry('480x320')

menu = Menu(window)

file_menu = Menu(menu, tearoff=0)

file_menu.add_command(label='Load Image File',command=loadimage)
file_menu.add_command(label='Load Sound File',command=loadsound)
file_menu.add_command(label='Load Input File',command=loadfile)
file_menu.add_command(label='Exit',command=exitprogram)

menu.add_cascade(label='File', menu=file_menu)

window.config(menu=menu)

putframe = LabelFrame(window,text="File Hiding Menu:", padx=5, pady=5)
putframe.pack(side = TOP,fill="both",expand="yes",padx=5, pady=5)

getframe = LabelFrame(window,text="File Recovery Menu:", padx=5, pady=5)
getframe.pack(side = BOTTOM,fill="both",expand="yes",padx=5, pady=5)

namelabel = Label(putframe, text="Image/Sound File Path:")
namelabel.grid(column=0,row=0,padx=3, pady=3,sticky="W")

imagesoundpath = Label(putframe, text="NOT LOADED",fg="red")
imagesoundpath.grid(column=1,row=0,padx=3, pady=3)

maxsizelabel = Label(putframe, text="Max Storable File Size:")
maxsizelabel.grid(column=0,row=1,padx=3, pady=3,sticky="W")

maxsize = Label(putframe, text="NOT LOADED",fg="red")
maxsize.grid(column=1,row=1,padx=3, pady=3)

filepathlabel = Label(putframe, text="Input File Name:")
filepathlabel.grid(column=0,row=2,padx=3, pady=3,sticky="W")

inputfilepath = Label(putframe, text="NOT LOADED",fg="red")
inputfilepath.grid(column=1,row=2,padx=3, pady=3)

sizelabel = Label(putframe, text="Input File Size:")
sizelabel.grid(column=0,row=3,padx=3, pady=3,sticky="W")

inputfilesize = Label(putframe, text="NOT LOADED",fg="red")
inputfilesize.grid(column=1,row=3,padx=3, pady=3)

loadfilebutton = Button(putframe, text="Hide Input File", command=hidefile)
loadfilebutton.grid(column=0,row=4,padx=3, pady=3,sticky="W")

warninglabel = Label(putframe, text="",fg="red")
warninglabel.grid(column=1,row=4,padx=3, pady=3)

outputsizelabel = Label(getframe, text="Apparent Output File Size:")
outputsizelabel.grid(column=0,row=0,padx=3, pady=3,sticky="W")

outputsize = Label(getframe, text="NOT LOADED",fg="red")
outputsize.grid(column=1,row=0,padx=3, pady=3)

outputfilebutton = Button(getframe, text="Recover File", command=recoverfile)
outputfilebutton.grid(column=0,row=1,padx=3, pady=3,sticky="W")


window.mainloop()
