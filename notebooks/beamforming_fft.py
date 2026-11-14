# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo==0.25.2",
#     "matplotlib>=3.11.1; sys_platform != 'emscripten'",
#     "numpy>=2.4.6; sys_platform != 'emscripten'",
#     "matplotlib==3.10.8; sys_platform == 'emscripten'",
#     "numpy==2.4.3; sys_platform == 'emscripten'",
# ]
# ///

# Publication copy of sigproc-notes/notebooks/beamforming_fft.py.
# The original remains authoritative; publication dependencies and navigation differ.
import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium", app_title="Beamforming with FFT")


@app.cell
def imports():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    return mo, np, plt


@app.cell(hide_code=True)
def site_navigation(mo):
    mo.md("[← Technical](../../technical/) · [Home](../../)")
    return


@app.cell(hide_code=True)
def introduction(mo):
    mo.md(r"""
    # Beamforming with FFT

    A discrete Fourier transform can operate across **sensor positions** just
    as it operates across time samples. This notebook develops that connection,
    compares a direct beam pattern calculation with an FFT, and scans a snapshot
    containing two plane waves.

    Adapted from Saurav Tuladhar's *Beamforming with FFT*, loosely based on a
    tutorial by [Prof. John R. Buck](https://twitter.com/ProfJohnRBuck) at
    [UMass Dartmouth](https://www.umassd.edu).
    """)
    return


@app.cell(hide_code=True)
def dft_background(mo):
    mo.md(r"""
    ## Discrete Fourier transform (DFT)

    For a finite sequence $x[m]$, $0\le m\le M-1$, its discrete-time Fourier
    transform (DTFT) is

    $$X(e^{j\omega})=\sum_{m=0}^{M-1}x[m]e^{-jm\omega}.$$

    The DTFT is continuous in angular frequency and periodic with period $2\pi$.
    Sampling it every $\Delta\omega=2\pi/L$ gives the $L$-point DFT:

    $$X[\ell]=X(e^{j\omega})\big|_{\omega=2\pi\ell/L}
      =\sum_{m=0}^{L-1}x[m]e^{-j2\pi\ell m/L},\quad 0\le\ell<L.$$

    Here $x[m]=0$ for $m\ge M$, and $L\ge M$. Frequency-domain sampling makes
    the inverse sequence periodic with period $L$; choosing $L\ge M$ prevents
    overlap of its repeated copies. A direct DFT takes $\mathcal O(L^2)$
    operations, whereas an FFT evaluates the same transform in
    $\mathcal O(L\log_2L)$.

    ### Time-domain filtering

    A finite impulse response $h[m]$ has frequency response

    $$H(e^{j\omega})=\sum_{m=0}^{M-1}h[m]e^{-jm\omega}.$$

    **Finite signal duration corresponds to finite array aperture.** Filter
    coefficients correspond to sensor weights, frequency response corresponds
    to a beam pattern, and a signal's frequency spectrum corresponds to a
    snapshot's spatial scan response.

    We use $N$ for the number of sensors and $L$ for the FFT length below.
    """)
    return


@app.cell(hide_code=True)
def spatial_background(mo):
    mo.md(r"""
    ## Spatial domain

    Consider $N$ equally spaced sensors observing narrowband plane waves.
    Let $d$ be the sensor spacing, $\lambda$ the wavelength,
    $k=2\pi/\lambda$, and $u=\cos\theta$, where $0\le\theta\le\pi$ is measured
    from the array axis. The visible directions satisfy $-1\le u\le1$;
    $u=0$ is broadside.

    We consistently use the negative-phase convention from the source's Python:

    $$v_n(u)=e^{-jkdnu}=e^{-j\pi\beta nu},\quad
      \beta=\frac{2d}{\lambda},\quad n=0,\ldots,N-1.$$

    The original prose mixes positive and negative phase conventions. Either
    works if used consistently; the choice determines whether a scan uses an
    FFT or an inverse FFT.

    For weights $\mathbf w=\mathbf v(u_0)/N$, the beam pattern is

    $$B(u)=\mathbf w^H\mathbf v(u)
      =\sum_{n=0}^{N-1}w_n^*e^{-j\pi\beta nu}.$$

    Thus **the FFT of the conjugated weights samples the beam pattern** at
    $\omega=\pi\beta u$. With $L$ FFT bins,

    $$u_\ell=\frac{2}{\beta}\operatorname{fftfreq}(L)_\ell,
      \qquad \Delta u=\frac{2}{\beta L}.$$

    Use `fftshift` on both the coordinates and the transform. At half-wavelength
    spacing ($\beta=1$), this covers one visible interval with the positive
    endpoint omitted. Zero-padding samples the same pattern more finely;
    the physical aperture determines angular resolution.
    """)
    return


