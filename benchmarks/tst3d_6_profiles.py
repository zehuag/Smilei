import math

L0 = 2.*math.pi # Wavelength in PIC units

Main(
	geometry = "3d3v",
	
	interpolation_order = 2,
	
	timestep = 0.005 * L0,
	sim_time  = 0.01 * L0,
	
	cell_length = [0.01 * L0]*3,
	sim_length  = [1. * L0]*3,
	
	number_of_patches = [ 4 ]*3,
	
	time_fields_frozen = 10000000.,
	
	bc_em_type_x = ["periodic"],
	bc_em_type_y = ["periodic"],
	bc_em_type_z = ["periodic"],
	print_every = 10,
	
	random_seed = smilei_mpi_rank
)

def custom(x, y, z):
	if z<L0/2.: return 0.
	else: return math.exp(-z)

profiles = {
"constant"   :constant   (1.),
"trapezoidal":trapezoidal(1.,
							xvacuum=0.1*L0, xplateau=0.4*L0, xslope1=0.1*L0, xslope2=0.1*L0,
							yvacuum=0.3*L0, yplateau=0.1*L0, yslope1=0.2*L0, yslope2=0.2*L0,
							zvacuum=0.2*L0, zplateau=0.6*L0, zslope1=0.1*L0, zslope2=0.1*L0),
"gaussian"   :gaussian   (1.,
							xvacuum=0.1 *L0, xlength=0.5*L0, xfwhm=0.2*L0, xcenter=0.2*L0, xorder=2,
							yvacuum=0.2 *L0, ylength=0.6*L0, yfwhm=0.4*L0, ycenter=0.5*L0, yorder=4,
							zvacuum=0.05*L0, zlength=0.7*L0, zfwhm=0.6*L0, zcenter=0.4*L0, zorder=2),
"polygonal"  :polygonal  (xpoints=[0.1*L0, 0.2*L0, 0.4*L0, 0.8*L0], xvalues=[1.,0.5,0.8, 0.1]),
"cosine"     :cosine     (1.,
							xamplitude=0.4, xvacuum=0.3*L0, xlength=0.4*L0, xphi=0.1*L0, xnumber=5,
							yamplitude=0.2, yvacuum=0.2*L0, ylength=0.6*L0, yphi=0.3*L0, ynumber=10,
							zamplitude=0.1, zvacuum=0.1*L0, zlength=0.6*L0, zphi=0. *L0, znumber=2),
"polynomial" :polynomial (x0=0.4*L0, y0=0.5*L0, z0=0.6*L0,
							order0=1.,
							order1=[-1./L0,-0.1/L0, 2./L0],
							order2=[(0.1/L0)**2]*6),
"custom"     :custom
}

for name, profile in profiles.items():
	Species(
		species_type = name,
		initPosition_type = "regular",
		initMomentum_type = "maxwell-juettner",
		n_part_per_cell= 8,
		mass = 1.0,
		charge = 1.0,
		nb_density = profile,
		time_frozen = 10000.0,
		bc_part_type_xmin = "none",
		bc_part_type_xmax = "none",
		bc_part_type_ymin = "none",
		bc_part_type_ymax = "none",
		bc_part_type_zmin = "none",
		bc_part_type_zmax = "none"
	)


DiagFields(
	every = 5,
)


