#---------------------------------------------------------------
# Select least-flagged reference antennas for calibration in CASA6
#---------------------------------------------------------------

from casatools import table

# --- User input ---
msfilename = input("Enter Measurement Set (MS) name: ")
fldF = input("Enter Field name or ID: ")

# --- Get flag summary ---
summary = flagdata(vis=msfilename, mode='summary', field=fldF, flagbackup=False)
antenna_flags = summary.get('antenna', {})

# --- Compute flagged percentage per antenna ---
flag_percent = {
    ant: (stats['flagged'] / stats['total']) * 100.0
    for ant, stats in antenna_flags.items()
    if stats['total'] > 0
}

# --- Define candidate reference antennas ---
refAntList = [
    'C00', 'C01', 'C02', 'C03', 'C04', 'C05', 'C06', 'C08',
    'C09', 'C10', 'C11', 'C12', 'C13', 'C14', 'S01', 'S02',
    'W01', 'W02', 'E02'
]

# --- Filter and sort by lowest flag percentage ---
filtered_flags = {ant: flag_percent[ant] for ant in refAntList if ant in flag_percent}
ref_ants = sorted(filtered_flags, key=filtered_flags.get)[:4]

# --- Map antenna names to IDs from MS ---
tb = table()
tb.open(msfilename + '/ANTENNA')
# Get the antenna names
antenna_names = tb.getcol('NAME')

antenna_id_map = {name: idx for idx, name in enumerate(antenna_names)}
ref_ant_ids = [antenna_id_map[ant] for ant in ref_ants if ant in antenna_id_map]

# --- Output results ---
print("Selected reference antennas:", ref_ants)
print("Corresponding antenna IDs:", ref_ant_ids)
