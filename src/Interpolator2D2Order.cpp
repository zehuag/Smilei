#include "Interpolator2D2Order.h"
#include "ElectroMagn.h"
#include "Field2D.h"
#include "Particle.h"
#include "SmileiMPI_Cart2D.h"

#include <iostream>
#include <cmath>

using namespace std;


// ---------------------------------------------------------------------------------------------------------------------
// Creator for Interpolator2D2Order
// ---------------------------------------------------------------------------------------------------------------------
Interpolator2D2Order::Interpolator2D2Order(PicParams *params, SmileiMPI* smpi) : Interpolator2D(params, smpi)
{
	SmileiMPI_Cart2D* smpi2D = static_cast<SmileiMPI_Cart2D*>(smpi);

	dx_inv_ = 1.0/params->cell_length[0];
    dy_inv_ = 1.0/params->cell_length[1];
    
	i_domain_begin = smpi2D->getCellStartingGlobalIndex(0);
    j_domain_begin = smpi2D->getCellStartingGlobalIndex(1);

}

Interpolator2D2Order::~Interpolator2D2Order()
{
}

// ---------------------------------------------------------------------------------------------------------------------
// 2nd Order Interpolation of the fields at a the particle position (3 nodes are used)
// ---------------------------------------------------------------------------------------------------------------------
void Interpolator2D2Order::operator() (ElectroMagn* champs, Particle* part, LocalFields* ELoc, LocalFields* BLoc)
{
    // Static cast of the electromagnetic fields
	Field2D* Ex2D = static_cast<Field2D*>(champs->Ex_);
	Field2D* Ey2D = static_cast<Field2D*>(champs->Ey_);
	Field2D* Ez2D = static_cast<Field2D*>(champs->Ez_);
	Field2D* Bx2D = static_cast<Field2D*>(champs->Bx_m);
	Field2D* By2D = static_cast<Field2D*>(champs->By_m);
	Field2D* Bz2D = static_cast<Field2D*>(champs->Bz_m);
    
    
    // Normalized particle position
    double xpn = part->position(0)*dx_inv_;
    double ypn = part->position(1)*dy_inv_;
    
    
    // Indexes of the central nodes
    unsigned int ic_p = round(xpn);
    unsigned int ic_d = round(xpn+0.5);
    unsigned int jc_p = round(ypn);
    unsigned int jc_d = round(ypn+0.5);
    
    
    // Declaration and calculation of the coefficient for interpolation
    double delta, delta2;
    
    std::vector<double> Cx_p(3); 
    delta   = xpn - (double)ic_p;
    delta2  = delta*delta;
    Cx_p[0] = 0.5 * (delta2-delta+0.25);
    Cx_p[1] = 0.75 - delta2;
    Cx_p[2] = 0.5 * (delta2+delta+0.25);
    
    std::vector<double> Cx_d(3); 
    delta   = xpn - (double)ic_d + 0.5;
    delta2  = delta*delta;
    Cx_d[0] = 0.5 * (delta2-delta+0.25);
    Cx_d[1] = 0.75 - delta2;
    Cx_d[2] = 0.5 * (delta2+delta+0.25);
    
    std::vector<double> Cy_p(3); 
    delta   = ypn - (double)jc_p;
    delta2  = delta*delta;
    Cy_p[0] = 0.5 * (delta2-delta+0.25);
    Cy_p[1] = 0.75 - delta2;
    Cy_p[2] = 0.5 * (delta2+delta+0.25);
    
    std::vector<double> Cy_d(3); 
    delta   = ypn - (double)jc_d + 0.5;
    delta2  = delta*delta;
    Cy_d[0] = 0.5 * (delta2-delta+0.25);
    Cy_d[1] = 0.75 - delta2;
    Cy_d[2] = 0.5 * (delta2+delta+0.25);
    
    //!\todo CHECK if this is correct for both primal & dual grids !!!
    // First index for summation
    unsigned int ip = ic_p - 1 - i_domain_begin;
    unsigned int id = ic_d - 1 - i_domain_begin;
    unsigned int jp = jc_p - 1 - j_domain_begin;
    unsigned int jd = jc_d - 1 - j_domain_begin;
    
    
    // -------------------------
	// Interpolation of Ex^(d,p)
    // -------------------------
    (*ELoc).x = 0.0;
    for (unsigned int iloc=0 ; iloc<3 ; iloc++) {
        for (unsigned int jloc=0 ; jloc<3 ; jloc++) {
            (*ELoc).x += Cx_d[iloc] * Cy_p[jloc] * (*Ex2D)(id+iloc,jp+jloc);
        }
    }
    
    // -------------------------
	// Interpolation of Ey^(p,d)
    // -------------------------
    (*ELoc).y = 0.0;
    for (unsigned int iloc=0 ; iloc<3 ; iloc++) {
        for (unsigned int jloc=0 ; jloc<3 ; jloc++) {
            (*ELoc).y += Cx_p[iloc] * Cy_d[jloc] * (*Ey2D)(ip+iloc,jd+jloc);
        }
    }
    
    // -------------------------
	// Interpolation of Ez^(p,p)
    // -------------------------
    (*ELoc).z = 0.0;
    for (unsigned int iloc=0 ; iloc<3 ; iloc++) {
        for (unsigned int jloc=0 ; jloc<3 ; jloc++) {
            (*ELoc).z += Cx_p[iloc] * Cy_p[jloc] * (*Ez2D)(ip+iloc,jp+jloc);
        }
    }

    // -------------------------
	// Interpolation of Bx^(p,d)
    // -------------------------
    (*BLoc).x = 0.0;
    for (unsigned int iloc=0 ; iloc<3 ; iloc++) {
        for (unsigned int jloc=0 ; jloc<3 ; jloc++) {
            (*BLoc).x += Cx_p[iloc] * Cy_d[jloc] * (*Bx2D)(ip+iloc,jd+jloc);
        }
    }
    
    // -------------------------
	// Interpolation of By^(d,p)
    // -------------------------
    (*BLoc).y = 0.0;
    for (unsigned int iloc=0 ; iloc<3 ; iloc++) {
        for (unsigned int jloc=0 ; jloc<3 ; jloc++) {
            (*BLoc).y += Cx_d[iloc] * Cy_p[jloc] * (*By2D)(id+iloc,jp+jloc);
        }
    }
    
    // -------------------------
	// Interpolation of Bz^(d,d)
    // -------------------------
    (*BLoc).z = 0.0;
    for (unsigned int iloc=0 ; iloc<3 ; iloc++) {
        for (unsigned int jloc=0 ; jloc<3 ; jloc++) {
            (*BLoc).z += Cx_d[iloc] * Cy_d[jloc] * (*Bz2D)(id+iloc,jd+jloc);
        }
    }
    
} // END Interpolator2D2Order