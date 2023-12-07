from lcapy import *
from numpy import logspace

# Display diagrams of plotted data
def perform_plot_analysis():
    # Each domain has different behavior for plotting
    # Range of time values can be defined as a tuple
    print("This analysis allows for various plotting analyses given an expression")

    print("Available plotting types:")
    print("1. Pole-Zero Plot")
    print("2. Frequency Domain Plot")
    print("3. Bode Plot")
    print("4. Nyquist Plot")
    print("5. Nichols Plot")
    print("6. Phasor Plot")
    print("7. Discrete-Time Plot")

    # Get user input for plot type
    plot_choice = input("Choose the analysis type (enter the corresponding number): ")

    # Perform the selected plot
    if plot_choice == '1':
        # Pole zero plot, laplace
        expr = input("Input your expression using the units s and j: ")
        transExpr = transfer(expr)
        # H = transfer((s - 2) * (s + 3) / (s * (s - 2 * j) * (s + 2 * j)))
        transExpr.plot()
        
    elif plot_choice == '2':
        # Frequency domain plot, fourier
        # Note, this has a marginally stable impulse response since it has a pole at s = 0.
        # Returns the axes used in the plot, returns tuple if multiple
        expr = input("Input your expression using the units s and j: ")
        transExpr = transfer(expr)
        # H = transfer((s - 2) * (s + 3) / (s * (s - 2 * j) * (s + 2 * j)))
        fv = logspace(-1, 3, 400)
        transExpr(j2pif).dB.plot(fv, log_scale=True)
        
    elif plot_choice == '3':
        # Bode plot
        # Plots magnitude and phase as a log freq
        expr = input("Input your expression using the unit s: ")
        # expr = 1 / (s**2 + 20*s + 10000)
        transExpr = transfer(expr)
        transExpr.bode_plot((1, 1000))
        
    elif plot_choice == '4':
        # Nyquist plot
        # Plots imaginary and real frequency response
        expr = input("Input your expression using the unit s: ")
        # expr = 10 * (s + 1) * (s + 2) / ((s - 3) * (s - 4))
        transExpr = transfer(expr)
        transExpr.nyquist_plot((-100, 100))
        
    elif plot_choice == '5':
        expr = input("Input your expression using the unit s: ")
        # expr = 10 * (s + 1) * (s + 2) / ((s - 3) * (s - 4))
        transExpr = transfer(expr)
        transExpr.nichols_plot((-100, 100))
        
    elif plot_choice == '6':
        expr = input("Input your expression using the unit j: ")
        # phasor(1 + j).plot()
        transExpr = transfer(expr)
        phasor(transExpr).plot()
        
    elif plot_choice == '7':
        expr = input("Input your expression using the unit n: ")
        # cos(2 * n * 0.2).plot()
        transExpr = transfer(expr)
        cos(transExpr).plot()

        expr = input("Input your complex expression using the unit n: ")
        # x = 0.9**n * exp(j * n * 0.5)
        transExpr = transfer(expr)
        transExpr.plot((1, 10), polar=True)