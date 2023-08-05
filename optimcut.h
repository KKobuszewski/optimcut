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


template <typename T>
inline void _cuts_to_material(T* state, int* material_id, T* material_length, const int n)
{
    T   current_length = 0.0;
    int current_material = 0;
    
    for (int it; it<n; it++)
    {
        current_length += state[it];
        
        if (current_length > material_length[current_material])
        {
            current_length = state[it];
            current_material += 1;
        }
        
        material_id[it] = current_material;
    }
}


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
T _reconfigure(T* state, int* material_id, T* material_length, T* leftovers, const T old_costf, const int n)
{
    T ap    = 0.0;
    T costf = 0.0;
    do {
        // randomly swap order of two slices
        _swap_order<T>(state, n);
        
        // get material ids
        _cuts_to_material<T>(state, material_id, material_length, n);
        
        // compute cost function & acceptance probability
        costf = _cost_function(state, material_id, material_length, leftovers, n);
        
    } while(ap < random<T>());
    
    return costf; // we need to know current cost function value in the next step
}





void finalize()
{
    if (q != NULL) gsl_qrng_free(q);
    q = NULL;
    //printf("%p \n",q);
}


} /* namespace optimcut */
#endif  /*__OPTIMCUT_H__*/
