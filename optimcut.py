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


def cuts_to_material(order,material_id,material_length,cut_length=0.0):
  current_length   = 0.0
  current_material = 0

  for it,slice in enumerate(order):
    current_length += slice + cut_length

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
  while (i == j):
    j = np.random.randint(n)

  new_order = np.copy(order)
  new_order[i]  = order[j]
  new_order[j]  = order[i]

  return new_order


def step(order, material_id, material_length, verbose=0):
  new_order = swap_order(order)

  material_id = cuts_to_material(new_order,material_id,material_length)
  leftovers = material_leftovers(new_order, material_id, material_length)

  if (verbose > 1):
    print(new_order, material_id)
  return new_order

def cost_function(order):
  #leftovers =


def material_leftovers(order, material_id, material_length):
  leftovers = np.zeros( np.max(material_id)+1 )
  for material in np.unique(material_id):
    leftovers[material] = material_length[material] -              \
                          np.sum( order[material_id == material] )
  return leftovers
