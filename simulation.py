def check_phase_matching_condition(no_w, ne_w, no_2w, ne_2w):
    # Check the phase-matching condition
    condition = no_w / no_2w - ne_w / ne_2w

    # Define a tolerance for the condition to be considered approximately satisfied
    tolerance = 0.01

    # Check if the condition is within the tolerance
    if abs(condition) < tolerance:
        print("The crystal is phase-matched for Second Harmonic Generation (SHG).")
    else:
        print("The crystal may not be efficiently phase-matched for SHG.")

# Given refractive indices
no_w = 1.4938
ne_w = 1.4598
no_2w = 1.5124
ne_2w = 1.4704

# Check the phase-matching condition
check_phase_matching_condition(no_w, ne_w, no_2w, ne_2w)
