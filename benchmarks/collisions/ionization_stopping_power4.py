# ---------------------------------------------
# SIMULATION PARAMETERS FOR THE PIC-CODE SMILEI
# ---------------------------------------------

import math
L0 = 2.*math.pi # conversion from normalization length to wavelength


Main(
    geometry = "1d3v",

    number_of_patches = [ 4 ],

    interpolation_order = 2,

    timestep = 1. * L0,
    sim_time = 170000 * L0,


    time_fields_frozen = 100000000000.,

    cell_length = [400.*L0],
    sim_length = [8000.*L0],

    bc_em_type_x = ["periodic"],


    random_seed = 0,

	referenceAngularFrequency_SI = L0 * 3e8 /1.e-6,
    print_every = 10000,
)




el = "electron1"
E = 1000. # keV
E /= 511.
vel = math.sqrt(1.-1./(1.+E)**2)
mom = math.sqrt((1.+E)**2-1.)
Species(
	species_type = el,
	initPosition_type = "regular",
	initMomentum_type = "maxwell-juettner",
	n_part_per_cell= 2,
	mass = 1.0,
	charge = -1.0,
	charge_density = 1e-9,
	mean_velocity = [vel, 0., 0.],
	temperature = [0.0000000001]*3,
	time_frozen = 100000000.0,
	bc_part_type_xmin = "none",
	bc_part_type_xmax = "none",
	bc_part_type_ymin = "none",
	bc_part_type_ymax = "none",
	c_part_max = 10.
)

Species(
	species_type = "ion1",
	initPosition_type = "regular",
	initMomentum_type = "maxwell-juettner",
	n_part_per_cell= 2,
	mass = 1836.0*27.,
	charge = 0,
	nb_density = 1.,
	mean_velocity = [0., 0., 0.],
	temperature = [0.00000000001]*3,
	time_frozen = 100000000.0,
	bc_part_type_xmin = "none",
	bc_part_type_xmax = "none",
	bc_part_type_ymin = "none",
	bc_part_type_ymax = "none",
	atomic_number = 13
)


Collisions(
	species1 = [el],
	species2 = ["ion1"],
	coulomb_log = 0.00000001,
	ionizing = True
)




DiagFields(
	every = 1000000
)


DiagScalar(
	every = 1000000000
)



DiagParticles(
	output = "px_density",
	every = 1000,
	species = [el],
	axes = [
		 ["x",    0.,    Main.sim_length[0],   1]
	]
)
DiagParticles(
	output = "density",
	every = 1000,
	species = [el],
	axes = [
		 ["x",    0.,    Main.sim_length[0],   1]
	]
)
