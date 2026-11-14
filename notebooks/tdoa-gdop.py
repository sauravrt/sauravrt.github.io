# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo==0.25.2",
#     "matplotlib==3.11.2; sys_platform != 'emscripten'",
#     "numpy==2.5.4; sys_platform != 'emscripten'",
#     "scipy==1.18.1; sys_platform != 'emscripten'",
#     "matplotlib==3.10.8; sys_platform == 'emscripten'",
#     "numpy==2.4.3; sys_platform == 'emscripten'",
#     "scipy==1.17.1; sys_platform == 'emscripten'",
# ]
# ///
# Publication copy of sigproc-notes/notebooks/tdoa-gdop.py.
# The original notebook remains authoritative; only dependency metadata differs.
import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def imports():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.patches import Ellipse
    from scipy.optimize import least_squares
    plt.rcParams.update({'font.family':'serif', 'figure.facecolor':'#fffff8', 'axes.facecolor':'#fffff8', 'axes.spines.top':False, 'axes.spines.right':False, 'axes.grid':False, 'figure.dpi':120})
    return Ellipse, least_squares, mo, np, plt


@app.cell(hide_code=True)
def background(mo):
    mo.md(r"""
    # UWB anchor layout: spacing, height, and position error

    Four anchors form a rectangle. The tag receives six pair measurements in separate scheduled slots and solves **x, y at a known height**. This experiment asks: how much do mounting height and an elongated footprint amplify measurement noise?

    For an anchor $(X_i,Y_i,H)$ and tag $(x,y,z_t)$, the hyperbolic range-difference equation is

    $$d_{ij}=r_i-r_j+\epsilon_{ij},\qquad r_i=\sqrt{(x-X_i)^2+(y-Y_i)^2+(H-z_t)^2}.$$

    We use independent pair errors of standard deviation $\sigma_d$. Throughout this notebook, **GDOP means horizontal DOP (HDOP)**:

    $$\text{predicted horizontal RMSE}\approx\sigma_d\times\mathrm{HDOP}.$$

    Larger HDOP means greater noise amplification. This is a local prediction with exact anchor coordinates and tag height; it does not include NLOS bias, shared clock errors, or motion between slots.
    """)
    return


@app.cell(hide_code=True)
def model(np):
    pair_names = ['AB','BC','CD','DA','AC','BD']
    B = np.zeros((6,4))
    for _k, (_i,_j) in enumerate([(0,1),(1,2),(2,3),(3,0),(0,2),(1,3)]):
        B[_k,_i], B[_k,_j] = 1, -1

    def dimensions(scale, aspect, convention):
        if convention == 'Fixed area':
            return scale*np.sqrt(aspect), scale/np.sqrt(aspect)
        return scale*aspect, scale

    def anchors(width, depth, height):
        return np.array([[-width/2,-depth/2,height],[width/2,-depth/2,height],
                         [width/2,depth/2,height],[-width/2,depth/2,height]])

    def noise_shape(model):
        return np.eye(6) if model == 'Independent pairs' else B @ B.T / 2

    def ranges_and_jacobian(xy, aa, tag_z):
        xy = np.asarray(xy)
        delta = xy[...,None,:] - aa[:,:2]
        rr = np.sqrt(np.sum(delta**2,axis=-1) + (tag_z-aa[:,2])**2)
        with np.errstate(divide='ignore', invalid='ignore'):
            unit = delta / rr[...,None]
        return np.einsum('ki,...i->...k',B,rr), np.einsum('ki,...ij->...kj',B,unit)

    def geometry(xy, aa, tag_z, model):
        _, jac = ranges_and_jacobian(xy,aa,tag_z)
        info = np.einsum('...ki,kl,...lj->...ij',jac,np.linalg.pinv(noise_shape(model)),jac)
        finite = np.all(np.isfinite(info),axis=(-2,-1))
        safe = np.where(finite[...,None,None],info,np.eye(2))
        eig = np.linalg.eigvalsh(safe)
        good = finite & (eig[...,0] > 1e-12*np.maximum(eig[...,1],1e-30))
        cov = np.linalg.inv(np.where(good[...,None,None],safe,np.eye(2)))
        cov = np.where(good[...,None,None],cov,np.nan)
        dop = np.where(good,np.sqrt(np.trace(cov,axis1=-2,axis2=-1)),np.inf)
        return dop,cov

    def footprint_points(width,depth,n=25):
        xx,yy = np.meshgrid(np.linspace(-.49,.49,n)*width,np.linspace(-.49,.49,n)*depth)
        return np.stack([xx,yy],axis=-1)

    def spatial_stat(width,depth,height,tag_z,model):
        dd,_ = geometry(footprint_points(width,depth),anchors(width,depth,height),tag_z,model)
        return np.quantile(dd,.95)

    def finish_axes(ax):
        ax.spines['bottom'].set_bounds(*ax.get_xlim())
        ax.spines['left'].set_bounds(*ax.get_ylim())


    return (
        anchors,
        dimensions,
        footprint_points,
        geometry,
        noise_shape,
        ranges_and_jacobian,
        spatial_stat,
    )