@app.cell
def helpers(np, plt):
    def steering_vector(N, u, beta=1.0):
        """Return an (N,) vector or (N, K) matrix for K direction cosines."""
        vectors = np.exp(-1j * np.pi * beta * np.outer(np.arange(N), np.atleast_1d(u)))
        return vectors[:, 0] if np.ndim(u) == 0 else vectors

    def amplitude_db(values, floor=-80):
        """Amplitude dB relative to unit gain, with a finite plotting floor."""
        return 20 * np.log10(np.maximum(np.abs(values), 10 ** (floor / 20)))

    def response_axes(title, polar=False):
        # A local style context avoids changing other notebooks' plotting state.
        with plt.rc_context({
            "font.family": "serif", "font.size": 11,
            "figure.facecolor": "#fffff8", "axes.facecolor": "#fffff8",
            "axes.spines.top": False, "axes.spines.right": False,
            "axes.grid": False, "text.color": "#222222",
            "axes.labelcolor": "#444444", "figure.dpi": 120,
        }):

            fig, ax = plt.subplots(
                figsize=(8, 5.3), layout="constrained",
                subplot_kw={"projection": "polar"} if polar else {},
            )
            ax.set_title(title, pad=24)
            if polar:
                # Shift dB to nonnegative radii; labels retain the actual dB values.
                ax.set_theta_zero_location("E")
                ax.set_thetamin(0)
                ax.set_thetamax(180)
                ax.set_thetagrids([0, 30, 60, 90, 120, 150, 180])
                ax.set_ylim(0, 86)
                ax.set_yticks([20, 40, 60, 80], labels=["−60 dB", "−40 dB", "−20 dB", "0 dB"])
                ax.set_rlabel_position(60)
                ax.grid(axis="y", alpha=0.1)
                ax.spines["polar"].set_visible(False)
            else:
                ax.set(xlabel=r"Direction cosine $u=\cos\theta$",
                       ylabel="Amplitude (dB re unit gain)", xlim=(-1, 1), ylim=(-80, 6))
                ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda value, position: f"{value:.2f}"))
                ax.spines["bottom"].set_bounds(-1, 1)
                ax.spines["left"].set_bounds(-80, 0)
        return fig, ax

    def response_coordinates(u, values, polar=False):
        if polar:
            return np.arccos(np.clip(u, -1, 1)), amplitude_db(values) + 80
        return u, amplitude_db(values)

    def direction_marker(ax, u, label, polar=False, height=0.93):
        if polar:
            theta = np.arccos(np.clip(u, -1, 1))
            ax.plot([theta, theta], [0, 80], color="#666666", linewidth=0.8, linestyle=":")
            ax.annotate(label, (theta, 80), xytext=(0, 12 if height > 0.9 else -22),
                        textcoords="offset points", ha="center", fontsize=9)
        else:
            ax.axvline(u, color="#666666", linewidth=0.8, linestyle=":")
            ax.text(u, height, label, transform=ax.get_xaxis_transform(),
                    ha="right" if u > 0 else "left", fontsize=9)

    def format_direction(u, polar=False):
        if polar:
            return f"{np.degrees(np.arccos(np.clip(u, -1, 1))):.0f}°"
        return f"{u:.2f}"


    return (
        direction_marker,
        format_direction,
        response_axes,
        response_coordinates,
        steering_vector,
    )


