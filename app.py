from tkinter import *
from tkinter import ttk, messagebox, filedialog

import cv2
from PIL import ImageTk, Image, ImageEnhance

import numpy as np
from cv2 import imread, cvtColor, COLOR_BGR2GRAY, imshow, waitKey
from numpy import zeros_like, ravel, sort, multiply, divide, int8

root = Tk()
root.configure(background="orange")


def show(tit, mess):
    messagebox.showinfo(
        message=mess,
        title=tit
    )


imgfile = Image.open("img.png")
imgfiletemp = Image.open("img.png")

slider=""
slider1=""
slider2=""
slider3=""
slider4=""
sliderHeight=""
sliderWidth=""

def openfilename():
    filename = filedialog.askopenfilename(title='Image')
    return filename


def open_img():
    x = openfilename()
    global img1
    global imgfile
    global imgfiletemp

    imgfile = Image.open(x)
    imgfiletemp = Image.open(x)
    # imgfile =ImageTk.PhotoImage(imgfile.resize(size=(400,400)))
    img1 = Image.open(x)
    img1 = ImageTk.PhotoImage(img1.resize(size=(400, 400)))

    global label1
    global frame1
    frame1 = Frame(root, highlightbackground="blue", highlightthickness=5, width=200, height=200)
    frame1.place(rely=0.13, relx=0.05)
    label1 = Label(frame1, image=img1)
    label1.pack()

    global label2
    global frame2
    frame2 = Frame(root, highlightbackground="blue", highlightthickness=5, width=200, height=200)
    frame2.place(rely=0.13, relx=0.95, anchor=NE)
    label2 = Label(frame2, image=img1)
    label2.pack()

    reset()


def gaussian_blur(img):
    return cv2.GaussianBlur(img, (15, 15), 5)


def median_filter(gray_img, mask=3):
    # set image borders
    bd = int(mask / 2)
    # copy image size
    median_img = zeros_like(gray_img)
    for i in range(bd, gray_img.shape[0] - bd):
        for j in range(bd, gray_img.shape[1] - bd):
            # get mask
            kernel = ravel(gray_img[i - bd: i + bd + 1, j - bd: j + bd + 1])
            # calculate mask median
            median = sort(kernel)[int8(divide((multiply(mask, mask)), 2) + 1)]
            median_img[i, j] = median
    return median_img


def bnw(img):
    # img_grey = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)
    thresh = 128
    return cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)[1]


def histogram():
    img = cv2.imread("cv.png", 0)

    # Apply Histogram Equalization
    equ = cv2.equalizeHist(img)
    return equ

def negate():
    imgfile.save("cv.png")
    img_bgr = cv2.imread("cv.png", 1)
    height, width, _ = img_bgr.shape

    for i in range(0, height - 1):
        for j in range(0, width - 1):
            # Get the pixel value
            pixel = img_bgr[i, j]

            # Negate each channel by
            # subtracting it from 255

            # 1st index contains red pixel
            pixel[0] = 255 - pixel[0]

            # 2nd index contains green pixel
            pixel[1] = 255 - pixel[1]

            # 3rd index contains blue pixel
            pixel[2] = 255 - pixel[2]

            # Store new values in the pixel
            img_bgr[i, j] = pixel
    return img_bgr

def showChanges():
    global label1
    global frame1
    global imgfile
    global label2
    global frame2


    slider.set(50)
    slider1.set(50)
    slider2.set(50)
    slider3.set(50)
    slider4.set(50)
    sliderHeight.set(100)
    sliderWidth.set(100)

    frame2 = Frame(root, highlightbackground="blue", highlightthickness=5, width=200, height=200)
    frame2.place(rely=0.13, relx=0.95, anchor=NE)

    imgfile = ImageTk.PhotoImage(imgfile.resize(size=(400, 400)))

    label2 = Label(frame2, image=imgfile)
    label2.pack()


def detect_edges(image, low_threshold=100, high_threshold=200):
    return cv2.Canny(image, low_threshold, high_threshold)

def reset():
    global imgfile
    global imgfiletemp
    global combo1
    global combo2

    combo1.set("")
    combo2.set("")
    imgfile=imgfiletemp


    showChanges()

imgfileadj =""