@app.cell(hide_code=True)
def controls(mo):
    scale_ui = mo.ui.slider(2,60,1,value=5,label='Footprint size: baseline square side (m)')
    aspect_ui = mo.ui.slider(1,8,.1,value=1.0,label='Aspect ratio: width / depth')
    height_ui = mo.ui.slider(2,20,.25,value=8.5,label='Anchor height above floor (m)')
    noise_ui = mo.ui.slider(.01,1,.01,value=0.2,label='Pair noise standard deviation (m)')
    tag_ui = mo.ui.slider(0,3,.1,value=1.5,label='Known tag height (m)')
    budget_ui = mo.ui.slider(.1,3,.05,value=0.5,label='Horizontal RMSE budget (m)')
    shape_ui = mo.ui.dropdown(['Fixed area','Fixed short side'],value='Fixed area',label='Shape comparison')
    theme_ui = mo.ui.dropdown(['Light','Dark'],value='Light',label='Plot theme')
    mo.vstack([mo.md('## 1. Choose an installation\nStart with size, shape, and height. Pair noise converts GDOP into predicted position error. Independent pair noise models the separate scheduled exchanges.'),mo.hstack([scale_ui,aspect_ui],wrap=True),mo.hstack([height_ui,noise_ui],wrap=True),mo.accordion({'More settings':mo.vstack([tag_ui,budget_ui,shape_ui,theme_ui,mo.md('With **Fixed area**, the size control is the equivalent square side. With **Fixed short side**, it is the depth. The tag is assumed stationary during the six-pair measurement cycle.')])})])
    return (
        aspect_ui,
        budget_ui,
        height_ui,
        noise_ui,
        scale_ui,
        shape_ui,
        tag_ui,
        theme_ui,
    )


@app.cell(hide_code=True)
def settings(
    anchors,
    aspect_ui,
    dimensions,
    geometry,
    height_ui,
    mo,
    noise_ui,
    np,
    scale_ui,
    shape_ui,
    tag_ui,
    theme_ui,
):
    width, depth = dimensions(scale_ui.value,aspect_ui.value,shape_ui.value)
    anchor_xyz = anchors(width,depth,height_ui.value)
    tag_z = tag_ui.value
    noise_model = 'Independent pairs'
    sigma_d = noise_ui.value
    probe = np.array([0.,0.])
    _dark = theme_ui.value == 'Dark'
    plot_style = {'figure.facecolor':'#151515' if _dark else '#fffff8','axes.facecolor':'#151515' if _dark else '#fffff8','text.color':'#dddddd' if _dark else '#111111','axes.labelcolor':'#dddddd' if _dark else '#111111','xtick.color':'#dddddd' if _dark else '#444444','ytick.color':'#dddddd' if _dark else '#444444','axes.edgecolor':'#999999' if _dark else '#666666'}
    line_colors = ['#bbbbbb' if _dark else '#666666','#5e9ed6' if _dark else '#256391','#dd9760' if _dark else '#99501e']
    probe_dop, probe_cov0 = geometry(probe,anchor_xyz,tag_z,noise_model)
    mo.md(f'**Current footprint: {width:.2f} × {depth:.2f} m** · Area **{width*depth:,.0f} m²** · Vertical separation **{abs(height_ui.value-tag_z):.2f} m** · Independent pair noise **{sigma_d:.2f} m**.')
    return (
        anchor_xyz,
        depth,
        line_colors,
        noise_model,
        plot_style,
        probe,
        probe_cov0,
        probe_dop,
        sigma_d,
        tag_z,
        width,
    )


