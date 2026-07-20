import numpy as np

'''Calculate delta-v required

Reference Materials:

[1] https://descanso.jpl.nasa.gov/descanso/monograph/series12_chapter.html
[1a] https://descanso.jpl.nasa.gov/descanso/monograph/series12/LunarTraj--04Chapter3TransferstoLunarLibrationOrbits.pdf

[2] https://amostech.com/TechnicalPapers/2024/Poster/Evans.pdf

[3] https://www.nasa.gov/wp-content/uploads/2020/05/saing_nasa_and_smallsat_cost_estimation_overview_and_model_tools_s3vi_webinar_series_10_jun_2020.pdf?emrc=fddbb0
'''

g0    = 9.8 # m/s^2
def rocketeqn(deltav,isp=300):
    return m_dry * np.exp(deltav / (isp*g0))

def costfn(mass, a=491, b=1.102):
    return a*(mass**b)

if __name__ == '__main__':
    print('Calculate rough-level delta-v to Earth-Moon Lagrange points and back')
    
    print('Assuming efficient direct transfer from approximately 200 km circular LEO')
    print('Source: https://descanso.jpl.nasa.gov/descanso/monograph/series12/LunarTraj--04Chapter3TransferstoLunarLibrationOrbits.pdf')
    print('This is from Table 3-4')
    deltav_leo_to_MI1 = 3108.9 # m/s
    deltav_MI1_to_L1  = 561.7  # m/s

    print('If Space X can deliver translunar injection from Low Earth Orbit (LEO) to Manifold Insertion (MI), we can cut the TLI delta-v')

    print('This is from Table 3-8')
    deltav_leo_to_MI2 = 3130.8 # m/s
    deltav_MI2_to_L2  = 496.3  # m/s

    # approximation for L4 and L5
    deltav_leo_toL4  = 3100 # m/s (approximation)
    deltav_MI4_to_L4 = 900  # m/s (approximation)

    print('Note that returning back to LEO will cost approximately the same delta-v as going there.')
    print('Note that going to low lunar orbit can cost approximately 500 m/s so assuming that for now')
    deltav_LX_to_LLO = 500 # m/s (approximation)

    print('Assume we have 5 satellites with each two each in lunar libration orbits around L1 and L2 and 1 either at L4 or L5. \n' \
    'Skip L3 since it on opposite side of moon and not a viable mission candidate.')
    print('Also assume Space X can send us on a TLI trajectory so we do not have to do the first major delta-v burn')

    L1_sat = deltav_MI1_to_L1 + deltav_LX_to_LLO
    L2_sat = deltav_MI2_to_L2 + deltav_LX_to_LLO
    L4_sat = deltav_MI4_to_L4 + deltav_LX_to_LLO

    m_dry = 50 # kg
    isp   = 300 # sec

    print('Let us say each spacecraft has a dry mass of 50 kg. Dry mass is the final mass. What will be the wet mass for each L1, L2, and L4 satellite?')
    print('Assumed isp in seconds: ', isp)
    print('Using rocket equation: mf = m0 / exp(delta-v / (isp*g0))')

    L1_sat_mf = rocketeqn(L1_sat, isp=300)
    L2_sat_mf = rocketeqn(L2_sat, isp=300)
    L4_sat_mf = rocketeqn(L4_sat, isp=300)

    print('L1 sat mass (kg): ', L1_sat_mf)
    print('L2 sat mass (kg): ', L2_sat_mf)
    print('L4 sat mass (kg): ', L4_sat_mf)


    print('Spacecraft build cost for small satellites (< 1000 kg)')
    print('Source: https://www.nasa.gov/wp-content/uploads/2020/05/saing_nasa_and_smallsat_cost_estimation_overview_and_model_tools_s3vi_webinar_series_10_jun_2020.pdf')
    print('Cost = a * Mass^b where a=491, b=1.102')
    L1_sat_cost = costfn(L1_sat_mf)
    L2_sat_cost = costfn(L2_sat_mf)
    L4_sat_cost = costfn(L4_sat_mf)

    print('L1 sat cost manufacture ($): ', L1_sat_cost)
    print('L2 sat cost manufacture ($): ', L2_sat_cost)
    print('L4 sat cost manufacture ($): ', L4_sat_cost)

    sat_manufacture_cost = round(2*L1_sat_cost + 2*L2_sat_cost + L4_sat_cost,2)

    print(f'Total manufacturing cost for constellation: ${sat_manufacture_cost:,.2f}')

    salary        = 100_000 # $ 
    num_engineers = 10
    num_satellites= 5
    print(f'Assuming a team of {num_engineers} engineers taking 1 year per satellite at an average salary of ${salary} / yr for each engineer')
    sat_human_cost= salary*num_engineers*num_satellites
    print(f'Total human cost: ${sat_human_cost:,.2f}')

    groundstation_cost = 1_000_000 # $
    sat_lifetime = 5 # years
    num_engineers = 7
    print(f'Assuming a team of {num_engineers} specialists to monitor the constellation with the same salary.')
    print(f'Assume fixed ground station cost to third party of {groundstation_cost} / year for telemetry and tracking.')
    print(f'Assume each satellite has operational lifetime of {sat_lifetime} years.')
    sat_operational_cost = sat_lifetime * (groundstation_cost + num_engineers * salary)
    print(f'Total satellite operational cost in its lifetime: ${sat_operational_cost:,.2f}') 

    sat_cost = sat_manufacture_cost + sat_human_cost + sat_operational_cost
    print(f'Total cost for {num_satellites} satellite constellation in L1, L2 and L4 lunar libration orbits with a lifetime of {sat_lifetime}: ')
    print(f"${sat_cost:,.2f}")