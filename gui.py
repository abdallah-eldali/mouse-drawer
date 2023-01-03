import PySimpleGUI as sg
from PIL import ImageTk, Image
from io import BytesIO
from time import sleep
from mouse import move

byte_io = BytesIO()                     #this is used to save the image in a ByteIO and pass it to the draw_image function
img = Image.open('muT5j.png')
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

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    #this is where we call the mouse script
    if event == 'Ok':   
        # window['graph'].update(background_color='red', visible=False)
        # window['graph'].tk_canvas.itemconfig(img, transparentcolor='red')
        window['graph'].delete_figure(img_id)
        # sleep(1)
        wx, wy = window.current_location()
        graph_widget = window['graph'].widget
        gx, gy = graph_widget.winfo_rootx(), graph_widget.winfo_rooty()
        print(gx, gy)


        move(gx, gy)
        #get the location of the canvas in the screen

        

window.close()