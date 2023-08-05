!-----------------------------------------------------------------------
!     Subroutine KT17_ECHO
!-----------------------------------------------------------------------
subroutine kt17_initialize(rhel, act)

! initializes KT17 setting dynamic parameters
!
!------------input parameters:
!
! rhel    - heliocentric distance in astronomical units
! act     - disturbance index as defined by Anderson et al. (2013)
!            A magnetic disturbance index for Mercury's magnetic field
!            derived from MESSENGER Magnetometer data.
!

    implicit none

    real*8 f, rhel, act

    include '_kt17_common.f90'
    include '_kt17_param.f90'

    f= 2.06873-0.00279*act   ! magnetopause scale factor
    rss= f*rhel**(1.0/3.0) 
    tamp1=6.4950+0.0229*act    
    tamp2=1.6245+0.0088*act   

end

!-----------------------------------------------------------------------
!     Subroutine KT17_BFIELD
!-----------------------------------------------------------------------

subroutine kt17_bfield(n,x_a,y_a,z_a,bx_a,by_a,bz_a)

  implicit none

  include '_kt17_common.f90'
 
! kt17py    integer*4     n,id_a(n),mode,msm,noshield,id,i
    integer*4     n,noshield,id,i
    real*8        x_a(n),y_a(n),z_a(n)
    real*8        x,y,z
! kt17py  real*8        x_mso,y_mso,z_mso
! kt17py  real*8        bx_mso,by_mso,bz_mso
    real*8        bx_msm,by_msm,bz_msm
    real*8        bx_dcf,by_dcf,bz_dcf
    real*8        bx_dsk,by_dsk,bz_dsk
    real*8        bx_slb,by_slb,bz_slb
    real*8        bx_a(n),by_a(n),bz_a(n)
    real*8        kappa,kappa3
    real*8        fi,gradfix,gradfiy,gradfiz
    real*8        fx,fy,fz,hx,hy,hz

!
! kt17py - initialize variables
!
    id = 0
    noshield = 0

!
! initialize variables
!
    kappa=r0/rss
    kappa3=kappa**3

!
! magnetic field computation
!
    do i=1,n
        x=x_a(i)
        y=y_a(i)
        z=z_a(i)

        x=x*kappa
        y=y*kappa
        z=z*kappa
        
        call kt17_mpdist(0,x,y,z,fi,id,gradfix,gradfiy,gradfiz)

        if (fi .lt. mptol) id=1
        if (noshield .eq. 1) id=1
        
        if (id .eq. 1) then
            bx_dcf=0.0d0
            by_dcf=0.0d0
            bz_dcf=0.0d0
            bx_dsk=0.0d0
            by_dsk=0.0d0
            bz_dsk=0.0d0
            bx_slb=0.0d0
            by_slb=0.0d0
            bz_slb=0.0d0

            fx=0.0d0
            fy=0.0d0
            fz=0.0d0
            hx=0.0d0
            hy=0.0d0
            hz=0.0d0
            call kt17_dipole(x,y,z,fx,fy,fz)
            call kt17_shield(n_dipshld,r_dipshld,x,y,z,hx,hy,hz)
            bx_dcf=kappa3*(fx+hx)
            by_dcf=kappa3*(fy+hy)
            bz_dcf=kappa3*(fz+hz)
         
            fx=0.0d0
            fy=0.0d0
            fz=0.0d0
            hx=0.0d0
            hy=0.0d0
            hz=0.0d0
            call kt17_taildisk(x,y,z,fx,fy,fz)
            call kt17_shield(n_diskshld,r_diskshld,x,y,z,hx,hy,hz)
            bx_dsk=tamp1*(fx+hx)
            by_dsk=tamp1*(fy+hy)
            bz_dsk=tamp1*(fz+hz)

            fx=0.0d0
            fy=0.0d0
            fz=0.0d0
            hx=0.0d0
            hy=0.0d0
            hz=0.0d0
            call kt17_tailslab(x,y,z,fx,fy,fz)
            call kt17_shield(n_slabshld,r_slabshld,x,y,z,hx,hy,hz)
            bx_slb=tamp2*(fx+hx)
            by_slb=tamp2*(fy+hy)
            bz_slb=tamp2*(fz+hz)
         
            bx_msm=bx_dcf+bx_dsk+bx_slb
            by_msm=by_dcf+by_dsk+by_slb
            bz_msm=bz_dcf+bz_dsk+bz_slb
         
            bx_a(i)=bx_msm
            by_a(i)=by_msm
            bz_a(i)=bz_msm
        else    
            bx_a(i)=1.0d-8
            by_a(i)=1.0d-8
            bz_a(i)=1.0d-8
        endif
    enddo

    return
