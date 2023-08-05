# mpyll

mpyll is a package for easy task parallelization across CPU threads.

## Installation

```python
pip install mpyll
```

## Usage

mpyll logic is as follows:

1. Identify the data on which to parallelize computation. The data should be 
   stored in a list.
2. Define the task: a python function that takes as input a list of
   data elements and performs the desired task. This is the parallelized task; 
   instances of this function are to be running in CPU threads.
3. Define an eventual post processing function that takes as input a list of
   data and returns the final result, if any.

### Example

Let's take as an example the estimation of Pi through Monte Carlo:

```python
# First, we define the data on which we would like to parallelize computation.
r = 1.
m = 10 ** 6
X = np.random.uniform(-r, r, size = m)
Y = np.random.uniform(-r, r, size = m)
data = [(X[i], Y[i]) for i in range(m)]

# Second, we define the task to be parallelized.
# It takes as input the data (a list) as well as other arguments, if any, 
# and it returns a result. If it is a procedure, then it does not return.
def count_in_circle_points(data, r, m):
    a = np.array(data) # matrix, each row contains a point coordinates
    d = np.sqrt(np.sum(a ** 2, axis = 1)) # distance to the origin
    in_circle = d <= r # an array, True if distance <= radius, False otherwise
    return np.sum(in_circle) 

# Finally, we define a post processor.
def estimate_pi(data, m):
    pi_estimation = 4 * np.sum(data) / m
    return pi_estimation

pi_estimation = parallelize(task = count_in_circle_points, 
                            data = data, data_shuffle = False, 
                            post_processor = estimate_pi, 
                            n_jobs = -1, 
                            # task arguments
                            count_in_circle_points_r = r, 
                            count_in_circle_points_m = m,
                            # post processor arguments
                            estimate_pi_m = m)
```
### API

```
parallelize(task, 
            data, 
            shuffle_data = False, 
            post_processor = None,
            n_jobs = -1,
            *args,
            **kwargs)

Parallelize a task that returns a value

Parameters
----------
task: function
  The task to be parallelized.
data: list
  The data on which the parallelization is performed.
shuffle\_data: boolean
  shuffle data before processing. Sometimes the data are not identically
  distributed, which could cause some threads to be overloaded compared to 
  others.
post\_processor: function
  A function that runs after all threads terminate.
n\_jobs: int
  The number of threads to be used. Specify -1 to use all CPU threads.

Other Parameters
----------------
Other parameters could be passed to `task` and `post_processor`. The argument
name should start with the name of the task or the post processor, followed 
by an underscore, then followed by the name of the argument.

Returns
-------
If a post processor is specified, then this function returns what is returned
by the post processor, otherwise, it returns a list of the objects returned by
each thread.
```

## License

GNU General Public License v3