@app.cell(hide_code=True)
def view_control(mo):
    plot_view = mo.ui.radio(["Cartesian", "Polar"], value='Cartesian', label="Plot view", inline=True)
    plot_view
    return (plot_view,)


@app.cell(hide_code=True)
def direction_state(mo):
    get_directions, set_directions = mo.state({'look': 0.45, 'one': 0.5909090909090908, 'two': -0.45454545454545453})
    return get_directions, set_directions


@app.cell(hide_code=True)
def array_controls(mo):
    sensor_count = mo.ui.slider(3, 32, value=11, label="Sensors N", show_value=True)
    fft_length = mo.ui.dropdown([64, 128, 256, 1024, 4096], value=1024, label="FFT length L")
    spacing = mo.ui.slider(0.5, 1.5, step=0.05, value=1.0, label="Spacing β = 2d/λ", show_value=True)
    mo.vstack([
        mo.md("## Direct and FFT beam patterns\n\nStart with the original 11-sensor, half-wavelength, broadside example. Move the look direction away from zero to check the transform sign."),
        sensor_count, fft_length, spacing,
    ])
    return fft_length, sensor_count, spacing


@app.cell(hide_code=True)
def look_control(get_directions, mo, np, plot_view, set_directions):

    _polar = plot_view.value == "Polar"
    _direction = get_directions()["look"]
    look_direction = mo.ui.slider(
        0 if _polar else -1, 180 if _polar else 1,
        step=1 if _polar else 0.01,
        value=round(float(np.degrees(np.arccos(np.clip(_direction, -1, 1))))) if _polar else round(_direction, 2),
        label="Look direction θ₀ (degrees)" if _polar else "Look direction u₀ (direction cosine)",
        show_value=True,
        on_change=lambda value: set_directions(
            lambda old: {**old, "look": float(np.cos(np.deg2rad(value))) if plot_view.value == "Polar" else value}
        ),
    )
    look_direction

    return (look_direction,)


@app.cell
def beam_calculation(
    fft_length,
    look_direction,
    np,
    plot_view,
    sensor_count,
    spacing,
    steering_vector,
):
    N = sensor_count.value
    L = fft_length.value
    beta = spacing.value
    u0 = float(np.cos(np.deg2rad(look_direction.value))) if plot_view.value == "Polar" else look_direction.value
    u_fft = np.fft.fftshift(np.fft.fftfreq(L)) * 2 / beta
    u_scan = np.linspace(-1, 1, 2001)
    weights = steering_vector(N, u0, beta) / N
    beam_direct = weights.conj() @ steering_vector(N, u_scan, beta)
    beam_fft = np.fft.fftshift(np.fft.fft(weights.conj(), n=L))
    beam_at_bins = weights.conj() @ steering_vector(N, u_fft, beta)
    beam_error = np.max(np.abs(beam_at_bins - beam_fft))
    return L, N, beam_direct, beam_error, beam_fft, beta, u0, u_fft, u_scan


@app.cell(hide_code=True)
def beam_plot(
    beam_direct,
    beam_fft,
    beta,
    direction_marker,
    format_direction,
    mo,
    np,
    plot_view,
    plt,
    response_axes,
    response_coordinates,
    u0,
    u_fft,
    u_scan,
):
    _polar = plot_view.value == "Polar"
    _fig, _ax = response_axes("The FFT samples the direct beam pattern", _polar)
    _ax.plot(*response_coordinates(u_scan, beam_direct, _polar), color="#666666", linewidth=1.5)
    _visible = np.abs(u_fft) <= 1
    _ax.plot(*response_coordinates(u_fft[_visible], beam_fft[_visible], _polar), linestyle="none",
             marker="o", markersize=3, markerfacecolor="none", color="#4e79a7")
    direction_marker(_ax, u0, f"Look direction {format_direction(u0, _polar)}", _polar)
    _ax.text(0.02, 0.07, "Gray line: direct sum\nBlue circles: FFT bins",
             transform=_ax.transAxes, fontsize=10, color="#333333")
    if beta > 1 and not _polar:
        for _left, _right in [(-1, -1 / beta), (1 / beta, 1)]:
            _ax.axvspan(_left, _right, color="#666666", alpha=0.08, linewidth=0)
    plt.close(_fig)
    mo.vstack([_fig, mo.md(
        "The direct sum covers every visible direction. Circles mark the FFT's "
        "principal interval; shaded edges in Cartesian view lie outside that interval. " +
        ("Polar angle is θ = arccos(u), measured from the array axis: broadside is 90°. "
         "Radius shows amplitude from −80 dB at the center to 0 dB at the outer reference ring." if _polar else "")
    )])
    return