end 


!
!-----------------------------------------------------------------------
!     Subroutine KT17_DIPOLE
!-----------------------------------------------------------------------
!
subroutine kt17_dipole(xmsm,ymsm,zmsm,bx,by,bz)

! calculates components of dipole field
!
! input parameters: x,y,z - msm coordinates in rm (1 rm = 2440 km)
!
! output parameters: bx,by,bz - field components in msm system, in nanotesla.

    implicit none
    include '_kt17_common.f90'
 
    real*8        xmsm,ymsm,zmsm
    real*8        bx,by,bz
    real*8        psi,sps,cps
    real*8        p,u,v,t,q
 
 ! dipole tilt
    psi=0.0d0
    sps=sin(psi/57.29577951d0)
    cps=sqrt(1.0d0-sps**2)
 
 ! compute field components
    p=xmsm**2
    u=zmsm**2
    v=3.0d0*zmsm*xmsm
    t=ymsm**2
    q=mu/sqrt(p+t+u)**5
    bx=q*((t+u-2.0d0*p)*sps-v*cps)
    by=-3.0d0*ymsm*q*(xmsm*sps+zmsm*cps)
    bz=q*((p+t-2.0d0*u)*cps-v*sps)

    return
end

!-----------------------------------------------------------------------
!     Subroutine KT17_MPDIST
!-----------------------------------------------------------------------
 
subroutine kt17_mpdist(mode,x,y,z,fi,id,gradfix,gradfiy,gradfiz) 
    
    implicit none
    
    include '_kt17_common.f90'

    integer*4   mode,id
    real*8      x,y,z,fi,gradfix,gradfiy,gradfiz
    real*8      rho2,r,rho
    real*8      ct,st,t,sp,cp
    real*8      rm,drm_dt
    real*8      gradfir,gradfit,gradfip

    rho2=y**2+z**2
    r=sqrt(x**2+rho2)
    rho=sqrt(rho2)

    id=1

    if (rho .gt. 1.0d-8) then   ! not on the x-axis - no singularities to worry
                                ! about
        ct=x/r
        st=rho/r
        t=atan2(st,ct)
        sp=z/rho
        cp=y/rho
    else                        ! on the x-axis
        if (x .gt. 0.0d0) then  ! on the dayside
            ct=x/r
            st=1.0d-8/r         ! set rho=10**-8, to avoid singularity of
                                ! grad_fi (if mode=1, see gradfip=... below)
            t=atan2(st,ct)
            sp=0.0d0
            cp=1.0d0
        else                    ! on the tail axis! to avoid singularity:
            fi=-1000.0d0        ! assign rm=1000 (a conventional substitute
                                ! value)    
            return   ! and exit
        endif
    endif                               

    rm=r0/sqrt(alfa*(1.0d0+ct)) ! standard form of shue et al.,1997,
                                ! magnetopause model

    if (rm .lt. r) id=-1

    fi=r-rm
    if (mode .eq. 0) return     ! skip calculation of the gradient of fi

    drm_dt=0.25d0*rm**3/r0**2*st

    gradfir=1.0d0
    gradfit=-drm_dt/r
    gradfip=0.0d0               ! axial symmetry
 
    gradfix=gradfir*ct-gradfit*st
    gradfiy=(gradfir*st+gradfit*ct)*cp-gradfip*sp
    gradfiz=(gradfir*st+gradfit*ct)*sp+gradfip*cp

    return
