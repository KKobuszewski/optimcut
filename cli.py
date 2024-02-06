import sys
import dearpygui.dearpygui as dpg

import numpy as np


import _optimcut


def callback(sender, app_data, user_data):
    print("Sender: ", sender)
    print("App Data: ", app_data)
    
    with open(app_data['file_path_name']) as f:
        data = np.loadtxt(f, delimiter=';')
        
        element_lengths = np.array(data[:,0], dtype=np.float64)
        element_counts  = np.array(data[:,1], dtype=np.int32)
        
        state = []
        for length, count in zip(element_lengths, element_counts):
            for i in range(count):
                state.append(length)
        state = np.array(state, dtype=np.float64, order='C')
        material_length = np.ones_like(state) * (state.max()+state.min())
        print(material_length)
        
        _optimcut.initialize_qrng()
        copt = _optimcut.CutOptimizer(state,material_length)
        print(copt.state)
        
        niter = 10000
        states, costfs  = copt.make_iterations(py_niter=niter,py_temp=1.0,_state=None,save_states=True)
        material_ids    = _optimcut.material_ids_from_saves(states,material_length)
        
        print()
        print(states.shape, material_ids.shape)
        for length, mat_id in zip(states[-1,:], material_ids[-1,:]):
            print('{:10.2f}\t{:10d}'.format(length, mat_id))
        
        print()



#with dpg.window(label="Tutorial", width=800, height=300):
#    dpg.add_button(label="File Selector", callback=lambda: dpg.show_item("file_dialog_id"))



if __name__ == '__main__':
    print('sys.argv:',sys.argv)
    if len(sys.argv) == 1:
        dpg.create_context()
        
        dpg.create_viewport(title='Optimcut')#, width=800, height=600)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.maximize_viewport()
        
        with dpg.file_dialog(directory_selector=False, show=True, callback=callback, id="file_dialog_id", 
                             width= dpg.get_viewport_client_width(),
                             height=dpg.get_viewport_client_height()):
            dpg.add_file_extension(".csv", color=(0, 25, 255, 255), custom_text="[csv]")
        dpg.show_item("file_dialog_id")
        
        dpg.start_dearpygui()
        dpg.destroy_context()
    else:
        with open(sys.argv[1]) as f:
            data = np.loadtxt(f)
            
            print(data)
        if len(sys.argv) > 2:
            print('Warning: Only first cmd-line argument used.')
        print()
