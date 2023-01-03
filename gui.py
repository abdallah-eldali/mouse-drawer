import PySimpleGUI as sg
from PIL import ImageTk, Image
from io import BytesIO
from time import sleep
from mouse import move
from test2 import draw_from

#TODO:
# 1. Find a way to cancel the script while running
# 2. Find a way to execute the code
# 3. Overall, make this work with the mouse script
# 4. Make sure to add an option to import your own images 
#    that will execute black-white.py -> display the newly created png -> call mouse script to start drawing it


byte_io = BytesIO()                     #this is used to save the image in a ByteIO and pass it to the draw_image function
img = Image.open('result_bw.png')
img.save(byte_io, format=img.format)
width, height = img.size

# All the stuff inside your window.
layout = [  [sg.Text('This is where the image will be drawn')],
            [sg.Graph(canvas_size=(width, height), graph_bottom_left=(0, height), graph_top_right=(width, 0), key='graph', background_color='red')],
            #[sg.Image('muT5j.png', key='image')],
            # [sg.Text('', size=(20, 5), background_color='red')],
            [sg.Button('Ok'), sg.Button('Cancel')] ]

# Create the Window
window = sg.Window('Window Title', layout, transparent_color='red', alpha_channel=0.75, keep_on_top=True, finalize=True)
# print(window['graph'].get_size())
img_id = window['graph'].draw_image(data=byte_io.getvalue(), location=(0, 0))

# Flag to know if we should draw or not
start_drawing = False
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    #this is where we call the mouse script
    if event == 'Ok':   
        # window['graph'].update(background_color='red', visible=False)
        # window['graph'].tk_canvas.itemconfig(img, transparentcolor='red')
        # window['graph'].delete_figure(img_id)

        # wx, wy = window.current_location()
        # graph_widget = window['graph'].widget
        # #get the location of the canvas in the screen
        # gx, gy = graph_widget.winfo_rootx(), graph_widget.winfo_rooty()
        # print(gx, gy)


        # sleep(0.5)
        # draw_from(gx+(offset/2), gy+(offset/2))
        # draw_from(gx, gy)
        start_drawing = True
        break



graph_widget = window['graph'].widget
gx, gy = graph_widget.winfo_rootx(), graph_widget.winfo_rooty()

window.close()
if start_drawing:
    draw_from(gx, gy)
