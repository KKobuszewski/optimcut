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
inline void _swap_order(T* old_state, T* new_state, const int n)
{
    // generate two different quasirandom numbers from 0.0 to 1.0, inclusive.
    double v[2] = {0.0,0.0};
    //gsl_qrng_get(q, v);
    //while (v[0] == v[1]) { gsl_qrng_get (q, v); }
    while (v[0] == v[1]) { v[0] = random<T>(); v[1] = random<T>(); }
    
    // cast quasirandom numbers to indexes of array
    const int i = static_cast<int>( std::round(v[0]*(n-1.0)) );
    const int j = static_cast<int>( std::round(v[1]*(n-1.0)) );
    
    // NOTE: allow possibility that new_state and old_state point to the same array
    const T tmp = old_state[i];
    new_state[i] = old_state[j];
    new_state[j] = tmp;
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
    // NOTE: Loop ends before counting last leftover
    // need to find last leftover 
    leftovers[current_id] = material_length[current_id] - sum;
    
}


template <typename T>
inline T _cost_function(T* state, int* material_id, T* material_length, T* leftovers, const int n)
{
    _material_leftovers(state, material_id, material_length, leftovers, n);
    return std::accumulate(leftovers, leftovers+n, 0, std::plus<T>());
}


template <typename T>
T _reconfigure(T* old_state, T* new_state, int* material_id, T* material_length, T* leftovers, 
               const T old_costf, const T temp, const int n)
{
    T ap    = 0.0;
    T costf = 0.0;
    int cnt = 0;
    do {
        // randomly swap order of two slices on new_state
        for (int i=0; i<n; i++) { new_state[i] == old_state[i]; }
        _swap_order<T>(old_state, new_state, n);
        
        // get material ids
        _cuts_to_material<T>(new_state, material_id, material_length, n);
        
        // compute cost function & acceptance probability
        costf = _cost_function<T>(new_state, material_id, material_length, leftovers, n);
        ap = std::exp( (old_costf - costf)/temp ); // old_cost > costf  =>  ap > 1
        cnt += 1;
    } while (ap < random<T>());             // accept new config. if ap > random num. from [0,1]
    
    printf("Reconfiguration %10d %10.5f/%10.5f \n",cnt,costf,old_costf);
    
    return costf; // we need to know current cost function value in the next step
}

template<typename T>
void make_iterations(T* state, int* material_id, T* material_length, T* leftovers, 
                     const int niter, const T temp, const int n)
{
    // get material ids & compute cost function
    _cuts_to_material<T>(state, material_id, material_length, n);
    T costf      = _cost_function<T>(state, material_id, material_length, leftovers, n);
    
    // mem buffers
    T  best_costf = static_cast<T>( FLT_MAX ); // T could be possible float or double, so should be large enough
    T* best_state = new T[n];
    T*  old_state = new T[n];

    for (int it=0; it < niter; it++)
    {
        // store current state in mem buffer
        for (int i=0; i<n; i++) {old_state[i] = state[i];}

        // find new state
        costf = _reconfigure<T>(old_state, state, material_id, material_length, leftovers, costf, temp, n);
        
        // if we have better solution we save it to mem buffer
        if (best_costf > costf)
        {
            for (int jt=0; jt<n; jt++) { best_state[jt] = state[jt]; }
            best_costf = costf;
        }
    }

    // while number of required reconfigurations is done, fill state array with best solution and clear mem
    for (int jt=0; jt<n; jt++) { state[jt] = best_state[jt]; }

    // clean memory
    delete[] best_state;
    delete[]  old_state;
}


/*
 *  T* states - array of length (niter+1)*n to collect consecutive states of algorithm.
 *  T* costfs - array of length  niter+1 to collect values of cost function
 *
 * We assume that first n elements of T* states is initial state.
 */
template<typename T>
void make_iterations_with_save(T* states, int* material_id, T* material_length, T* leftovers, T* costfs,
                               const int niter, const T temp, const int n)
{
    // get material ids & compute cost function
    _cuts_to_material<T>(states, material_id, material_length, n);
    costfs[0] = _cost_function<T>(states, material_id, material_length, leftovers, n);
    
    // mem buffer to store costf from previous iteration
    T  costf = static_cast<T>( FLT_MAX ); // T could be possible float or double, so should be large enough

    for (int it=0; it < niter; it++)
    {
        // 
        for (int jt=0; jt<n; jt++) { states[(it+1)*n+jt] = states[it*n+jt]; }

        // states+it*n     - pointer to the it-th solution
        // states+(it+1)*n - pointer to the next solution
        costf = _reconfigure<T>(states+it*n,states+(it+1)*n, material_id, material_length, leftovers, costf, temp, n);
        
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