def adjust(val):
    global imgfile
    global imgfileadj
    global slider
    global slider1
    global slider2
    global slider3
    global slider4
    global sliderHeight
    global sliderWidth

    if(slider1=="" or slider2=="" or slider3=="" or slider4=="" or sliderWidth=="" or sliderHeight==""):
        return


    imgfileadj = imgfile
    if (str(imgfile.__class__).__contains__("PhotoImage")):
        imgfileadj = ImageTk.getimage(imgfileadj)
    img_enhancer = ImageEnhance.Brightness(imgfileadj)
    factor = 2 * float(slider.get()) / 100
    imgfileadj = img_enhancer.enhance(factor)

    # Convert to RGB if image mode is RGBA
    if imgfileadj.mode == 'RGBA':
        image = imgfileadj.convert('RGB')

    # Adjust contrast (increase or decrease)
    contrast_factor = 2*float(slider2.get())/100
    enhancer = ImageEnhance.Contrast(imgfileadj)
    imgfileadj = enhancer.enhance(contrast_factor)

    # Enhance the sharpness of the image
    sharpness_factor = 2*float(slider3.get())/100  # Adjust this value as needed (higher values increase sharpness)
    enhancer = ImageEnhance.Sharpness(imgfileadj)
    imgfileadj = enhancer.enhance(sharpness_factor)




    global label2
    global frame2

    frame2 = Frame(root, highlightbackground="blue", highlightthickness=5, width=200, height=200)
    frame2.place(rely=0.13, relx=0.95, anchor=NE)

    imgfileadj = ImageTk.PhotoImage(imgfileadj.resize(size=(int(float(sliderWidth.get())/100*400), int(float(sliderHeight.get())/100*400))))

    label2 = Label(frame2, image=imgfileadj)
    label2.pack()

def pil2cv(img):
    numpy_image = np.array(img)
    return cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)


def cv2pil(img):
    color_coverted = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return Image.fromarray(color_coverted)

def quitProgram():
    show("End of Presentation","Thank you for listening to our presentation")
    root.destroy()
def save():
    global imgfileadj
    change=0
    temp=imgfileadj

    if (str(imgfileadj.__class__).__contains__("PhotoImage")):
        temp = ImageTk.getimage(temp)
        change=1

    temp = temp.convert('RGB')
    temp.save("output.jpg")
    #if(change==1):
      #  imgfileadj = ImageTk.PhotoImage(imgfileadj.resize(size=(400, 400)))
    show("Save Status", "Processed image has been successfully saved in the project root folder as output.jpg")

def apply():
    if (combo1.get() == "" or combo2.get() == ""):
        show("Selection", "You must select rotation and filter type")
        return


    rot = combo1.get()
    filter = combo2.get()



    global imgfile
    global imgfiletemp

    imgfile = imgfiletemp

    if (filter == "MEDIAN FILTERING"):
        imgfile = median_filter(pil2cv(imgfile))
        imgfile = cv2pil(imgfile)
    elif (filter == "GAUSSIAN BLUR"):
        imgfile = gaussian_blur(pil2cv(imgfile))
        imgfile = cv2pil(imgfile)
    elif (filter == "BLACK AND WHITE"):
        imgfile = imgfile.convert('L')
        imgfile = bnw(pil2cv(imgfile))
        imgfile = cv2pil(imgfile)
    elif (filter == "EDGE DETECTION"):
        imgfile = imgfile.convert('L')
        imgfile = detect_edges(pil2cv(imgfile))
        imgfile = cv2pil(imgfile)
    elif (filter == "HISTOGRAM EQUALISATION"):
        imgfile.save("cv.png")
        imgfile = histogram()
        imgfile = cv2pil(imgfile)
    elif(filter=="NEGATIVE"):
        imgfile = negate()
        imgfile=cv2pil(imgfile)

    if (rot == "FLIP LEFT TO RIGHT"):
        imgfile = imgfile.transpose(method=Image.FLIP_LEFT_RIGHT)
    elif (rot == "FLIP TOP TO BOTTOM"):
        imgfile = imgfile.transpose(method=Image.FLIP_TOP_BOTTOM)
    elif (rot == "ROTATE 90°"):
        imgfile = imgfile.transpose(Image.ROTATE_90)
    elif (rot == "ROTATE 180°"):
        imgfile = imgfile.rotate(180)

    showChanges()


root.title("Signals Project Group 4")

root.geometry('1920x1080')

lbl = Label(root, text="Image Processing (Group 4)", font=('Helvetica bold', 26), bg="orange")

lbl.place(relx=0.5, rely=0.05, anchor=CENTER)

Label(root, text="Original image", font=('Helvetica bold', 20), bg="orange").place(relx=0.2, rely=0.1, anchor=CENTER, )
Label(root, text="Processed image", font=('Helvetica bold', 20), bg="orange").place(relx=0.8, rely=0.1, anchor=CENTER)

frame1 = Frame(root, highlightbackground="blue", highlightthickness=5, width=200, height=200)
frame2 = Frame(root, highlightbackground="blue", highlightthickness=5, width=200, height=200)

frame1.place(rely=0.13, relx=0.05)
frame2.place(rely=0.13, relx=0.95, anchor=NE)

