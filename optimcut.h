#ifndef __OPTIMCUT_H__
#define __OPTIMCUT_H__

#include <iostream>
#include <cmath>
#include <numeric>
#include <gsl/gsl_qrng.h>
#include <string.h>


/* ***************************************************************************************************************** * 
 *                                                                                                                   * 
 * sources: https://www.gnu.org/software/gsl/doc/html/qrng.html                                                      * 
 *          https://www.gnu.org/software/gsl/doc/html/rng.html                                                       *
 *                                                                                                                   *
 * ***************************************************************************************************************** */

namespace optimcut
{

gsl_qrng* q; /* automatically initialized with NULL */

void initialize(int seed = -1)
{
    // initialize pseudorandom number generator
    if   (seed == -1) { srand(time(0)); } 
    else              { srand(seed); }
    
    // initialize quasirandom number generator
    const int qrng_dim = 2;
    if (q == NULL) q = gsl_qrng_alloc(gsl_qrng_sobol, qrng_dim);
}


/*
 * This function generates a random number from 0.0 to 1.0, inclusive.
 */
template <typename T>
inline T random()
{
    return static_cast<T>(rand()) / static_cast<T>(RAND_MAX);
}


template <typename T>
inline void _swap_order(T* state, const int n)
{
  // draw two different quasirandom numbers
  double v[2];
  gsl_qrng_get(q, v);
  while (v[0] == v[1]) { gsl_qrng_get (q, v); }
  
  // cast quasirandom numbers to indexes of array
  const int i = static_cast<int>( std::round(v[0]*n) );
  const int j = static_cast<int>( std::round(v[1]*n) );
  
  const T tmp = state[i];
  state[i] = state[j];
  state[j] = tmp;
}


/* TODO: Code functions below in C/C++
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
*/


template <typename T>
inline void _material_leftovers(T* state, int* material_id, T* material_length, T* leftovers, const int n)
{
    // set leftovers array to zeros
    // (see: https://stackoverflow.com/questions/9146395/reset-c-int-array-to-zero-the-fastest-way)
    memset(leftovers, 0, n*sizeof(*leftovers));
    
    int current_id = 0;
    T sum = 0.0;
    for (int i=0; i<n; i++)
    {
        if (current_id != material_id[i])
        {
            leftovers[current_id] = material_length[current_id] - sum;
            sum = 0.0;
            current_id += 1;
        }
        sum += state[i];
    }
    
    
}


template <typename T>
inline T _cost_function(T* state, int* material_id, T* material_length, T* leftovers, const int n)
{
    _material_leftovers(state, material_id, material_length, leftovers, n);
    return std::accumulate(leftovers, leftovers+n, 0, std::plus<T>());
}


template <typename T>
T _reconfigure(T* state, int* material_id, T* material_length, T* leftovers, T old_costf, const int n)
{
    T ap    = 0.0;
    T costf = 0.0;
    do {
        _swap_order<T>(state, n);
        // get material ids
        // compute cost function & acceptance probability
        costf = _cost_function(state, material_id, material_length, leftovers, n);
    } while(ap < random<T>());
    
    return costf; // we need to know current cost function in next step
}

/* TODO: Code functions below in C/C++

def acceptance_probability(order,material_id, new_order,new_material_id, material_length, temp=1.0):
  return np.exp( (cost_function(order,     material_id,     material_length) - \
                  cost_function(new_order, new_material_id, material_length)) / temp )

template <typename T>
inline T acceptance_probability(T* state, int* material_id, T* material_length, T* leftovers, const int n)
{
    T prob = std::exp()
}



def step(order, material_id, material_length, temp=1.0, verbose=0):
  ap = 0.0
  while( (ap == 0.0) or (ap < np.random.rand()) ):
    new_order       = swap_order(order)
    new_material_id = cuts_to_material(new_order, material_length)
    ap = acceptance_probability(order,material_id, new_order,new_material_id, material_length, temp=temp)

  if (verbose > 0):
    print(new_order, new_material_id,
          cost_function(new_order, new_material_id, material_length))
  return new_order, new_material_id
*/



void finalize()
{
    if (q != NULL) gsl_qrng_free(q);
    q = NULL;
    //printf("%p \n",q);
}


} /* namespace optimcut */
#endif /*__OPTIMCUT_H__*/
