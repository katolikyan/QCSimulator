import qcsimulator as qcs
import numpy as np
import tensornetwork as tn
import pytest
import networkx as nx
from qiskit import QuantumRegister, QuantumCircuit, execute, Aer

def test_circuit_init():
  circuit = qcs.circuit_init(1)
  with(pytest.raises(ValueError)):
    circuit_to_much = qcs.circuit_init(21)
  with(pytest.raises(ValueError)):
    circuit_negative = qcs.circuit_init(-1)
  with(pytest.raises(ValueError)):
    circuit_zero = qcs.circuit_init(0)
  assert len(circuit._qbits) == 1

def test_circuit1_qiskit_comparison():
  circuit = qcs.circuit_init(2)
  circuit.h(0)
  circuit.cx(0, 1)
  result = circuit.execute()
  sv = result.get_state_vector()

  S_simulator = Aer.backends(name='statevector_simulator')[0]
  q = QuantumRegister(2)
  qubit = QuantumCircuit(q)
  qubit.h(q[0])
  qubit.cx(q[0], q[1])
  job = execute(qubit, S_simulator)
  result_qkit = job.result()
  sv_qkit = result_qkit.get_statevector()

  assert np.testing.assert_allclose(sv, sv_qkit, atol=1e-8, rtol=1e-8) == None

def test_circuit2_qiskit_comparison():
  circuit = qcs.circuit_init(2)
  circuit.x(1)
  circuit.cx(0, 1)
  circuit.cx(1, 0)
  circuit.cx(0, 1)
  result = circuit.execute()
  sv = result.get_state_vector()

  S_simulator = Aer.backends(name='statevector_simulator')[0]
  q = QuantumRegister(2)
  qubit = QuantumCircuit(q)
  qubit.x(q[1])
  qubit.cx(q[0], q[1])
  qubit.cx(q[1], q[0])
  qubit.cx(q[0], q[1])
  job = execute(qubit, S_simulator)
  result_qkit = job.result()
  sv_qkit = result_qkit.get_statevector()

  assert np.testing.assert_allclose(sv, sv_qkit, atol=1e-8, rtol=1e-8) == None

def test_circuit3_qiskit_comparison():
  circuit = qcs.circuit_init(3)
  circuit.y(0)
  circuit.h(1)
  circuit.x(2)
  circuit.cx(0, 1)
  circuit.h(0)
  circuit.cz(1, 2)
  circuit.cy(0, 2)
  circuit.cy(0, 2)
  circuit.cz(1, 2)
  circuit.h(0)
  circuit.cx(0, 1)
  circuit.x(2)
  circuit.h(1)
  circuit.y(0)
  result = circuit.execute()
  sv = result.get_state_vector()

  S_simulator = Aer.backends(name='statevector_simulator')[0]
  q = QuantumRegister(3)
  qubit = QuantumCircuit(q)
  qubit.y(q[0])
  qubit.h(q[1])
  qubit.x(q[2])
  qubit.cx(q[0], q[1])
  qubit.h(q[0])
  qubit.cz(q[1], q[2])
  qubit.cy(q[0], q[2])
  qubit.cy(q[0], q[2])
  qubit.cz(q[1], q[2])
  qubit.h(q[0])
  qubit.cx(q[0], q[1])
  qubit.x(q[2])
  qubit.h(q[1])
  qubit.y(q[0])
  job = execute(qubit, S_simulator)
  result_qkit = job.result()
  sv_qkit = result_qkit.get_statevector()

  assert np.testing.assert_allclose(sv, sv_qkit, atol=1e-8, rtol=1e-8) == None

def test_circuit4_qiskit_comparison():
  circuit = qcs.circuit_init(4)
  circuit.h(2)
  result = circuit.execute()
  sv = result.get_state_vector()

  S_simulator = Aer.backends(name='statevector_simulator')[0]
  q = QuantumRegister(4)
  qubit = QuantumCircuit(q)
  qubit.h(q[2])
  job = execute(qubit, S_simulator)
  result_qkit = job.result()
  sv_qkit = result_qkit.get_statevector()

  assert np.testing.assert_allclose(sv, sv_qkit, atol=1e-8, rtol=1e-8) == None

def test_empty_circuit_qiskit_comparison():
  circuit = qcs.circuit_init(10)
  result = circuit.execute()
  sv = result.get_state_vector()

  S_simulator = Aer.backends(name='statevector_simulator')[0]
  q = QuantumRegister(10)
  qubit = QuantumCircuit(q)
  job = execute(qubit, S_simulator)
  result_qkit = job.result()
  sv_qkit = result_qkit.get_statevector()

  assert np.testing.assert_allclose(sv, sv_qkit, atol=1e-8, rtol=1e-8) == None