end

!
!-----------------------------------------------------------------------
!     Subroutine KT17_SHIELD
!-----------------------------------------------------------------------
!
subroutine kt17_shield(n,r,x,y,z,bx,by,bz)
  
    implicit none
 
    integer*4   jmax,kmax,j,k,n,o
    real*8      r(n),x,y,z
    real*8      c(n),p(n),cypj,sypj,szpk,czpk,sqpp,epp
    real*8      hx,hy,hz
    real*8      bx,by,bz
 
    o=nint(-0.5+sqrt(n+0.25))
    c(1:o*o)=r(1:o*o)
    p(1:o)=r(o*o+1:o*o+o)

    jmax=o
    kmax=o

    bx=0.0d0
    by=0.0d0
    bz=0.0d0
    do j=1,jmax
        do k=1,kmax
            cypj=cos(y*p(j))
            sypj=sin(y*p(j))
            szpk=sin(z*p(k))
            czpk=cos(z*p(k))
            sqpp=sqrt(p(j)**2+p(k)**2)
            epp=exp(x*sqpp)

            hx=-sqpp*epp*cypj*szpk
            hy=+epp*sypj*szpk*p(j)
            hz=-epp*cypj*czpk*p(k)
 
            bx=bx+hx*c((j-1)*kmax+k)
            by=by+hy*c((j-1)*kmax+k)
            bz=bz+hz*c((j-1)*kmax+k)
        enddo
    enddo
 
    return
end

!
!-----------------------------------------------------------------------
!     Subroutine KT17_TAILDISK
!-----------------------------------------------------------------------
subroutine kt17_taildisk(xmsm,ymsm,zmsm,bx,by,bz)