@app.cell(hide_code=True)
def center_formula(mo):
    mo.accordion({'How HDOP is calculated':mo.md(r"""
    Each row of the 6×2 Jacobian is

    $$J_{ij,:}=\left[\frac{x-X_i}{r_i}-\frac{x-X_j}{r_j},\ \frac{y-Y_i}{r_i}-\frac{y-Y_j}{r_j}\right].$$

    For independent pair noise, $C_{xy}\approx\sigma_d^2(J^TJ)^{-1}$ and $\mathrm{HDOP}=\sqrt{\operatorname{tr}((J^TJ)^{-1})}$. Rank-deficient horizontal information gives unbounded uncertainty. The six noiseless differences have only three algebraically independent components, but separately measured pairs can still provide independent noise observations.

    At the rectangle centre, with full sides W, L and separation $h=|H-z_t|$,

    $$\mathrm{HDOP}^2=\frac{(W^2+L^2)/4+h^2}{4}\left(\frac1{W^2}+\frac1{L^2}\right).$$

    For a square of side s, $\mathrm{HDOP}=\frac12\sqrt{1+2(h/s)^2}$. Scaling all geometry uniformly leaves HDOP unchanged. At fixed area, the square minimizes centre HDOP; centre performance alone does not certify coverage.

    The Jacobian/information method follows [Yang & Scheuing (2005)](https://www.iss.uni-stuttgart.de/en/research/publications/yang_icassp2005.pdf). The covariance is a local linear prediction / Gaussian CRLB, not a guaranteed field error.
    """)})
    return


@app.cell(hide_code=True)
def dimensionless(
    depth,
    height_ui,
    line_colors,
    mo,
    np,
    plot_style,
    plt,
    tag_z,
    width,
):
    height_side_ratio = np.linspace(0,max(3,1.15*abs(height_ui.value-tag_z)/np.sqrt(width*depth)),161)
    _ratio_now = abs(height_ui.value-tag_z)/np.sqrt(width*depth)
    _a = width/depth
    _penalty = np.sqrt(1+4*height_side_ratio**2/(_a+1/_a))
    _now = np.sqrt(1+4*_ratio_now**2/(_a+1/_a))
    with plt.rc_context(plot_style):
        ratio_fig,_ax = plt.subplots(figsize=(8,4.5),layout='constrained')
        _ax.plot(height_side_ratio,_penalty,color=line_colors[1])
        _ax.axhline(1,color=line_colors[0],ls=':',lw=1)
        _ax.scatter(_ratio_now,_now,color=line_colors[2],s=45,zorder=3)
        _ax.annotate(f'Current: {_now:.2f}×',(_ratio_now,_now),xytext=(8,12),textcoords='offset points')
        _ax.set(xlabel='Vertical separation / equivalent square side, |H − zt| / √area',ylabel='Centre HDOP / centre HDOP at zero separation',title=f'Height penalty for the selected shape (aspect ratio {_a:g})')
        plt.close(ratio_fig)
    mo.vstack([mo.md('## 2. Understand the height penalty\nOne curve isolates the effect of height: **1× means no height penalty**, relative to this same rectangle with anchors at tag height. This is a ratio of HDOP values, not absolute HDOP. The shape is held fixed along the curve; the dot uses your current size and heights.'),ratio_fig,mo.md(f'Current vertical separation is **{abs(height_ui.value-tag_z):.2f} m**, equivalent square side is **{np.sqrt(width*depth):.2f} m**, and their ratio is **{_ratio_now:.3f}**. Raising the anchors multiplies centre HDOP by **{_now:.2f}** relative to zero separation. This isolates height; it does not measure the separate penalty from an elongated shape.')])
    return


