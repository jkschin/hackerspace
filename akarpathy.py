import random

'''
The code and text in this tutorial is based on karpathy.github.io/neuralnets. I
type my own explanation in it to deepen my own understanding. I might omit
certain things that seem obvious to me.
'''

'''
Assume we have a simple gate that takes in 2 inputs, x and y, and the output is
the multiplication of these 2 inputs:
    x = -2
    y = 3
    output = -6
Great! This is the most simple form of a neural network. How do we tweak it to
get a larger number than -6? Note that -5.95 is larger.
'''
def forward_multiply_gate(x, y):
    return x * y

'''
Strategy 1: Random Local Search
This randomly tweaks x and y and finds the best output.
'''
def random_local_search():
    tweak_amount = 0.01
    best_output = -10000000000
    x, y = -2, 3
    best_x, best_y = x, y
    for i in xrange(100000):
        try_x = x + tweak_amount * (random.random() - 0.5)
        try_y = y + tweak_amount * (random.random() - 0.5)
        output = forward_multiply_gate(try_x, try_y)
        if output > best_output:
            best_output = output
            best_x = try_x
            best_y = try_y
    print 'Best X: %f, Best Y: %f Best Output: %f' %(best_x, best_y, best_output)

'''
Strategy 2: Numerical Gradient
This uses actual gradients to find the direction to ascend.
h is the epsilon that you increase x and y by. In this context, the derivative
does not change when h varies. Evaluation of the analytical gradient will tell
you why. Note that the step size is really arbitrary here, and in larger neural
networks small step sizes are generally better.
'''
def numerical_gradient():
    print 'Strategy 2: Numerical Gradient'
    h = 0.000001
    step_size = 0.01
    x, y = -2, 3
    out = forward_multiply_gate(x, y)
    out_x = forward_multiply_gate(x+h, y)
    out_y = forward_multiply_gate(x, y+h)
    print 'Out X: %f, Out Y: %f' %(out_x, out_y)
    derivative_x = (out_x - out) / h
    derivative_y = (out_y - out) / h
    print 'Derivative X: %f, Derivative Y: %f' %(derivative_x, derivative_y)
    new_x = x + derivative_x * step_size
    new_y = y + derivative_y * step_size
    new_out = forward_multiply_gate(new_x, new_y)
    print 'Best X: %f, Best Y: %f Best Output: %f' %(new_x, new_y, new_out)
numerical_gradient()

'''
Strategy 3: Analytical Gradient
Numerical Gradient is not the best because we need to compute the circuit's
output as we tweak every input value independently by a small amount. The
complexity of evaluating the gradient is linear in number of inputs. 1 million
inputs means 1 million forward propagations! The better solution is the analytic
gradient.

For our simple function above:
    f(x, y) = x * y
    gradient of f w.r.t x = y
    gradient of f w.r.t y = x
    Hence, if you recall the above numerical_gradient() example, derivative_x is
    3.0 and derivative_y is -2.0.

If we extend this and think about the following equation:
    f(x, y) = x * x * y
    gradient of f w.r.t x = 2xy
    gradient of f w.r.t y = x**2

We get identical results as above!
'''
def analytical_gradient():
    print 'Strategy 3: Analytical Gradient'
    x, y = -2, 3
    step_size = 0.01
    out = forward_multiply_gate(x, y)
    gradient_x = y
    gradient_y = x
    new_x = x + step_size * gradient_x
    new_y = y + step_size * gradient_y
    new_out = forward_multiply_gate(new_x, new_y)
    print 'Best X: %f, Best Y: %f Best Output: %f' %(new_x, new_y, new_out)
analytical_gradient()

'''
We now add another add gate and combined the above multiply gate into a circuit.
'''
def forward_add_gate(x, y):
    return x + y

def forward_circuit(x, y, z):
    q = forward_add_gate(x, y)
    f = forward_multiply_gate(q, z)
    return f

def circuit_analytical_gradient():
    print 'Circuit Analytical Gradient'
    step_size = 0.01
    x, y, z = -2, 5, -4
    q = forward_add_gate(x, y)
    derivative_f_wrt_q = z
    derivative_f_wrt_z = q
    derivative_q_wrt_x = 1
    derivative_q_wrt_y = 1
    derivative_f_wrt_x = derivative_f_wrt_q * derivative_q_wrt_x
    derivative_f_wrt_y = derivative_f_wrt_q * derivative_q_wrt_y
    out = forward_circuit(x, y, z)
    new_x = x + step_size * derivative_f_wrt_x
    new_y = y + step_size * derivative_f_wrt_y
    new_z = z + step_size * derivative_f_wrt_z
    new_out = forward_circuit(new_x, new_y, new_z)
    print 'Best X: %f, Best Y: %f, Best Z: %f, Best Output: %f' \
                %(new_x, new_y, new_z, new_out)
circuit_analytical_gradient()











