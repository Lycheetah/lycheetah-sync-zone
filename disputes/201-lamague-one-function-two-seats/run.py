# Falsifier: if "Seat B" were an independent implementation, replacing the shared engine with a broken one
# must make the harness report a mismatch, or the harness must at least be able to host a different seat.
# Observed: the harness has no second implementation; sabotage is invisible because both calls share it.
import sys, importlib.util, inspect
sys.dont_write_bytecode = True
P = "/home/guestpc/lycheetah-sync-zone/experiments/lamague-symbolic-grounding/lamague_grammar.py"
spec = importlib.util.spec_from_file_location("lg", P); lg = importlib.util.module_from_spec(spec)
sys.modules["lg"] = lg; spec.loader.exec_module(lg)
sim = lg.DualSeatSimulator()
txt = "CENTER -> FLOW; IGNITION -> FLOW -> LIGHT -> COAGULATE"
def trials(n=1000):
    return sum(sim.simulate_cross_seat_transmission(txt)[0] for _ in range(n))
print("baseline identical:", trials(), "/ 1000")
src = inspect.getsource(lg.DualSeatSimulator.simulate_cross_seat_transmission)
print("execute_ast_on_state call sites in simulate_cross_seat_transmission:", src.count("self.execute_ast_on_state"))
print("origin_id strings used:", sorted(set(__import__("re").findall(r'origin_id="([A-Z_]+)"', src))))
# Sabotage: replace the flow vector with arbitrary garbage. A real second seat would disagree with a correct first seat.
orig = lg.LamagueEngine.flow
def garbage(state, alpha=0.05, steps=3):
    s = state.copy()
    for k in s.nodes: s.nodes[k] = 123.456
    return s
lg.LamagueEngine.flow = staticmethod(garbage)
print("with flow() replaced by garbage, identical:", trials(), "/ 1000")
lg.LamagueEngine.flow = orig