@app.cell(hide_code=True)
def beam_validation(L, N, beam_error, beta, mo):
    mo.md(f"""
    Direct sum versus FFT on **identical bins**: maximum complex error
    **{beam_error:.2e}**. The direct beam has unit gain at its look direction.
    Here $N={N}$, $L={L}$, and $\\Delta u={2 / (beta * L):.5f}$.
    """)
    return


@app.cell(hide_code=True)
def scan_background(mo):
    mo.md(r"""
    ## Scan response example

    A beam pattern describes the directional gain of fixed weights. A scanned
    response instead varies the weights to examine a measured snapshot $\mathbf x$:

    $$y(u)=\frac{\mathbf v(u)^H\mathbf x}{N}
      =\frac1N\sum_{n=0}^{N-1}x_n e^{+j\pi\beta nu}.$$

    NumPy's inverse FFT includes a factor $1/L$, so the correctly scaled scan is

    $$y(u_\ell)=\frac{L}{N}\operatorname{fftshift}
       \{\operatorname{ifft}(\mathbf x,L)\}_\ell.$$

    The original example uses two coherent, noiseless sources with
    $u_1=3/11$, $u_2=-5/11$, and amplitudes $1$ and $0.5$:

    $$\mathbf x=\mathbf v(u_1)+a_2\mathbf v(u_2).$$

    The array settings above apply here too. A single snapshot's lobes can
    interfere, so peaks need not coincide exactly with the source directions.
    """)
    return


@app.cell(hide_code=True)
def source_amplitude_control(mo):
    source_amplitude = mo.ui.slider(0, 1, step=0.05, value=0.5, label="Source 2 amplitude a₂", show_value=True)
    return (source_amplitude,)


@app.cell(hide_code=True)
def source_controls(
    get_directions,
    mo,
    np,
    plot_view,
    set_directions,
    source_amplitude,
):

    _polar = plot_view.value == "Polar"
    _directions = get_directions()
    source_one = mo.ui.slider(
        0 if _polar else -1, 180 if _polar else 1,
        step=1 if _polar else 0.01,
        value=round(float(np.degrees(np.arccos(np.clip(_directions["one"], -1, 1))))) if _polar else round(_directions["one"], 2),
        label="Source 1 θ₁ (degrees)" if _polar else "Source 1 u₁ (direction cosine)",
        show_value=True,
        on_change=lambda value: set_directions(
            lambda old: {**old, "one": float(np.cos(np.deg2rad(value))) if plot_view.value == "Polar" else value}
        ),
    )
    source_two = mo.ui.slider(
        0 if _polar else -1, 180 if _polar else 1,
        step=1 if _polar else 0.01,
        value=round(float(np.degrees(np.arccos(np.clip(_directions["two"], -1, 1))))) if _polar else round(_directions["two"], 2),
        label="Source 2 θ₂ (degrees)" if _polar else "Source 2 u₂ (direction cosine)",
        show_value=True,
        on_change=lambda value: set_directions(
            lambda old: {**old, "two": float(np.cos(np.deg2rad(value))) if plot_view.value == "Polar" else value}
        ),
    )
    mo.vstack([source_one, source_two, source_amplitude])

    return source_one, source_two