img1 = ImageTk.PhotoImage(Image.open("img.png").resize(size=(400, 400)))
img2 = ImageTk.PhotoImage(Image.open("img.png").resize(size=(400, 400)))

label1 = Label(frame1, image=img1)
label2 = Label(frame2, image=img2)
label1.pack()
label2.pack()

slider = ttk.Scale(root, from_=0, to=100, orient='horizontal', command=adjust)
slider.set(50)
txt = Label(root, text="Brightness: ", font=('Helvetica bold', 15), bg="orange", ).place(relx=0.48, rely=0.2, anchor=E)
slider.place(relx=0.5, rely=0.2, anchor=W)

slider1 = ttk.Scale(root, from_=0, to=100, orient='horizontal', command=adjust)
slider1.set(50)
#txt1 = Label(root, text="Colors: ", font=('Helvetica bold', 15), bg="orange").place(relx=0.48, rely=0.25, anchor=E)
#slider1.place(relx=0.5, rely=0.25, anchor=W)

slider2 = ttk.Scale(root, from_=0, to=100, orient='horizontal', command=adjust)
slider2.set(50)
txt2 = Label(root, text="Contrast: ", font=('Helvetica bold', 15), bg="orange").place(relx=0.48, rely=0.275, anchor=E)
slider2.place(relx=0.5, rely=0.275, anchor=W)

slider3 = ttk.Scale(root, from_=0, to=100, orient='horizontal', command=adjust)
slider3.set(50)
txt3 = Label(root, text="Sharpen: ", font=('Helvetica bold', 15), bg="orange").place(relx=0.48, rely=0.35, anchor=E)
slider3.place(relx=0.5, rely=0.35, anchor=W)

slider4 = ttk.Scale(root, from_=0, to=100, orient='horizontal', command=adjust)
slider4.set(50)
#txt4 = Label(root, text="Blur: ", font=('Helvetica bold', 15), bg="orange").place(relx=0.48, rely=0.4, anchor=E)
#slider4.place(relx=0.5, rely=0.4, anchor=W)


Label(root, text="Rotation", font=('Helvetica bold', 18, "bold"), bg="orange").place(relx=0.5, rely=0.5, anchor=CENTER)
combo1 = ttk.Combobox(state="readonly",
                      values=["NO ROTATION", "FLIP LEFT TO RIGHT", "FLIP TOP TO BOTTOM", "ROTATE 90°", "ROTATE 180°"])
combo1.place(relx=0.5, rely=0.53, anchor=CENTER)

Label(root, text="Filters", font=('Helvetica bold', 18, "bold"), bg="orange").place(relx=0.5, rely=0.58, anchor=CENTER)
combo2 = ttk.Combobox(state="readonly",
                      values=["NO FILTER", "MEDIAN FILTERING", "BLACK AND WHITE", "GAUSSIAN BLUR", "EDGE DETECTION",
                              "HISTOGRAM EQUALISATION","NEGATIVE"])
combo2.place(relx=0.5, rely=0.61, anchor=CENTER)

btnSel = Button(root, text='Select Image', bg="yellow", font=('Helvetica bold', 15), command=open_img)
btnSel.place(relx=0.17, rely=0.68, anchor=CENTER)

btnRes = Button(root, text='Reset', font=('Helvetica bold', 15), bg="blue", command=reset)
btnRes.place(relx=0.12, rely=0.74, anchor=CENTER)

btnExit = Button(root, text='Exit', font=('Helvetica bold', 15), bg="red", command=quitProgram)
btnExit.place(relx=0.2, rely=0.74, anchor=W)

btnSave = Button(root, text='Save', font=('Helvetica bold', 15), bg="green", command=save)
btnSave.place(relx=0.165, rely=0.8, anchor=CENTER)

btnApply = Button(root, text='Process Image', font=('Helvetica bold', 15), bg="green", command=apply)
btnApply.place(relx=0.5, rely=0.8, anchor=CENTER)

sliderWidth = ttk.Scale(root, from_=1, to=100, orient='horizontal',command=adjust)
sliderWidth.set(100)
Label(root, text="Width: ", font=('Helvetica bold', 15), bg="orange").place(relx=0.78, rely=0.68, anchor=E)
sliderWidth.place(relx=0.83, rely=0.68, anchor=CENTER)

sliderHeight = ttk.Scale(root, from_=1, to=100, orient='horizontal',command=adjust)
sliderHeight.set(100)
Label(root, text="Height: ", font=('Helvetica bold', 15), bg="orange").place(relx=0.78, rely=0.73, anchor=E)
sliderHeight.place(relx=0.83, rely=0.73, anchor=CENTER)

root.mainloop()
