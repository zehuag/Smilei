
# ----------------------------------------------------------------------------------------
#                   SIMULATION PARAMETERS FOR THE PIC-CODE SMILEI
# ----------------------------------------------------------------------------------------
#
# Remember: never override the following names:
#           SmileiComponent, Species, Laser, Collisions, DiagProbe, DiagParticles,
#           DiagScalar, DiagPhase or ExtField
#
import math as m
    #DumpRestart(
            #restart_dir = "/ccc/scratch/cont003/gen7678/grassia/Results/Test_S45Laser",
            #        dump_step = 20000,
            #dump_minutes = 240.,
            #dump_deflate = 0,
            #exit_after_dump = True,
            #dump_file_sequence = 2
#)

## CHARACTERISTIC DISTANCES, TEMPERATURE & TIMES
# ---------------------------------------------

# plasma parameters
n0      = 1.0
Mi      = 1.0

Te      = 0.0001

g0      = 10.
v0      = m.sqrt(1.-1./g0**2)
nppc    = 10
sigma   = 0.
B0      = m.sqrt(sigma*2.*g0)
E0      = v0*B0
# simulation box


dx      = 1./4.
dt      = dx*0.5

Lx    = 1216./8.
Ly    = 256/8.
t_sim = 500./8.


def B(x,y):
    return B0
def E(x,y):
    return E0

LoadBalancing(
              every = 20,
              coef_cell = 1.,
              coef_frozen = 0.1
              )
Main(
     #dim: Geometry of the simulation
     #      1d3v = cartesian grid with 1d in space + 3d in velocity
     #      2d3v = cartesian grid with 2d in space + 3d in velocity
     #      3d3v = cartesian grid with 3d in space + 3d in velocity
     #      2drz = cylindrical (r,z) grid with 3d3v particles
     #
     geometry = '2d3v',
     
     # order of interpolation
     #
     interpolation_order = 2,
     
     # SIMULATION BOX : for all space directions (use vector)
     # cell_length: length of the cell
     # sim_length: length of the simulation in units of the normalization wavelength
     cell_length = [dx,dx],
     sim_length  = [Lx,Ly],
     maxwell_sol = 'Yee',
     currentFilter_int = 3,
     Friedman_filter = True,
     Friedman_theta = 0.3,

     number_of_patches = [16,16],
     clrw = 1,
     
     # SIMULATION TIME
     # timestep: duration of the timestep
     # sim_time: duration of the simulation in units of the normalization period
     #,
     timestep = dt,
     sim_time = t_sim,
     
     # ELECTROMAGNETIC BOUNDARY CONDITIONS
     # bc_em_type_x/y/z : boundary conditions used for EM fields
     #                    periodic = periodic BC (using MPI topology)
     #                    silver-muller = injecting/absorbing BC
     #                    reflective = consider the ghost-cells as a perfect conductor
     #
     bc_em_type_x = ['silver-muller'],
     bc_em_type_y = ['periodic'],
 
     
     print_every = int(t_sim/dt/50.),

     # regular seed
     # this is used to regularize the regular number generator
     random_seed = smilei_mpi_rank
     )

Species(
        species_type = 'pos',
        initPosition_type = 'random',
        initMomentum_type = 'mj',
        ionization_model = 'none',
        n_part_per_cell = nppc,
        c_part_max = 1.0,
        mass = Mi,
        charge = 1.0,
        nb_density = n0,
        mean_velocity = [v0,0.,0.],
        temperature = [Te],
        thermT = [0.],
        thermVelocity = [0.,0.,0.],
        time_frozen = 0.,
        bc_part_type_xmin  = 'refl',
        bc_part_type_xmax  = 'refl',
        bc_part_type_ymin  = 'none',
        bc_part_type_ymax  = 'none'
)

     

Species(
        species_type = 'eon',
        initPosition_type = 'random',
        initMomentum_type = 'mj',
        ionization_model = 'none',
        n_part_per_cell = nppc,
        c_part_max = 1.0,
        mass = 1.0,
        charge = -1.0,
        nb_density = n0,
        mean_velocity = [v0,0.,0.],
        temperature = [Te],
        thermT = [0.],
        thermVelocity = [0.,0.,0.],
        time_frozen = 0,
        bc_part_type_xmin  = 'refl',
        bc_part_type_xmax  = 'refl',
        bc_part_type_ymin  = 'none',
        bc_part_type_ymax  = 'none'
        )


#ExtField(
#         field = 'Bz',
#         profile = B
#         )

#ExtField(
#         field = 'Ey',
#         profile = E
#         )

globalEvery = int(5./dt)

# scalar diagnostics
DiagScalar(every=int(1))

DiagFields(
         every = globalEvery ,
         fields = ['Ey','Bz','Rho_eon','Jy_eon','Jy_pos']
)

DiagParticles(
    output = "density",
    every = globalEvery,
    time_average = 1,
    species = ["eon"],
    axes = [
        ["x", Lx/2., Lx, 600 ],
        ["gamma", 1, 500, 500]
        ]
)

DiagParticles(
    output = "density",
    every = globalEvery,
    time_average = 1,
    species = ["eon"],
    axes = [
        ["x", Lx/2., Lx, 600 ],
        ["px",-75, 75, 400],
        ["py",-75, 75, 400]
        ]
)