@app.cell
def scan_calculation(
    L,
    N,
    beta,
    np,
    plot_view,
    source_amplitude,
    source_one,
    source_two,
    steering_vector,
    u_fft,
    u_scan,
):
    u1 = float(np.cos(np.deg2rad(source_one.value))) if plot_view.value == "Polar" else source_one.value
    u2 = float(np.cos(np.deg2rad(source_two.value))) if plot_view.value == "Polar" else source_two.value
    a2 = source_amplitude.value
    snapshot = steering_vector(N, u1, beta) + a2 * steering_vector(N, u2, beta)
    scan_ifft = (L / N) * np.fft.fftshift(np.fft.ifft(snapshot, n=L))
    scan_direct = steering_vector(N, u_scan, beta).conj().T @ snapshot / N
    scan_at_bins = steering_vector(N, u_fft, beta).conj().T @ snapshot / N
    scan_error = np.max(np.abs(scan_at_bins - scan_ifft))
    return a2, scan_direct, scan_error, scan_ifft, u1, u2


@app.cell(hide_code=True)
def scan_plot(
    a2,
    direction_marker,
    format_direction,
    mo,
    np,
    plot_view,
    plt,
    response_axes,
    response_coordinates,
    scan_direct,
    scan_ifft,
    u1,
    u2,
    u_fft,
    u_scan,
):
    _polar = plot_view.value == "Polar"
    _fig, _ax = response_axes("An inverse FFT scans the two-source snapshot", _polar)
    _ax.plot(*response_coordinates(u_scan, scan_direct, _polar), color="#666666", linewidth=1.5)
    _visible = np.abs(u_fft) <= 1
    _ax.plot(*response_coordinates(u_fft[_visible], scan_ifft[_visible], _polar), linestyle="none",
             marker="o", markersize=3, markerfacecolor="none", color="#4e79a7")
    for _u, _label, _height in [(u1, f"Source 1: {format_direction(u1, _polar)} · amplitude 1", 0.93),
                                (u2, f"Source 2: {format_direction(u2, _polar)} · amplitude {a2:g}", 0.85)]:
        direction_marker(_ax, _u, _label, _polar, _height)
    _ax.text(0.02, 0.07, "Gray line: direct scan\nBlue circles: inverse FFT bins",
             transform=_ax.transAxes, fontsize=10, color="#333333")
    plt.close(_fig)
    mo.vstack([_fig, mo.md(
        f"Source directions ({'degrees' if _polar else 'direction cosine'}): **{format_direction(u1, _polar)}** and **{format_direction(u2, _polar)}**. "
        "The dotted lines show the known directions; the curve shows their combined response. "
        "Amplitudes use a unit reference and are not normalized to the largest peak."
    )])
    return


@app.cell(hide_code=True)
def notes(beta, mo, scan_error):
    mo.md(rf"""
    Direct scan versus inverse FFT on identical bins: maximum complex error
    **{scan_error:.2e}**.

    ## Spacing, resolution, and implementation notes

    - **Half-wavelength spacing** ($\beta=1$): one FFT period covers the visible
      interval, with the usual endpoint convention. The two endfire directions
      have the same steering vector at this spacing.
    - **Closer spacing** ($\beta<1$): some FFT bins have $|u|>1$ and represent
      invisible directions. Only visible bins are plotted.
    - **Wider spacing** ($\beta>1$): the spatial response repeats every
      $2/\beta$ in $u$. The principal FFT interval covers only part of the visible
      region; periodic replicas can produce grating lobes and ambiguous bearings.
    - **Zero-padding** increases the sampling density of the response, not the
      resolving power of the array. Increase $N$ at fixed spacing to increase
      aperture and narrow the main lobe.
    - A direct scan forms an $N\times K$ steering matrix here for clarity.
      An FFT avoids that matrix and efficiently evaluates a regular grid.
      Whether a transform runs in place depends on the library and API.

    Current spacing: $d/\lambda={beta / 2:.3f}$.

    Try steering away from broadside, increasing the FFT length with $N$ fixed,
    and moving the two sources closer together. These expose the sign convention,
    interpolation, and aperture limits separately.
    """)
    return


if __name__ == "__main__":
    app.run()