@app.cell(hide_code=True)
def sweeps(
    aspect_ui,
    budget_ui,
    depth,
    dimensions,
    height_ui,
    line_colors,
    mo,
    noise_model,
    np,
    plot_style,
    plt,
    scale_ui,
    shape_ui,
    sigma_d,
    spatial_stat,
    tag_z,
    width,
):
    height_values = np.linspace(2,20,60)
    aspect_values = np.linspace(1,8,60)
    height_area = np.array([spatial_stat(width,depth,h,tag_z,noise_model) for h in height_values])
    aspect_area = np.array([spatial_stat(*dimensions(scale_ui.value,a,shape_ui.value),height_ui.value,tag_z,noise_model) for a in aspect_values])
    current_p95 = spatial_stat(width,depth,height_ui.value,tag_z,noise_model)
    with plt.rc_context(plot_style):
        sweep_fig,_axes = plt.subplots(1,2,figsize=(10,4.5),sharey=True,layout='constrained')
        _constraint = f'area = {scale_ui.value**2:g} m²' if shape_ui.value=='Fixed area' else f'depth = {scale_ui.value:g} m'
        for _ax,_xs,_ys,_now,_xlabel,_title in [(_axes[0],height_values,height_area,height_ui.value,'Anchor height above floor (m)',f'Hold layout at {width:.1f} × {depth:.1f} m'),(_axes[1],aspect_values,aspect_area,aspect_ui.value,'Aspect ratio = width / depth',f'Hold height at {height_ui.value:g} m; {_constraint}')]:
            _ax.plot(_xs,_ys,color=line_colors[1])
            _ax.scatter(_now,current_p95,color=line_colors[2],s=40,zorder=3)
            _ax.axhline(budget_ui.value/sigma_d,color=line_colors[0],ls=':',lw=1)
            _ax.set(xlabel=_xlabel,title=_title)
            _ax.annotate('current',(_now,current_p95),xytext=(5,8),textcoords='offset points',fontsize=9)
        _axes[0].set_ylabel('Spatial P95 HDOP')
        plt.close(sweep_fig)
    mo.vstack([mo.md('## 3. Change one installation variable at a time\nBoth panels show **spatial P95 HDOP** on the same vertical scale. Left: vary height at the selected shape. Right: vary shape at the selected height. Dots mark the same current installation; the dotted line is the RMSE budget divided by pair noise.'),sweep_fig,mo.md(f'Current spatial P95: **{current_p95:.2f} HDOP → {sigma_d*current_p95:.2f} m predicted RMSE**. Spatial P95 means 95% of the sampled interior locations have a lower value; it is **not** a 95% error radius. Each candidate uses a uniform 25 × 25 grid spanning 98% of its footprint sides, so the sampled region changes with the layout.')])
    return


@app.cell(hide_code=True)
def spatial(
    anchor_xyz,
    budget_ui,
    depth,
    footprint_points,
    geometry,
    mo,
    noise_model,
    np,
    plot_style,
    plt,
    sigma_d,
    tag_z,
    width,
):
    _gx,_gy = np.meshgrid(np.linspace(-.85*width,.85*width,101),np.linspace(-.85*depth,.85*depth,101))
    spatial_dop,_ = geometry(np.stack([_gx,_gy],axis=-1),anchor_xyz,tag_z,noise_model)
    inside_dop,_ = geometry(footprint_points(width,depth,51),anchor_xyz,tag_z,noise_model)
    coverage = np.mean(inside_dop*sigma_d <= budget_ui.value)
    with plt.rc_context(plot_style):
        spatial_fig,_ax = plt.subplots(figsize=(8,6),layout='constrained')
        _im = _ax.pcolormesh(_gx,_gy,np.ma.masked_invalid(spatial_dop),cmap='cividis',shading='auto')
        spatial_fig.colorbar(_im,ax=_ax,label='HDOP (multiply by pair σ for RMSE in m)')
        if np.nanmin(spatial_dop) < budget_ui.value/sigma_d < np.nanmax(spatial_dop):
            _cs = _ax.contour(_gx,_gy,spatial_dop,levels=[budget_ui.value/sigma_d],colors=['#b22222'])
            _ax.clabel(_cs,fmt={budget_ui.value/sigma_d:'RMSE budget'})
        _ax.plot(anchor_xyz[[0,1,2,3,0],0],anchor_xyz[[0,1,2,3,0],1],'--',color='#b22222',lw=1)
        _ax.scatter(anchor_xyz[:,0],anchor_xyz[:,1],marker='^',color='#b22222')
        for _label,_aa in zip('ABCD',anchor_xyz):
            _ax.annotate(_label,_aa[:2],xytext=(5,5),textcoords='offset points',color='#111111',bbox=dict(facecolor='#fffff8',edgecolor='none',pad=1.5))
        _ax.set(xlabel='x (m)',ylabel='y (m)',aspect='equal',title='Accuracy depends on where the tag operates')
        plt.close(spatial_fig)
    mo.vstack([mo.md('## 4. Check where accuracy degrades\nThe dashed rectangle is the anchor footprint. The map extends outside it to reveal weak geometry. Undefined or numerically singular points are masked.'),spatial_fig,mo.md(f'Interior grid: median HDOP **{np.median(inside_dop):.2f}**, spatial P95 **{np.quantile(inside_dop,.95):.2f}**, sampled maximum **{np.max(inside_dop):.2f}**. **{coverage:.1%}** of interior samples meet the {budget_ui.value:.2f} m RMSE budget. These are grid estimates, not continuous-area guarantees.')])
    return