def test_ones_circuit_qiskit_comparison():
  circuit = qcs.circuit_init(10)
  for i in range(10):
    circuit.x(i)
  result = circuit.execute()
  sv = result.get_state_vector()

  S_simulator = Aer.backends(name='statevector_simulator')[0]
  q = QuantumRegister(10)
  qubit = QuantumCircuit(q)
  for i in range(10):
    qubit.x(q[i])
  job = execute(qubit, S_simulator)
  result_qkit = job.result()
  sv_qkit = result_qkit.get_statevector()

  assert np.testing.assert_allclose(sv, sv_qkit, atol=1e-8, rtol=1e-8) == None

def test_h_ch_circuit_qiskit_comparison():
  circuit = qcs.circuit_init(2)
  circuit.h(0)
  circuit.ch(0, 1)
  result = circuit.execute()
  sv = result.get_state_vector()

  S_simulator = Aer.backends(name='statevector_simulator')[0]
  q = QuantumRegister(2)
  qubit = QuantumCircuit(q)
  qubit.h(q[0])
  qubit.ch(q[0], q[1])
  job = execute(qubit, S_simulator)
  result_qkit = job.result()
  sv_qkit = result_qkit.get_statevector()

  assert np.testing.assert_allclose(sv, sv_qkit, atol=1e-8, rtol=1e-8) == None

def test_qft_reverse_qft():
  circuit = qcs.circuit_init(4)
  circuit.h(0)
  circuit.x(1)
  circuit.h(2)
  circuit.x(3)
  result = circuit.execute()
  sv_init = result.get_state_vector()

  circuit.qft(0, 3)
  circuit.qft_rev(0, 3)
  result = circuit.execute()
  sv = result.get_state_vector()

  assert np.testing.assert_allclose(sv, sv_init, atol=1e-8, rtol=1e-8) == None

def test_qft_vs_manual_qiskit_qft_comparison():
  circuit = qcs.circuit_init(3)
  circuit.i(0)
  circuit.i(1)
  circuit.x(2)
  circuit.qft(0, 2)
  result = circuit.execute()
  sv = result.get_state_vector()

  S_simulator = Aer.backends(name='statevector_simulator')[0]
  q = QuantumRegister(3)
  qubit = QuantumCircuit(q)
  qubit.iden(q[0])
  qubit.iden(q[1])
  qubit.x(q[2])
  #QFT
  qubit.h(q[0])
  qubit.cu1(np.pi / 2, q[1], q[0])
  qubit.cu1(np.pi / 4, q[2], q[0])
  qubit.h(q[1])
  qubit.cu1(np.pi / 4, q[2], q[1])
  qubit.h(q[2])

  job = execute(qubit, S_simulator)
  result_qkit = job.result()
  sv_qkit = result_qkit.get_statevector()

  assert np.testing.assert_allclose(sv, sv_qkit, atol=1e-8, rtol=1e-8) == None

def test_simple_qaoa_vs_manual_qiskit_qaoa_comparison():
  n = 5
  p = 2
  V = np.arange(0,n,1)
  E = [(0,1,1.0),(0,2,1.0),(1,2,1.0),(3,2,1.0),(3,4,1.0),(4,2,1.0)]
  graph = nx.Graph()
  graph.add_nodes_from(V)
  graph.add_weighted_edges_from(E)

  betas = np.random.uniform(-np.pi, np.pi, size=p)
  gammas = np.random.uniform(-np.pi, np.pi, size=p)
  circuit = qcs.circuit_init(n)

  for i in range(n):
    circuit.h(i)
  for beta, gamma in zip(betas, gammas):
    for i, j in graph.edges:
      circuit.cx(i, j)
      circuit.rot(j, gamma)
      circuit.cx(i, j)
    for i in range(n):
      circuit.rx(i, 2 * beta)

  result = circuit.execute()
  sv = result.get_state_vector()

  S_simulator = Aer.backends(name='statevector_simulator')[0]
  q = QuantumRegister(n)
  qubit = QuantumCircuit(q)
  for i in range(n):
    qubit.h(q[i])
  for beta, gamma in zip(betas, gammas):
    for i, j in graph.edges:
      qubit.cx(q[int(i)], q[int(j)])
      qubit.u1(gamma, q[int(j)])
      qubit.cx(q[int(i)], q[int(j)])
    for i in range(n):
      qubit.rx(beta * 2, q[i])

  job = execute(qubit, S_simulator)
  result_qkit = job.result()
  sv_qkit = result_qkit.get_statevector()

  assert np.testing.assert_allclose(sv, sv_qkit, atol=1e-8, rtol=1e-8) == None
