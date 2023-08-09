#ifndef __OPTIMCUT_H__
#define __OPTIMCUT_H__

#include <iostream>
#include <cmath>
#include <numeric>
#include <algorithm>
#include <gsl/gsl_qrng.h>
#include <string.h>
#include <float.h>


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
  // generate two different quasirandom numbers from 0.0 to 1.0, inclusive.
  double v[2] = {0.0,0.0};
  //gsl_qrng_get(q, v);
  while (v[0] == v[1]) { gsl_qrng_get (q, v); }
  
  // cast quasirandom numbers to indexes of array
  const int i = static_cast<int>( std::round(v[0]*(n-1.0)) );
  const int j = static_cast<int>( std::round(v[1]*(n-1.0)) );
  
  const T tmp = state[i];
  state[i] = state[j];
  state[j] = tmp;
}


template <typename T>
inline void _cuts_to_material(T* state, int* material_id, T* material_length, const int n)
{
    T   current_length = 0.0;
    int current_material = 0;
    
    for (int it=0; it<n; it++)
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
    //memset(leftovers, 0, static_cast<size_t>(n)*sizeof(*leftovers));
    std::fill(leftovers,leftovers+n,0.0);

    int current_id = 0;
    T sum = 0.0;
    for (int it=0; it<n; it++)
    {
        if (current_id != material_id[it])
        {
            leftovers[current_id] = material_length[current_id] - sum;
            sum         = 0.0;
            current_id += 1;
        }
        sum += state[it];
    }
    
    
}


template <typename T>
inline T _cost_function(T* state, int* material_id, T* material_length, T* leftovers, const int n)
{
    _material_leftovers(state, material_id, material_length, leftovers, n);
    return std::accumulate(leftovers, leftovers+n, 0, std::plus<T>());
}


template <typename T>
T _reconfigure(T* state, int* material_id, T* material_length, T* leftovers, 
               const T old_costf, const T temp, const int n)
{
    T ap    = 0.0;
    T costf = 0.0;
    do {
        // randomly swap order of two slices
        _swap_order<T>(state, n);
        
        // get material ids
        _cuts_to_material<T>(state, material_id, material_length, n);
        
        // compute cost function & acceptance probability
        costf = _cost_function<T>(state, material_id, material_length, leftovers, n);
        ap = std::exp( (old_costf - costf)/temp ); // old_cost > costf  =>  ap > 1
    } while (ap < random<T>());             // accept new config. if ap > random num. from [0,1]
    
    return costf; // we need to know current cost function value in the next step
}

template<typename T>
void make_iterations(T* state, int* material_id, T* material_length, T* leftovers, 
                     const int niter, const T temp, const int n)
{
    // get material ids & compute cost function
    _cuts_to_material<T>(state, material_id, material_length, n);
    T costf      = _cost_function<T>(state, material_id, material_length, leftovers, n);
    
    // mem buffer to store best solution
    T  best_costf = static_cast<T>( FLT_MAX ); // T could be possible float or double, so should be large enough
    T* best_state = new T[n];

    for (int it=0; it < niter; it++)
    {
        // const T old_costf = costf; // needed?
        costf = _reconfigure<T>(state, material_id, material_length, leftovers, costf, temp, n);
        
        // if we have better solution we save it to mem buffer
        if (best_costf > costf)
        {
            for (int jt=0; jt<n; jt++) { best_state[jt] = state[jt]; }
            best_costf = costf;
        }
    }

    // while number of required reconfigurations is done, fill state array with best solution and clear mem
    for (int jt=0; jt<n; jt++) { state[jt] = best_state[jt]; }
    delete[] best_state;
}


/*
 *  T* states - array of length (niter+1)*n to collect states of 
 *  T* costfs - array of length  niter+1 to collect values of cost function
 *
 *
 */
template<typename T>
void make_iterations_with_save(T* states, int* material_id, T* material_length, T* leftovers, T* costfs,
                               const int niter, const T temp, const int n)
{
    // get material ids & compute cost function
    _cuts_to_material<T>(states, material_id, material_length, n);
    costfs[0] = _cost_function(states, material_id, material_length, leftovers, n);
    
    // mem buffer to store costf from previous iteration
    T  costf = static_cast<T>( FLT_MAX ); // T could be possible float or double, so should be large enough

    for (int it=0; it < niter; it++)
    {
        // 
        for (int jt=0; jt<n; jt++) { states[(it+1)*n+jt] = states[it*n+jt]; }

        // const T old_costf = costf; // needed?
        costf = _reconfigure<T>(states+(it+1)*n, material_id, material_length, leftovers, costf, temp, n);
        
        costfs[it+1] = costf;
    }
}




void finalize()
{
    if (q != NULL) gsl_qrng_free(q);
    q = NULL;
    //printf("%p \n",q);
}


} /* namespace optimcut */
#endif  /*__OPTIMCUT_H__*/
