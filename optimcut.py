#
import numpy as np
np.random.seed(11)

import matplotlib.pyplot as plt
import matplotlib as mpl

from tqdm import tqdm

def draw_(order, material_id, material_length):

  fig, ax = plt.subplots()
  ax.set_xlim([0, max( [material_id.max()+2,5] )])

  _,occ = np. unique(material_id, return_counts=True)
  #cmap = cm.get_cmap('viridis', int(material_length.max())+1)
  cmap = mpl.colormaps['viridis']
  norm = mpl.colors.Normalize(vmin=0, vmax=int(material_length.max())+1)

  for uid in np.unique(material_id):
    bottom=0
    order_id = order[material_id==uid]

    for (i,id_) in enumerate(order_id):
      p = ax.bar(uid+1, id_, bottom=bottom, color=cmap(norm(id_)), edgecolor='darkgrey')
      bottom += id_

    p = ax.bar(uid+1, material_length[uid], fill=False, edgecolor='black')

  plt.xlabel("Material ID")
  plt.ylabel("Material length")
  plt.show()


def cuts_to_material(order, material_length):
  material_id      = np.empty(order.size,dtype=np.int32)
  current_length   = 0.0
  current_material = 0

  for it,slice in enumerate(order):
    current_length += slice

    if (current_length > material_length[current_material]):
      current_length = slice
      current_material += 1

    material_id[it] = current_material

  return material_id


def material_leftovers(order, material_id, material_length):
  leftovers = np.zeros( np.max(material_id)+1 )
  for material in np.unique(material_id):
    leftovers[material] = material_length[material] -              \
                          np.sum( order[material_id == material] )
  return leftovers


def swap_order(order):
  n = order.size
  i = np.random.randint(n)
  j = np.random.randint(n)
  while ((i == j) or (order[i] == order[j])):
    j = np.random.randint(n)

  new_order = np.copy(order)
  new_order[i]  = order[j]
  new_order[j]  = order[i]

  return new_order


def cost_function(order,material_id, material_length):
  leftovers = material_leftovers(order, material_id, material_length)
  #n_materials = material_id.max()
  return leftovers.sum() #+ leftovers.mean()*n_materials

def acceptance_probability(order,material_id, new_order,new_material_id, material_length, temp=1.0):
  return np.exp( (cost_function(order,     material_id,     material_length) - \
                  cost_function(new_order, new_material_id, material_length)) / temp )


def step(order, material_id, material_length, temp=1.0, verbose=0):
  #new_order = order.copy()
  ap = 0.0
  while( (ap == 0.0) or (ap < np.random.rand()) ):
    new_order       = swap_order(order)
    new_material_id = cuts_to_material(new_order, material_length)
    ap = acceptance_probability(order,material_id, new_order,new_material_id, material_length, temp=temp)

  if (verbose > 0):
    print(new_order, new_material_id,
          cost_function(new_order, new_material_id, material_length))
  return new_order, new_material_id