@app.cell(hide_code=True)
def design_map(
    aspect_ui,
    budget_ui,
    depth,
    dimensions,
    height_ui,
    mo,
    noise_model,
    np,
    plot_style,
    plt,
    scale_ui,
    shape_ui,
    sigma_d,
    spatial_stat,
    tag_z,
    width,
):
    if shape_ui.value == 'Fixed area':
        _constraint = f"Fixed footprint area: {scale_ui.value**2:,.0f} m² ({scale_ui.value:g} m baseline square)"
        _explanation = f"Every point on this map uses the same **{scale_ui.value**2:,.0f} m² anchor footprint area**. Moving along the aspect-ratio axis changes width and depth while preserving that area."
    else:
        _constraint = f"Fixed short side (depth): {scale_ui.value:g} m; area varies"
        _explanation = f"Every point on this map uses the same **{scale_ui.value:g} m depth**. Width = aspect ratio × depth, so footprint area increases from **{scale_ui.value**2:,.0f} to {8*scale_ui.value**2:,.0f} m²** across the x-axis."
    design_heights = np.linspace(2,20,25)
    design_aspects = np.linspace(1,8,29)
    design_error = np.array([[sigma_d*spatial_stat(*dimensions(scale_ui.value,a,shape_ui.value),h,tag_z,noise_model) for a in design_aspects] for h in design_heights])
    with plt.rc_context(plot_style):
        design_fig,_ax = plt.subplots(figsize=(8,5),layout='constrained')
        _im = _ax.pcolormesh(design_aspects,design_heights,design_error,cmap='cividis',shading='auto')
        design_fig.colorbar(_im,ax=_ax,label='Spatial P95 of predicted horizontal RMSE (m)')
        if design_error.min() < budget_ui.value < design_error.max():
            _cs = _ax.contour(design_aspects,design_heights,design_error,levels=[budget_ui.value],colors=['#b22222'],linewidths=2)
            _ax.clabel(_cs,fmt={budget_ui.value:f'{budget_ui.value:.2f} m budget'})
        _ax.scatter(aspect_ui.value,height_ui.value,marker='x',color='#b22222',s=65)
        _ax.set(xlabel='Aspect ratio = width / depth',ylabel='Anchor height above floor (m)',title=f'Height and shape versus the error budget\n{_constraint}')
        plt.close(design_fig)
    mo.accordion({'Optional: compare height and shape jointly':mo.vstack([mo.md(f'### Installation design map — footprint constraint\n{_explanation} Changing the baseline size control recalculates the entire map.\n\nThe cross marks the current **{width:.2f} × {depth:.2f} m** layout at **{height_ui.value:g} m anchor height**. The labelled contour, when present, marks your RMSE budget. Tag height is held at **{tag_z:g} m**, with **{noise_model.lower()}** noise and **{sigma_d:.2f} m pair standard deviation**. Colour scales adapt to the scenario; compare values rather than colours between updates.'),design_fig,mo.md(f'Across this design sweep, spatial P95 predicted RMSE ranges from **{design_error.min():.2f} to {design_error.max():.2f} m**. The service region is the interior of each candidate footprint.')])})
    return


