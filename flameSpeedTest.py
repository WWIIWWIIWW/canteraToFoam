import cantera as ct

P_in  = 101325
T_in  = 600
phi   = 1.0
mechanism = "./mechanism/jws-kin_therm.cti" #methanoal mechanism
gas = ct.Solution(mechanism)

Lx= 0.02
tol_ss      = [1.0e-6, 1.0e-14]        # [rtol atol] for steady-state problem
tol_ts      = [1.0e-5, 1.0e-13]        # [rtol atol] for time stepping
loglevel    = 0                        # amount of diagnostic output (0
refine_grid = True                     # True to enable refinement
dt          = 1.0e-5

fuel  = 'CH3OH:{}'.format(1.0)
gas.TP  = T_in, P_in
gas.set_equivalence_ratio(phi, fuel, 'O2:0.21, N2:0.79')


f = ct.FreeFlame(gas, width=Lx)

f.transport_model = 'Multi'
f.soret_enabled=True

f.flame.set_steady_tolerances(default=tol_ss)
f.flame.set_steady_tolerances(default=tol_ss)
f.flame.set_transient_tolerances(default=tol_ts)

f.set_refine_criteria(ratio=3, slope=0.01, curve=0.01)

f.solve(loglevel=loglevel, refine_grid=refine_grid, auto=True)
f.write_csv('cantera_save.csv', species='X')





