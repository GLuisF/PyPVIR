import PySimpleGUI as sg
from engineering_notation import EngNumber
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

precisão = 5
up = {'mW':1e-3,'W':1,'kW':1e3}
uv = {'mV':1e-3,'V':1,'kV':1e3}
ui = {'nA':1e-9,'μA':1e-6,'mA':1e-3,'A':1}
ur = {'mΩ':1e-3,'Ω':1,'kΩ':1e3,'MΩ':1e6}

def formatar(n):
    n = str(EngNumber(n,significant=precisão))
    if n[-1] in 'pnumkMGT':
        return n[:-1],n[-1]
    else:
        return n,''

sg.theme('Reddit')
sg.SetGlobalIcon(resource_path('PVIR.ico'))

layout = [[sg.Text('Precisão:',(12,1),justification='right'),sg.Spin([i for i in range(1,8)],precisão,(1,2),key='-N-',change_submits=True)],
          [sg.Text('Potência (P):',(12,1),justification='right'),sg.Input(s=(8,1),k='-P-',change_submits=True),sg.Combo(list(up.keys()),'W',(4,1),readonly=True,k='-UP-',change_submits=True,),sg.Button('Limpar',k='-LP-')],
          [sg.Text('Tensão (V)',(12,1),justification='right'),sg.Input(s=(8,1),k='-V-',change_submits=True),sg.Combo(list(uv.keys()),'V',(4,1),readonly=True,k='-UV-',change_submits=True),sg.Button('Limpar',k='-LV-')],
          [sg.Text('Corrente (I)',(12,1),justification='right'),sg.Input(s=(8,1),k='-I-',change_submits=True),sg.Combo(list(ui.keys()),'A',(4,1),readonly=True,k='-UI-',change_submits=True),sg.Button('Limpar',k='-LI-')],
          [sg.Text('Resistência (R)',(12,1),justification='right'),sg.Input(s=(8,1),k='-R-',change_submits=True),sg.Combo(list(ur.keys()) ,'Ω',(4,1),readonly=True,k='-UR-',change_submits=True),sg.Button('Limpar',k='-LR-')],
          [sg.T('',(4,1)),sg.Button('Calcular',k='-CALCULAR-'),sg.Button('Limpar tudo',k='-LIMPAR-')],
          [sg.Image(k='-IMG-',expand_x=True)]]

window = sg.Window('Calculadora PVIR', layout, return_keyboard_events=True,use_default_focus=False)   

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == '-LIMPAR-':
        window['-P-'].update('')
        window['-V-'].update('')
        window['-I-'].update('')
        window['-R-'].update('')
        window['-IMG-'].update('')
    if event == '-LP-':
        window['-P-'].update('')
    if event == '-LV-':
        window['-V-'].update('')
    if event == '-LI-':
        window['-I-'].update('')
    if event == '-LR-':
        window['-R-'].update('')
    
    if event ==  '-N-':
        precisão = int(values['-N-'])
    
    if event in ['-P-','-V-','-I-','-R-'] and values[event]:
        if values[event][-1] not in '0123456789.' or '.' in values[event][:-1] and values[event][-1] == '.' or len(values[event]) > 8:
            window[event].update(values[event][:-1])
        #print(event,values[event])

    if event == '-CALCULAR-':
        if values['-P-'] != '' and values['-V-'] != '':
            p = float(values['-P-'])*up[values['-UP-']]
            v = float(values['-V-'])*uv[values['-UV-']]
            i,pi = formatar(p/v)
            r,pr = formatar(v**2/p)
            window['-I-'].update(i)
            window['-R-'].update(r)
            window['-UI-'].update(pi+'A')
            window['-UR-'].update(pr+'Ω')
            window['-IMG-'].update(filename=resource_path('pv.png'))
        elif values['-P-'] != '' and values['-I-'] != '':
            p = float(values['-P-'])*up[values['-UP-']]
            i = float(values['-I-'])*ui[values['-UI-']]
            v,pv = formatar(p/i)
            r,pr = formatar(p/i**2)
            window['-V-'].update(v)
            window['-R-'].update(r)
            window['-UV-'].update(pv+'V')
            window['-UR-'].update(pr+'Ω')
            window['-IMG-'].update(filename=resource_path('pi.png'))
        elif values['-P-'] != '' and values['-R-'] != '':
            p = float(values['-P-'])*up[values['-UP-']]
            r = float(values['-R-'])*ur[values['-UR-']]
            v,pv = formatar((p*r)**0.5)
            i,pi = formatar((p/r)**0.5)
            window['-V-'].update(v)
            window['-I-'].update(i)
            window['-UV-'].update(pv+'V')
            window['-UI-'].update(pi+'A')
            window['-IMG-'].update(filename=resource_path('pr.png'))
        elif values['-V-'] != '' and values['-I-'] != '':
            v = float(values['-V-'])*uv[values['-UV-']]
            i = float(values['-I-'])*ui[values['-UI-']]
            p,pp = formatar(v*i)
            r,pr = formatar(v/i)
            window['-P-'].update(p)
            window['-R-'].update(r)
            window['-UP-'].update(pp+'W')
            window['-UR-'].update(pr+'Ω')
            window['-IMG-'].update(filename=resource_path('vi.png'))
        elif values['-V-'] != '' and values['-R-'] != '':
            v = float(values['-V-'])*uv[values['-UV-']]
            r = float(values['-R-'])*ur[values['-UR-']]
            p,pp = formatar(v**2/r)
            i,pi = formatar(v/r)
            window['-P-'].update(p)
            window['-I-'].update(i)
            window['-UP-'].update(pp+'W')
            window['-UI-'].update(pi+'A')
            window['-IMG-'].update(filename=resource_path('vr.png'))
        elif values['-I-'] != '' and values['-R-'] != '':
            i = float(values['-I-'])*ui[values['-UI-']]
            r = float(values['-R-'])*ur[values['-UR-']]
            p,pp = formatar(i**2*r)
            v,pv = formatar(i*r)
            window['-P-'].update(p)
            window['-V-'].update(v)
            window['-UP-'].update(pp+'W')
            window['-UV-'].update(pv+'V')
            window['-IMG-'].update(filename=resource_path('ir.png'))