! calculates msm components of the field from a t01-like 'long-module' equatorial
! current disk with a 'hole' in the center and a smooth inner edge
! (see tsyganenko, jgra, v107, no a8, doi 10.1029/2001ja000219, 2002, fig.1, right
! panel).
!
!------------input parameters:
!
! d0       - basic (minimal) half-thickness
! deltadx - sunward expansion factor for the current sheet thickness
! deltady - flankward expansion factor for the current sheet thickness
! x,y,z    - msm coordinates
!------------output parameters:
! bx,by,bz - field components in msm system, in nanotesla.  

    implicit none

    include '_kt17_common.f90'

    integer*4   nr3,i
    real*8      xmsm,ymsm,zmsm,bx,by,bz
    real*8      f(n_taildisk),b(n_taildisk),c(n_taildisk)
    real*8      xshift,sc,x,y,z,d0_sc,deltadx_sc,deltady_sc
    real*8      rho,drhodx,drhody
    real*8      dex,d,dddy,dddx
    real*8      dzeta,ddzetadx,ddzetady,ddzetadz
    real*8      bi,ci,s1,s2,ds1drho
    real*8      ds2drho,ds1ddz,ds2ddz
    real*8      ds1dx,ds1dy,ds1dz,ds2dx,ds2dy,ds2dz
    real*8      s1ts2,s1ps2,s1ps2sq,fac1,as,dasds1,dasds2
    real*8      dasdx,dasdy,dasdz
 
    nr3=n_taildisk/3
    f(1:nr3)=r_taildisk(1:nr3)
    b(1:nr3)=r_taildisk(nr3+1:2*nr3)
    c(1:nr3)=r_taildisk(2*nr3+1:3*nr3)

    xshift=0.3d0        ! shift the center of the disk to the dayside by xshift
    sc=7.0d0            ! renormalize length scales
  
    x=(xmsm-xshift)*sc
    y=ymsm*sc
    z=zmsm*sc
    d0_sc=d0*sc
    deltadx_sc=deltadx*sc
    deltady_sc=deltady*sc

    rho=sqrt(x**2+y**2)
    drhodx=x/rho
    drhody=y/rho

    dex=exp(x/7.0d0)
    d=d0_sc+deltady_sc*(y/20.0d0)**2+deltadx_sc*dex     ! the last term makes the
                                                        ! sheet thicken sunward, to
    dddy=deltady_sc*y*0.005d0                           ! avoid problems in the
                                                        ! subsolar region
    
    dddx=deltadx_sc/7.0d0*dex
 
    dzeta=sqrt(z**2+d**2)                               ! this is to spread out the
                                                        ! sheet in z direction over
                                                        ! finite thickness 2d
    ddzetadx=d*dddx/dzeta
    ddzetady=d*dddy/dzeta
    ddzetadz=z/dzeta
 
    bx=0.0d0
    by=0.0d0
    bz=0.0d0
 
    do i=1,5
        bi=b(i)
        ci=c(i)

        s1=sqrt((rho+bi)**2+(dzeta+ci)**2)
        s2=sqrt((rho-bi)**2+(dzeta+ci)**2)

        ds1drho=(rho+bi)/s1
        ds2drho=(rho-bi)/s2
        ds1ddz=(dzeta+ci)/s1
        ds2ddz=(dzeta+ci)/s2

        ds1dx=ds1drho*drhodx+ds1ddz*ddzetadx
        ds1dy=ds1drho*drhody+ds1ddz*ddzetady
        ds1dz=ds1ddz*ddzetadz

        ds2dx=ds2drho*drhodx+ds2ddz*ddzetadx
        ds2dy=ds2drho*drhody+ds2ddz*ddzetady
        ds2dz=ds2ddz*ddzetadz

        s1ts2=s1*s2
        s1ps2=s1+s2
        s1ps2sq=s1ps2**2

        fac1=sqrt(s1ps2sq-(2.0d0*bi)**2)
        as=fac1/(s1ts2*s1ps2sq)
        dasds1=(1.0d0/(fac1*s2)-as/s1ps2*(s2*s2+s1*(3.0d0*s1+4.0d0*s2)))/(s1*s1ps2) 
        dasds2=(1.0d0/(fac1*s1)-as/s1ps2*(s1*s1+s2*(3.0d0*s2+4.0d0*s1)))/(s2*s1ps2)
        
        dasdx=dasds1*ds1dx+dasds2*ds2dx
        dasdy=dasds1*ds1dy+dasds2*ds2dy
        dasdz=dasds1*ds1dz+dasds2*ds2dz
     
        bx=bx-f(i)*x*dasdz
        by=by-f(i)*y*dasdz
        bz=bz+f(i)*(2.0d0*as+x*dasdx+y*dasdy)
 
    enddo

    return
end

!
!-----------------------------------------------------------------------
!     Subroutine KT17_TAILSLAB
!-----------------------------------------------------------------------
!
subroutine kt17_tailslab(xmsm,ymsm,zmsm,bx,by,bz)
 
! calculates msm components of the field from an equatorial harris-type current
! sheet, slowly expanding sunward
!
!------------input parameters:
!
! d0       - basic (minimal) half-thickness
! deltadx - sunward expansion factor for the current sheet thickness
! deltady - flankward expansion factor for the current sheet thickness
! scalex - e-folding distance for the sunward expansion of the current sheet
! scaley   - scale distance for the flankward expansion of the current sheet
! zshift   - z shift of image sheets
! x,y,z    - msm coordinates
!------------output parameters:
! bx,by,bz - field components in msm system, in nanotesla.

    implicit none

    include '_kt17_common.f90'
    
    real*8   xmsm,ymsm,zmsm,bx,by,bz
    real*8   d,dddx,zpzi,zmzi
 
    d=d0+deltadx*exp(xmsm/scalex)+deltady*(ymsm/scaley)**2
    dddx=deltadx/scalex*exp(xmsm/scalex)
    zpzi=zmsm+zshift
    zmzi=zmsm-zshift
    bx=(tanh(zmsm/d)-0.5d0*(tanh(zmzi/d)+tanh(zpzi/d)))/d
    by=0.0d0
    bz=(zmsm*tanh(zmsm/d)-0.5d0*(zmzi*tanh(zmzi/d)+zpzi*tanh(zpzi/d)))*dddx/d**2
    
    return
end 