@app.cell(hide_code=True)
def mc_control(mo):
    mc_ui = mo.ui.run_button(label='Run 400 noisy nonlinear position solves')
    mo.accordion({'Optional: validate the centre prediction with noisy solves':mo.vstack([mo.md('Monte Carlo check at the rectangle centre\nGenerate Gaussian pair noise with the selected covariance and solve weighted nonlinear least squares. Initializing at truth deliberately isolates local noise amplification; it does not test acquisition or global ambiguity. Runs are deterministic (seed 2026). Change a control and run again.'),mc_ui])})
    return (mc_ui,)


@app.cell(hide_code=True)
def monte_carlo(
    Ellipse,
    anchor_xyz,
    least_squares,
    line_colors,
    mc_ui,
    mo,
    noise_model,
    noise_shape,
    np,
    plot_style,
    plt,
    probe,
    probe_cov0,
    probe_dop,
    ranges_and_jacobian,
    sigma_d,
    tag_z,
):
    mo.stop(not mc_ui.value,mo.md(''))
    mo.stop(not np.isfinite(probe_dop),mo.md('The probe is singular; choose another geometry.'))
    _rng = np.random.default_rng(2026)
    _qeig,_qvec = np.linalg.eigh(noise_shape(noise_model))
    _keep = _qeig > 1e-10
    _whiten = (_qvec[:,_keep]/np.sqrt(_qeig[_keep])).T
    _noise_root = _qvec[:,_keep]*np.sqrt(_qeig[_keep])
    _truth,_ = ranges_and_jacobian(probe,anchor_xyz,tag_z)
    _mc_errors = []
    _failures = 0
    for _sample in range(400):
        _measurement = _truth + sigma_d*_noise_root@_rng.standard_normal(np.sum(_keep))
        _fit = least_squares(lambda p: _whiten@(ranges_and_jacobian(p,anchor_xyz,tag_z)[0]-_measurement),probe.copy(),jac=lambda p: _whiten@ranges_and_jacobian(p,anchor_xyz,tag_z)[1],max_nfev=150)
        _failures += int(not _fit.success)
        _mc_errors.append(_fit.x-probe)
    mc_errors = np.array(_mc_errors)
    mc_rmse = np.sqrt(np.mean(np.sum(mc_errors**2,axis=1)))
    _mc_cov = sigma_d**2*probe_cov0
    _eig,_vec = np.linalg.eigh(_mc_cov)
    _ellipse_fraction = np.mean(np.einsum('ni,ij,nj->n',mc_errors,np.linalg.inv(_mc_cov),mc_errors)<=5.991)
    with plt.rc_context(plot_style):
        mc_fig,_ax = plt.subplots(figsize=(7,5),layout='constrained')
        _ax.scatter(mc_errors[:,0],mc_errors[:,1],s=7,alpha=.45,color=line_colors[0])
        _angle = np.degrees(np.arctan2(_vec[1,1],_vec[0,1]))
        _ax.add_patch(Ellipse((0,0),2*np.sqrt(5.991*_eig[1]),2*np.sqrt(5.991*_eig[0]),angle=_angle,fill=False,edgecolor=line_colors[1],lw=2))
        _ax.scatter(0,0,marker='+',color=line_colors[2])
        _ax.set(xlabel='x error (m)',ylabel='y error (m)',aspect='equal',title='Noisy solves versus predicted 95% ellipse')
        plt.close(mc_fig)
    mo.accordion({'Monte Carlo result':mo.vstack([mc_fig,mo.md(f'Predicted RMSE **{sigma_d*probe_dop:.3f} m**; empirical RMSE **{mc_rmse:.3f} m**. Predicted ellipse contains **{_ellipse_fraction:.1%}** of trials. Solver-reported failures: **{_failures}/400** (all returned solutions retained). Large discrepancies suggest nonlinear effects or weak geometry. Sampling variability remains with 400 trials.')])})
    return


@app.cell(hide_code=True)
def field_guidance(mo):
    mo.md("""
    ## Reading this as an installation guideline
    Use the sweeps to choose spacing, shape, and height, then check the spatial map across the service area. Grid coverage is an estimate; validate weak regions with finer sampling and real measurements. Higher anchors can improve line of sight even while worsening geometric sensitivity. That benefit must be assessed through measured noise and bias.
    """)
    return


if __name__ == "__main__":
    app.run()
