import gate_classes as gates
from circuit_init import Circuit
import tensornetwork as tn
import numpy as np

def _check_input(circuit, *indexes):
  if not isinstance(circuit, Circuit):
    raise ValueError("The first argument have to be the a Circuit type")
  for item in indexes:
    if not isinstance(item, int):
      raise ValueError("Starting from second argument the values have to be "
                       "indexes of circuit qubits")

#
# some realisation ideas prototipe:
#
# def apply_X(circuit, i, contract=False):
#  if contract:
#    qbit = tn.contract_between(qbit, not_gate)
#

def apply_X(circuit, i):
  _check_input(circuit, i);
  X_gate = gates.X_gate()
  circuit._edges[i] ^ X_gate.node[0]
  circuit._edges[i] = X_gate.node[1]

def apply_Y(circuit, i):
  _check_input(circuit, i)
  Y_gate = gates.Y_gate()
  circuit._edges[i] ^ Y_gate.node[0]
  circuit._edges[i] = Y_gate.node[1]

def apply_T(circuit, i):
  _check_input(circuit, i)
  T_gate = gates.T_gate()
  circuit._edges[i] ^ T_gate.node[0]
  circuit._edges[i] = T_gate.node[1]

def apply_CNOT(circuit, a, b):
  _check_input(circuit, a, b)
  cnot_gate = gates.CNOT_gate()
  circuit._edges[a] ^ cnot_gate.node[0]
  circuit._edges[b] ^ cnot_gate.node[1]
  circuit._edges[a] = cnot_gate.node[2]
  circuit._edges[b] = cnot_gate.node[3]

def apply_H(circuit, i):
  _check_input(circuit, i);
  H_gate = gates.H_gate()
  circuit._edges[i] ^ H_gate.node[0]
  circuit._edges[i] = H_gate.node[1]

def calculate(circuit):
  if not isinstance(circuit, Circuit):
    raise ValueError("calculate function accepts only circuit object")
  nodes = tn.reachable(circuit._edges[0])
  result = tn.contractors.optimal(nodes, circuit._edges)

  for i in range(len(result.tensor.shape)):
    circuit._edges[i] = result.get_edge(i)

  return result

def get_probability(result, bitstring):
  demention = len(result.tensor.shape)
  if not demention == len(bitstring):
    raise ValueError("The bitstring have to be equal to number of qbits.")
  crnt = result.tensor
  for i in range(demention):
    crnt = crnt[bitstring[i]]
  return (crnt * crnt)