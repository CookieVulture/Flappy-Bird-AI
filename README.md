# Flappy Bird AI
 NEAT module -> teach computer how to play flappy bird

**NEAT-**<br>
(NeuroEvolution of Augmenting Topologies) is an evolutionary algorithm that creates artificial neural networks.
<br><p>To evolve a solution to a problem, the user must provide a fitness function which computes a single real number indicating the quality of an individual genome: better ability to solve the problem means a higher score. The algorithm progresses through a user-specified number of generations, with each generation being produced by reproduction (either sexual or asexual) and mutation of the most fit individuals of the previous generation.
</p>
<br> <i>Documentation Link</i> - <a href="https://neat-python.readthedocs.io/en/latest/config_file.html"> Documentation Website </a>
<br><br>
<i>Research Paper</i> - <a href="http://nn.cs.utexas.edu/downloads/papers/stanley.cec02.pdf"> Efficient Evolution of Neural Network Topologies</a>
<br>
<br>

**Important terms for NEAT**
<br>
Inputs -> Bird position Y-axis, Top pipe and Bottom Pipe<br>
Output -> Jump or Not Jump<br>
Activation Function -> TanH (Larger positive number closer to 1 and larger negatie number close to -1) <br> 
Population Size -> 100 (Choose best birds from current Gen and then breed next Gen)  <br>    
Fitness Function -> Most important part. Way to valuate how good bird is by distance travelled by bird <br>
Max generations -> 30    

