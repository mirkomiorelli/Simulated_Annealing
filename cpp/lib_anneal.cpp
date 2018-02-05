// Include pybind headers
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/complex.h>

// headers
#include <vector>
#include <math.h>
#include <random>
#include <iostream>
#include <tuple>

// Function to calculate the cost given two constraints and the mixing parameter
double get_cost(std::vector<std::vector<double>> const &dtable, std::vector<std::vector<double>> const &ptable,
   std::vector<int> const &s, double const &alpha, std::vector<int>::size_type const &N){
   double L = 0.0;
   double P = 0.0;
   #pragma omp parallel for reduction(+: L,P)
   for (std::vector<int>::size_type i = 0; i < N; i++){
      // Calculate length and price components
      if (alpha != 0.0d)
         L += dtable[s[i]][s[i+1]];
      if (alpha != 1.0d)
         P += ptable[s[i]][s[i+1]];
   }
   return alpha * L + (1.0d - alpha) * P;
}

// Annealing schedule to optimize the path between cities at coordinates x and y
void anneal(std::vector<std::vector<double>> const &dtable,
   std::vector<std::vector<double>> const &ptable, double const &alpha,
   std::vector<int>::size_type const &N, std::vector<int> &s, double const &T0, int const &iter_max,
   int const &seed, bool const &verbose, int &acc, int &rej, double &T,
   std::vector<double> &l_arr){

   // Initialize random generators
   std::mt19937 _rng;
   _rng.seed(seed);
   std::uniform_int_distribution<int> _uniform_int(1, N-1); //exclude first and last cities which should also be the same
   std::uniform_real_distribution<double> _uniform_real(0.0d, 1.0d);
   // Preallocate l_arr
   l_arr.reserve(std::ceil((double) iter_max / 10.0d));
   // Temp snew vector
   std::vector<int> snew;
   // Reset counters
   acc = 0; rej = 0;
   // Get initial cost for the random configuration
   double l = get_cost(dtable, ptable, s, alpha, N);
   if (verbose)
      std::cout << "Initial guess length: " << l << '\n';
   l_arr.push_back(l);
   // Set temperature
   T = T0;
   if (verbose)
      std::cout << "Initial temperature: " << T << '\n';
      // Initiate iterative steps
   for (int i = 1; i != iter_max+1; i++){
      // Annealing (reduce temperature, cool down with steps)
      // Here we decrease the temperature every 100 steps
      if (i % 100 == 0)
         T = 0.999 * T;
      // Generate two random indices and switch them (switch cities)
      std::vector<double>::size_type j = _uniform_int(_rng);
      std::vector<double>::size_type k = _uniform_int(_rng);
      snew = s;
      snew[j] = s[k];
      snew[k] = s[j];
      // Calculate cost of new configuration
      double lnew = get_cost(dtable, ptable, snew, alpha, N);
      double deltal = lnew - l;
      // Accept the move if new path is shorter than previous one
      if (deltal <= 0.0d){
          s = snew;
          l = lnew;
          acc += 1;
      } else {
      // If new path is larger than previous, accept the move with probability
      // proportional to the Boltzmann factor
         double u = _uniform_real(_rng);
         if (u < std::exp( - deltal / T)){
            s = snew;
            l = lnew;
            acc += 1;
         } else {
            rej += 1;
         }
      }
      if (i % 10 == 0)
         l_arr.push_back(l);
   }

   return;
}


// Python bindings
namespace py = pybind11;
PYBIND11_MODULE(lib_anneal, m) {
   m.doc() = "LibAnneal";
   // anneal function for Python; inputs are:
   // * dtable: distance look-up table (list of lists)
   // * ptable: price look-up table (list of lists)
   // * alpha: mixing parameter
   // * s: initial configuration (list)
   // * N: number of cities
   // * T0: initial temperature
   // * iter_max: maximum number of iterations
   // * seed: random seed for the random generators
   // * verbose: switch for text output while running
   m.def("anneal", [](std::vector<std::vector<double>> const &dtable,
         std::vector<std::vector<double>> const &ptable, double const &alpha,
          std::vector<int> &s, std::vector<int>::size_type const &N, double const &T0,
         int const &iter_max, int const &seed, bool const &verbose){
            int acc, rej;
            double T;
            std::vector<double> l_arr;
            anneal(dtable,ptable,alpha,N,s,T0,iter_max,seed,verbose,acc,rej,T,l_arr);
            return std::make_tuple(s, l_arr, T, acc, rej);
      });
}
